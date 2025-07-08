#!/usr/bin/env python3
"""
Robust YouTube Transcript Downloader
Uses the most reliable methods for transcript extraction:
1. YouTube Transcript API (youtube-transcript-api)
2. yt-dlp automatic subtitle extraction
3. Whisper transcription (only as last resort)

This version focuses on reliability and avoids methods that commonly fail.
"""

import os
import json
import time
import requests
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Optional
import tempfile
from pathlib import Path

# Third-party imports
import yt_dlp
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# Load environment variables
load_dotenv()

# Configuration
PROGRESS_FILE = "transcript_progress.json"
TRANSCRIPT_DIR = "transcripts"
VIDEOS_JSON = "outlier_trading_videos.json"
MAX_RETRIES = 3

# Ensure directories exist
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

class TranscriptDownloader:
    def __init__(self):
        self.progress = self.load_progress()
        self.stats = {
            'transcript_api_success': 0,
            'yt_dlp_success': 0,
            'whisper_success': 0,
            'total_failures': 0,
            'skipped_existing': 0
        }
        
        # Load Whisper model if available
        self.whisper_model = None
        if WHISPER_AVAILABLE:
            try:
                print("🎤 Loading Whisper model...")
                self.whisper_model = whisper.load_model("base")
                print("✅ Whisper model loaded successfully")
            except Exception as e:
                print(f"⚠️ Could not load Whisper model: {e}")
    
    def load_progress(self) -> Dict:
        """Load processing progress from file."""
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        return {
            'processed': [],
            'failed': [],
            'methods': {}
        }
    
    def save_progress(self):
        """Save processing progress to file."""
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def get_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        if not url:
            return None
            
        # Handle different YouTube URL formats
        if 'youtu.be' in url:
            return url.split('/')[-1].split('?')[0]
        elif 'youtube.com' in url:
            parsed = urlparse(url)
            return parse_qs(parsed.query).get('v', [None])[0]
        return None
    
    def get_transcript_via_transcript_api(self, video_id: str) -> Optional[List[Dict]]:
        """Get transcript using youtube-transcript-api (most reliable)."""
        try:
            # Try to get transcript in English
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'en-GB'])
            return transcript
        except (TranscriptsDisabled, NoTranscriptFound):
            return None
        except Exception as e:
            print(f"  ❌ Transcript API error for {video_id}: {e}")
            return None
    
    def get_transcript_via_yt_dlp(self, url: str) -> Optional[List[Dict]]:
        """Get transcript using yt-dlp automatic subtitle extraction."""
        try:
            ydl_opts = {
                'writeautomaticsub': True,
                'skip_download': True,
                'quiet': True,
                'no_warnings': True,
                'subtitleslangs': ['en', 'en-US', 'en-GB'],
                'writesubtitles': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Check for automatic captions
                auto_subs = info.get('automatic_captions', {})
                manual_subs = info.get('subtitles', {})
                
                # Try manual subtitles first (usually better quality)
                subs = manual_subs.get('en') or auto_subs.get('en')
                
                if subs:
                    # Find VTT format
                    vtt_url = None
                    for subtitle in subs:
                        if subtitle.get('ext') == 'vtt':
                            vtt_url = subtitle.get('url')
                            break
                    
                    if vtt_url:
                        # Download and parse VTT content
                        response = requests.get(vtt_url, timeout=30)
                        if response.status_code == 200:
                            return self.parse_vtt_content(response.text)
                
                return None
                
        except Exception as e:
            print(f"  ❌ yt-dlp error for {url}: {e}")
            return None
    
    def parse_vtt_content(self, content: str) -> List[Dict]:
        """Parse VTT subtitle content into transcript format."""
        transcript = []
        lines = content.strip().split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for timestamp lines
            if '-->' in line and not line.startswith('NOTE'):
                # Parse timestamp
                timestamp_part = line.split(' --> ')[0]
                start_seconds = self.vtt_time_to_seconds(timestamp_part)
                
                # Get text content
                text_lines = []
                i += 1
                while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
                    text_line = lines[i].strip()
                    if text_line and not text_line.startswith('NOTE'):
                        text_lines.append(text_line)
                    i += 1
                
                if text_lines:
                    # Clean and combine text
                    text = ' '.join(text_lines)
                    text = self.clean_vtt_text(text)
                    if text:  # Only add non-empty text
                        transcript.append({
                            'start': start_seconds,
                            'text': text
                        })
                continue
            
            i += 1
        
        return transcript
    
    def vtt_time_to_seconds(self, time_str: str) -> float:
        """Convert VTT timestamp to seconds."""
        # Format: HH:MM:SS.mmm
        try:
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            return hours * 3600 + minutes * 60 + seconds
        except:
            return 0.0
    
    def clean_vtt_text(self, text: str) -> str:
        """Clean VTT text by removing formatting tags."""
        import re
        # Remove HTML-like tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove HTML entities
        text = re.sub(r'&[^;]+;', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def download_audio_and_transcribe(self, url: str, video_id: str) -> Optional[List[Dict]]:
        """Download audio and transcribe with Whisper (last resort)."""
        if not self.whisper_model:
            return None
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                audio_path = os.path.join(temp_dir, f"{video_id}.mp3")
                
                # Download audio only
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': audio_path,
                    'quiet': True,
                    'no_warnings': True,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Check if audio file was created
                if not os.path.exists(audio_path):
                    return None
                
                # Transcribe with Whisper
                print(f"  🎤 Transcribing audio with Whisper...")
                result = self.whisper_model.transcribe(audio_path)
                
                # Convert to our format
                transcript = []
                for segment in result.get("segments", []):
                    transcript.append({
                        'start': segment["start"],
                        'text': segment["text"].strip()
                    })
                
                return transcript
                
        except Exception as e:
            print(f"  ❌ Whisper transcription error: {e}")
            return None
    
    def download_transcript(self, video_id: str, title: str, url: str) -> bool:
        """Download transcript using the best available method."""
        transcript_file = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
        
        # Skip if already exists
        if os.path.exists(transcript_file):
            print(f"  ⏭️  Transcript already exists for {video_id}")
            self.stats['skipped_existing'] += 1
            return True
        
        # Try methods in order of preference
        methods = [
            ("YouTube Transcript API", lambda: self.get_transcript_via_transcript_api(video_id)),
            ("yt-dlp Subtitles", lambda: self.get_transcript_via_yt_dlp(url)),
        ]
        
        # Add Whisper as last resort if available
        if self.whisper_model:
            methods.append(("Whisper", lambda: self.download_audio_and_transcribe(url, video_id)))
        
        for method_name, method_func in methods:
            print(f"  🔄 Trying {method_name} for {video_id}...")
            
            try:
                transcript = method_func()
                if transcript and len(transcript) > 0:
                    # Save transcript
                    with open(transcript_file, 'w', encoding='utf-8') as f:
                        for entry in transcript:
                            f.write(f"{entry['start']:.2f}s: {entry['text']}\n")
                    
                    print(f"  ✅ Success with {method_name} for {video_id} ({len(transcript)} segments)")
                    self.progress['processed'].append(url)
                    self.progress['methods'][video_id] = method_name
                    
                    # Update stats
                    if method_name == "YouTube Transcript API":
                        self.stats['transcript_api_success'] += 1
                    elif method_name == "yt-dlp Subtitles":
                        self.stats['yt_dlp_success'] += 1
                    elif method_name == "Whisper":
                        self.stats['whisper_success'] += 1
                    
                    return True
                else:
                    print(f"  ❌ No transcript found with {method_name} for {video_id}")
                    
            except Exception as e:
                print(f"  ❌ Error with {method_name} for {video_id}: {e}")
                continue
        
        # All methods failed
        print(f"  ❌ All methods failed for {video_id}")
        self.progress['failed'].append(url)
        self.stats['total_failures'] += 1
        return False
    
    def process_videos(self):
        """Process all videos from the JSON file."""
        # Load video data
        try:
            with open(VIDEOS_JSON, 'r', encoding='utf-8') as f:
                videos = json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: {VIDEOS_JSON} not found. Please run outlier_scraper.py first.")
            return
        
        print(f"📚 Found {len(videos)} videos to process")
        
        # Filter out already processed videos
        processed_urls = set(self.progress['processed'])
        failed_urls = set(self.progress['failed'])
        
        remaining_videos = [
            v for v in videos 
            if v.get('url') not in processed_urls and v.get('url') not in failed_urls
        ]
        
        print(f"📝 {len(processed_urls)} already processed")
        print(f"❌ {len(failed_urls)} previously failed")
        print(f"🎯 {len(remaining_videos)} remaining to process")
        
        if not remaining_videos:
            print("✅ All videos have been processed!")
            return
        
        # Process remaining videos
        start_time = time.time()
        
        for i, video in enumerate(remaining_videos):
            video_id = self.get_video_id(video.get('url'))
            if not video_id:
                print(f"⚠️  Could not extract ID from {video.get('url')}")
                continue
            
            title = video.get('title', 'Unknown Title')
            print(f"\n📹 Processing {i+1}/{len(remaining_videos)}: {title}")
            
            success = self.download_transcript(video_id, title, video.get('url'))
            
            # Save progress after each video
            self.save_progress()
            
            # Rate limiting - be nice to YouTube
            time.sleep(1)
        
        # Final statistics
        elapsed_time = time.time() - start_time
        print(f"\n📊 Processing Summary:")
        print(f"✅ YouTube Transcript API successes: {self.stats['transcript_api_success']}")
        print(f"✅ yt-dlp subtitle successes: {self.stats['yt_dlp_success']}")
        print(f"✅ Whisper transcription successes: {self.stats['whisper_success']}")
        print(f"⏭️  Skipped existing: {self.stats['skipped_existing']}")
        print(f"❌ Total failures: {self.stats['total_failures']}")
        print(f"⏱️  Total time: {elapsed_time:.2f} seconds")
        
        # Calculate success rate
        total_attempted = len(remaining_videos)
        total_successful = self.stats['transcript_api_success'] + self.stats['yt_dlp_success'] + self.stats['whisper_success']
        if total_attempted > 0:
            success_rate = (total_successful / total_attempted) * 100
            print(f"📈 Success rate: {success_rate:.1f}%")
        
        # Show failed videos for manual review
        if self.progress['failed']:
            print(f"\n❌ Failed videos ({len(self.progress['failed'])}):")
            for url in self.progress['failed'][-5:]:  # Show last 5 failures
                video_id = self.get_video_id(url)
                print(f"  - {video_id}: {url}")
            if len(self.progress['failed']) > 5:
                print(f"  ... and {len(self.progress['failed']) - 5} more")
                
        # Show successful methods breakdown
        if self.progress['methods']:
            print(f"\n📊 Method breakdown:")
            method_counts = {}
            for method in self.progress['methods'].values():
                method_counts[method] = method_counts.get(method, 0) + 1
            
            for method, count in method_counts.items():
                print(f"  - {method}: {count} videos")

def main():
    """Main function to run the transcript downloader."""
    print("🚀 Starting YouTube Transcript Downloader")
    print("=" * 50)
    
    downloader = TranscriptDownloader()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not WHISPER_AVAILABLE:
        print("⚠️  Whisper not available. Install with: pip install openai-whisper")
        print("   Only YouTube transcript methods will be used.")
    
    downloader.process_videos()

if __name__ == "__main__":
    main() 