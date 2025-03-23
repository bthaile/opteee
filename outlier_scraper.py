import yt_dlp
import json

channel_url = 'https://www.youtube.com/@OutlierTrading/videos'

ydl_opts = {
    'ignoreerrors': True,
    'quiet': True,
    'extract_flat': False,  # Set to False to get more complete info
    'playlistend': 1000,    # Set high limit to get all videos
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    data = ydl.extract_info(channel_url, download=False)

video_entries = data.get('entries', [])

videos_data = []
for entry in video_entries:
    video_info = {
        'title': entry.get('title', 'No Title'),
        'url': f"https://www.youtube.com/watch?v={entry.get('id')}" if entry.get('id') else None,
        'upload_date': entry.get('upload_date'),
        'view_count': entry.get('view_count'),
        'duration': entry.get('duration'),
        'description': entry.get('description')
    }
    videos_data.append(video_info)

with open('outlier_trading_videos.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(videos_data, jsonfile, indent=4, ensure_ascii=False)

print(f"✅ {len(videos_data)} videos saved to outlier_trading_videos.json")
