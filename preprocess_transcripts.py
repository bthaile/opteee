import os
import re
import pandas as pd
import json
from tqdm import tqdm
from collections import defaultdict
from pipeline_config import (
    TRANSCRIPT_DIR, PROCESSED_DIR, CHUNK_SIZE, OVERLAP, MIN_CHUNK_WORDS,
    get_metadata_file, ensure_directories
)

# Add error tracking
skipped_files = defaultdict(list)  # Track skipped files by reason

print("="*80)
print(f"TRANSCRIPT PREPROCESSING SCRIPT - VERBOSE MODE")
print(f"Chunk size: {CHUNK_SIZE} words with {OVERLAP} words overlap")
print("="*80)

def load_metadata():
    """Load video metadata from JSON file"""
    try:
        METADATA_FILE = get_metadata_file()
        print(f"\n[1/3] Loading video metadata from {METADATA_FILE}...")
        
        # Try to load from JSON first
        if os.path.exists(METADATA_FILE):
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert list to dictionary if needed
                if isinstance(data, list):
                    metadata_dict = {}
                    for item in data:
                        video_id = item.get('video_id')
                        if video_id:
                            metadata_dict[video_id] = item
                    print(f"Successfully converted list to dictionary with {len(metadata_dict)} videos")
                else:
                    metadata_dict = data
                    print(f"Successfully loaded dictionary with {len(metadata_dict)} videos")
                return metadata_dict
        
        # No CSV fallback - JSON format is required
        print("❌ No metadata file found! Please run outlier_scraper.py first to create video metadata.")
        return {}
        
        print("⚠️ No metadata file found!")
        return {}
        
    except Exception as e:
        print(f"❌ Error loading metadata: {e}")
        return {}

def extract_timestamps_and_clean(text):
    """
    Extract timestamps and clean transcript, preserving timestamp information
    Returns cleaned text and a dictionary of timestamp positions
    """
    # First, split the text into lines to process each line
    lines = text.split('\n')
    
    # Initialize variables to store cleaned text and timestamps
    cleaned_lines = []
    timestamps = {}
    current_position = 0
    
    for line in lines:
        # Look for timestamp at the beginning of the line
        timestamp_match = re.match(r'^(\d+\.\d+)s:', line)
        if timestamp_match:
            timestamp_seconds = float(timestamp_match.group(1))
            # Remove the timestamp from the line
            content = re.sub(r'^\d+\.\d+s:', '', line).strip()
            
            # Remove speaker labels if any
            content = re.sub(r'^\s*[A-Za-z0-9_\- ]+:', '', content).strip()
            
            if content:  # Only add non-empty lines
                # Record the position in the final text where this timestamp applies
                timestamps[current_position] = timestamp_seconds
                cleaned_lines.append(content)
                current_position += len(content) + 1  # +1 for the space we'll add between lines
        else:
            # For lines without timestamps, just clean and add them
            content = line.strip()
            # Remove speaker labels if any
            content = re.sub(r'^\s*[A-Za-z0-9_\- ]+:', '', content).strip()
            
            if content:  # Only add non-empty lines
                cleaned_lines.append(content)
                current_position += len(content) + 1
    
    # Join the cleaned lines with spaces
    cleaned_text = ' '.join(cleaned_lines)
    
    # Remove emojis and other Unicode characters
    cleaned_text = re.sub(r'[\U0001F300-\U0001F9FF]', '', cleaned_text)
    
    # Remove any remaining special characters or formatting
    cleaned_text = re.sub(r'[^\w\s.,?!\'"-]', '', cleaned_text)
    
    # Remove extra whitespace
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return cleaned_text, timestamps

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format for video referencing"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def chunk_text_with_timestamps(text, timestamps, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Split text into chunks of approximately chunk_size words with overlap
    Include timestamp information for each chunk
    """
    words = text.split()
    
    # If text is shorter than chunk_size, return as a single chunk
    if len(words) <= chunk_size:
        # Find the earliest timestamp that applies to this text
        start_timestamp = min(timestamps.values()) if timestamps else 0
        return [{
            'text': text,
            'start_timestamp_seconds': start_timestamp,
            'start_timestamp': format_timestamp(start_timestamp)
        }]
    
    chunks = []
    start = 0
    
    while start < len(words):
        # Calculate end index (start + chunk_size or end of text)
        end = min(start + chunk_size, len(words))
        
        # Create chunk from words[start:end]
        chunk = ' '.join(words[start:end])
        
        # Find the position of this chunk in the original text
        chunk_start_pos = len(' '.join(words[:start])) + (1 if start > 0 else 0)
        
        # Find the closest timestamp that comes before or at this position
        applicable_timestamps = {pos: ts for pos, ts in timestamps.items() if pos <= chunk_start_pos}
        chunk_timestamp = max(applicable_timestamps.values()) if applicable_timestamps else 0
        
        chunks.append({
            'text': chunk,
            'start_timestamp_seconds': chunk_timestamp,
            'start_timestamp': format_timestamp(chunk_timestamp)
        })
        
        # Move start position for next chunk (with overlap)
        start += (chunk_size - overlap)
    
    return chunks

def extract_video_id_from_filename(filename):
    """Extract video ID from transcript filename with robust fallbacks"""
    # Remove file extension
    base_name = os.path.splitext(filename)[0]
    
    # Look for standard YouTube ID pattern (11 characters) in the filename
    youtube_id_match = re.search(r'([-\w]{11})', base_name)
    if youtube_id_match:
        return youtube_id_match.group(1)
    
    # Return the base name if we can't find a YouTube ID pattern
    return base_name

def find_metadata_for_transcript(filename, metadata_dict):
    """Find the best matching metadata for a transcript file using multiple approaches"""
    try:
        # First attempt: Direct video ID extraction and lookup
        video_id = extract_video_id_from_filename(filename)
        if video_id in metadata_dict:
            print(f" Found metadata by direct ID match: {video_id}")
            return video_id, metadata_dict[video_id]
        
        # Second attempt: Try to match by title or filename pattern
        base_name = os.path.splitext(filename)[0]
        cleaned_filename = base_name.replace('_', ' ').lower()
        
        best_match = None
        best_score = 0
        
        # Ensure metadata_dict is a dictionary
        if isinstance(metadata_dict, list):
            metadata_dict = {item.get('video_id', ''): item for item in metadata_dict}
        
        for vid_id, metadata in metadata_dict.items():
            if not isinstance(metadata, dict):
                continue
                
            title = metadata.get('title', '')
            if not title:
                continue
                
            # Clean and normalize the title for comparison
            cleaned_title = title.replace('_', ' ').lower()
            
            # Simple string contains matching
            if cleaned_title in cleaned_filename or cleaned_filename in cleaned_title:
                # Calculate a similarity score based on the length of matching text
                match_length = len(cleaned_title) if cleaned_title in cleaned_filename else len(cleaned_filename)
                score = match_length / max(len(cleaned_title), len(cleaned_filename))
                
                if score > best_score:
                    best_score = score
                    best_match = vid_id
        
        if best_match and best_score > 0.5:  # Threshold for a good match
            print(f" Found metadata by title match: {best_match} (score: {best_score:.2f})")
            return best_match, metadata_dict[best_match]
        
        # If no good match found, construct basic metadata
        print(f"⚠️ No metadata found for '{filename}'")
        base_id = video_id if len(video_id) == 11 else None  # Use only if it looks like a valid YouTube ID
        
        # Construct fallback metadata
        fallback_metadata = {
            'video_id': base_id or "unknown",
            'title': base_name.replace('_', ' '),
            'url': f"https://www.youtube.com/watch?v={base_id}" if base_id else "",
        }
        
        return base_id or "unknown", fallback_metadata
        
    except Exception as e:
        print(f"❌ Error in find_metadata_for_transcript: {e}")
        # Return basic fallback metadata
        base_name = os.path.splitext(filename)[0]
        return "unknown", {
            'video_id': "unknown",
            'title': base_name.replace('_', ' '),
            'url': "",
        }

def process_transcripts(metadata_dict):
    """Process all transcripts in the transcript directory"""
    # Create output directory if it doesn't exist
    ensure_directories()
    print(f"\n[2/3] Created or confirmed existence of output directory: {PROCESSED_DIR}")
    
    # Get list of transcript files
    if not os.path.exists(TRANSCRIPT_DIR):
        print(f"❌ ERROR: Transcript directory {TRANSCRIPT_DIR} does not exist!")
        return
        
    transcript_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith('.txt')]
    print(f"Found {len(transcript_files)} transcript files to process in {TRANSCRIPT_DIR}")
    
    # Initialize counters
    total_chunks = 0
    processed_files = 0
    
    # Process each transcript file
    print("\n[3/3] Beginning processing of transcript files...")
    print("="*80)
    for filename in tqdm(transcript_files, desc="Processing transcripts"):
        try:
            # Find metadata for this transcript
            video_id, video_metadata = find_metadata_for_transcript(filename, metadata_dict)

            # Read and clean the transcript text
            with open(os.path.join(TRANSCRIPT_DIR, filename), 'r', encoding='utf-8') as f:
                raw_text = f.read()
            
            cleaned_text, timestamps = extract_timestamps_and_clean(raw_text)
            
            if not cleaned_text:
                skipped_files['empty_after_cleaning'].append(filename)
                continue

            # Chunk the text
            chunks = chunk_text_with_timestamps(cleaned_text, timestamps)
            total_chunks_for_file = len(chunks)
            
            video_chunks = []
            # Process each chunk and add it to a list for the current video
            for i, chunk_info in enumerate(chunks):
                # Create the final chunk object
                final_chunk = {
                    'video_id': video_id,
                    'title': video_metadata.get('title', 'Unknown Title'),
                    'url': video_metadata.get('url', f"https://www.youtube.com/watch?v={video_id}"),
                    'upload_date': video_metadata.get('upload_date') or video_metadata.get('publishedAt'),
                    'duration': video_metadata.get('duration'),
                    'channel_name': video_metadata.get('channel_name', ''),
                    'description': video_metadata.get('description', ''),
                    'chunk_index': i + 1,
                    'total_chunks': total_chunks_for_file,
                    'text': chunk_info['text'],
                    'start_timestamp_seconds': chunk_info['start_timestamp_seconds'],
                    'start_timestamp': chunk_info['start_timestamp']
                }

                # Add the timestamped URL
                timestamp_sec = int(final_chunk['start_timestamp_seconds'])
                final_chunk['video_url_with_timestamp'] = f"https://www.youtube.com/watch?v={video_id}&t={timestamp_sec}"
                video_chunks.append(final_chunk)

            # Write all chunks for this video to a single JSON file
            if video_chunks:
                output_filename = os.path.join(PROCESSED_DIR, f"{video_id}_processed.json")
                with open(output_filename, 'w', encoding='utf-8') as f:
                    json.dump(video_chunks, f, indent=2)
                
                processed_files += 1
                total_chunks += total_chunks_for_file

        except Exception as e:
            skipped_files[str(e)].append(filename)
            print(f"❌ Error processing {filename}: {e}")
            continue
    
    # Print summary
    print("\n" + "="*80)
    print(" Processing complete!")
    print(f" Processed {processed_files} transcript files")
    print(f" Created {total_chunks} total chunks")

    if skipped_files:
        print("\n⚠️ Skipped Files Report:")
        for reason, files in skipped_files.items():
            print(f"\nREASON: {reason} ({len(files)} files)")
            for file_info in files:
                if isinstance(file_info, dict):
                    print(f"- {file_info.get('filename', 'Unknown file')}: {file_info.get('reason', 'No reason specified')}")
                else:
                    print(f"- {file_info}") # Handle cases where it's just a filename string
    
    print("="*80)

def main():
    print("="*80)
    print("Starting main function...")
    
    # Ensure directories exist
    ensure_directories()
    
    # Load video metadata
    metadata_dict = load_metadata()
    print(f"Loaded metadata_dict with {len(metadata_dict)} entries")
    
    # Check if transcripts directory exists
    if not os.path.exists(TRANSCRIPT_DIR):
        print(f"ERROR: Transcript directory '{TRANSCRIPT_DIR}' not found!")
        return
    
    # Check if any transcript files exist
    transcript_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith('.txt')]
    print(f"Found {len(transcript_files)} transcript files: {transcript_files}")
    
    # Process transcripts
    process_transcripts(metadata_dict)
    
    # Check processed output
    if os.path.exists(PROCESSED_DIR):
        processed_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
        print(f"Created {len(processed_files)} processed files: {processed_files}")
    
    print("\n Script execution complete! Your transcripts are now ready for RAG.")

if __name__ == "__main__":
    main() 