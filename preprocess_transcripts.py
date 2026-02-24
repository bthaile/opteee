#!/usr/bin/env python3
"""
Transcript Preprocessing Script

This script processes raw transcript files into chunked JSON format for vector search.
It creates overlapping chunks with metadata including timestamps and video URLs.

Usage:
    python3 preprocess_transcripts.py                    # Process all transcripts
    python3 preprocess_transcripts.py --force            # Force reprocess all files
    python3 preprocess_transcripts.py --video-id ABC123  # Process specific video
"""

import os
import json
import re
import argparse
from datetime import datetime
from tqdm import tqdm

from pipeline_config import (
    VIDEOS_JSON, TRANSCRIPT_DIR, PROCESSED_DIR,
    CHUNK_SIZE, OVERLAP, MIN_CHUNK_WORDS, ensure_directories, get_metadata_file
)


def parse_timestamp(timestamp_str):
    """Parse timestamp string (e.g., '123.45s') to seconds"""
    try:
        # Remove 's' suffix and convert to float
        return float(timestamp_str.rstrip('s'))
    except (ValueError, AttributeError):
        return 0.0


def format_timestamp(seconds):
    """Format seconds into HH:MM:SS or MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def normalize_upload_date(value):
    """Normalize upload/publish date values to YYYYMMDD when possible."""
    if value is None:
        return None

    if isinstance(value, (int, float)):
        value = str(int(value))

    if not isinstance(value, str):
        return None

    value = value.strip()
    if not value or value.lower() in {"unknown", "n/a", "none", "null"}:
        return None

    if re.fullmatch(r"\d{8}", value):
        return value

    try:
        if "T" in value:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt.strftime("%Y%m%d")
        dt = datetime.strptime(value.split("T")[0], "%Y-%m-%d")
        return dt.strftime("%Y%m%d")
    except ValueError:
        return None


def load_video_metadata():
    """Load video metadata from the videos JSON file"""
    try:
        metadata_file = get_metadata_file()
    except FileNotFoundError:
        print(f"⚠️  {VIDEOS_JSON} not found. Metadata will be limited.")
        return {}
    
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            videos = json.load(f)
        
        # Create lookup by video_id and normalize date keys across metadata formats
        metadata_lookup = {}
        for video in videos:
            video_id = video.get('video_id')
            if not video_id:
                continue

            normalized = dict(video)
            normalized_upload_date = normalize_upload_date(
                video.get('upload_date')
                or video.get('published_at')
                or video.get('publishedAt')
                or video.get('publish_date')
            )
            normalized['upload_date'] = normalized_upload_date

            published_at = (
                video.get('published_at')
                or video.get('publishedAt')
                or video.get('publish_date')
            )
            if published_at:
                normalized['published_at'] = published_at

            metadata_lookup[video_id] = normalized

        return metadata_lookup
    except Exception as e:
        print(f"⚠️  Error loading video metadata: {e}")
        return {}


def parse_transcript(file_path):
    """Parse a transcript file into a list of (timestamp, text) tuples"""
    segments = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match timestamp and text: "123.45s: Some text here"
        pattern = r'(\d+\.?\d*)s:\s*(.+?)(?=\n\d+\.?\d*s:|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for timestamp_str, text in matches:
            timestamp = parse_timestamp(timestamp_str + 's')
            text = text.strip()
            if text:
                segments.append({
                    'timestamp': timestamp,
                    'text': text
                })
        
        return segments
        
    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return []


def create_chunks(segments, chunk_size=CHUNK_SIZE, overlap=OVERLAP, min_words=MIN_CHUNK_WORDS):
    """
    Create overlapping chunks from transcript segments.
    
    Args:
        segments: List of {'timestamp': float, 'text': str} dicts
        chunk_size: Target number of words per chunk
        overlap: Number of words to overlap between chunks
        min_words: Minimum words required for a valid chunk
    
    Returns:
        List of chunk dictionaries with text and timestamp info
    """
    if not segments:
        return []
    
    chunks = []
    
    # Combine all text with timestamp markers
    all_words = []
    word_timestamps = []
    
    for segment in segments:
        words = segment['text'].split()
        for word in words:
            all_words.append(word)
            word_timestamps.append(segment['timestamp'])
    
    if len(all_words) < min_words:
        # Return single chunk if too short
        return [{
            'text': ' '.join(all_words),
            'start_timestamp_seconds': segments[0]['timestamp'] if segments else 0,
            'end_timestamp_seconds': segments[-1]['timestamp'] if segments else 0,
            'word_count': len(all_words),
            'chunk_index': 0
        }]
    
    # Create overlapping chunks
    step_size = max(1, chunk_size - overlap)
    chunk_index = 0
    
    i = 0
    while i < len(all_words):
        # Get chunk words
        end_idx = min(i + chunk_size, len(all_words))
        chunk_words = all_words[i:end_idx]
        
        if len(chunk_words) >= min_words:
            chunk_text = ' '.join(chunk_words)
            start_ts = word_timestamps[i]
            end_ts = word_timestamps[end_idx - 1] if end_idx > 0 else start_ts
            
            chunks.append({
                'text': chunk_text,
                'start_timestamp_seconds': start_ts,
                'end_timestamp_seconds': end_ts,
                'word_count': len(chunk_words),
                'chunk_index': chunk_index
            })
            chunk_index += 1
        
        # Move to next chunk position
        i += step_size
        
        # If we're at the end and there's some remaining text, include it
        if i >= len(all_words):
            break
    
    return chunks


def process_transcript(video_id, transcript_path, video_metadata, force_reprocess=False):
    """
    Process a single transcript file into chunks.
    
    Args:
        video_id: The YouTube video ID
        transcript_path: Path to the raw transcript file
        video_metadata: Dict of video metadata keyed by video_id
        force_reprocess: Whether to reprocess existing files
    
    Returns:
        List of processed chunks with full metadata
    """
    output_path = os.path.join(PROCESSED_DIR, f"{video_id}_processed.json")
    
    # Skip if already processed and not forcing reprocess
    if os.path.exists(output_path) and not force_reprocess:
        return None
    
    # Parse transcript
    segments = parse_transcript(transcript_path)
    if not segments:
        return []
    
    # Create chunks
    chunks = create_chunks(segments)
    if not chunks:
        return []
    
    # Get video metadata
    metadata = video_metadata.get(video_id, {})
    title = metadata.get('title', video_id)
    base_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Add full metadata to each chunk
    processed_chunks = []
    resolved_upload_date = normalize_upload_date(
        metadata.get('upload_date')
        or metadata.get('published_at')
        or metadata.get('publishedAt')
    )

    for chunk in chunks:
        start_seconds = chunk['start_timestamp_seconds']
        
        processed_chunk = {
            'video_id': video_id,
            'title': title,
            'text': chunk['text'],
            'start_timestamp_seconds': start_seconds,
            'end_timestamp_seconds': chunk['end_timestamp_seconds'],
            'start_timestamp': format_timestamp(start_seconds),
            'video_url': base_url,
            'video_url_with_timestamp': f"{base_url}&t={int(start_seconds)}",
            'chunk_index': chunk['chunk_index'],
            'word_count': chunk['word_count'],
            'upload_date': resolved_upload_date,
            'published_at': metadata.get('published_at') or metadata.get('publishedAt'),
            'duration': metadata.get('duration'),
        }
        processed_chunks.append(processed_chunk)
    
    # Save processed chunks
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_chunks, f, indent=2, ensure_ascii=False)
    
    return processed_chunks


def main(force_reprocess=False, video_id=None):
    """
    Main preprocessing function.
    
    Args:
        force_reprocess: Whether to reprocess existing files
        video_id: Optional specific video ID to process
    
    Returns:
        True if successful, False otherwise
    """
    print("=" * 60)
    print("📝 TRANSCRIPT PREPROCESSING")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Ensure directories exist
    ensure_directories()
    
    # Load video metadata
    video_metadata = load_video_metadata()
    print(f"📋 Loaded metadata for {len(video_metadata)} videos")
    
    # Get transcript files to process
    if not os.path.exists(TRANSCRIPT_DIR):
        print(f"❌ Transcript directory not found: {TRANSCRIPT_DIR}")
        return False
    
    transcript_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith('.txt')]
    
    if video_id:
        # Filter to specific video
        transcript_files = [f for f in transcript_files if video_id in f]
    
    if not transcript_files:
        print(f"⚠️  No transcript files found in {TRANSCRIPT_DIR}")
        return True  # Not an error, just nothing to process
    
    print(f"📁 Found {len(transcript_files)} transcript files")
    print(f"⚙️  Chunk size: {CHUNK_SIZE} words, Overlap: {OVERLAP} words")
    
    # Process transcripts
    total_chunks = 0
    processed_count = 0
    skipped_count = 0
    failed_count = 0
    
    for filename in tqdm(transcript_files, desc="Processing transcripts"):
        # Extract video ID from filename
        vid_id = os.path.splitext(filename)[0]
        transcript_path = os.path.join(TRANSCRIPT_DIR, filename)
        
        try:
            result = process_transcript(vid_id, transcript_path, video_metadata, force_reprocess)
            
            if result is None:
                skipped_count += 1
            elif result:
                processed_count += 1
                total_chunks += len(result)
            else:
                failed_count += 1
                
        except Exception as e:
            print(f"\n❌ Error processing {filename}: {e}")
            failed_count += 1
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 PREPROCESSING SUMMARY")
    print("=" * 60)
    print(f"  ✅ Processed: {processed_count} transcripts")
    print(f"  ⏭️  Skipped (already done): {skipped_count}")
    print(f"  ❌ Failed: {failed_count}")
    print(f"  📦 Total chunks created: {total_chunks}")
    print(f"  📁 Output directory: {PROCESSED_DIR}/")
    
    if processed_count > 0:
        avg_chunks = total_chunks / processed_count
        print(f"  📈 Average chunks per transcript: {avg_chunks:.1f}")
    
    # Consider success if failure rate is acceptable
    # Count total files (including skipped as "successful")
    total_files = processed_count + skipped_count + failed_count
    if total_files > 0 and failed_count > 0:
        failure_rate = failed_count / total_files
        if failure_rate > 0.05:  # More than 5% failures
            print(f"  ⚠️  High failure rate: {failure_rate:.1%}")
            return False
        else:
            print(f"  ℹ️  Acceptable failure rate: {failure_rate:.1%} ({failed_count}/{total_files})")
    
    return True  # Success if acceptable failure rate or no failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Preprocess transcripts into chunks for vector search'
    )
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force reprocess all files'
    )
    parser.add_argument(
        '--video-id',
        type=str,
        help='Process only a specific video ID'
    )
    
    args = parser.parse_args()
    
    success = main(force_reprocess=args.force, video_id=args.video_id)
    
    if success:
        print("\n✅ Preprocessing completed successfully!")
    else:
        print("\n⚠️  Preprocessing completed with some failures")
        exit(1)

