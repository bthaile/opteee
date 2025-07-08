#!/usr/bin/env python3
"""
Improved YouTube Transcript Downloader
Prioritizes transcript downloading over video downloading using multiple methods:
1. YouTube API captions (most reliable)
2. YouTube Transcript API (fallback)
3. yt-dlp transcript extraction (fallback)
4. Whisper transcription (last resort)
"""

import os
import json
import time
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Optional, Tuple
import tempfile
import subprocess
from pathlib import Path

# Third-party imports
import yt_dlp
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# Load environment variables
load_dotenv()

# Configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
PROGRESS_FILE = "transcript_progress.json"
TRANSCRIPT_DIR = "transcripts"
VIDEOS_JSON = "outlier_trading_videos.json"
BATCH_SIZE = 50  # YouTube API batch size
MAX_RETRIES = 3

# Ensure directories exist
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

class TranscriptDownloader:
    def __init__(self):
        self.youtube_api = None
        if YOUTUBE_API_KEY:
            self.youtube_api = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        
        self.progress = self.load_progress()
        self.stats = {
            'youtube_api_success': 0,
            'youtube_transcript_api_success': 0,
            'yt_dlp_success': 0,
            'whisper_success': 0,
            'total_failures': 0,
            'skipped_existing': 0
        }
    
    def load_progress(self) -> Dict:
        """Load processing progress from file."""
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        return {
            'processed': [],
            'failed': [],
            'methods': {}  # Track which method was used for each video
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
    
    def get_transcript_via_youtube_api(self, video_id: str) -> Optional[List[Dict]]:
        """Get transcript using YouTube API (most reliable method)."""
        if not self.youtube_api:
            return None
            
        try:
            # Get video details including available captions
            request = self.youtube_api.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()
            
            if not response.get('items'):
                return None
            
            # Get captions list
            captions_request = self.youtube_api.captions().list(
                part="snippet",
                videoId=video_id
            )
            captions_response = captions_request.execute()
            
            # Find English captions
            caption_id = None
            for item in captions_response.get('items', []):
                snippet = item.get('snippet', {})
                if snippet.get('language') in ['en', 'en-US', 'en-GB']:
                    caption_id = item.get('id')
                    break
            
            if not caption_id:
                return None
            
            # Download the caption
            caption_request = self.youtube_api.captions().download(
                id=caption_id,
                tfmt='srt'  # SubRip format
            )
            caption_content = caption_request.execute()
            
            # Parse SRT format
            transcript = self.parse_srt_content(caption_content)
            return transcript
            
        except HttpError as e:
            if e.resp.status == 403:
                print(f"  ⚠️  Captions disabled for video {video_id}")
            else:
                print(f"  ❌ YouTube API error for {video_id}: {e}")
            return None
        except Exception as e:
            print(f"  ❌ Unexpected error with YouTube API for {video_id}: {e}")
            return None
    
    def parse_srt_content(self, content: str) -> List[Dict]:
        """Parse SRT subtitle content into transcript format."""
        transcript = []
        lines = content.strip().split('\n')
        
        i = 0
        while i < len(lines):
            # Skip sequence number
            if lines[i].strip().isdigit():
                i += 1
                continue
                
            # Parse timestamp line
            if '-->' in lines[i]:
                timestamp_line = lines[i]
                start_time = timestamp_line.split(' --> ')[0]
                start_seconds = self.srt_time_to_seconds(start_time)
                
                # Get text content
                text_lines = []
                i += 1
                while i < len(lines) and lines[i].strip():
                    text_lines.append(lines[i].strip())
                    i += 1
                
                if text_lines:
                    transcript.append({
                        'start': start_seconds,
                        'text': ' '.join(text_lines)
                    })
            
            i += 1
        
        return transcript
    
    def srt_time_to_seconds(self, time_str: str) -> float:
        """Convert SRT timestamp to seconds."""
        # Format: HH:MM:SS,mmm
        time_str = time_str.replace(',', '.')
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    
    def get_transcript_via_transcript_api(self, video_id: str) -> Optional[List[Dict]]:
        """Get transcript using youtube-transcript-api."""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except (TranscriptsDisabled, NoTranscriptFound):
            return None
        except Exception as e:
            print(f"  ❌ Transcript API error for {video_id}: {e}")
            return None
    
    def get_transcript_via_yt_dlp(self, url: str) -> Optional[List[Dict]]:
        """Get transcript using yt-dlp (can extract more formats)."""
        try:
            ydl_opts = {
                'writeautomaticsub': True,
                'skip_download': True,
                'quiet': True,
                'no_warnings': True,
                'subtitleslangs': ['en', 'en-US', 'en-GB'],
                'subtitlesformat': 'vtt',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Check if automatic subtitles were found
                auto_subs = info.get('automatic_captions', {})
                if 'en' in auto_subs:
                    # Get the VTT subtitle URL
                    vtt_url = None
                    for subtitle in auto_subs['en']:
                        if subtitle['ext'] == 'vtt':
                            vtt_url = subtitle['url']
                            break
                    
                    if vtt_url:
                        # Download and parse VTT content
                        response = requests.get(vtt_url)
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
            if '-->' in line:
                # Parse timestamp
                start_time = line.split(' --> ')[0]
                start_seconds = self.vtt_time_to_seconds(start_time)
                
                # Get text content
                text_lines = []
                i += 1
                while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
                    text_lines.append(lines[i].strip())
                    i += 1
                
                if text_lines:
                    # Remove VTT tags
                    text = ' '.join(text_lines)
                    text = self.clean_vtt_text(text)
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
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    
    def clean_vtt_text(self, text: str) -> str:
        """Clean VTT text by removing formatting tags."""
        # Remove common VTT tags
        import re
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML-like tags
        text = re.sub(r'&[^;]+;', '', text)  # Remove HTML entities
        return text.strip()
    
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
            ("YouTube API", lambda: self.get_transcript_via_youtube_api(video_id)),
            ("Transcript API", lambda: self.get_transcript_via_transcript_api(video_id)),
            ("yt-dlp", lambda: self.get_transcript_via_yt_dlp(url))
        ]
        
        for method_name, method_func in methods:
            print(f"  🔄 Trying {method_name} for {video_id}...")
            
            try:
                transcript = method_func()
                if transcript:
                    # Save transcript
                    with open(transcript_file, 'w', encoding='utf-8') as f:
                        for entry in transcript:
                            f.write(f"{entry['start']:.2f}s: {entry['text']}\n")
                    
                    print(f"  ✅ Success with {method_name} for {video_id}")
                    self.progress['processed'].append(url)
                    self.progress['methods'][video_id] = method_name
                    self.stats[f"{method_name.lower().replace(' ', '_')}_success"] += 1
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
            
            # Rate limiting
            time.sleep(1)
        
        # Final statistics
        elapsed_time = time.time() - start_time
        print(f"\n📊 Processing Summary:")
        print(f"✅ YouTube API successes: {self.stats['youtube_api_success']}")
        print(f"✅ Transcript API successes: {self.stats['youtube_transcript_api_success']}")
        print(f"✅ yt-dlp successes: {self.stats['yt_dlp_success']}")
        print(f"⏭️  Skipped existing: {self.stats['skipped_existing']}")
        print(f"❌ Total failures: {self.stats['total_failures']}")
        print(f"⏱️  Total time: {elapsed_time:.2f} seconds")
        
        # Show failed videos for manual review
        if self.progress['failed']:
            print(f"\n❌ Failed videos ({len(self.progress['failed'])}):")
            for url in self.progress['failed'][-10:]:  # Show last 10 failures
                print(f"  - {url}")
            if len(self.progress['failed']) > 10:
                print(f"  ... and {len(self.progress['failed']) - 10} more")

def main():
    """Main function to run the transcript downloader."""
    downloader = TranscriptDownloader()
    
    if not YOUTUBE_API_KEY:
        print("⚠️  WARNING: No YouTube API key found. Some methods may not work.")
        print("   Set YOUTUBE_API_KEY in your .env file for best results.")
    
    downloader.process_videos()

if __name__ == "__main__":
    main() 