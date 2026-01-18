#!/usr/bin/env python3
"""
Retry failed videos and use Whisper for those without YouTube captions.
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline_config import TRANSCRIPT_DIR, AUDIO_DIR, WHISPER_MODEL, ensure_directories

def load_progress():
    """Load transcript progress."""
    if os.path.exists('transcript_progress.json'):
        with open('transcript_progress.json', 'r') as f:
            return json.load(f)
    return {'processed': [], 'failed': [], 'whisper_processed': []}

def save_progress(progress):
    """Save transcript progress."""
    with open('transcript_progress.json', 'w') as f:
        json.dump(progress, f, indent=2)

def get_video_id(url):
    """Extract video ID from URL."""
    if 'v=' in url:
        return url.split('v=')[-1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('/')[-1].split('?')[0]
    return url

def retry_youtube_transcripts(urls_to_retry, progress, delay=2):
    """Retry getting YouTube transcripts for failed videos."""
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    
    successful = []
    still_failed = []
    
    print(f"\n🔄 Retrying {len(urls_to_retry)} videos for YouTube transcripts...")
    
    for i, url in enumerate(urls_to_retry, 1):
        video_id = get_video_id(url)
        transcript_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
        
        # Skip if transcript already exists
        if os.path.exists(transcript_path):
            print(f"  ⏭️  [{i}/{len(urls_to_retry)}] {video_id} - already has transcript")
            successful.append(url)
            continue
        
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Save transcript
            with open(transcript_path, 'w', encoding='utf-8') as f:
                for entry in transcript:
                    f.write(f"{entry['start']:.2f}s: {entry['text']}\n")
            
            print(f"  ✅ [{i}/{len(urls_to_retry)}] {video_id} - YouTube transcript found!")
            successful.append(url)
            
            # Update progress
            if url in progress.get('failed', []):
                progress['failed'].remove(url)
            if url not in progress.get('processed', []):
                progress['processed'].append(url)
            save_progress(progress)
            
        except (TranscriptsDisabled, NoTranscriptFound):
            print(f"  ❌ [{i}/{len(urls_to_retry)}] {video_id} - no YouTube captions")
            still_failed.append(url)
            
        except Exception as e:
            if '429' in str(e) or 'Too Many Requests' in str(e):
                print(f"  ⚠️  Rate limited! Waiting 60 seconds...")
                time.sleep(60)
                still_failed.append(url)
            else:
                print(f"  ❌ [{i}/{len(urls_to_retry)}] {video_id} - error: {str(e)[:50]}")
                still_failed.append(url)
        
        # Small delay between requests
        if i < len(urls_to_retry):
            time.sleep(delay)
    
    return successful, still_failed

def download_audio(video_id, url):
    """Download audio for a video using yt-dlp."""
    import yt_dlp
    
    audio_path = os.path.join(AUDIO_DIR, f"{video_id}.mp3")
    
    # Skip if audio already exists and is valid
    if os.path.exists(audio_path) and os.path.getsize(audio_path) > 10000:
        return audio_path
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'outtmpl': os.path.join(AUDIO_DIR, f"{video_id}.%(ext)s"),
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
            return audio_path
    except Exception as e:
        print(f"    ⚠️  Audio download failed: {str(e)[:50]}")
    
    return None

def transcribe_with_whisper(video_id, audio_path):
    """Transcribe audio using Whisper."""
    import whisper
    
    transcript_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
    
    try:
        model = whisper.load_model(WHISPER_MODEL)
        result = model.transcribe(audio_path)
        
        if not result["text"].strip():
            return False
        
        with open(transcript_path, 'w', encoding='utf-8') as f:
            for segment in result.get("segments", []):
                start = segment.get("start", 0)
                text = segment.get("text", "").strip()
                if text:
                    f.write(f"{start:.2f}s: {text}\n")
        
        return True
    except Exception as e:
        print(f"    ⚠️  Whisper failed: {str(e)[:50]}")
        return False

def process_with_whisper(urls_to_process, progress, max_videos=None):
    """Process videos with Whisper transcription."""
    successful = []
    failed = []
    
    if max_videos:
        urls_to_process = urls_to_process[:max_videos]
    
    print(f"\n🎤 Processing {len(urls_to_process)} videos with Whisper...")
    print(f"   Model: {WHISPER_MODEL}")
    
    for i, url in enumerate(urls_to_process, 1):
        video_id = get_video_id(url)
        transcript_path = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
        
        # Skip if transcript already exists
        if os.path.exists(transcript_path):
            print(f"  ⏭️  [{i}/{len(urls_to_process)}] {video_id} - already has transcript")
            successful.append(url)
            continue
        
        print(f"  🎬 [{i}/{len(urls_to_process)}] {video_id}")
        
        # Download audio
        print(f"    📥 Downloading audio...")
        audio_path = download_audio(video_id, url)
        
        if not audio_path:
            print(f"    ❌ Could not download audio")
            failed.append(url)
            continue
        
        # Transcribe
        print(f"    🎤 Transcribing with Whisper...")
        if transcribe_with_whisper(video_id, audio_path):
            print(f"    ✅ Transcript saved!")
            successful.append(url)
            
            # Update progress
            if url in progress.get('failed', []):
                progress['failed'].remove(url)
            if url not in progress.get('whisper_processed', []):
                progress['whisper_processed'].append(url)
            save_progress(progress)
        else:
            print(f"    ❌ Transcription failed")
            failed.append(url)
    
    return successful, failed

def main():
    parser = argparse.ArgumentParser(description='Retry failed videos and use Whisper')
    parser.add_argument('--retry-only', action='store_true', help='Only retry YouTube transcripts')
    parser.add_argument('--whisper-only', action='store_true', help='Only run Whisper on failed')
    parser.add_argument('--max-whisper', type=int, default=None, help='Max videos to process with Whisper')
    parser.add_argument('--delay', type=float, default=2, help='Delay between YouTube API requests')
    args = parser.parse_args()
    
    ensure_directories()
    progress = load_progress()
    
    # Get videos that need transcripts
    failed_urls = progress.get('failed', [])
    videos_needing_transcripts = []
    
    for url in failed_urls:
        video_id = get_video_id(url)
        if not os.path.exists(os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")):
            videos_needing_transcripts.append(url)
    
    print(f"📊 Status:")
    print(f"   Total failed: {len(failed_urls)}")
    print(f"   Missing transcripts: {len(videos_needing_transcripts)}")
    
    if not videos_needing_transcripts:
        print("✅ All videos have transcripts!")
        return
    
    # Step 1: Retry YouTube transcripts
    if not args.whisper_only:
        successful_yt, still_failed = retry_youtube_transcripts(
            videos_needing_transcripts, progress, delay=args.delay
        )
        print(f"\n📊 YouTube Retry Results:")
        print(f"   ✅ Successful: {len(successful_yt)}")
        print(f"   ❌ Still need Whisper: {len(still_failed)}")
    else:
        still_failed = videos_needing_transcripts
    
    # Step 2: Process remaining with Whisper
    if not args.retry_only and still_failed:
        successful_whisper, failed_whisper = process_with_whisper(
            still_failed, progress, max_videos=args.max_whisper
        )
        print(f"\n📊 Whisper Results:")
        print(f"   ✅ Successful: {len(successful_whisper)}")
        print(f"   ❌ Failed: {len(failed_whisper)}")
    
    # Final summary
    progress = load_progress()  # Reload
    print(f"\n🎉 Final Status:")
    print(f"   YouTube transcripts: {len(progress.get('processed', []))}")
    print(f"   Whisper transcripts: {len(progress.get('whisper_processed', []))}")
    print(f"   Remaining failed: {len(progress.get('failed', []))}")

if __name__ == "__main__":
    main()
