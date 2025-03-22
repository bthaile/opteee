import os
import csv
import json
from datetime import datetime
import yt_dlp
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables from .env file
load_dotenv()

# Configuration variables
INPUT_CSV = 'outlier_trading_videos.csv'
OUTPUT_CSV = 'outlier_trading_videos_metadata.csv'
TRANSCRIPT_DIR = 'transcripts'
API_KEY = os.getenv('YOUTUBE_API_KEY')  # Load from .env file

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    if 'youtu.be' in url:
        return url.split('/')[-1]
    elif 'youtube.com/watch' in url:
        return url.split('v=')[1].split('&')[0]
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

def get_video_details_from_yt_dlp(url):
    """Fetch additional details using yt-dlp."""
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Extract guest names from title and description
            guest_names = []
            title = info.get('title', '')
            description = info.get('description', '')
            
            # Basic guest detection (can be improved)
            if 'with' in title or 'featuring' in title or 'ft.' in title:
                guest_names.append('Guest mentioned in title')
            
            # Get available fields
            return {
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
        return {}

def main():
    # Check if API key is set
    if API_KEY == 'YOUR_YOUTUBE_API_KEY':
        print("Warning: YouTube API key not set. Some metadata will be limited.")
        use_api = False
    else:
        use_api = True
    
    # Read existing CSV
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"Read {len(df)} videos from {INPUT_CSV}")
    except Exception as e:
        print(f"Error reading input CSV: {e}")
        return
    
    # Extract video IDs
    df['video_id'] = df['URL'].apply(extract_video_id)
    
    # Get YouTube API data if available
    video_api_data = {}
    if use_api:
        print("Fetching data from YouTube API...")
        video_ids = df['video_id'].dropna().tolist()
        video_api_data = get_video_details_from_youtube(video_ids)
    
    # Prepare to collect all metadata
    all_metadata = []
    
    # Process each video
    for i, row in df.iterrows():
        video_id = row.get('video_id')
        url = row.get('URL')
        title = row.get('Title')
        
        if not video_id or not url:
            continue
        
        print(f"Processing video {i+1}/{len(df)}: {title}")
        
        # Initialize with basic data
        metadata = {
            'video_id': video_id,
            'title': title,
            'url': url
        }
        
        # Add transcript info
        transcript_info = get_transcript_info(video_id)
        metadata.update(transcript_info)
        
        # Add content summary (would need ML or manual input)
        metadata['content_summary'] = f"Content about {title}"
        
        # Try to get API data first
        if video_id in video_api_data:
            metadata.update(video_api_data[video_id])
        
        # Fill in gaps with yt-dlp data
        ytdlp_data = get_video_details_from_yt_dlp(url)
        
        # Only update fields that are not already filled
        for key, value in ytdlp_data.items():
            if key not in metadata or metadata.get(key) is None:
                metadata[key] = value
        
        all_metadata.append(metadata)
    
    # Convert to DataFrame and save
    metadata_df = pd.DataFrame(all_metadata)
    
    # Format durations and dates
    if 'duration_seconds' in metadata_df.columns:
        metadata_df['duration'] = metadata_df['duration_seconds'].apply(
            lambda x: str(datetime.utcfromtimestamp(x).strftime('%H:%M:%S')) if x else None
        )
    
    # Save to CSV
    metadata_df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Metadata for {len(metadata_df)} videos saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main() 