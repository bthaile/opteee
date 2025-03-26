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
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
MANUAL_PROCESSING_FILE = "manual_processing_needed.json"

# Debug: Print API key info (first few characters)
if YOUTUBE_API_KEY:
    print(f"\n🔑 API Key loaded: {YOUTUBE_API_KEY[:8]}...")
else:
    print("\n❌ No API key found in environment variables!")

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
                continue
                
            # Get video details
            video_response = youtube.videos().list(
                part='snippet,contentDetails,statistics',
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
            
            # Format upload date from YouTube API
            published_at = snippet.get('publishedAt', '')
            if published_at:
                # Convert ISO 8601 format to YYYYMMDD format
                try:
                    dt = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
                    upload_date = dt.strftime('%Y%m%d')
                except:
                    upload_date = published_at
            else:
                # Fallback to yt-dlp upload_date if available
                upload_date = video.get('upload_date', '')
            
            # Enhance video data with additional metadata
            enhanced_video = {
                **video,  # Keep existing data
                'title': snippet.get('title', video.get('title', '')),
                'description': snippet.get('description', ''),
                'published_at': published_at,
                'upload_date': upload_date,  # Add formatted upload date
                'channel_id': snippet.get('channelId', ''),
                'channel_title': snippet.get('channelTitle', ''),
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
                'view_count': statistics.get('viewCount', '0'),
                'like_count': statistics.get('likeCount', '0'),
                'comment_count': statistics.get('commentCount', '0'),
                'favorite_count': statistics.get('favoriteCount', '0'),
                'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                'content_summary': generate_content_summary(snippet.get('description', ''))
            }
            
            enhanced_videos.append(enhanced_video)
            print(f"✅ Enhanced metadata for video {video_id} (upload date: {upload_date})")
            
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
        'extract_flat': True,
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

    # Remove duplicates
    seen_ids = set()
    unique_videos = []
    for video in all_videos_data:
        if video['video_id'] not in seen_ids:
            seen_ids.add(video['video_id'])
            unique_videos.append(video)

    # Collect enhanced metadata
    unique_videos = collect_video_metadata(unique_videos)

    # Save both JSON and CSV formats
    with open(VIDEOS_JSON, 'w', encoding='utf-8') as jsonfile:
        json.dump(unique_videos, jsonfile, indent=4, ensure_ascii=False)
    
    # Also save as CSV for compatibility
    df = pd.DataFrame(unique_videos)
    csv_file = VIDEOS_JSON.replace('.json', '.csv')
    df.to_csv(csv_file, index=False, encoding='utf-8')

    print(f"✅ Found {len(unique_videos)} unique videos")
    print(f"📁 Saved metadata to {VIDEOS_JSON} and {csv_file}")
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
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            raise Exception(f"FFmpeg failed with code {result.returncode}")
            
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"✅ Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
            return True
    except Exception as e:
        print(f"Method 1 (direct FFmpeg) failed: {str(e)}")
    
    # Method 2: Try with yt-dlp with mobile API
    try:
        print("Trying yt-dlp with mobile API...")
        
        # Create fake cookies as a fallback
        fake_cookies = "fake_cookies.txt"
        with open(fake_cookies, "w") as f:
            f.write("# Netscape HTTP Cookie File\n")
            f.write(".youtube.com\tTRUE\t/\tFALSE\t2147483647\tCONSENT\tYES+cb.20220301-11-p0.en+FX+123\n")
            f.write(".youtube.com\tTRUE\t/\tFALSE\t2147483647\tLOGIN_INFO\tdummy_value\n")
            f.write(".youtube.com\tTRUE\t/\tFALSE\t2147483647\tPREF\tf1=50000000&f6=8\n")
            f.write(".youtube.com\tTRUE\t/\tFALSE\t2147483647\tYSC\tdummy_value\n")
            f.write(".youtube.com\tTRUE\t/\tFALSE\t2147483647\tWIDE\t1\n")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
            'ffmpeg_location': os.path.dirname(ffmpeg_path),
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'cookiefile': fake_cookies,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_warnings': True,
            'quiet': False,
            'api_key': YOUTUBE_API_KEY,
            'player_client': 'ANDROID',
            'user_agent': 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'],
                    'player_skip': ['webpage', 'configs', 'js'],
                }
            },
            'http_headers': {
                'User-Agent': 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'X-YouTube-Client-Name': '3',
                'X-YouTube-Client-Version': '17.36.4',
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✅ Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
                return True
    except Exception as e:
        print(f"Method 2 (mobile API) failed: {str(e)}")
    
    # Method 3: Try with browser API + different format options
    try:
        print("Trying yt-dlp with browser API and alternative format settings...")
        ydl_opts.update({
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'force_generic_extractor': True,
            'extract_flat': True,
            'youtube_include_dash_manifest': False,
            'player_client': 'WEB',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.youtube.com/',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['web', 'web_embedded'],
                    'player_skip': ['webpage', 'configs', 'js'],
                }
            },
        })
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✅ Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
                return True
    except Exception as e:
        print(f"Method 3 (browser API) failed: {str(e)}")
    
    # Method 4: Try direct yt-dlp command
    try:
        print("Trying direct yt-dlp command...")
        cmd = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--output", output_path,
            "--cookies", fake_cookies,
            "--force-ipv4",
            "--geo-bypass",
            "--user-agent", "com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip",
            url
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"✅ Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
            return True
    except Exception as e:
        print(f"Method 4 (direct yt-dlp) failed: {str(e)}")
    
    # Method 5: Try using pytube with custom options
    try:
        print("Trying pytube method...")
        pytube.innertube._default_clients['ANDROID'] = pytube.innertube._default_clients['WEB']
        yt = pytube.YouTube(
            url,
            use_oauth=False,
            allow_oauth_cache=False
        )
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if audio_stream:
            temp_file = audio_stream.download(filename=f"temp_{os.path.basename(output_path)}")
            
            # Convert to mp3 using ffmpeg
            cmd = [
                ffmpeg_path,
                '-i', temp_file,
                '-codec:a', 'libmp3lame',
                '-qscale:a', '2',
                output_path,
                '-y'
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✅ Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
                return True
    except Exception as e:
        print(f"Method 5 (pytube) failed: {str(e)}")
    
    # Last resort: Look for any related files
    print("Looking for any files related to this video...")
    for file in os.listdir(os.path.dirname(output_path)):
        if video_id in file:
            file_path = os.path.join(os.path.dirname(output_path), file)
            if os.path.getsize(file_path) > 0:
                # Copy or convert to the expected output path
                if file.endswith('.mp3'):
                    shutil.copy(file_path, output_path)
                else:
                    try:
                        cmd = [
                            ffmpeg_path,
                            '-i', file_path,
                            '-codec:a', 'libmp3lame',
                            '-qscale:a', '2',
                            output_path,
                            '-y'
                        ]
                        subprocess.run(cmd, check=True, capture_output=True)
                    except:
                        shutil.copy(file_path, output_path)
                
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    print(f"✅ Successfully copied/converted to {output_path} (size: {os.path.getsize(output_path)} bytes)")
                    return True
    
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

def main():
    print("🚀 Starting Outlier Trading video processing pipeline...")
    
    # Step 1: Scrape videos
    videos = scrape_channel_videos()
    
    # Step 2: Find missing transcripts
    missing_videos = find_missing_transcripts(videos)
    
    if not missing_videos:
        print("✅ No videos need processing!")
        return
    
    # Step 3: Process missing transcripts
    successful, failed = process_transcripts(missing_videos)
    
    # Final report
    print("\n📊 Final Summary:")
    print(f"Total videos found: {len(videos)}")
    print(f"Videos needing transcripts: {len(missing_videos)}")
    print(f"Successfully processed: {len(successful)}")
    print(f"Failed to process: {len(failed)}")
    
    if failed:
        print("\n❌ Failed videos:")
        for video in failed:
            print(f"- {video['url']}")

if __name__ == "__main__":
    main() 