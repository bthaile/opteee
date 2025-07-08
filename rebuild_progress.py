import json
import os
import re
from urllib.parse import urlparse, parse_qs
from pipeline_config import VIDEOS_JSON, TRANSCRIPT_DIR, TRANSCRIPT_PROGRESS_JSON

# Use centralized configuration
JSON_FILE = VIDEOS_JSON
PROGRESS_FILE = TRANSCRIPT_PROGRESS_JSON

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    if 'youtube.com' in url:
        query = urlparse(url).query
        params = parse_qs(query)
        return params.get('v', ['unknown'])[0]
    elif 'youtu.be' in url:
        return url.split('/')[-1]
    return 'unknown'

def clean_title(title):
    """Clean a title to match transcript filename format"""
    # Remove special characters and replace spaces with underscores
    cleaned = re.sub(r'[^\w\s-]', '', title)
    cleaned = re.sub(r'[\s]+', '_', cleaned)
    return cleaned

def main():
    # Get all YouTube URLs and titles from JSON
    all_video_info = []
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        videos = json.load(f)
        for video in videos:
            if video.get('url') and video['url'].strip():
                all_video_info.append({
                    'url': video['url'],
                    'title': video.get('title', ''),
                    'id': video.get('video_id') or extract_video_id(video['url'])
                })
    
    print(f"Found {len(all_video_info)} videos in JSON")
    
    # Get list of transcript files
    transcript_files = os.listdir(TRANSCRIPT_DIR)
    print(f"Found {len(transcript_files)} transcript files")
    
    # Extract video IDs from transcript filenames that are IDs
    id_based_files = set()
    title_based_files = set()
    whisper_processed_files = set()
    
    for filename in transcript_files:
        if not filename.endswith('.txt'):
            continue
            
        base_name = os.path.splitext(filename)[0]
        
        # Check for known test videos that were processed with Whisper
        if base_name in ['dQw4w9WgXcQ', 'jNQXAC9IVRw']:
            whisper_processed_files.add(base_name)
        elif re.match(r'^[a-zA-Z0-9_-]{11}$', base_name):
            # This looks like a YouTube ID (11 characters of alphanumeric, underscore, hyphen)
            id_based_files.add(base_name)
        else:
            # This is a title-based filename
            title_based_files.add(filename)
    
    # Categorize videos
    processed_urls = []
    whisper_processed_urls = []
    failed_urls = []
    failed_videos = []
    
    # Add test videos to whisper processed
    for video_id in whisper_processed_files:
        whisper_processed_urls.append(f"https://www.youtube.com/watch?v={video_id}")
    
    # Process each video
    for video in all_video_info:
        # Skip videos we've already categorized (test videos)
        if video['id'] in whisper_processed_files:
            continue
            
        # Check if video ID matches a transcript file
        if video['id'] in id_based_files:
            processed_urls.append(video['url'])
            continue
        
        # Try to match by title
        if video['title']:
            cleaned_title = clean_title(video['title'])
            title_match = False
            
            # Check for matching title-based files
            for filename in title_based_files:
                basename = os.path.splitext(filename)[0]
                # Try partial matching since titles might have been truncated or modified
                if cleaned_title in basename or basename in cleaned_title:
                    title_match = True
                    break
                
                # Check for significant word overlap
                title_words = set(cleaned_title.lower().split('_'))
                filename_words = set(basename.lower().split('_'))
                common_words = title_words.intersection(filename_words)
                if len(common_words) >= 3 and len(common_words) / len(title_words) > 0.5:
                    title_match = True
                    break
            
            if title_match:
                processed_urls.append(video['url'])
                continue
        
        # If we reach here, this video has no transcript
        failed_urls.append(video['url'])
        failed_videos.append(video)
    
    # Build progress file
    progress = {
        'processed': processed_urls,
        'failed': failed_urls,
        'whisper_processed': whisper_processed_urls
    }
    
    # Save the progress file
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)
    
    print(f"Progress file rebuilt: {PROGRESS_FILE}")
    print(f"  - Processed: {len(processed_urls)} videos")
    print(f"  - Failed: {len(failed_urls)} videos")
    print(f"  - Whisper processed: {len(whisper_processed_urls)} videos")
    
    # Print failed video details
    if failed_videos:
        print("\nFailed videos (need processing):")
        for i, video in enumerate(failed_videos, 1):
            print(f"{i}. {video['title']} - {video['url']} (ID: {video['id']})")

if __name__ == "__main__":
    main() 