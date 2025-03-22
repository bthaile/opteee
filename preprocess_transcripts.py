import os
import re
import pandas as pd
import json
from tqdm import tqdm

# Configuration
TRANSCRIPT_DIR = "transcripts"
PROCESSED_DIR = "processed_transcripts"
METADATA_FILE = "outlier_trading_videos_metadata.csv"
CHUNK_SIZE = 250  # Target words per chunk
OVERLAP = 50  # Words of overlap between chunks

print("="*80)
print(f"TRANSCRIPT PREPROCESSING SCRIPT - VERBOSE MODE")
print(f"Chunk size: {CHUNK_SIZE} words with {OVERLAP} words overlap")
print("="*80)

def load_metadata():
    """Load video metadata from CSV file"""
    print(f"\n[1/3] Loading video metadata from {METADATA_FILE}...")
    try:
        df = pd.read_csv(METADATA_FILE)
        print(f"Successfully loaded CSV with {len(df)} rows")
        # Create a dictionary with video_id as key for faster lookups
        metadata_dict = {}
        for _, row in df.iterrows():
            # Extract YouTube video ID from URL
            video_id = row.get('video_id')
            if not video_id and 'url' in row:
                # Try to extract from URL if video_id is not directly available
                url = row['url']
                if 'youtube.com' in url:
                    video_id = url.split('v=')[1].split('&')[0]
                elif 'youtu.be' in url:
                    video_id = url.split('/')[-1]
            
            if video_id:
                metadata_dict[video_id] = {
                    'title': row.get('title', ''),
                    'url': row.get('url', ''),
                    'upload_date': row.get('upload_date', ''),
                    'duration': row.get('duration', ''),
                    'channel_name': row.get('channel_name', ''),
                    'description': row.get('description', '')
                }
        
        print(f"✅ Loaded metadata for {len(metadata_dict)} videos")
        return metadata_dict
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

def get_video_id_from_filename(filename):
    """Extract video ID from transcript filename"""
    # Remove file extension
    base_name = os.path.splitext(filename)[0]
    return base_name

def process_transcripts(metadata_dict):
    """Process all transcripts in the transcript directory"""
    # Create output directory if it doesn't exist
    os.makedirs(PROCESSED_DIR, exist_ok=True)
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
    skipped_files = 0
    
    # Process each transcript
    print("\n[3/3] Beginning processing of transcript files...")
    print("="*80)
    for filename in tqdm(transcript_files):
        try:
            file_path = os.path.join(TRANSCRIPT_DIR, filename)
            video_id = get_video_id_from_filename(filename)
            
            # Get metadata for this video
            metadata = metadata_dict.get(video_id, {})
            
            # If no metadata found, use minimal info from filename
            if not metadata:
                print(f"⚠️ No metadata found for {video_id}, using filename only")
                metadata = {
                    'title': video_id,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'upload_date': '',
                    'duration': '',
                    'channel_name': '',
                    'description': ''
                }
            
            # Read the transcript
            with open(file_path, 'r', encoding='utf-8') as f:
                transcript_text = f.read()
            
            # Clean the transcript and extract timestamps
            cleaned_text, timestamps = extract_timestamps_and_clean(transcript_text)
            
            # Skip if cleaned text is too short
            if len(cleaned_text.split()) < 10:
                print(f"⚠️ Skipping {filename} - too short after cleaning")
                skipped_files += 1
                continue
            
            # Split into chunks with timestamp information
            chunks_with_timestamps = chunk_text_with_timestamps(cleaned_text, timestamps)
            
            # Create JSON for each chunk with metadata
            chunk_data = []
            for i, chunk_info in enumerate(chunks_with_timestamps):
                chunk_obj = {
                    'text': chunk_info['text'],
                    'metadata': {
                        'video_id': video_id,
                        'title': metadata.get('title', ''),
                        'url': metadata.get('url', ''),
                        'upload_date': metadata.get('upload_date', ''),
                        'duration': metadata.get('duration', ''),
                        'channel_name': metadata.get('channel_name', ''),
                        'chunk_index': i,
                        'total_chunks': len(chunks_with_timestamps),
                        'start_timestamp': chunk_info['start_timestamp'],
                        'start_timestamp_seconds': chunk_info['start_timestamp_seconds'],
                        'video_url_with_timestamp': f"{metadata.get('url', f'https://www.youtube.com/watch?v={video_id}')}&t={int(chunk_info['start_timestamp_seconds'])}"
                    }
                }
                chunk_data.append(chunk_obj)
            
            # Save processed chunks to JSON file
            output_path = os.path.join(PROCESSED_DIR, f"{video_id}_processed.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(chunk_data, f, indent=2)
            
            total_chunks += len(chunks_with_timestamps)
            processed_files += 1
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            skipped_files += 1
    
    print("="*80)
    print(f"\n✅ Processing complete!")
    print(f"✅ Processed {processed_files} transcript files")
    print(f"✅ Created {total_chunks} total chunks")
    print(f"⚠️ Skipped {skipped_files} files due to errors or insufficient content")
    print(f"📁 Results saved to {PROCESSED_DIR}/")
    print("="*80)

def main():
    # Load video metadata
    metadata_dict = load_metadata()
    
    # Process transcripts
    process_transcripts(metadata_dict)
    
    print("\n📝 Script execution complete! Your transcripts are now ready for RAG.")

if __name__ == "__main__":
    main() 