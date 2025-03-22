import yt_dlp
import csv

channel_url = 'https://www.youtube.com/@OutlierTrading/videos'

ydl_opts = {
    'extract_flat': True,
    'dump_single_json': True,
    'quiet': True
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    data = ydl.extract_info(channel_url, download=False)

video_entries = data.get('entries', [])

with open('outlier_trading_videos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'URL'])

    for entry in video_entries:
        title = entry.get('title', 'No Title')
        video_id = entry.get('id')
        if video_id:
            url = f"https://www.youtube.com/watch?v={video_id}"
            writer.writerow([title, url])

print(f"✅ {len(video_entries)} videos saved to outlier_trading_videos.csv")
