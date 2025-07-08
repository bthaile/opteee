#!/usr/bin/env python3
"""
Enhanced Whisper-Focused Transcript Downloader with Browser-Based Cookie Extraction

This script focuses on Whisper transcription with a working browser-based approach
that extracts cookies from real browser sessions to avoid YouTube's anti-bot detection.
"""

import json
import os
import time
import sys
import argparse
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import whisper
import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configuration
PROGRESS_FILE = "transcript_progress.json"
AUDIO_DIR = "audio_files"
TRANSCRIPT_DIR = "transcripts"
BATCH_SIZE = 5  # Reduced for more conservative approach
DELAY_BETWEEN_VIDEOS = 1  # seconds
DELAY_BETWEEN_BATCHES = 1  # seconds

def setup_browser():
    """Set up Chrome with realistic settings to avoid detection."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Enhanced anti-detection measures
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # Hide webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"❌ Could not start Chrome: {e}")
        print("💡 Install ChromeDriver: brew install chromedriver")
        return None

def extract_cookies_from_browser(video_url: str) -> Optional[str]:
    """Extract cookies from a browser session accessing the video."""
    driver = setup_browser()
    if not driver:
        return None
    
    try:
        # Navigate to YouTube main page first
        driver.get("https://www.youtube.com")
        time.sleep(2)
        
        # Then navigate to the specific video
        driver.get(video_url)
        time.sleep(3)
        
        # Extract cookies
        cookies = driver.get_cookies()
        
        # Create a temporary cookie file
        cookie_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        
        # Write cookies in Netscape format for yt-dlp
        cookie_file.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            domain = cookie.get('domain', '.youtube.com')
            if not domain.startswith('.'):
                domain = '.' + domain
            
            line = f"{domain}\tTRUE\t/\t{str(cookie.get('secure', False)).upper()}\t0\t{cookie['name']}\t{cookie['value']}\n"
            cookie_file.write(line)
        
        cookie_file.close()
        return cookie_file.name
        
    except Exception as e:
        print(f"❌ Cookie extraction failed: {e}")
        return None
    finally:
        driver.quit()

def load_progress() -> Dict:
    """Load processing progress from file."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return {
        "processed": [],
        "failed": [],
        "whisper_processed": [],
        "audio_downloaded": [],  # Track successful audio downloads
        "methods": {},
        "batch_info": {},
        "statistics": {}
    }

def save_progress(progress: Dict):
    """Save processing progress to file."""
    try:
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f, indent=2)
    except Exception as e:
        print(f"⚠️ Could not save progress: {e}")

def load_videos() -> List[Dict]:
    """Load video metadata from JSON files."""
    videos = []
    
    # Try enhanced metadata first
    for filename in ['outlier_trading_videos_metadata.json', 'outlier_trading_videos.json']:
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        videos = data
                        print(f"✅ Loaded {len(videos)} videos from {filename}")
                        break
            except Exception as e:
                print(f"⚠️ Could not load {filename}: {e}")
    
    if not videos:
        print("❌ No video metadata found. Run outlier_scraper.py first.")
        return []
    
    return videos

def download_audio_with_cookies(video_url: str, video_id: str, progress: Dict) -> bool:
    """Download audio using browser-extracted cookies."""
    print(f"  🍪 Extracting cookies from browser session...")
    
    # Extract cookies first
    cookie_file = extract_cookies_from_browser(video_url)
    if not cookie_file:
        print("  ❌ Could not extract cookies")
        return False
    
    # Ensure output directory exists
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    # Output template with proper naming convention
    output_template = os.path.join(AUDIO_DIR, f"{video_id}.%(ext)s")
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'outtmpl': output_template,
            'cookiefile': cookie_file,
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'sleep_interval': 2,
            'max_sleep_interval': 5,
            'extract_flat': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'overwrites': True,  # Allow overwriting existing files
            'continue_dl': False,  # Don't try to resume partial downloads
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("  🔄 Downloading audio...")
            ydl.download([video_url])
            
            # Check if file was created with correct naming
            expected_file = os.path.join(AUDIO_DIR, f"{video_id}.mp3")
            if os.path.exists(expected_file):
                size_mb = os.path.getsize(expected_file) / (1024 * 1024)
                print(f"  ✅ Audio downloaded: {size_mb:.1f} MB")
                
                # Update progress tracking - audio successfully downloaded
                if video_url not in progress.get('audio_downloaded', []):
                    progress['audio_downloaded'].append(video_url)
                
                # Save progress immediately after successful download
                save_progress(progress)
                print(f"  📝 Progress saved: audio downloaded")
                
                return True
            else:
                # Check for other possible extensions
                for ext in ['mp3', 'webm', 'm4a', 'ogg']:
                    alt_file = os.path.join(AUDIO_DIR, f"{video_id}.{ext}")
                    if os.path.exists(alt_file):
                        # Rename to .mp3 for consistency
                        os.rename(alt_file, expected_file)
                        size_mb = os.path.getsize(expected_file) / (1024 * 1024)
                        print(f"  ✅ Audio downloaded: {size_mb:.1f} MB (renamed from {ext})")
                        
                        # Update progress tracking - audio successfully downloaded
                        if video_url not in progress.get('audio_downloaded', []):
                            progress['audio_downloaded'].append(video_url)
                        
                        # Save progress immediately after successful download
                        save_progress(progress)
                        print(f"  📝 Progress saved: audio downloaded")
                        
                        return True
                
                print(f"  ❌ No audio file created")
                return False
                
    except Exception as e:
        print(f"  ❌ Download failed: {e}")
        return False
    finally:
        # Clean up cookie file
        if os.path.exists(cookie_file):
            os.remove(cookie_file)

def transcribe_with_whisper(video_id: str, video_url: str, audio_file: str, progress: Dict) -> bool:
    """Transcribe audio using Whisper."""
    transcript_file = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
    
    # Check if audio file exists and is valid
    if not os.path.exists(audio_file):
        print(f"  ❌ Audio file not found: {audio_file}")
        return False
    
    if os.path.getsize(audio_file) < 1000:  # Less than 1KB is likely corrupted
        print(f"  ❌ Audio file too small (likely corrupted): {audio_file}")
        return False
    
    try:
        print(f"  🎤 Transcribing with Whisper...")
        
        # Load Whisper model
        model = whisper.load_model("base")
        
        # Transcribe
        result = model.transcribe(audio_file)
        
        # Check if we got any text
        if not result["text"].strip():
            print(f"  ❌ No text extracted from audio")
            return False
        
        # Save transcript
        os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(result["text"])
        
        print(f"  ✅ Transcript saved: {transcript_file}")
        
        # Update progress tracking - transcript successfully created
        if video_url not in progress.get('whisper_processed', []):
            progress['whisper_processed'].append(video_url)
        
        # Track the method used
        progress['methods'][video_id] = 'Whisper'
        
        # Save progress immediately after successful transcription
        save_progress(progress)
        print(f"  📝 Progress saved: transcript processed")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Whisper transcription failed: {e}")
        return False

def process_video(video: Dict, progress: Dict, reprocess: bool = False) -> bool:
    """Process a single video with the working approach."""
    video_id = video.get('video_id')
    video_url = video.get('url')
    title = video.get('title', 'Unknown')
    
    if not video_id or not video_url:
        print(f"  ❌ Missing video_id or url")
        return False
    
    print(f"📹 Processing: {title}")
    print(f"    Video ID: {video_id}")
    
    # Check if already processed (skip if not reprocessing)
    if not reprocess and video_url in progress.get('whisper_processed', []):
        print(f"  ✅ Already processed")
        return True
    
    # If reprocessing, remove from all tracking lists
    if reprocess:
        if video_url in progress.get('whisper_processed', []):
            progress['whisper_processed'].remove(video_url)
        if video_url in progress.get('audio_downloaded', []):
            progress['audio_downloaded'].remove(video_url)
        if video_url in progress.get('failed', []):
            progress['failed'].remove(video_url)
        if video_id in progress.get('methods', {}):
            del progress['methods'][video_id]
    
    # Check if audio file exists
    audio_file = os.path.join(AUDIO_DIR, f"{video_id}.mp3")
    
    # Always try to download audio (will overwrite if exists)
    # This ensures we get the latest version and handle any corrupted files
    if not download_audio_with_cookies(video_url, video_id, progress):
        if video_url not in progress['failed']:
            progress['failed'].append(video_url)
        save_progress(progress)  # Save failure immediately
        return False
    
    # Transcribe with Whisper
    if not transcribe_with_whisper(video_id, video_url, audio_file, progress):
        if video_url not in progress['failed']:
            progress['failed'].append(video_url)
        save_progress(progress)  # Save failure immediately
        return False
    
    # Progress is already saved in transcribe_with_whisper function
    return True

def update_statistics(progress: Dict, videos: List[Dict]):
    """Update processing statistics."""
    total_videos = len(videos)
    audio_downloaded_count = len(progress.get('audio_downloaded', []))
    transcripts_completed_count = len(progress.get('whisper_processed', []))
    failed_count = len(progress.get('failed', []))
    
    progress['statistics'] = {
        'total_videos_discovered': total_videos,
        'audio_downloaded': audio_downloaded_count,
        'total_processed': transcripts_completed_count,
        'total_failed': failed_count,
        'success_rate': (transcripts_completed_count / total_videos * 100) if total_videos > 0 else 0,
        'last_updated': datetime.now().isoformat()
    }

def show_status(progress: Dict, videos: List[Dict]):
    """Show current processing status."""
    stats = progress.get('statistics', {})
    batch_info = progress.get('batch_info', {})
    
    # Calculate detailed progress
    audio_downloaded_count = len(progress.get('audio_downloaded', []))
    transcripts_completed_count = len(progress.get('whisper_processed', []))
    failed_count = len(progress.get('failed', []))
    total_videos = len(videos)
    
    print(f"📋 Current Processing Status")
    print(f"============================================================")
    print(f"📚 Total videos discovered: {total_videos}")
    print(f"🎵 Audio files downloaded: {audio_downloaded_count}")
    print(f"✅ Transcripts completed: {transcripts_completed_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"🎯 Remaining: {total_videos - transcripts_completed_count - failed_count}")
    print(f"📈 Completion rate: {(transcripts_completed_count / total_videos * 100) if total_videos > 0 else 0:.1f}%")
    
    if batch_info:
        print(f"\n📦 Batch Progress:")
        print(f"    🔄 Last batch completed: {batch_info.get('last_batch_completed', 0)}")
        print(f"    📊 Batch size: {batch_info.get('videos_per_batch', BATCH_SIZE)}")
        if batch_info.get('processing_started'):
            print(f"    🕐 Started: {batch_info.get('processing_started')}")
        if batch_info.get('last_updated'):
            print(f"    🕐 Last updated: {batch_info.get('last_updated')}")
    
    # Show recent failures
    recent_failures = progress.get('failed', [])[-5:]
    if recent_failures:
        print(f"\n❌ Recent failures (last {len(recent_failures)}):")
        for failure in recent_failures:
            # Extract video ID from URL
            video_id = failure.split('v=')[-1] if 'v=' in failure else failure
            print(f"    - {video_id}")
    
    print(f"\n📁 Progress file: {PROGRESS_FILE}")

def main():
    """Main processing function."""
    parser = argparse.ArgumentParser(description='Whisper-Focused Transcript Downloader with Browser Cookies')
    parser.add_argument('--status', action='store_true', help='Show current status only')
    parser.add_argument('--batch-size', type=int, default=BATCH_SIZE, help='Videos to process per batch')
    parser.add_argument('--reprocess', action='store_true', help='Reprocess already processed videos (overwrite existing files)')
    
    args = parser.parse_args()
    
    # Load videos and progress
    videos = load_videos()
    if not videos:
        return
    
    progress = load_progress()
    update_statistics(progress, videos)
    
    if args.status:
        show_status(progress, videos)
        return
    
    print(f"🚀 Whisper-Focused Transcript Downloader (Browser-Based)")
    print(f"============================================================")
    print(f"🔧 Using browser-extracted cookies to avoid detection")
    print(f"🆕 Updated yt-dlp with latest anti-bot countermeasures")
    print(f"📦 Processing in batches of {args.batch_size} videos")
    print(f"⏱️ Delays: {DELAY_BETWEEN_VIDEOS}s between videos, {DELAY_BETWEEN_BATCHES}s between batches")
    
    show_status(progress, videos)
    
    # Find videos to process
    processed_urls = set(progress.get('whisper_processed', []))
    failed_urls = set(progress.get('failed', []))
    
    videos_to_process = []
    for video in videos:
        video_url = video.get('url')
        if not video_url:
            continue
            
        if args.reprocess:
            # Reprocess all videos (including already processed ones)
            videos_to_process.append(video)
        else:
            # Only process unprocessed videos
            if video_url not in processed_urls and video_url not in failed_urls:
                videos_to_process.append(video)
    
    if not videos_to_process:
        print(f"\n✅ All videos processed or failed!")
        return
    
    print(f"\n🎯 Found {len(videos_to_process)} videos to process")
    
    # Process in batches
    batch_size = args.batch_size
    total_batches = (len(videos_to_process) + batch_size - 1) // batch_size
    
    # Initialize batch info
    if 'batch_info' not in progress:
        progress['batch_info'] = {}
    
    progress['batch_info'].update({
        'videos_per_batch': batch_size,
        'total_batches': total_batches,
        'processing_started': datetime.now().isoformat()
    })
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(videos_to_process))
        batch_videos = videos_to_process[start_idx:end_idx]
        
        print(f"\n🔄 Processing batch {batch_num + 1}/{total_batches} ({len(batch_videos)} videos)")
        print(f"============================================================")
        
        batch_start_time = time.time()
        batch_successes = 0
        
        for i, video in enumerate(batch_videos, 1):
            print(f"\n📹 Video {i}/{len(batch_videos)} in batch {batch_num + 1}")
            
            if process_video(video, progress, reprocess=args.reprocess):
                batch_successes += 1
                print(f"    ✅ Success!")
            else:
                print(f"    ❌ Failed")
            
            # Update statistics and save progress
            update_statistics(progress, videos)
            save_progress(progress)
            
            # Delay between videos
            if i < len(batch_videos):
                print(f"    ⏸️  Pausing {DELAY_BETWEEN_VIDEOS} seconds...")
                time.sleep(DELAY_BETWEEN_VIDEOS)
        
        # Batch summary
        batch_time = time.time() - batch_start_time
        batch_success_rate = (batch_successes / len(batch_videos) * 100) if batch_videos else 0
        
        print(f"\n📊 Batch {batch_num + 1}/{total_batches} Complete!")
        print(f"    ✅ Successes: {batch_successes}")
        print(f"    ❌ Failures: {len(batch_videos) - batch_successes}")
        print(f"    ⏱️  Batch time: {batch_time:.1f}s")
        print(f"    📈 Batch success rate: {batch_success_rate:.1f}%")
        
        # Update batch info
        progress['batch_info'].update({
            'last_batch_completed': batch_num + 1,
            'last_updated': datetime.now().isoformat()
        })
        save_progress(progress)
        
        # Delay between batches
        if batch_num < total_batches - 1:
            print(f"    ⏸️  Pausing {DELAY_BETWEEN_BATCHES} seconds before next batch...")
            time.sleep(DELAY_BETWEEN_BATCHES)
    
    # Final summary
    update_statistics(progress, videos)
    save_progress(progress)
    
    print(f"\n🎉 Processing Complete!")
    show_status(progress, videos)

if __name__ == "__main__":
    main() 