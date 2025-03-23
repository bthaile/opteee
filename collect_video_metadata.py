import os
import json
from datetime import datetime
import yt_dlp
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

# Load environment variables from .env file
load_dotenv()

# Configuration variables
INPUT_JSON = 'outlier_trading_videos.json'  # Changed from CSV to JSON
OUTPUT_JSON = 'outlier_trading_videos_metadata.json'
OUTPUT_CSV = 'outlier_trading_videos_metadata.csv'  # Keep CSV output for backward compatibility
TRANSCRIPT_DIR = 'transcripts'
API_KEY = os.getenv('YOUTUBE_API_KEY')  # Load from .env file

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
                
                all_video_data[video_id] = {
                    'video_id': video_id,
                    'title': snippet.get('title'),
                    'url': f"https://www.youtube.com/watch?v={video_id}",  # Standard URL format
                    'channel_name': snippet.get('channelTitle'),
                    'upload_date': snippet.get('publishedAt'),
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

def main():
    # Check if API key is set
    use_api = API_KEY is not None and API_KEY.strip() != '' and API_KEY != 'YOUR_YOUTUBE_API_KEY'
    if not use_api:
        print("Warning: YouTube API key not set. Some metadata will be limited.")
    
    # Read existing JSON
    try:
        with open(INPUT_JSON, 'r', encoding='utf-8') as f:
            videos_data = json.load(f)
        
        # Convert JSON to DataFrame for consistent processing
        df = pd.DataFrame(videos_data)
        print(f"Read {len(df)} videos from {INPUT_JSON}")
    except Exception as e:
        print(f"Error reading input JSON: {e}")
        return
    
    # Extract video IDs from URLs
    df['video_id'] = df['url'].apply(extract_video_id)
    
    # Filter out rows with invalid video IDs
    df = df[df['video_id'].notna()]
    print(f"Found {len(df)} videos with valid YouTube IDs")
    
    # Get YouTube API data if available
    video_api_data = {}
    if use_api:
        print("Fetching data from YouTube API...")
        video_ids = df['video_id'].dropna().tolist()
        video_api_data = get_video_details_from_youtube(video_ids)
    
    # Prepare to collect all metadata
    all_metadata = {}
    
    # Process each video
    for i, row in df.iterrows():
        video_id = row.get('video_id')
        url = row.get('url')
        title = row.get('title')
        
        if not video_id:
            continue
        
        print(f"Processing video {i+1}/{len(df)}: {title or url}")
        
        # Initialize with basic data
        metadata = {
            'video_id': video_id,
            'title': title,
            'url': url if url else f"https://www.youtube.com/watch?v={video_id}"
        }
        
        # Add transcript info
        transcript_info = get_transcript_info(video_id)
        metadata.update(transcript_info)
        
        # Add content summary (would need ML or manual input)
        metadata['content_summary'] = f"Content about {title}" if title else "Options trading content"
        
        # Try to get API data first
        if video_id in video_api_data:
            metadata.update(video_api_data[video_id])
        
        # Fill in gaps with yt-dlp data
        ytdlp_data = get_video_details_from_yt_dlp(url, video_id)
        
        # Only update fields that are not already filled
        for key, value in ytdlp_data.items():
            if key not in metadata or metadata.get(key) is None:
                metadata[key] = value
        
        # Ensure video_id is consistently used
        metadata['video_id'] = video_id
        
        # Add to all metadata
        all_metadata[video_id] = metadata
    
    # Save to JSON file
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_metadata, f, indent=2, ensure_ascii=False)
    
    # Also create a CSV for backward compatibility
    metadata_df = pd.DataFrame(list(all_metadata.values()))
    metadata_df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    
    print(f"✅ Metadata for {len(all_metadata)} videos saved to {OUTPUT_JSON} and {OUTPUT_CSV}")

if __name__ == "__main__":
    main() 