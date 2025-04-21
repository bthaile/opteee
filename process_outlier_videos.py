import yt_dlp
import json
import os
import time
import pytube
import whisper
from urllib.parse import urlparse, parse_qs
import subprocess
import shutil
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from datetime import datetime
import re
from tqdm import tqdm
from collections import defaultdict
import preprocess_transcripts as transcript_processor  # Import with alias to avoid name conflicts

# Load environment variables
load_dotenv()

# Channel URLs
CHANNEL_URLS = [
    'https://www.youtube.com/@OutlierTrading/videos',
    'https://www.youtube.com/@OutlierTrading/shorts',
    'https://www.youtube.com/@OutlierTrading/streams',
    'https://www.youtube.com/@OutlierTrading/podcasts'
]

# File paths
VIDEOS_JSON = 'outlier_trading_videos.json'
MISSING_TRANSCRIPTS_JSON = 'missing_transcripts.json'
TRANSCRIPT_DIR = 'transcripts'
AUDIO_DIR = 'audio_files'
PROCESSED_DIR = 'processed_transcripts'
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
MANUAL_PROCESSING_FILE = "manual_processing_needed.json"

# Configuration for transcript preprocessing
CHUNK_SIZE = 250  # Target words per chunk
OVERLAP = 50  # Words of overlap between chunks

# Debug: Print API key info (first few characters)
if YOUTUBE_API_KEY:
    print(f"\n🔑 API Key loaded: {YOUTUBE_API_KEY[:8]}...")
else:
    print("\n❌ WARNING: No YouTube API key found in environment variables!")
    print("For proper metadata, please add your YouTube API key to a .env file:")
    print("1. Create a .env file in the same directory as this script")
    print("2. Add the following line: YOUTUBE_API_KEY=your_api_key_here")
    print("3. Get an API key from: https://console.cloud.google.com/apis/credentials")
    print("4. Enable the YouTube Data API v3 in the Google Cloud Console")
    print("Without an API key, metadata will be incomplete and chunked files may have missing properties.")

def save_manual_processing_list(video_list):
    """Save list of videos that need manual processing"""
    if os.path.exists(MANUAL_PROCESSING_FILE):
        with open(MANUAL_PROCESSING_FILE, 'r') as f:
            existing_data = json.load(f)
        # Merge with existing data
        merged_list = list(set(existing_data + video_list))
    else:
        merged_list = video_list
        
    with open(MANUAL_PROCESSING_FILE, 'w') as f:
        json.dump(merged_list, f, indent=2)
    
    print(f"📝 Saved {len(merged_list)} videos for manual processing to {MANUAL_PROCESSING_FILE}")

def find_ffmpeg():
    """Find ffmpeg executable in common locations"""
    print("\n🔍 Looking for ffmpeg...")
    
    # Try using which command
    try:
        result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            ffmpeg_path = result.stdout.strip()
            print(f"✅ Found ffmpeg at: {ffmpeg_path}")
            return ffmpeg_path
    except:
        pass
    
    # Try common locations
    common_paths = [
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/opt/homebrew/bin/ffmpeg',
        '/opt/local/bin/ffmpeg',
        '/Applications/ffmpeg',
        os.path.expanduser('~/.brew/bin/ffmpeg'),  # Homebrew user directory
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"✅ Found ffmpeg at: {path}")
            return path
    
    print("\n❌ ffmpeg not found! Please install it:")
    print("\nFor macOS (using Homebrew):")
    print("1. Install Homebrew if you don't have it:")
    print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
    print("2. Install ffmpeg:")
    print("   brew install ffmpeg")
    print("\nFor other systems:")
    print("- Ubuntu/Debian: sudo apt-get install ffmpeg")
    print("- Windows: Download from https://ffmpeg.org/download.html")
    print("- Or use your system's package manager")
    
    raise FileNotFoundError("ffmpeg not found. Please install it using the instructions above.")

def collect_video_metadata(videos_data):
    """Collect detailed metadata for videos using YouTube Data API"""
    print("\n📊 Collecting detailed video metadata...")
    
    if not YOUTUBE_API_KEY:
        print("❌ ERROR: No YouTube API key found in .env file!")
        print("Please add your YouTube API key to the .env file:")
        print("YOUTUBE_API_KEY=your_api_key_here")
        return videos_data
    
    # Validate API key format
    if YOUTUBE_API_KEY.endswith('.apps.googleusercontent.com'):
        print("❌ ERROR: Invalid API key format!")
        print("You're using an OAuth client ID instead of an API key.")
        print("Please get a proper YouTube API key from Google Cloud Console:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project or select existing one")
        print("3. Enable YouTube Data API v3")
        print("4. Create credentials (API key)")
        print("5. Add the API key to your .env file")
        return videos_data
    
    try:
        print("🔌 Initializing YouTube API client...")
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        print("✅ YouTube API client initialized successfully")
        
        # Test the API key with a simple request
        print("🔍 Testing API key with a sample request...")
        test_response = youtube.videos().list(part='snippet', id='dQw4w9WgXcQ').execute()
        print("✅ API key test successful!")
    except HttpError as e:
        print(f"❌ ERROR: Invalid API key! Error: {e}")
        print("Please check your API key in the .env file")
        return videos_data
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize YouTube API: {e}")
        return videos_data
    
    enhanced_videos = []
    
    for video in videos_data:
        try:
            video_id = video.get('video_id')
            if not video_id:
                print(f"⚠️ Skipping video with no ID: {video}")
                continue
                
            print(f"\n🔍 Processing video {video_id}")
                
            # Get video details
            video_response = youtube.videos().list(
                part='snippet,contentDetails,statistics,status',
                id=video_id
            ).execute()
            
            if not video_response.get('items'):
                print(f"⚠️ No metadata found for video {video_id}")
                enhanced_videos.append(video)
                continue
                
            video_details = video_response['items'][0]
            snippet = video_details.get('snippet', {})
            statistics = video_details.get('statistics', {})
            content_details = video_details.get('contentDetails', {})
            status = video_details.get('status', {})
            
            # Get publishAt from status if available, fallback to snippet publishedAt
            publish_date = status.get('publishAt') or snippet.get('publishedAt')
            
            if publish_date:
                # Convert ISO 8601 format to YYYYMMDD format for upload_date
                try:
                    dt = datetime.strptime(publish_date, '%Y-%m-%dT%H:%M:%SZ')
                    upload_date = dt.strftime('%Y%m%d')
                except Exception as e:
                    upload_date = publish_date
            else:
                # Fallback to yt-dlp upload_date if available
                upload_date = video.get('upload_date', '')
            
            # Enhance video data with additional metadata
            enhanced_video = {
                **video,  # Keep existing data
                'title': snippet.get('title', video.get('title', '')),
                'description': snippet.get('description', ''),
                'published_at': publish_date,  # Keep original ISO format
                'upload_date': upload_date,  # Add formatted upload date
                'channel_id': snippet.get('channelId', ''),
                'channel_title': snippet.get('channelTitle', ''),
                'channel_name': snippet.get('channelTitle', ''),  # Add channel_name for compatibility
                'tags': snippet.get('tags', []),
                'category_id': snippet.get('categoryId', ''),
                'live_broadcast_content': snippet.get('liveBroadcastContent', ''),
                'default_language': snippet.get('defaultLanguage', ''),
                'duration': content_details.get('duration', ''),
                'dimension': content_details.get('dimension', ''),
                'definition': content_details.get('definition', ''),
                'caption': content_details.get('caption', ''),
                'licensed_content': content_details.get('licensedContent', False),
                'projection': content_details.get('projection', ''),
                'favorite_count': statistics.get('favoriteCount', '0'),
                'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                'content_summary': generate_content_summary(snippet.get('description', '')),
                'privacy_status': status.get('privacyStatus', ''),
                'license': status.get('license', ''),
                'embeddable': status.get('embeddable', True)
            }
            
            enhanced_videos.append(enhanced_video)
            
            # Respect API quota limits
            time.sleep(0.1)
            
        except HttpError as e:
            print(f"❌ API Error for video {video_id}: {e}")
            enhanced_videos.append(video)
        except Exception as e:
            print(f"❌ Error processing video {video_id}: {e}")
            enhanced_videos.append(video)
    
    return enhanced_videos

def generate_content_summary(description):
    """Generate a concise summary of the video content from description"""
    if not description:
        return ""
    
    # Remove URLs and special characters
    clean_desc = re.sub(r'http\S+|www\S+', '', description)
    clean_desc = re.sub(r'[^\w\s.,!?-]', ' ', clean_desc)
    
    # Split into sentences and take first few
    sentences = re.split(r'[.!?]+', clean_desc)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Take up to 3 sentences
    summary = '. '.join(sentences[:3])
    
    # Truncate if too long
    if len(summary) > 200:
        summary = summary[:197] + '...'
    
    return summary

def scrape_channel_videos():
    """Step 1: Scrape all videos from the channel"""
    print("\n🔍 Step 1: Scraping channel videos...")
    
    ydl_opts = {
        'ignoreerrors': True,
        'quiet': True,
        'extract_flat': 'in_playlist',
        'dateformat': '%Y%m%d',
        'playlistend': 5000,
        'no_warnings': True,
        'ignoreerrors': True,
        'no_check_certificates': True,
        'prefer_insecure': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }

    all_videos_data = []
    scheduled_videos = []
    
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
                        live_status = entry.get('live_status', '')
                        availability = entry.get('availability', '')
                        
                        # Skip scheduled videos
                        if live_status == 'scheduled' or availability == 'scheduled':
                            print(f"\n⏰ Skipping scheduled video {video_id}")
                            scheduled_videos.append({
                                'video_id': video_id,
                                'title': entry.get('title', 'No Title'),
                                'url': f"https://www.youtube.com/watch?v={video_id}" if video_id else None,
                                'scheduled_time': entry.get('scheduled_time', ''),
                                'upload_date': upload_date
                            })
                            continue
                        
                        print(f"\n📥 Found video {video_id}")
                        print(f"  Title: {entry.get('title', 'No Title')}")
                        print(f"  Upload date from yt-dlp: {upload_date}")
                        
                        video_info = {
                            'video_id': video_id,
                            'title': entry.get('title', 'No Title'),
                            'url': f"https://www.youtube.com/watch?v={video_id}" if video_id else None,
                            'upload_date': upload_date,
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
            print(f"  Title: {video.get('title', 'No Title')}")
            print(f"  Upload date: {video.get('upload_date', 'None')}")

    # Save scheduled videos to a separate file
    if scheduled_videos:
        print("\n📝 Saving scheduled videos list...")
        with open('scheduled_videos.json', 'w', encoding='utf-8') as f:
            json.dump(scheduled_videos, f, indent=2)
        print(f"✅ Saved {len(scheduled_videos)} scheduled videos to scheduled_videos.json")

    # Try to enhance metadata with YouTube API if available
    if YOUTUBE_API_KEY:
        print("\n🔍 Attempting to enhance metadata with YouTube API...")
        unique_videos = collect_video_metadata(unique_videos)
        
        # Debug: Print first video metadata after API enhancement
        if unique_videos and len(unique_videos) > 0:
            print("\n✅ API Metadata Enhancement Sample:")
            sample_video = unique_videos[0]
            print(f"  Video ID: {sample_video.get('video_id', 'MISSING')}")
            print(f"  Title: {sample_video.get('title', 'MISSING')}")
            print(f"  Channel: {sample_video.get('channel_title', 'MISSING')}")
            print(f"  Published At: {sample_video.get('published_at', 'MISSING')}")
            print(f"  Duration: {sample_video.get('duration', 'MISSING')}")
    else:
        print("\n⚠️ No YouTube API key found - using yt-dlp metadata only")
        # Get additional metadata from yt-dlp for each video
        enhanced_videos = []
        for video in unique_videos:
            try:
                video_url = video['url']
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    video.update({
                        'description': info.get('description', ''),
                        'channel_id': info.get('channel_id', ''),
                        'channel_title': info.get('channel', ''),
                        'tags': info.get('tags', []),
                        'upload_date': info.get('upload_date', video.get('upload_date', '')),
                    })
            except Exception as e:
                print(f"Error getting additional metadata for {video['video_id']}: {e}")
            enhanced_videos.append(video)
        unique_videos = enhanced_videos
        
        # Debug: Print first video metadata after yt-dlp enhancement
        if unique_videos and len(unique_videos) > 0:
            print("\n✅ yt-dlp Metadata Enhancement Sample:")
            sample_video = unique_videos[0]
            print(f"  Video ID: {sample_video.get('video_id', 'MISSING')}")
            print(f"  Title: {sample_video.get('title', 'MISSING')}")
            print(f"  Channel: {sample_video.get('channel_title', 'MISSING')}")
            print(f"  Upload Date: {sample_video.get('upload_date', 'MISSING')}")
            print(f"  Duration: {sample_video.get('duration', 'MISSING')}")

    # Save to metadata file
    print("\n📝 Saving metadata to file...")
    with open('outlier_trading_videos_metadata.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(unique_videos, jsonfile, indent=4, ensure_ascii=False)
    print("✅ Saved to outlier_trading_videos_metadata.json")
    
    print(f"\n📊 Final Summary:")
    print(f"  Total videos found: {len(unique_videos)}")
    print(f"  Scheduled videos skipped: {len(scheduled_videos)}")
    print(f"  Videos with upload dates: {sum(1 for v in unique_videos if v.get('upload_date'))}")
    print(f"  Videos without upload dates: {sum(1 for v in unique_videos if not v.get('upload_date'))}")
    return unique_videos

def find_missing_transcripts(videos_data):
    """Step 2: Identify videos missing transcripts"""
    print("\n🔍 Step 2: Finding videos without transcripts...")
    
    # First, check if transcripts directory exists
    if not os.path.exists(TRANSCRIPT_DIR):
        print(f"❌ ERROR: Transcript directory '{TRANSCRIPT_DIR}' does not exist!")
        return []
    
    # List all files in transcripts directory
    transcript_files = os.listdir(TRANSCRIPT_DIR)
    print(f"\n📁 Found {len(transcript_files)} files in {TRANSCRIPT_DIR}")
    
    missing_transcripts = []
    
    for video in videos_data:
        video_id = video['video_id']
        transcript_exists = False
        
        # List all possible filenames we're looking for
        possible_filenames = [
            f"{video_id}.txt",
            f"video_{video_id}.txt",
            f"{video.get('title', '').replace(' ', '_')}.txt"
        ]
        
        print(f"\n🔍 Checking video {video_id}:")
        print(f"  Title: {video.get('title', 'No Title')}")
        print(f"  Looking for files: {possible_filenames}")
        
        for filename in possible_filenames:
            full_path = os.path.join(TRANSCRIPT_DIR, filename)
            if os.path.exists(full_path):
                transcript_exists = True
                print(f"  ✅ Found transcript: {filename}")
                break
        
        if not transcript_exists:
            print(f"  ❌ No transcript found for video {video_id}")
            missing_transcripts.append(video)
    
    print(f"\n📊 Summary:")
    print(f"  Total videos checked: {len(videos_data)}")
    print(f"  Total transcript files: {len(transcript_files)}")
    print(f"  Videos missing transcripts: {len(missing_transcripts)}")
    
    # Save missing transcripts to JSON
    with open(MISSING_TRANSCRIPTS_JSON, 'w', encoding='utf-8') as f:
        json.dump(missing_transcripts, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Saved missing transcripts list to {MISSING_TRANSCRIPTS_JSON}")
    return missing_transcripts

def download_audio(url, output_path, ffmpeg_path):
    """Download audio from YouTube video with multiple fallback methods"""
    print(f"⬇️ Downloading audio for {url}...")
    
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Extract video_id from URL
    video_id = url.split('=')[-1]
    print(f"Video ID: {video_id}")
    
    # Method 1: Direct FFmpeg streaming method (most reliable)
    try:
        print("Trying direct FFmpeg streaming method...")
        
        # This method uses FFmpeg to directly stream from YouTube
        cmd = [
            ffmpeg_path,
            '-y',  # Overwrite output file
            '-v', 'warning',  # Only show warnings/errors
            '-http_proxy', '',  # Clear any proxy settings
            '-user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            '-referer', 'https://www.youtube.com/',
            '-i', url,  # Input from YouTube URL
            '-vn',  # Skip video
            '-acodec', 'libmp3lame',  # Use MP3 codec
            '-ar', '44100',  # Audio sample rate
            '-ab', '192k',  # Audio bitrate
            output_path  # Output file
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check for scheduled video error in stderr
        if "This live event will begin in" in result.stderr:
            print("⚠️ Video is scheduled for future broadcast - skipping")
            # Create a note file to indicate this is a scheduled video
            note_path = output_path.replace('.mp3', '.note.txt')
            with open(note_path, 'w') as f:
                f.write(f"Scheduled video: {url}\nCreated note file on {datetime.now()}\n")
                f.write("This video is scheduled for future broadcast.\n")
            return False
            
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            raise Exception(f"FFmpeg failed with code {result.returncode}")
            
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"✅ Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
            return True
    except Exception as e:
        print(f"Method 1 (direct FFmpeg) failed: {str(e)}")
    
    # Method 2: Try with mobile API
    try:
        print("Trying mobile API method...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'no_check_certificates': True,
            'prefer_insecure': True,
            'http_headers': {
                'User-Agent': 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'X-YouTube-Client-Name': '3',
                'X-YouTube-Client-Version': '17.36.4',
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                if "This live event will begin in" in str(e):
                    print("⚠️ Video is scheduled for future broadcast - skipping")
                    # Create a note file to indicate this is a scheduled video
                    note_path = output_path.replace('.mp3', '.note.txt')
                    with open(note_path, 'w') as f:
                        f.write(f"Scheduled video: {url}\nCreated note file on {datetime.now()}\n")
                        f.write("This video is scheduled for future broadcast.\n")
                    return False
                raise e
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✅ Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
                return True
    except Exception as e:
        print(f"Method 2 (mobile API) failed: {str(e)}")
    
    # Method 3: Try with browser API + different format options
    try:
        print("Trying browser API method...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'no_check_certificates': True,
            'prefer_insecure': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except Exception as e:
                if "This live event will begin in" in str(e):
                    print("⚠️ Video is scheduled for future broadcast - skipping")
                    # Create a note file to indicate this is a scheduled video
                    note_path = output_path.replace('.mp3', '.note.txt')
                    with open(note_path, 'w') as f:
                        f.write(f"Scheduled video: {url}\nCreated note file on {datetime.now()}\n")
                        f.write("This video is scheduled for future broadcast.\n")
                    return False
                raise e
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✅ Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
                return True
    except Exception as e:
        print(f"Method 3 (browser API) failed: {str(e)}")
    
    # If all methods fail, record this URL for manual processing
    print("👤 Flagging video for manual processing...")
    save_manual_processing_list([url])
    
    # Create a note file to indicate this is a failed download
    note_path = output_path.replace('.mp3', '.note.txt')
    with open(note_path, 'w') as f:
        f.write(f"Failed to download audio for: {url}\nCreated note file on {datetime.now()}\n")
        f.write("This video has been flagged for manual processing.\n")
    
    raise Exception("All download methods failed")

def process_transcripts(missing_videos):
    """Step 3: Process missing transcripts with Whisper"""
    print("\n🎯 Step 3: Processing missing transcripts with Whisper...")
    
    # Create necessary directories
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    # Initialize Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    ffmpeg_path = find_ffmpeg()
    print(f"Using ffmpeg at: {ffmpeg_path}")
    
    successful = []
    failed = []
    
    for i, video in enumerate(missing_videos, 1):
        url = video['url']
        video_id = video['video_id']
        print(f"\nProcessing video {i}/{len(missing_videos)}: {url}")
        
        # Add retry logic
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Setup filenames
                audio_path = os.path.join(AUDIO_DIR, f"{video_id}.mp3")
                transcript_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
                
                # Check if we already have a valid audio file
                if os.path.exists(audio_path):
                    file_size = os.path.getsize(audio_path)
                    if file_size > 10000:  # More than 10KB
                        print(f"✅ Found existing audio file: {audio_path} ({file_size} bytes)")
                    else:
                        print(f"⚠️ Found small audio file ({file_size} bytes), will try to download again")
                        os.remove(audio_path)  # Remove small file
                else:
                    print(f"⬇️ No existing audio file found, downloading...")
                
                # Download audio if needed
                if not os.path.exists(audio_path):
                    download_audio(url, audio_path, ffmpeg_path)
                
                # Check for possible double extension
                double_ext_path = audio_path + '.mp3'
                if os.path.exists(double_ext_path) and not os.path.exists(audio_path):
                    print(f"🔄 Fixing double extension: {double_ext_path} -> {audio_path}")
                    shutil.move(double_ext_path, audio_path)
                
                # Verify the audio file exists before transcribing
                if not os.path.exists(audio_path):
                    print(f"❌ Audio file not found after download: {audio_path}")
                    raise Exception("Audio file not found after download")
                
                # Print file info
                print(f"🔍 Audio file info: {os.path.getsize(audio_path)} bytes")
                
                # Transcribe
                print("Transcribing audio...")
                result = model.transcribe(audio_path)
                
                # Save transcript
                with open(transcript_path, 'w') as f:
                    for segment in result["segments"]:
                        f.write(f"{segment['start']:.2f}s: {segment['text']}\n")
                
                successful.append(video)
                print(f"✅ Successfully processed {video_id}")
                break  # Success, exit retry loop
                
            except Exception as e:
                retry_count += 1
                print(f"❌ Attempt {retry_count} failed: {e}")
                if retry_count == max_retries:
                    print(f"❌ All attempts failed for {video_id}")
                    failed.append(video)
                else:
                    print(f"Retrying in 5 seconds...")
                    time.sleep(5)
    
    return successful, failed

def perform_transcript_preprocessing(metadata):
    """Process all transcripts in the transcript directory using the imported module"""
    print("\n📝 Step 4: Preprocessing transcripts...")
    
    # Convert to dictionary if it's a list
    metadata_dict = {}
    if isinstance(metadata, list):
        print("Converting list to dictionary...")
        for video in metadata:
            video_id = video.get('video_id')
            if video_id:
                metadata_dict[video_id] = video
        print(f"Converted {len(metadata)} videos to dictionary with {len(metadata_dict)} entries")
    else:
        metadata_dict = metadata
        print(f"Using provided dictionary with {len(metadata_dict)} entries")
    
    # Debug: Print a few sample entries to verify metadata
    if metadata_dict:
        print("\nSample metadata entries for preprocessing:")
        for i, (video_id, video) in enumerate(list(metadata_dict.items())[:3]):
            print(f"\nSample video {i+1}: {video_id}")
            print(f"  Title: {video.get('title', 'MISSING')}")
            print(f"  Upload date (published_at): {video.get('published_at', 'MISSING')}")
            print(f"  Upload date (upload_date): {video.get('upload_date', 'MISSING')}")
            print(f"  Duration: {video.get('duration', 'MISSING')}")
            print(f"  Channel (channel_title): {video.get('channel_title', 'MISSING')}")
            print(f"  Channel (channel_name): {video.get('channel_name', 'MISSING')}")
            
    # Hand off processing to the imported module
    try:
        transcript_processor.process_transcripts(metadata_dict)
        print(f"\n✅ Transcript preprocessing complete using preprocess_transcripts module!")
    except Exception as e:
        print(f"❌ Error in preprocess_transcripts module: {e}")
        print(f"Error details: {str(e)}")
        raise  # Re-raise the error to be handled by the caller

def main():
    print("🚀 Starting Outlier Trading video processing pipeline...")
    
    # Step 1: Scrape videos (force this step)
    print("\n📥 Step 1: Scraping channel videos...")
    videos = scrape_channel_videos()
    
    # Step 2: Find missing transcripts
    print("\n🔍 Step 2: Finding videos without transcripts...")
    missing_videos = find_missing_transcripts(videos)
    
    if missing_videos:
        # Step 3: Process missing transcripts
        successful, failed = process_transcripts(missing_videos)
    else:
        print("✅ No videos need processing!")
    
    # Step 4: Use preprocess_transcripts module for chunking
    print("\n📝 Step 4: Preprocessing transcripts...")
    
    # Important: Don't use the videos list directly, load the metadata from the saved JSON file
    # This ensures we're using the same metadata that preprocess_transcripts.py would use
    print("Loading metadata from file for transcript preprocessing...")
    try:
        with open('outlier_trading_videos_metadata.json', 'r', encoding='utf-8') as f:
            metadata_json = json.load(f)
            
        # Convert to dictionary if it's a list
        if isinstance(metadata_json, list):
            metadata_dict = {}
            for item in metadata_json:
                video_id = item.get('video_id')
                if video_id:
                    metadata_dict[video_id] = item
            print(f"Converted {len(metadata_json)} videos to dictionary with {len(metadata_dict)} entries")
        else:
            metadata_dict = metadata_json
            print(f"Loaded dictionary with {len(metadata_dict)} entries")
            
        # Debug: Print sample metadata
        if metadata_dict and len(metadata_dict) > 0:
            first_key = list(metadata_dict.keys())[0]
            sample_video = metadata_dict[first_key]
            print("\n✅ Sample Metadata for Preprocessing:")
            print(f"  Video ID: {sample_video.get('video_id', 'MISSING')}")
            print(f"  Title: {sample_video.get('title', 'MISSING')}")
            print(f"  Channel: {sample_video.get('channel_title', 'MISSING')}")
            print(f"  Published At: {sample_video.get('published_at', 'MISSING')}")
            print(f"  Duration: {sample_video.get('duration', 'MISSING')}")
        
        perform_transcript_preprocessing(metadata_dict)
    except Exception as e:
        print(f"❌ Error loading metadata for preprocessing: {e}")
        print("Falling back to using videos list...")
        perform_transcript_preprocessing(videos)
    
    # Final report
    print("\n📊 Final Summary:")
    print(f"Total videos found: {len(videos)}")
    print(f"Videos needing transcripts: {len(missing_videos) if 'missing_videos' in locals() else 0}")
    print(f"Successfully processed: {len(successful) if 'successful' in locals() else 0}")
    print(f"Failed to process: {len(failed) if 'failed' in locals() else 0}")
    
    if 'failed' in locals() and failed:
        print("\n❌ Failed videos:")
        for video in failed:
            print(f"- {video['url']}")

if __name__ == "__main__":
    main() 