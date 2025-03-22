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

# Track progress
PROGRESS_FILE = "transcript_progress.json"

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
print(f"🔍 Using ffmpeg at: {FFMPEG_PATH}")

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'processed': [], 'failed': [], 'whisper_processed': []}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def download_audio(url, output_path):
    print(f"⬇️ Downloading audio...")
    
    # First try: Use yt-dlp with browser cookies and explicit ffmpeg path
    try:
        print("📥 Trying yt-dlp with browser cookies...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'cookiesfrombrowser': ('chrome',),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
            'verbose': True,
            'progress_hooks': [lambda d: print(f"📥 Download progress: {d.get('_percent_str', '0%')}") if d['status'] == 'downloading' else None],
            'no_check_certificates': True,
            'ignoreerrors': True,
            'no_warnings': False,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'ffmpeg_location': os.path.dirname(FFMPEG_PATH),
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("✅ Successfully downloaded with yt-dlp")
            
            # Check for the file with potential double extension
            double_ext_path = output_path + '.mp3'
            if os.path.exists(double_ext_path):
                print(f"🔄 Fixing double extension: {double_ext_path} -> {output_path}")
                shutil.move(double_ext_path, output_path)
            
            return
    except Exception as e:
        print(f"❌ Error downloading with yt-dlp: {e}")

    # Second try: Use pytube with explicit ffmpeg path
    try:
        print("📥 Trying pytube...")
        youtube = pytube.YouTube(url)
        audio_stream = youtube.streams.filter(only_audio=True).first()
        
        # Get temporary file path without extension
        base_path = output_path.replace('.mp3', '')
        temp_path = f"{base_path}.{audio_stream.subtype}"
        
        # Download the audio
        print(f"📥 Downloading {youtube.title}...")
        audio_stream.download(filename=temp_path)
        
        # Convert to mp3 using ffmpeg with full path
        print(f"🔄 Converting to mp3 using {FFMPEG_PATH}...")
        cmd = [FFMPEG_PATH, '-i', temp_path, '-codec:a', 'libmp3lame', '-qscale:a', '2', output_path, '-y']
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Remove the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        print(f"✅ Successfully downloaded with pytube")
        return
    except Exception as e:
        print(f"❌ Error downloading with pytube: {e}")
    
    # Last resort: Try youtube-dl command line tool with explicit ffmpeg path
    try:
        print("📥 Trying youtube-dl...")
        cmd = ['youtube-dl', '-v', '-x', '--audio-format', 'mp3', 
               '--ffmpeg-location', os.path.dirname(FFMPEG_PATH),
               '--cookies', os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Cookies'), 
               '-o', output_path, url]
        subprocess.run(cmd, check=True)
        print("✅ Successfully downloaded with youtube-dl")
        return
    except Exception as e:
        print(f"❌ All download methods failed: {e}")
        raise

def transcribe_with_whisper(audio_path, output_path):
    # Load the Whisper model (using 'base' model for faster processing)
    print("🎯 Loading Whisper model (this might take a minute on first run)...")
    model = whisper.load_model("base")
    
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
        with open(output_path, 'w') as f:
            for segment in result["segments"]:
                start_time = segment["start"]
                text = segment["text"]
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
            with open(output_path, 'w') as f:
                for segment in result["segments"]:
                    start_time = segment["start"]
                    text = segment["text"]
                    f.write(f"{start_time:.2f}s: {text}\n")
                    
            # Clean up temporary wav file
            if os.path.exists(wav_path):
                os.remove(wav_path)
        except Exception as e2:
            print(f"❌ Both transcription methods failed: {e2}")
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
    # Load progress
    progress = load_progress()
    failed_videos = progress['failed']
    
    if not failed_videos:
        print("✅ No failed videos to process!")
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
            transcript_filename = os.path.join(output_dir, f"{title}.txt")
            
            # Use a permanent audio file instead of a temporary one
            audio_filename = os.path.join(audio_dir, f"{title}.mp3")
            
            # Download audio to a permanent location
            if not os.path.exists(audio_filename):
                download_audio(url, audio_filename)
            else:
                print(f"✅ Audio file already exists: {audio_filename}")
            
            # Check for possible double extension
            double_ext_path = audio_filename + '.mp3'
            if os.path.exists(double_ext_path) and not os.path.exists(audio_filename):
                print(f"🔄 Fixing double extension: {double_ext_path} -> {audio_filename}")
                shutil.move(double_ext_path, audio_filename)
                
            # Verify the audio file exists before transcribing
            if not os.path.exists(audio_filename):
                print(f"❌ Audio file not found after download: {audio_filename}")
                still_failed.append(url)
                continue
                
            # Print file info
            print(f"🔍 Audio file info: {os.path.getsize(audio_filename)} bytes")
            
            # Transcribe with Whisper
            transcribe_with_whisper(audio_filename, transcript_filename)
            
            processing_time = time.time() - start_time
            print(f"✅ Transcript saved for {title} (took {processing_time:.2f} seconds)")
            
            # Update progress
            successful.append(url)
            
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")
            # Keep the video in failed list if there's an error
            still_failed.append(url)
    
    # Update and save progress
    if successful:
        for url in successful:
            if url in progress['failed']:
                progress['failed'].remove(url)
            progress['whisper_processed'].append(url)
    
    save_progress(progress)
    
    print("\n📊 Processing Summary:")
    print(f"✅ Successfully processed with Whisper: {len(successful)} videos")
    print(f"❌ Still failed: {len(still_failed)} videos")

if __name__ == "__main__":
    main() 