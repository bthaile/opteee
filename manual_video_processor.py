#!/usr/bin/env python3
"""
Manual Video Processing Pipeline

This script provides a clean, systematic approach to handling failed video downloads
with proper state tracking and resumable processing at each step.

States:
1. FAILED_DOWNLOAD - Video download failed, needs manual download
2. HAVE_VIDEO_NO_TRANSCRIPT - Video downloaded but transcript generation failed
3. COMPLETED - Video downloaded and transcript generated successfully
4. REQUIRES_MANUAL - Video requires manual intervention (blocked, private, etc.)
"""

import json
import os
import glob
import sys
from pathlib import Path
from typing import Dict, List, Set
import subprocess
import whisper
from datetime import datetime

class VideoProcessor:
    def __init__(self):
        self.base_dir = Path(".")
        self.audio_dir = self.base_dir / "audio_files"
        self.transcript_dir = self.base_dir / "transcripts"
        self.status_file = self.base_dir / "video_processing_status.json"
        
        # Create directories if they don't exist
        self.audio_dir.mkdir(exist_ok=True)
        self.transcript_dir.mkdir(exist_ok=True)
        
        # Load or create status tracking
        self.status_data = self.load_status()
        
    def load_status(self) -> Dict:
        """Load the video processing status from file"""
        if self.status_file.exists():
            with open(self.status_file, 'r') as f:
                return json.load(f)
        return {"videos": {}, "last_updated": None}
    
    def save_status(self):
        """Save the current status to file"""
        self.status_data["last_updated"] = datetime.now().isoformat()
        with open(self.status_file, 'w') as f:
            json.dump(self.status_data, f, indent=2)
    
    def get_video_id_from_url(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        return url  # Assume it's already a video ID
    
    def scan_current_state(self):
        """Scan current files and update status for all videos"""
        print("🔍 Scanning current state of all videos...")
        
        # Load failed videos from existing tracking files
        failed_videos = self.load_failed_videos()
        
        for video_info in failed_videos:
            video_id = self.get_video_id_from_url(video_info.get("url", ""))
            if not video_id:
                continue
                
            status = self.determine_video_status(video_id)
            
            self.status_data["videos"][video_id] = {
                "url": video_info.get("url", ""),
                "title": video_info.get("title", "Unknown"),
                "status": status,
                "audio_file": f"audio_files/{video_id}.mp3",
                "transcript_file": f"transcripts/{video_id}.txt",
                "last_checked": datetime.now().isoformat()
            }
        
        self.save_status()
        print(f"✅ Scanned {len(self.status_data['videos'])} videos")
    
    def load_failed_videos(self) -> List[Dict]:
        """Load failed videos from various tracking files"""
        failed_videos = []
        
        # Load from failed_video_urls.txt
        if os.path.exists("failed_video_urls.txt"):
            with open("failed_video_urls.txt", 'r') as f:
                for line in f:
                    url = line.strip()
                    if url:
                        failed_videos.append({"url": url, "title": "Unknown"})
        
        # Load from manual_processing_needed.json
        if os.path.exists("manual_processing_needed.json"):
            with open("manual_processing_needed.json", 'r') as f:
                manual_needed = json.load(f)
                for url in manual_needed:
                    failed_videos.append({"url": url, "title": "Manual Processing Needed"})
        
        # Load from missing_transcripts.json
        if os.path.exists("missing_transcripts.json"):
            with open("missing_transcripts.json", 'r') as f:
                missing = json.load(f)
                for item in missing:
                    failed_videos.append({
                        "url": item.get("url", ""),
                        "title": item.get("title", "Unknown")
                    })
        
        return failed_videos
    
    def determine_video_status(self, video_id: str) -> str:
        """Determine the current status of a video"""
        audio_file = self.audio_dir / f"{video_id}.mp3"
        transcript_file = self.transcript_dir / f"{video_id}.txt"
        
        # Check if we have a real audio file (not dummy)
        has_real_audio = False
        if audio_file.exists():
            file_size = audio_file.stat().st_size
            has_real_audio = file_size > 50000  # More than 50KB indicates real audio
        
        # Check if we have a real transcript (not error message)
        has_real_transcript = False
        if transcript_file.exists():
            with open(transcript_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check if it's not an error message
                has_real_transcript = (
                    len(content) > 1000 and 
                    "DOWNLOAD FAILED" not in content and
                    "This transcript is a placeholder" not in content
                )
        
        # Determine status based on what we have
        if has_real_audio and has_real_transcript:
            return "COMPLETED"
        elif has_real_audio and not has_real_transcript:
            return "HAVE_VIDEO_NO_TRANSCRIPT"
        else:
            return "FAILED_DOWNLOAD"
    
    def show_status_summary(self):
        """Show a summary of all video statuses"""
        if not self.status_data["videos"]:
            print("⚠️  No videos tracked. Run --scan first.")
            return
        
        status_counts = {}
        for video_id, info in self.status_data["videos"].items():
            status = info["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("\n📊 VIDEO PROCESSING STATUS SUMMARY")
        print("=" * 50)
        
        for status, count in status_counts.items():
            emoji = {
                "FAILED_DOWNLOAD": "❌",
                "HAVE_VIDEO_NO_TRANSCRIPT": "🎵",
                "COMPLETED": "✅",
                "REQUIRES_MANUAL": "🔧"
            }.get(status, "❓")
            
            print(f"{emoji} {status}: {count} videos")
        
        total = sum(status_counts.values())
        completed = status_counts.get("COMPLETED", 0)
        progress = (completed / total * 100) if total > 0 else 0
        
        print(f"\n🎯 Overall Progress: {completed}/{total} ({progress:.1f}%)")
    
    def show_videos_by_status(self, status: str, limit: int = 10):
        """Show videos with a specific status"""
        matching_videos = [
            (vid, info) for vid, info in self.status_data["videos"].items()
            if info["status"] == status
        ]
        
        if not matching_videos:
            print(f"✅ No videos with status: {status}")
            return
        
        status_names = {
            "FAILED_DOWNLOAD": "❌ Need Manual Download",
            "HAVE_VIDEO_NO_TRANSCRIPT": "🎵 Need Transcript Generation",
            "COMPLETED": "✅ Completed Successfully",
            "REQUIRES_MANUAL": "🔧 Requires Manual Intervention"
        }
        
        print(f"\n{status_names.get(status, status)}")
        print("=" * 50)
        
        for i, (video_id, info) in enumerate(matching_videos[:limit]):
            title = info.get("title", "Unknown")[:60]
            print(f"{i+1:2d}. {video_id} - {title}")
            if status == "FAILED_DOWNLOAD":
                print(f"    📥 Download: {info['url']}")
                print(f"    💾 Save as: audio_files/{video_id}.mp3")
        
        if len(matching_videos) > limit:
            print(f"... and {len(matching_videos) - limit} more")
    
    def process_transcripts(self, video_ids: List[str] = None):
        """Process transcripts for videos that have audio but no transcript"""
        if video_ids is None:
            # Process all videos with status HAVE_VIDEO_NO_TRANSCRIPT
            video_ids = [
                vid for vid, info in self.status_data["videos"].items()
                if info["status"] == "HAVE_VIDEO_NO_TRANSCRIPT"
            ]
        
        if not video_ids:
            print("✅ No videos need transcript processing")
            return
        
        print(f"🎤 Processing transcripts for {len(video_ids)} videos...")
        
        # Load Whisper model
        try:
            model = whisper.load_model("base")
            print("✅ Whisper model loaded")
        except Exception as e:
            print(f"❌ Failed to load Whisper model: {e}")
            return
        
        successful = 0
        failed = 0
        
        for i, video_id in enumerate(video_ids):
            print(f"\n🎵 Processing {i+1}/{len(video_ids)}: {video_id}")
            
            audio_file = self.audio_dir / f"{video_id}.mp3"
            transcript_file = self.transcript_dir / f"{video_id}.txt"
            
            if not audio_file.exists():
                print(f"❌ Audio file not found: {audio_file}")
                failed += 1
                continue
            
            try:
                # Transcribe with Whisper
                result = model.transcribe(str(audio_file))
                
                # Save transcript
                with open(transcript_file, 'w', encoding='utf-8') as f:
                    f.write(result['text'])
                
                # Update status
                self.status_data["videos"][video_id]["status"] = "COMPLETED"
                self.status_data["videos"][video_id]["last_checked"] = datetime.now().isoformat()
                
                char_count = len(result['text'])
                print(f"✅ Transcript saved: {char_count} characters")
                successful += 1
                
            except Exception as e:
                print(f"❌ Transcription failed: {e}")
                failed += 1
        
        self.save_status()
        print(f"\n📊 Transcript processing complete: {successful} successful, {failed} failed")
    
    def cleanup_dummy_files(self):
        """Remove dummy audio files and error transcript files"""
        print("🧹 Cleaning up dummy files...")
        
        cleaned_audio = 0
        cleaned_transcripts = 0
        
        # Clean up dummy audio files
        for audio_file in self.audio_dir.glob("*.mp3"):
            if audio_file.stat().st_size <= 50000:  # Less than 50KB is likely dummy
                video_id = audio_file.stem
                print(f"🗑️  Removing dummy audio: {audio_file.name}")
                audio_file.unlink()
                cleaned_audio += 1
                
                # Update status
                if video_id in self.status_data["videos"]:
                    self.status_data["videos"][video_id]["status"] = "FAILED_DOWNLOAD"
        
        # Clean up error transcript files
        for transcript_file in self.transcript_dir.glob("*.txt"):
            try:
                with open(transcript_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "DOWNLOAD FAILED" in content or "This transcript is a placeholder" in content:
                        video_id = transcript_file.stem
                        print(f"🗑️  Removing error transcript: {transcript_file.name}")
                        transcript_file.unlink()
                        cleaned_transcripts += 1
                        
                        # Update status
                        if video_id in self.status_data["videos"]:
                            current_status = self.status_data["videos"][video_id]["status"]
                            if current_status == "COMPLETED":
                                # Check if we still have audio
                                audio_file = self.audio_dir / f"{video_id}.mp3"
                                if audio_file.exists() and audio_file.stat().st_size > 50000:
                                    self.status_data["videos"][video_id]["status"] = "HAVE_VIDEO_NO_TRANSCRIPT"
                                else:
                                    self.status_data["videos"][video_id]["status"] = "FAILED_DOWNLOAD"
            except Exception as e:
                print(f"⚠️  Error reading {transcript_file}: {e}")
        
        self.save_status()
        print(f"✅ Cleanup complete: {cleaned_audio} audio files, {cleaned_transcripts} transcript files")
    
    def export_download_list(self, filename: str = "download_list.txt"):
        """Export a list of videos that need manual download"""
        failed_videos = [
            (vid, info) for vid, info in self.status_data["videos"].items()
            if info["status"] == "FAILED_DOWNLOAD"
        ]
        
        if not failed_videos:
            print("✅ No videos need manual download")
            return
        
        with open(filename, 'w') as f:
            f.write("# Videos requiring manual download\n")
            f.write("# Format: VIDEO_ID | URL | TITLE\n\n")
            
            for video_id, info in failed_videos:
                f.write(f"{video_id} | {info['url']} | {info.get('title', 'Unknown')}\n")
        
        print(f"📋 Download list exported to {filename} ({len(failed_videos)} videos)")

def main():
    processor = VideoProcessor()
    
    if len(sys.argv) == 1:
        # Default: show status
        processor.show_status_summary()
        return
    
    command = sys.argv[1]
    
    if command == "--scan":
        processor.scan_current_state()
        processor.show_status_summary()
    
    elif command == "--status":
        processor.show_status_summary()
    
    elif command == "--failed":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        processor.show_videos_by_status("FAILED_DOWNLOAD", limit)
    
    elif command == "--need-transcript":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        processor.show_videos_by_status("HAVE_VIDEO_NO_TRANSCRIPT", limit)
    
    elif command == "--completed":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        processor.show_videos_by_status("COMPLETED", limit)
    
    elif command == "--process-transcripts":
        if len(sys.argv) > 2:
            # Process specific video IDs
            video_ids = sys.argv[2:]
            processor.process_transcripts(video_ids)
        else:
            # Process all videos that need transcripts
            processor.process_transcripts()
    
    elif command == "--cleanup":
        processor.cleanup_dummy_files()
    
    elif command == "--export":
        filename = sys.argv[2] if len(sys.argv) > 2 else "download_list.txt"
        processor.export_download_list(filename)
    
    else:
        print("""
🎬 Manual Video Processing Pipeline

Usage:
  python3 manual_video_processor.py [command]

Commands:
  --scan                    Scan all files and update status
  --status                  Show processing status summary
  --failed [limit]          Show videos needing manual download
  --need-transcript [limit] Show videos needing transcript processing
  --completed [limit]       Show completed videos
  --process-transcripts     Process all videos needing transcripts
  --process-transcripts ID1 ID2...  Process specific video IDs
  --cleanup                 Remove dummy files and error transcripts
  --export [filename]       Export download list to file

Examples:
  python3 manual_video_processor.py --scan
  python3 manual_video_processor.py --failed 20
  python3 manual_video_processor.py --process-transcripts
  python3 manual_video_processor.py --process-transcripts abc123 def456
""")

if __name__ == "__main__":
    main() 