import yt_dlp
import json

channel_urls = [
    'https://www.youtube.com/@OutlierTrading/videos',
    'https://www.youtube.com/@OutlierTrading/shorts',
    'https://www.youtube.com/@OutlierTrading/streams',
    'https://www.youtube.com/@OutlierTrading/podcasts'
]

ydl_opts = {
    'ignoreerrors': True,
    'quiet': True,
    'extract_flat': True,  # Changed to True for faster initial extraction
    'playlistend': 5000,   # Increased limit
}

all_videos_data = []

for channel_url in channel_urls:
    print(f"Processing: {channel_url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            data = ydl.extract_info(channel_url, download=False)
            video_entries = data.get('entries', [])
            
            for entry in video_entries:
                if entry:  # Check if entry is not None
                    video_info = {
                        'video_id': entry.get('id'),
                        'title': entry.get('title', 'No Title'),
                        'url': f"https://www.youtube.com/watch?v={entry.get('id')}" if entry.get('id') else None,
                        'upload_date': entry.get('upload_date'),
                        'view_count': entry.get('view_count'),
                        'duration': entry.get('duration'),
                        'description': entry.get('description')
                    }
                    all_videos_data.append(video_info)
        except Exception as e:
            print(f"Error processing {channel_url}: {e}")

# Remove duplicates based on video_id
seen_ids = set()
unique_videos = []
for video in all_videos_data:
    if video['video_id'] not in seen_ids:
        seen_ids.add(video['video_id'])
        unique_videos.append(video)

with open('outlier_trading_videos.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(unique_videos, jsonfile, indent=4, ensure_ascii=False)

print(f"✅ {len(unique_videos)} unique videos saved to outlier_trading_videos.json")
