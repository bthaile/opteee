import yt_dlp
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Channel URLs
CHANNEL_URLS = [
    'https://www.youtube.com/@OutlierTrading/videos',
    'https://www.youtube.com/@OutlierTrading/shorts',
    'https://www.youtube.com/@OutlierTrading/streams',
    'https://www.youtube.com/@OutlierTrading/podcasts'
]

def main():
    """Get upload dates for all videos"""
    print("🔍 Getting video metadata...")
    
    ydl_opts = {
        'ignoreerrors': True,
        'quiet': True,
        'extract_flat': 'in_playlist',
        'dateformat': '%Y%m%d',
        'playlistend': 5000,
    }

    all_videos_data = []
    
    for channel_url in CHANNEL_URLS:
        print(f"Processing: {channel_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                data = ydl.extract_info(channel_url, download=False)
                video_entries = data.get('entries', [])
                
                for entry in video_entries:
                    if entry:
                        video_id = entry.get('id')
                        upload_date = entry.get('upload_date')
                        print(f"\n📥 Found video {video_id}")
                        print(f"  Upload date: {upload_date}")
                        
                        video_info = {
                            'video_id': video_id,
                            'title': entry.get('title', 'No Title'),
                            'url': f"https://www.youtube.com/watch?v={video_id}" if video_id else None,
                            'upload_date': upload_date,
                            'view_count': entry.get('view_count'),
                            'duration': entry.get('duration'),
                            'description': entry.get('description')
                        }
                        all_videos_data.append(video_info)
            except Exception as e:
                print(f"Error processing {channel_url}: {e}")

    # Remove duplicates
    seen_ids = set()
    unique_videos = []
    for video in all_videos_data:
        if video['video_id'] not in seen_ids:
            seen_ids.add(video['video_id'])
            unique_videos.append(video)
            print(f"\n📝 Unique video {video['video_id']}")
            print(f"  Upload date: {video.get('upload_date', 'None')}")

    # Save to JSON
    with open('video_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(unique_videos, f, indent=2, ensure_ascii=False)

    print(f"\n📊 Summary:")
    print(f"  Total videos found: {len(unique_videos)}")
    print(f"  Videos with upload dates: {sum(1 for v in unique_videos if v.get('upload_date'))}")
    print(f"  Videos without upload dates: {sum(1 for v in unique_videos if not v.get('upload_date'))}")
    print(f"📁 Saved metadata to video_metadata.json")

if __name__ == "__main__":
    main() 