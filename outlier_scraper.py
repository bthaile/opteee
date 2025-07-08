import yt_dlp
import json
from pipeline_config import CHANNEL_URLS, VIDEOS_JSON

channel_urls = CHANNEL_URLS

ydl_opts = {
    'ignoreerrors': True,
    'quiet': False,  # Changed to False for more debug info
    'extract_flat': True,  # Changed to True for faster initial extraction
    'playlistend': 10000,   # Increased limit significantly
    'writesubtitles': False,  # Don't download subtitles during scraping
    'writeautomaticsub': False,  # Don't download auto-generated subtitles
    'no_warnings': False,  # Show warnings for debugging
}

all_videos_data = []
url_stats = {}

for channel_url in channel_urls:
    print(f"Processing: {channel_url}")
    url_stats[channel_url] = {'found': 0, 'errors': 0}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            data = ydl.extract_info(channel_url, download=False)
            if not data:
                print(f"  ❌ No data returned for {channel_url}")
                url_stats[channel_url]['errors'] += 1
                continue
                
            video_entries = data.get('entries', [])
            print(f"  📹 Found {len(video_entries)} videos")
            
            for entry in video_entries:
                if entry:  # Check if entry is not None
                    video_info = {
                        'video_id': entry.get('id'),
                        'title': entry.get('title', 'No Title'),
                        'url': f"https://www.youtube.com/watch?v={entry.get('id')}" if entry.get('id') else None,
                        'upload_date': entry.get('upload_date'),
                        'duration': entry.get('duration'),
                        'description': entry.get('description'),
                        'view_count': entry.get('view_count'),
                        'like_count': entry.get('like_count'),
                        'source_url': channel_url  # Track which URL found this video
                    }
                    all_videos_data.append(video_info)
                    url_stats[channel_url]['found'] += 1
                    
        except Exception as e:
            print(f"  ❌ Error processing {channel_url}: {e}")
            url_stats[channel_url]['errors'] += 1

# Remove duplicates based on video_id
seen_ids = set()
unique_videos = []
duplicate_count = 0

for video in all_videos_data:
    if video['video_id'] and video['video_id'] not in seen_ids:
        seen_ids.add(video['video_id'])
        unique_videos.append(video)
    else:
        duplicate_count += 1

# Save results
with open(VIDEOS_JSON, 'w', encoding='utf-8') as jsonfile:
    json.dump(unique_videos, jsonfile, indent=4, ensure_ascii=False)

# Print detailed statistics
print(f"\n📊 Discovery Results:")
print(f"=" * 60)
print(f"✅ {len(unique_videos)} unique videos saved to {VIDEOS_JSON}")
print(f"🔄 {duplicate_count} duplicates removed")
print(f"📺 {len(all_videos_data)} total videos found (including duplicates)")

print(f"\n📋 Per-URL Statistics:")
for url, stats in url_stats.items():
    print(f"  {url}")
    print(f"    📹 Found: {stats['found']} videos")
    print(f"    ❌ Errors: {stats['errors']}")

# Additional analysis
video_years = {}
for video in unique_videos:
    if video.get('upload_date'):
        year = video['upload_date'][:4]
        video_years[year] = video_years.get(year, 0) + 1

if video_years:
    print(f"\n📅 Videos by Year:")
    for year in sorted(video_years.keys(), reverse=True):
        print(f"  {year}: {video_years[year]} videos")

print(f"\n💡 Channel likely has more videos if YouTube shows 655 vs our {len(unique_videos)}")
print(f"   Missing videos could be: private, unlisted, deleted, or community posts")
