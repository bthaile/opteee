from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs
import os
import json
import time
from datetime import datetime
import whisper
import yt_dlp
import tempfile
import subprocess

# Track processed videos
PROGRESS_FILE = "transcript_progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'processed': [], 'failed': [], 'whisper_processed': []}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def download_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_with_whisper(audio_path, output_path):
    # Load the Whisper model (using centralized config)
    from pipeline_config import WHISPER_MODEL
    model = whisper.load_model(WHISPER_MODEL)
    
    # Transcribe the audio
    result = model.transcribe(audio_path)
    
    # Save the transcript with timestamps
    with open(output_path, 'w') as f:
        for segment in result["segments"]:
            start_time = segment["start"]
            text = segment["text"].strip()
            if text:  # Only write non-empty segments
                f.write(f"{start_time:.2f}s: {text}\n")

# Read URLs and titles from the JSON file (not CSV)
video_data = []
try:
    with open('outlier_trading_videos.json', 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        for video in data:
            if video.get('url') and video.get('title'):
                video_data.append({
                    'url': video['url'],
                    'title': video['title'].replace(' ', '_').replace('/', '_')  # Clean title for filename
                })
    print(f"📚 Found {len(video_data)} videos to process")
except FileNotFoundError:
    print("❌ Error: outlier_trading_videos.json not found. Please run outlier_scraper.py first.")
    exit(1)

output_dir = "transcripts"
os.makedirs(output_dir, exist_ok=True)

def get_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    elif query.hostname in ('www.youtube.com', 'youtube.com'):
        return parse_qs(query.query).get('v', [None])[0]
    return None

# Load progress
progress = load_progress()
print(f" Found {len(progress['processed'])} previously processed videos")
print(f"🎯 Found {len(progress['whisper_processed'])} previously whisper-processed videos")
print(f"❌ Found {len(progress['failed'])} previously failed videos")

# Filter out already processed videos
video_data = [v for v in video_data if v['url'] not in progress['processed'] + progress['whisper_processed']]

for video in video_data:
    video_id = get_video_id(video['url'])
    if not video_id:
        print(f"⚠️ Could not extract ID from {video['url']}")
        continue

    start_time = time.time()
    filename = os.path.join(output_dir, f"{video['title']}.txt")

    try:
        # First try to get YouTube transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        with open(filename, 'w') as f:
            for entry in transcript:
                text = entry['text'].strip()
                if text:  # Only write non-empty segments
                    f.write(f"{entry['start']:.2f}s: {text}\n")

        processing_time = time.time() - start_time
        print(f" YouTube transcript saved for {video['title']} (took {processing_time:.2f} seconds)")
        progress['processed'].append(video['url'])
        save_progress(progress)

    except (TranscriptsDisabled, NoTranscriptFound):
        print(f" No YouTube transcript found for {video['url']}, trying Whisper...")
        try:
            # Create a temporary directory for audio files
            with tempfile.TemporaryDirectory() as temp_dir:
                audio_path = os.path.join(temp_dir, "audio.mp3")
                
                # Download audio
                print(f"⬇️ Downloading audio for {video['title']}...")
                download_audio(video['url'], audio_path)
                
                # Transcribe with Whisper
                print(f"🎯 Transcribing {video['title']} with Whisper...")
                transcribe_with_whisper(audio_path, filename)
                
                processing_time = time.time() - start_time
                print(f" Whisper transcript saved for {video['title']} (took {processing_time:.2f} seconds)")
                progress['whisper_processed'].append(video['url'])
                save_progress(progress)

        except Exception as e:
            print(f"❌ Error processing {video['url']} with Whisper: {e}")
            progress['failed'].append(video['url'])
            save_progress(progress)

    except Exception as e:
        print(f"❌ Error processing {video['url']}: {e}")
        progress['failed'].append(video['url'])
        save_progress(progress)

print("\n📊 Processing Summary:")
print(f" Successfully processed with YouTube transcript: {len(progress['processed'])} videos")
print(f" Successfully processed with Whisper: {len(progress['whisper_processed'])} videos")
print(f"❌ Failed to process: {len(progress['failed'])} videos")
print(f"⏱️ Total processing time: {time.time() - start_time:.2f} seconds")