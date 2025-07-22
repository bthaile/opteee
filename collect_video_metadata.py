import os
import json
from datetime import datetime
import yt_dlp
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
from pipeline_config import (
    VIDEOS_JSON, METADATA_JSON, TRANSCRIPT_DIR, 
    CHANNEL_URLS, YOUTUBE_API_KEY
)

# Load environment variables from .env file
load_dotenv()

# Configuration variables (using centralized config)
INPUT_JSON = VIDEOS_JSON
OUTPUT_JSON = METADATA_JSON
API_KEY = YOUTUBE_API_KEY

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    if not url or not isinstance(url, str):
        return None
        
    # Match standard YouTube URL
    if 'youtube.com/watch' in url:
        # Extract video ID from v parameter
        pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\s?]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Match youtu.be format
    elif 'youtu.be' in url:
        pattern = r'youtu\.be\/([^&\s?]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Match YouTube embed format
    elif 'youtube.com/embed/' in url:
        pattern = r'youtube\.com\/embed\/([^&\s?\/]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Last resort: try to find any 11-character ID in the URL
    pattern = r'(?:^|[^a-zA-Z0-9_-])([a-zA-Z0-9_-]{11})(?:$|[^a-zA-Z0-9_-])'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    
    return None

def get_transcript_info(video_id):
    """Get transcript file information if available."""
    transcript_info = {
        'transcript_path': None,
        'transcript_creation_date': None,
        'transcript_method': None
    }
    
    # Check different possible filenames
    possible_filenames = [
        f"{video_id}.txt",
        f"video_{video_id}.txt"
    ]
    
    for filename in possible_filenames:
        filepath = os.path.join(TRANSCRIPT_DIR, filename)
        if os.path.exists(filepath):
            transcript_info['transcript_path'] = filepath
            transcript_info['transcript_creation_date'] = datetime.fromtimestamp(
                os.path.getctime(filepath)).strftime('%Y-%m-%d')
            
            # Determine transcript method
            if os.path.getsize(filepath) > 0:
                with open(filepath, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.endswith('s:'):
                        transcript_info['transcript_method'] = 'Whisper'
                    else:
                        transcript_info['transcript_method'] = 'YouTube Captions'
            break
    
    return transcript_info

def get_video_details_from_youtube(video_ids):
    """Fetch video details from YouTube API in batches."""
    if not API_KEY:
        print("No YouTube API key provided. Skipping API requests.")
        return {}
        
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    all_video_data = {}
    batch_size = 50  # YouTube API allows up to 50 IDs per request
    
    # Process in batches to respect API limits
    for i in range(0, len(video_ids), batch_size):
        batch = video_ids[i:i+batch_size]
        
        try:
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=','.join(batch)
            )
            response = request.execute()
            
            for item in response.get('items', []):
                video_id = item['id']
                snippet = item.get('snippet', {})
                stats = item.get('statistics', {})
                content_details = item.get('contentDetails', {})
                
                # Format the upload_date from ISO 8601 to YYYYMMDD
                upload_date = snippet.get('publishedAt')
                if upload_date:
                    try:
                        from datetime import datetime
                        dt = datetime.strptime(upload_date, '%Y-%m-%dT%H:%M:%SZ')
                        formatted_upload_date = dt.strftime('%Y%m%d')
                    except Exception as e:
                        formatted_upload_date = upload_date  # Keep original if parsing fails
                else:
                    formatted_upload_date = None
                
                all_video_data[video_id] = {
                    'video_id': video_id,
                    'title': snippet.get('title'),
                    'url': f"https://www.youtube.com/watch?v={video_id}",  # Standard URL format
                    'channel_name': snippet.get('channelTitle'),
                    'upload_date': formatted_upload_date,  # Now properly formatted
                    'published_at': upload_date,  # Keep original ISO format as well
                    'duration': content_details.get('duration'),
                    'view_count': stats.get('viewCount'),
                    'description': snippet.get('description'),
                    'topics_tags': snippet.get('tags', []),
                    'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url')
                }
            
            print(f"Processed batch of {len(batch)} videos")
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            continue
    
    return all_video_data

def get_video_details_from_yt_dlp(url, video_id):
    """Fetch additional details using yt-dlp."""
    if not url:
        return {}
        
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Get the video_id from yt-dlp if available
            extracted_id = info.get('id', video_id)
            
            # Extract guest names from title and description
            guest_names = []
            title = info.get('title', '')
            description = info.get('description', '')
            
            # Basic guest detection (can be improved)
            if 'with' in title or 'featuring' in title or 'ft.' in title:
                guest_names.append('Guest mentioned in title')
            
            # Get available fields and ensure URL is correct
            standard_url = f"https://www.youtube.com/watch?v={extracted_id}"
            
            return {
                'video_id': extracted_id,
                'title': title,
                'url': standard_url,
                'duration_seconds': info.get('duration'),
                'upload_date': info.get('upload_date'),
                'view_count': info.get('view_count'),
                'description': description,
                'guest_names': guest_names,
                'likes': info.get('like_count'),
                'channel_name': info.get('channel', info.get('uploader')),
                'thumbnail_url': info.get('thumbnail')
            }
    except Exception as e:
        print(f"Error extracting info for {url}: {e}")
        return {
            'video_id': video_id,
            'url': f"https://www.youtube.com/watch?v={video_id}" if video_id else url
        }

def get_channel_videos(channel_urls):
    """Fetch all videos from channel URLs using yt-dlp."""
    all_videos = []
    
    # Use extract_flat for speed, but we'll enhance with API if available
    ydl_opts = {
        'extract_flat': 'in_playlist',  # Get more metadata than just 'True'
        'skip_download': True,
        'ignoreerrors': True,
        'quiet': True,
        'dateformat': '%Y%m%d',  # Format dates consistently
    }
    
    for url in channel_urls:
        print(f"Fetching videos from: {url}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=False)
                if 'entries' in result:
                    # Process each video entry
                    for entry in result['entries']:
                        if entry:
                            video_data = {
                                'video_id': entry.get('id'),
                                'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                                'title': entry.get('title'),
                                'upload_date': entry.get('upload_date'),  # yt-dlp format (YYYYMMDD if available)
                                'duration': entry.get('duration'),
                                'view_count': entry.get('view_count'),
                                'description': entry.get('description'),
                                'channel_name': entry.get('uploader') or entry.get('channel'),
                            }
                            all_videos.append(video_data)
                    print(f"Found {len(result['entries'])} videos in {url}")
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    
    return all_videos

def find_missing_transcripts(videos_data, transcript_dir="transcripts"):
    """Find videos that don't have transcripts."""
    missing_transcripts = []
    
    for video in videos_data:
        video_id = video['video_id']
        transcript_exists = False
        
        # Check different possible filenames
        possible_filenames = [
            f"{video_id}.txt",
            f"video_{video_id}.txt",
            f"{video.get('title', '').replace(' ', '_')}.txt"
        ]
        
        for filename in possible_filenames:
            if os.path.exists(os.path.join(transcript_dir, filename)):
                transcript_exists = True
                break
        
        if not transcript_exists:
            missing_transcripts.append(video)
    
    return missing_transcripts

def main():
    # Use centralized channel URLs from configuration
    channel_urls = CHANNEL_URLS
    
    # Get all videos from channel
    print("Fetching all channel videos...")
    all_videos = get_channel_videos(channel_urls)
    print(f"Found total of {len(all_videos)} videos")
    
    # If we have a YouTube API key, enhance the metadata
    if API_KEY:
        print(" Enhancing metadata with YouTube API...")
        video_ids = [video['video_id'] for video in all_videos if video.get('video_id')]
        print(f"Getting enhanced metadata for {len(video_ids)} videos...")
        
        enhanced_data = get_video_details_from_youtube(video_ids)
        
        # Merge enhanced data with basic data
        for video in all_videos:
            video_id = video.get('video_id')
            if video_id and video_id in enhanced_data:
                # Update with enhanced data, keeping existing data as fallback
                enhanced_video = enhanced_data[video_id]
                for key, value in enhanced_video.items():
                    if value is not None:  # Only update if enhanced data has a value
                        video[key] = value
        print(" Metadata enhancement complete")
    else:
        print("⚠️ No YouTube API key found - using basic yt-dlp metadata only")
    
    # Save all videos metadata
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_videos, f, indent=2, ensure_ascii=False)
    print(f"Saved metadata for {len(all_videos)} videos to {OUTPUT_JSON}")
    
    # Find videos missing transcripts
    missing_transcripts = find_missing_transcripts(all_videos)
    print(f"Found {len(missing_transcripts)} videos without transcripts")
    
    # Save missing transcripts list for whisper processing
    missing_transcripts_file = "missing_transcripts.json"
    with open(missing_transcripts_file, 'w', encoding='utf-8') as f:
        json.dump(missing_transcripts, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(missing_transcripts)} videos needing transcription to {missing_transcripts_file}")
    
    # Create a script to process missing transcripts with whisper
    whisper_batch_file = "process_missing_transcripts.sh"
    with open(whisper_batch_file, 'w') as f:
        f.write("#!/bin/bash\n\n")
        for video in missing_transcripts:
            f.write(f"python whisper_transcribe.py \"{video['url']}\"\n")
    os.chmod(whisper_batch_file, 0o755)  # Make executable
    
    # In the main() function, before creating process_missing_transcripts.sh:
    progress_data = {
        'processed': [],
        'failed': [video['url'] for video in missing_transcripts],
        'whisper_processed': []
    }
    with open('transcript_progress.json', 'w') as f:
        json.dump(progress_data, f, indent=2)
    
    print("\nNext steps:")
    print(f"1. Review the collected metadata in {OUTPUT_JSON}")
    print(f"2. Check {missing_transcripts_file} for videos needing transcription")
    print(f"3. Run ./{whisper_batch_file} to process missing transcripts with Whisper")

if __name__ == "__main__":
    main() 