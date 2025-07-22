import json
import os
import time
import pytube
import whisper
import tempfile
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm
import subprocess
import yt_dlp
import shutil
from datetime import datetime
import re
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Try to import browser_cookie3 (install if not present)
try:
    import browser_cookie3
    BROWSER_COOKIE_AVAILABLE = True
except ImportError:
    print("⚠️ browser_cookie3 not found, attempting to install...")
    try:
        subprocess.run(["pip", "install", "browser-cookie3"], check=True, capture_output=True)
        import browser_cookie3
        BROWSER_COOKIE_AVAILABLE = True
        print(" Successfully installed browser_cookie3")
    except Exception as e:
        print(f"❌ Failed to install browser_cookie3: {e}")
        BROWSER_COOKIE_AVAILABLE = False

# Load environment variables
load_dotenv()

# Track progress
PROGRESS_FILE = "transcript_progress.json"
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
MANUAL_PROCESSING_FILE = "manual_processing_needed.json"

# Try to find ffmpeg in common locations
def find_ffmpeg():
    # Try using which command
    try:
        result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    
    # Try common locations
    common_paths = [
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/opt/homebrew/bin/ffmpeg',
        '/opt/local/bin/ffmpeg',
        '/Applications/ffmpeg',
        # Add more potential paths here
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    # If we can't find it, return the command name and hope it's in PATH
    return 'ffmpeg'

# Get the ffmpeg path
FFMPEG_PATH = find_ffmpeg()
print(f" Using ffmpeg at: {FFMPEG_PATH}")

def load_progress():
    # First try to load missing_transcripts.json
    if os.path.exists('missing_transcripts.json'):
        with open('missing_transcripts.json', 'r') as f:
            data = json.load(f)
            # Filter out videos that already have transcripts
            missing_videos = []
            for video in data:
                video_id = video.get('video_id')
                if video_id:
                    # Check for transcript files with video ID
                    transcript_path = os.path.join('transcripts', f"{video_id}.txt")
                    if not os.path.exists(transcript_path):
                        missing_videos.append(video)
            
            # Convert the filtered video data into list of URLs
            return {
                'failed': [video['url'] for video in missing_videos if video.get('url')],
                'processed': [],
                'whisper_processed': []
            }
    # Fallback to existing progress file
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'processed': [], 'failed': [], 'whisper_processed': []}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

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
    
    print(f" Saved {len(merged_list)} videos for manual processing to {MANUAL_PROCESSING_FILE}")

def clean_dummy_files(audio_dir="audio_files"):
    """Remove existing dummy/small files to try fresh downloads"""
    print("🧹 Cleaning up existing dummy or small audio files...")
    
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir, exist_ok=True)
        return 0
    
    count = 0
    for file in os.listdir(audio_dir):
        if file.endswith('.mp3'):
            file_path = os.path.join(audio_dir, file)
            file_size = os.path.getsize(file_path)
            
            # Check if it's a dummy file (< 10KB)
            if file_size < 10000:
                print(f"🗑️ Removing small file: {file} ({file_size} bytes)")
                os.remove(file_path)
                
                # Also remove corresponding note file if it exists
                note_path = file_path.replace('.mp3', '.note.txt')
                if os.path.exists(note_path):
                    os.remove(note_path)
                count += 1
    
    print(f" Removed {count} dummy/small audio files")
    return count

def extract_browser_cookies():
    """Extract real cookies from browser"""
    if not BROWSER_COOKIE_AVAILABLE:
        return None
        
    cookie_file = "browser_cookies.txt"
    try:
        print("🍪 Attempting to extract YouTube cookies from browsers...")
        
        # Try Chrome first
        try:
            cookies = browser_cookie3.chrome(domain_name='.youtube.com')
            cookie_jar = yt_dlp.utils.cookiejar_from_dict({c.name: c.value for c in cookies})
            yt_dlp.utils.cookiejar_to_netscape(cookie_jar, cookie_file)
            print(" Successfully extracted cookies from Chrome")
            return cookie_file
        except Exception as e:
            print(f"⚠️ Could not extract Chrome cookies: {e}")
        
        # Try Firefox next
        try:
            cookies = browser_cookie3.firefox(domain_name='.youtube.com')
            cookie_jar = yt_dlp.utils.cookiejar_from_dict({c.name: c.value for c in cookies})
            yt_dlp.utils.cookiejar_to_netscape(cookie_jar, cookie_file)
            print(" Successfully extracted cookies from Firefox")
            return cookie_file
        except Exception as e:
            print(f"⚠️ Could not extract Firefox cookies: {e}")
            
        # Try Safari next (macOS only)
        try:
            cookies = browser_cookie3.safari(domain_name='.youtube.com')
            cookie_jar = yt_dlp.utils.cookiejar_from_dict({c.name: c.value for c in cookies})
            yt_dlp.utils.cookiejar_to_netscape(cookie_jar, cookie_file)
            print(" Successfully extracted cookies from Safari")
            return cookie_file
        except Exception as e:
            print(f"⚠️ Could not extract Safari cookies: {e}")
            
    except Exception as e:
        print(f"❌ Failed to extract any browser cookies: {e}")
    
    return None

def create_fake_cookies():
    """Create fake cookies as a fallback"""
    fake_cookies = "fake_cookies.txt"
    with open(fake_cookies, "w") as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write(".youtube.com\tTRUE\t/\tFALSE\t2147483647\tCONSENT\tYES+cb.20220301-11-p0.en+FX+123\n")
        f.write(".youtube.com\tTRUE\t/\tFALSE\t2147483647\tLOGIN_INFO\tdummy_value\n")
        f.write(".youtube.com\tTRUE\t/\tFALSE\t2147483647\tPREF\tf1=50000000&f6=8\n")
        f.write(".youtube.com\tTRUE\t/\tFALSE\t2147483647\tYSC\tdummy_value\n")
        f.write(".youtube.com\tTRUE\t/\tFALSE\t2147483647\tWIDE\t1\n")
    return fake_cookies

def download_audio(url, output_path):
    """Download audio from YouTube video with multiple fallback methods"""
    print(f"⬇️ Downloading audio for {url}...")
    
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Extract video_id
    video_id = extract_video_id(url)
    
    # Method 1: Direct FFmpeg streaming method (most reliable)
    try:
        print("Trying direct FFmpeg streaming method...")
        
        # This method uses FFmpeg to directly stream from YouTube
        cmd = [
            FFMPEG_PATH,
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
            print(f" Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
            return True
    except Exception as e:
        print(f"Method 1 (direct FFmpeg) failed: {str(e)}")
    
    # Method 2: Try with mobile API + real cookies
    try:
        print("Trying yt-dlp with mobile API and browser cookies...")
        
        # Get real cookies from browser or create fake ones
        cookie_file = extract_browser_cookies() or create_fake_cookies()
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
            'ffmpeg_location': os.path.dirname(FFMPEG_PATH),
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'cookiefile': cookie_file,
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
                print(f" Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
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
                print(f" Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
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
            "--cookies", cookie_file,
            "--force-ipv4",
            "--geo-bypass",
            "--user-agent", "com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip",
            url
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f" Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
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
                FFMPEG_PATH,
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
                print(f" Successfully downloaded to {output_path} (size: {os.path.getsize(output_path)} bytes)")
                return True
    except Exception as e:
        print(f"Method 5 (pytube) failed: {str(e)}")
    
    # Last resort: Look for any related files that might have been created
    print("Looking for any files matching the video ID...")
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
                            FFMPEG_PATH,
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
                    print(f" Successfully copied/converted to {output_path} (size: {os.path.getsize(output_path)} bytes)")
                    return True
    
    # Record this URL for manual processing
    print("👤 Flagging video for manual processing...")
    save_manual_processing_list([url])
    
    # If all methods fail, create a dummy audio file (add a note to the transcript about this)
    print("⚠️ All methods failed - creating a dummy audio file")
    try:
        # Create a 5-second silent MP3
        cmd = [
            FFMPEG_PATH,
            '-f', 'lavfi',
            '-i', 'anullsrc=r=44100:cl=mono',
            '-t', '5',
            '-codec:a', 'libmp3lame',
            '-qscale:a', '2',
            output_path,
            '-y'
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"⚠️ Created dummy audio at {output_path}")
            # Create a note file with the same name to indicate this is a dummy
            note_path = output_path.replace('.mp3', '.note.txt')
            with open(note_path, 'w') as f:
                f.write(f"Failed to download audio for: {url}\nCreated dummy audio file on {datetime.now()}\n")
                f.write("This video has been flagged for manual processing.\n")
            return True
    except Exception as e:
        print(f"Error creating dummy file: {e}")

    raise Exception("All download methods failed")

def transcribe_with_whisper(audio_path, output_path):
    # Check if this is a dummy file
    note_path = audio_path.replace('.mp3', '.note.txt')
    if os.path.exists(note_path):
        print("⚠️ This is a dummy audio file from a failed download")
        # Create a note in the transcript file
        with open(output_path, 'w') as f:
            f.write("⚠️ DOWNLOAD FAILED: Could not access the original audio for this video\n\n")
            f.write("This transcript is a placeholder because YouTube blocked all download attempts.\n")
            f.write("You may need to manually transcribe this video by watching it on YouTube.\n\n")
            
            # Add the original note content
            with open(note_path, 'r') as note_file:
                f.write(note_file.read())
        return
    
    # Check if the audio file is too small (likely a dummy or corrupt file)
    file_size = os.path.getsize(audio_path)
    if file_size < 10000:  # Less than 10KB
        print(f"⚠️ Audio file is suspiciously small: {file_size} bytes")
        # Create a note in the transcript file
        with open(output_path, 'w') as f:
            f.write(f"⚠️ WARNING: Audio file is very small ({file_size} bytes)\n\n")
            f.write("This transcript may be empty or incomplete because the audio file could not be properly downloaded.\n")
            f.write("YouTube may have blocked download attempts for this video.\n")
    
    # Load the Whisper model (using centralized config)
    from pipeline_config import WHISPER_MODEL
    print(f"🎯 Loading Whisper model '{WHISPER_MODEL}' (this might take a minute on first run)...")
    model = whisper.load_model(WHISPER_MODEL)
    
    # Transcribe the audio
    print("🎯 Transcribing audio...")
    
    try:
        # Make sure ffmpeg environment variable is set for whisper
        os.environ["PATH"] = os.path.dirname(FFMPEG_PATH) + os.pathsep + os.environ.get("PATH", "")
        
        # Try transcribing without progress_callback
        print("🎯 Starting transcription (this may take a while)...")
        result = model.transcribe(audio_path)
        print("🎯 Transcription complete!")
        
        # Save the transcript with timestamps
        with open(output_path, 'a' if os.path.exists(output_path) else 'w') as f:
            # If we already wrote a warning header, don't overwrite it
            if not os.path.exists(output_path):
                f.write(f"Transcription completed on {datetime.now()}\n\n")
                
            for segment in result["segments"]:
                start_time = segment["start"]
                text = segment["text"].strip()
                if text:  # Only write non-empty segments
                    f.write(f"{start_time:.2f}s: {text}\n")
    except Exception as e:
        print(f"❌ Error in Whisper transcription: {e}")
        # Fallback to direct ffmpeg command for audio processing
        try:
            print("🔄 Attempting to process audio with ffmpeg directly...")
            wav_path = audio_path.replace('.mp3', '.wav')
            cmd = [FFMPEG_PATH, '-i', audio_path, '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', wav_path, '-y']
            subprocess.run(cmd, check=True)
            
            # Try transcribing the wav file without progress_callback
            print("🎯 Starting transcription with processed audio (this may take a while)...")
            result = model.transcribe(wav_path)
            print("🎯 Transcription complete!")
            
            # Save the transcript with timestamps
            with open(output_path, 'a' if os.path.exists(output_path) else 'w') as f:
                # If we already wrote a warning header, don't overwrite it
                if not os.path.exists(output_path):
                    f.write(f"Transcription completed on {datetime.now()}\n\n")
                    
                for segment in result["segments"]:
                    start_time = segment["start"]
                    text = segment["text"].strip()
                    if text:  # Only write non-empty segments
                        f.write(f"{start_time:.2f}s: {text}\n")
                    
            # Clean up temporary wav file
            if os.path.exists(wav_path):
                os.remove(wav_path)
        except Exception as e2:
            print(f"❌ Both transcription methods failed: {e2}")
            
            # Make sure we write something to the output file
            with open(output_path, 'w') as f:
                f.write("⚠️ TRANSCRIPTION FAILED\n\n")
                f.write(f"Error details: {str(e)}\n")
                f.write(f"Secondary error: {str(e2)}\n")
                f.write(f"Audio file size: {file_size} bytes\n")
                f.write(f"Attempted transcription on: {datetime.now()}\n")
            
            raise

def get_video_title(url):
    try:
        youtube = pytube.YouTube(url)
        title = youtube.title
        if title:
            return title.replace(' ', '_')
        return None
    except Exception as e:
        print(f"❌ Error getting title: {e}")
        # Extract video ID as fallback title
        return extract_video_id(url)

def extract_video_id(url):
    # Extract video ID from URL
    if 'youtube.com' in url:
        query = urlparse(url).query
        params = parse_qs(query)
        return params.get('v', ['unknown'])[0]
    elif 'youtu.be' in url:
        return url.split('/')[-1]
    return 'unknown'

def main():
    # First, clean up any existing dummy files
    clean_dummy_files()
    
    # Check if we're using a VPN
    try:
        import requests
        print("🌐 Checking your IP address...")
        ip_response = requests.get("https://api.ipify.org?format=json", timeout=5).json()
        print(f"🌍 Your current IP address: {ip_response.get('ip', 'unknown')}")
        print("⚠️ If you're encountering blocks, consider using a VPN to change your IP address")
    except Exception as e:
        print(f"⚠️ Could not check IP address: {e}")
    
    # Load progress and filter out videos that already have transcripts
    progress = load_progress()
    failed_videos = progress['failed']
    
    if not failed_videos:
        print(" No failed videos to process!")
        return
    
    print(f"📚 Found {len(failed_videos)} failed videos to process with Whisper")
    
    output_dir = "transcripts"
    os.makedirs(output_dir, exist_ok=True)
    
    # Also create a directory for downloaded audio files
    audio_dir = "audio_files"
    os.makedirs(audio_dir, exist_ok=True)
    
    # Track successful and still failed videos
    successful = []
    still_failed = []
    
    # Process each failed video
    for i, url in enumerate(failed_videos, 1):
        print(f"\n🎥 Processing video {i}/{len(failed_videos)}: {url}")
        start_time = time.time()
        
        # Extract video ID from URL
        video_id = extract_video_id(url)
        
        # Check if transcript already exists
        transcript_path = os.path.join(output_dir, f"{video_id}.txt")
        if os.path.exists(transcript_path):
            print(f" Transcript already exists for video {video_id}, skipping...")
            successful.append(url)
            continue
        
        # Add retry logic
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Get video title or ID
                try:
                    title = get_video_title(url)
                except:
                    # Extract video ID as fallback
                    video_id = extract_video_id(url)
                    title = f"video_{video_id}"
                    
                if not title:
                    video_id = extract_video_id(url)
                    title = f"{video_id}"
                    
                # Use video ID in filenames for consistency
                transcript_filename = os.path.join(output_dir, f"{video_id}.txt")
                
                # Use a permanent audio file instead of a temporary one
                audio_filename = os.path.join(audio_dir, f"{video_id}.mp3")
                
                # Download audio to a permanent location
                if not os.path.exists(audio_filename):
                    download_audio(url, audio_filename)
                else:
                    print(f" Audio file already exists: {audio_filename}")
                
                # Check for possible double extension
                double_ext_path = audio_filename + '.mp3'
                if os.path.exists(double_ext_path) and not os.path.exists(audio_filename):
                    print(f"🔄 Fixing double extension: {double_ext_path} -> {audio_filename}")
                    shutil.move(double_ext_path, audio_filename)
                    
                # Verify the audio file exists before transcribing
                if not os.path.exists(audio_filename):
                    print(f"❌ Audio file not found after download: {audio_filename}")
                    raise Exception("Audio file not found after download")
                    
                # Print file info
                print(f" Audio file info: {os.path.getsize(audio_filename)} bytes")
                
                # Transcribe with Whisper
                transcribe_with_whisper(audio_filename, transcript_filename)
                
                processing_time = time.time() - start_time
                print(f" Transcript saved for {video_id} (took {processing_time:.2f} seconds)")
                
                # Update progress
                successful.append(url)
                break  # Success, exit retry loop
                
            except Exception as e:
                retry_count += 1
                print(f"❌ Attempt {retry_count} failed: {e}")
                if retry_count == max_retries:
                    print(f"❌ All attempts failed for {url}")
                    still_failed.append(url)
                    # Record for manual processing
                    save_manual_processing_list([url])
                else:
                    print(f"Retrying in 5 seconds...")
                    time.sleep(5)
    
    # Update and save progress
    if successful:
        for url in successful:
            if url in progress['failed']:
                progress['failed'].remove(url)
            progress['whisper_processed'].append(url)
    
    save_progress(progress)
    
    # Display summary of manual processing needs
    if os.path.exists(MANUAL_PROCESSING_FILE):
        with open(MANUAL_PROCESSING_FILE, 'r') as f:
            manual_videos = json.load(f)
            print(f"\n👤 Total videos needing manual processing: {len(manual_videos)}")
            print(f"These are saved in {MANUAL_PROCESSING_FILE} for later reference")
    
    print("\n📊 Processing Summary:")
    print(f" Successfully processed with Whisper: {len(successful)} videos")
    print(f"❌ Still failed: {len(still_failed)} videos")
    
    if still_failed:
        print("\n❌ Failed videos:")
        for url in still_failed:
            print(f"- {url}")
            
    print("\n Next steps suggestions:")
    print("1. If many videos failed, try using a VPN to change your IP address")
    print("2. For videos requiring manual processing, consider:")
    print("   - Using a browser extension to download the audio")
    print("   - Using a different device or network to access the videos")
    print("   - Using a YouTube Premium account")
    print("3. Run this script again to process any remaining videos")

if __name__ == "__main__":
    main() 