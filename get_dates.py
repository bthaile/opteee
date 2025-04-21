import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv
import sys
import re
import time

# Load environment variables
print("Loading environment variables...")
load_dotenv()

# Get API key from environment
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
if not YOUTUBE_API_KEY:
    YOUTUBE_API_KEY = "AIzaSyBB3r6glp3TDQCoK5r0Kjj4-leRizGnIzE"
print(f"API Key loaded: {YOUTUBE_API_KEY[:8]}...")

# Channel handle
CHANNEL_HANDLE = "@OutlierTrading"

# Define headers
HEADERS = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

def make_request(url, params, max_retries=3):
    """Make an API request with retry logic"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=HEADERS)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"Rate limit hit, waiting 60 seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(60)  # Wait 60 seconds on rate limit
            else:
                print(f"HTTP Error: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(5)  # Wait 5 seconds on other errors
        except Exception as e:
            print(f"Error making request: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(5)
    return None

def get_channel_id_from_handle():
    """Get channel ID from handle using channel lookup"""
    print(f"🔍 Getting channel ID for @{CHANNEL_HANDLE}...")
    
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'id',
        'q': f"@{CHANNEL_HANDLE}",
        'type': 'channel',
        'key': YOUTUBE_API_KEY
    }
    
    try:
        data = make_request(url, params)
        if data and data.get('items'):
            channel_id = data['items'][0]['id']['channelId']
            print(f"✅ Found channel ID: {channel_id}")
            return channel_id
    except Exception as e:
        print(f"❌ Error getting channel ID: {e}")
    
    return None

def get_channel_videos():
    """Get all videos from the channel using YouTube Data API"""
    print("🔍 Getting video metadata...")
    
    if not YOUTUBE_API_KEY:
        print("❌ No YouTube API key found in environment!")
        return
    
    # First get channel ID
    channel_id = get_channel_id_from_handle()
    if not channel_id:
        print("❌ Could not get channel ID!")
        return
    
    videos = []
    seen_video_ids = set()  # Track seen video IDs
    next_page_token = None
    page_count = 0
    max_pages = 10  # Limit to 10 pages (500 videos) to avoid excessive API usage
    
    while page_count < max_pages:
        try:
            page_count += 1
            print(f"\nFetching page {page_count}...")
            
            # Build search URL
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'id',
                'channelId': channel_id,
                'maxResults': 50,
                'order': 'date',
                'type': 'video',
                'key': YOUTUBE_API_KEY
            }
            if next_page_token:
                params['pageToken'] = next_page_token
            
            # Make request with retry logic
            search_response = make_request(search_url, params)
            if not search_response:
                print("Failed to get search response after retries")
                break
            
            if not search_response.get('items'):
                print("No videos found in search response")
                break
                
            # Filter out duplicate video IDs
            video_ids = []
            for item in search_response['items']:
                video_id = item['id']['videoId']
                if video_id not in seen_video_ids:
                    video_ids.append(video_id)
                    seen_video_ids.add(video_id)
            
            if not video_ids:
                print("No new video IDs found")
                break
                
            print(f"Found {len(video_ids)} new video IDs")
            
            # Then get full video details including status
            print(f"Fetching details for {len(video_ids)} videos...")
            
            # Build videos URL
            videos_url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'snippet,status,contentDetails,statistics',
                'id': ','.join(video_ids),
                'key': YOUTUBE_API_KEY
            }
            
            # Make request with retry logic
            videos_response = make_request(videos_url, params)
            if not videos_response:
                print("Failed to get video details after retries")
                break
            
            if not videos_response.get('items'):
                print("No video details found in response")
                break
                
            for item in videos_response['items']:
                try:
                    video_id = item['id']
                    snippet = item['snippet']
                    status = item['status']
                    content_details = item['contentDetails']
                    statistics = item['statistics']
                    
                    # Get publishAt from status if available, fallback to snippet publishedAt
                    publish_date = status.get('publishAt') or snippet.get('publishedAt')
                    
                    if publish_date:
                        # Convert ISO 8601 format to YYYYMMDD format
                        dt = datetime.strptime(publish_date, '%Y-%m-%dT%H:%M:%SZ')
                        upload_date = dt.strftime('%Y%m%d')
                    else:
                        upload_date = None
                    
                    print(f"\nVideo {video_id}:")
                    print(f"  Title: {snippet['title']}")
                    print(f"  Upload date: {upload_date}")
                    print(f"  Publish date: {publish_date}")
                    
                    video_info = {
                        'video_id': video_id,
                        'title': snippet['title'],
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'upload_date': upload_date,
                        'publish_date': publish_date,
                        'description': snippet['description'],
                        'channel_title': snippet['channelTitle'],
                        'privacy_status': status.get('privacyStatus'),
                        'license': status.get('license'),
                        'embeddable': status.get('embeddable'),
                        'duration': content_details.get('duration'),
                        'dimension': content_details.get('dimension'),
                        'definition': content_details.get('definition'),
                        'caption': content_details.get('caption')
                    }
                    videos.append(video_info)
                except Exception as e:
                    print(f"Error processing video item: {e}")
                    continue
            
            # Save progress after each page
            print(f"\nSaving progress ({len(videos)} videos so far)...")
            with open('video_metadata.json', 'w', encoding='utf-8') as f:
                json.dump(videos, f, indent=2, ensure_ascii=False)
            
            next_page_token = search_response.get('nextPageToken')
            if not next_page_token:
                print("No more pages to fetch")
                break
                
            # Add a small delay between pages
            time.sleep(2)
                
        except Exception as e:
            print(f"Error in main loop: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            break
    
    print(f"\n📊 Summary:")
    print(f"  Total videos found: {len(videos)}")
    print(f"  Videos with upload dates: {sum(1 for v in videos if v.get('upload_date'))}")
    print(f"  Videos with publish dates: {sum(1 for v in videos if v.get('publish_date'))}")
    print(f"  Videos without dates: {sum(1 for v in videos if not v.get('upload_date') and not v.get('publish_date'))}")
    print(f"📁 Saved metadata to video_metadata.json")

if __name__ == "__main__":
    print("Starting script...")
    get_channel_videos()
    print("Script completed.") 