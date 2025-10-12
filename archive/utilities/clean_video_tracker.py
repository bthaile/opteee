#!/usr/bin/env python3
"""
Clean Video Tracker - No Dummy Files!

This system tracks video processing state using only JSON files.
No dummy files, no .note.txt files, just clean state management.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set
import whisper
from datetime import datetime

class CleanVideoTracker:
    def __init__(self):
        self.base_dir = Path(".")
        self.audio_dir = self.base_dir / "audio_files"
        self.transcript_dir = self.base_dir / "transcripts"
        self.state_file = self.base_dir / "video_state.json"
        
        # Create directories if they don't exist
        self.audio_dir.mkdir(exist_ok=True)
        self.transcript_dir.mkdir(exist_ok=True)
        
        # Load or create state tracking
        self.state = self.load_state()
        
    def load_state(self) -> Dict:
        """Load the video state from JSON file"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {
            "videos": {},
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": None,
                "total_videos": 0,
                "completed": 0,
                "failed_downloads": 0,
                "pending_transcripts": 0
            }
        }
    
    def save_state(self):
        """Save the current state to JSON file"""
        # Update metadata
        self.state["metadata"]["last_updated"] = datetime.now().isoformat()
        self.state["metadata"]["total_videos"] = len(self.state["videos"])
        
        # Count statuses
        status_counts = {}
        for video_info in self.state["videos"].values():
            status = video_info["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        self.state["metadata"]["completed"] = status_counts.get("COMPLETED", 0)
        self.state["metadata"]["failed_downloads"] = status_counts.get("FAILED_DOWNLOAD", 0)
        self.state["metadata"]["pending_transcripts"] = status_counts.get("HAVE_AUDIO_NO_TRANSCRIPT", 0)
        
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL"""
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        return url.strip()
    
    def import_failed_videos(self):
        """Import failed videos from existing tracking files into clean JSON state"""
        print("📥 Importing failed videos from existing files...")
        
        imported_count = 0
        
        # Import from failed_video_urls.txt
        if os.path.exists("failed_video_urls.txt"):
            with open("failed_video_urls.txt", 'r') as f:
                for line in f:
                    url = line.strip()
                    if url and url.startswith("http"):
                        video_id = self.extract_video_id(url)
                        if video_id and video_id not in self.state["videos"]:
                            self.state["videos"][video_id] = {
                                "url": url,
                                "title": "Unknown Title",
                                "status": "FAILED_DOWNLOAD",
                                "audio_file_path": f"audio_files/{video_id}.mp3",
                                "transcript_file_path": f"transcripts/{video_id}.txt",
                                "created": datetime.now().isoformat(),
                                "last_updated": datetime.now().isoformat(),
                                "source": "failed_video_urls.txt"
                            }
                            imported_count += 1
        
        # Import from manual_processing_needed.json
        if os.path.exists("manual_processing_needed.json"):
            with open("manual_processing_needed.json", 'r') as f:
                manual_needed = json.load(f)
                for url in manual_needed:
                    if isinstance(url, str) and url.startswith("http"):
                        video_id = self.extract_video_id(url)
                        if video_id and video_id not in self.state["videos"]:
                            self.state["videos"][video_id] = {
                                "url": url,
                                "title": "Manual Processing Required",
                                "status": "FAILED_DOWNLOAD",
                                "audio_file_path": f"audio_files/{video_id}.mp3",
                                "transcript_file_path": f"transcripts/{video_id}.txt",
                                "created": datetime.now().isoformat(),
                                "last_updated": datetime.now().isoformat(),
                                "source": "manual_processing_needed.json"
                            }
                            imported_count += 1
        
        # Import from missing_transcripts.json
        if os.path.exists("missing_transcripts.json"):
            with open("missing_transcripts.json", 'r') as f:
                missing = json.load(f)
                for item in missing:
                    if isinstance(item, dict) and "url" in item:
                        url = item["url"]
                        video_id = self.extract_video_id(url)
                        if video_id and video_id not in self.state["videos"]:
                            self.state["videos"][video_id] = {
                                "url": url,
                                "title": item.get("title", "Unknown Title"),
                                "status": "FAILED_DOWNLOAD",
                                "audio_file_path": f"audio_files/{video_id}.mp3",
                                "transcript_file_path": f"transcripts/{video_id}.txt",
                                "created": datetime.now().isoformat(),
                                "last_updated": datetime.now().isoformat(),
                                "source": "missing_transcripts.json"
                            }
                            imported_count += 1
        
        print(f" Imported {imported_count} videos into clean tracking system")
        self.save_state()
    
    def scan_existing_files(self):
        """Scan existing audio and transcript files to update status"""
        print(" Scanning existing files to update status...")
        
        updated_count = 0
        
        for video_id, video_info in self.state["videos"].items():
            old_status = video_info["status"]
            new_status = self.determine_status(video_id)
            
            if old_status != new_status:
                video_info["status"] = new_status
                video_info["last_updated"] = datetime.now().isoformat()
                updated_count += 1
                print(f" {video_id}: {old_status} → {new_status}")
        
        print(f" Updated status for {updated_count} videos")
        self.save_state()
    
    def determine_status(self, video_id: str) -> str:
        """Determine current status based on files that exist"""
        audio_file = self.audio_dir / f"{video_id}.mp3"
        transcript_file = self.transcript_dir / f"{video_id}.txt"
        
        # Check for real audio file (not dummy)
        has_real_audio = False
        if audio_file.exists():
            file_size = audio_file.stat().st_size
            has_real_audio = file_size > 50000  # More than 50KB = real audio
        
        # Check for real transcript (not error message)
        has_real_transcript = False
        if transcript_file.exists():
            try:
                with open(transcript_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    has_real_transcript = (
                        len(content) > 1000 and 
                        "DOWNLOAD FAILED" not in content and
                        "This transcript is a placeholder" not in content
                    )
            except:
                has_real_transcript = False
        
        # Determine status
        if has_real_audio and has_real_transcript:
            return "COMPLETED"
        elif has_real_audio and not has_real_transcript:
            return "HAVE_AUDIO_NO_TRANSCRIPT"
        else:
            return "FAILED_DOWNLOAD"
    
    def cleanup_dummy_files(self):
        """Remove all dummy files and error files"""
        print("🧹 Cleaning up dummy files and error files...")
        
        cleaned_audio = 0
        cleaned_transcripts = 0
        cleaned_notes = 0
        
        # Remove dummy audio files (< 50KB)
        for audio_file in self.audio_dir.glob("*.mp3"):
            if audio_file.stat().st_size <= 50000:
                print(f"🗑️  Removing dummy audio: {audio_file.name}")
                audio_file.unlink()
                cleaned_audio += 1
        
        # Remove error transcript files
        for transcript_file in self.transcript_dir.glob("*.txt"):
            try:
                with open(transcript_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "DOWNLOAD FAILED" in content or "This transcript is a placeholder" in content:
                        print(f"🗑️  Removing error transcript: {transcript_file.name}")
                        transcript_file.unlink()
                        cleaned_transcripts += 1
            except:
                pass
        
        # Remove .note.txt files
        for note_file in self.audio_dir.glob("*.note.txt"):
            print(f"🗑️  Removing note file: {note_file.name}")
            note_file.unlink()
            cleaned_notes += 1
        
        print(f" Cleanup complete:")
        print(f"   🗑️  Dummy audio files: {cleaned_audio}")
        print(f"   🗑️  Error transcripts: {cleaned_transcripts}")
        print(f"   🗑️  Note files: {cleaned_notes}")
        
        # Update status for all videos after cleanup
        self.scan_existing_files()
    
    def show_status(self):
        """Show current status summary"""
        meta = self.state["metadata"]
        
        print("\n📊 CLEAN VIDEO TRACKER STATUS")
        print("=" * 50)
        print(f"📹 Total Videos: {meta['total_videos']}")
        print(f" Completed: {meta['completed']}")
        print(f"❌ Failed Downloads: {meta['failed_downloads']}")
        print(f"🎵 Pending Transcripts: {meta['pending_transcripts']}")
        
        if meta['total_videos'] > 0:
            progress = (meta['completed'] / meta['total_videos']) * 100
            print(f"🎯 Progress: {progress:.1f}%")
        
        print(f"\n📅 Last Updated: {meta.get('last_updated', 'Never')}")
    
    def list_videos_by_status(self, status: str, limit: int = 10):
        """List videos with specific status"""
        matching = [
            (vid, info) for vid, info in self.state["videos"].items()
            if info["status"] == status
        ]
        
        status_names = {
            "FAILED_DOWNLOAD": "❌ Need Manual Download",
            "HAVE_AUDIO_NO_TRANSCRIPT": "🎵 Need Transcript Processing",
            "COMPLETED": " Completed Successfully"
        }
        
        print(f"\n{status_names.get(status, status)}")
        print("=" * 50)
        
        if not matching:
            print(" No videos with this status")
            return
        
        for i, (video_id, info) in enumerate(matching[:limit]):
            title = info.get("title", "Unknown")[:60]
            print(f"{i+1:2d}. {video_id} - {title}")
            if status == "FAILED_DOWNLOAD":
                print(f"    📥 URL: {info['url']}")
                print(f"    💾 Save as: {info['audio_file_path']}")
        
        if len(matching) > limit:
            print(f"... and {len(matching) - limit} more")
    
    def export_download_list(self, filename: str = "clean_download_list.txt"):
        """Export download list without dummy files"""
        failed_videos = [
            (vid, info) for vid, info in self.state["videos"].items()
            if info["status"] == "FAILED_DOWNLOAD"
        ]
        
        with open(filename, 'w') as f:
            f.write("# Clean Video Download List\n")
            f.write("# No dummy files - just real tracking!\n")
            f.write("# Format: VIDEO_ID | URL | SAVE_AS\n\n")
            
            for video_id, info in failed_videos:
                title = info.get("title", "Unknown")[:40]
                f.write(f"{video_id} | {info['url']} | audio_files/{video_id}.mp3 | {title}\n")
        
        print(f"📋 Clean download list exported: {filename} ({len(failed_videos)} videos)")
    
    def process_transcripts(self, video_ids: List[str] = None):
        """Process transcripts for videos that have audio but no transcript"""
        if video_ids is None:
            video_ids = [
                vid for vid, info in self.state["videos"].items()
                if info["status"] == "HAVE_AUDIO_NO_TRANSCRIPT"
            ]
        
        if not video_ids:
            print(" No videos need transcript processing")
            return
        
        print(f"🎤 Processing transcripts for {len(video_ids)} videos...")
        
        # Load Whisper model (using centralized config)
        try:
            from pipeline_config import WHISPER_MODEL
            model = whisper.load_model(WHISPER_MODEL)
            print(f" Whisper model '{WHISPER_MODEL}' loaded")
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
                
                # Update state
                self.state["videos"][video_id]["status"] = "COMPLETED"
                self.state["videos"][video_id]["last_updated"] = datetime.now().isoformat()
                
                char_count = len(result['text'])
                print(f" Transcript saved: {char_count} characters")
                successful += 1
                
            except Exception as e:
                print(f"❌ Transcription failed: {e}")
                failed += 1
        
        self.save_state()
        print(f"\n📊 Transcript processing complete: {successful} successful, {failed} failed")

def main():
    tracker = CleanVideoTracker()
    
    if len(sys.argv) == 1:
        tracker.show_status()
        return
    
    command = sys.argv[1]
    
    if command == "--import":
        tracker.import_failed_videos()
        tracker.show_status()
    
    elif command == "--scan":
        tracker.scan_existing_files()
        tracker.show_status()
    
    elif command == "--cleanup":
        tracker.cleanup_dummy_files()
    
    elif command == "--status":
        tracker.show_status()
    
    elif command == "--failed":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        tracker.list_videos_by_status("FAILED_DOWNLOAD", limit)
    
    elif command == "--need-transcript":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        tracker.list_videos_by_status("HAVE_AUDIO_NO_TRANSCRIPT", limit)
    
    elif command == "--completed":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        tracker.list_videos_by_status("COMPLETED", limit)
    
    elif command == "--export":
        filename = sys.argv[2] if len(sys.argv) > 2 else "clean_download_list.txt"
        tracker.export_download_list(filename)
    
    elif command == "--process-transcripts":
        if len(sys.argv) > 2:
            video_ids = sys.argv[2:]
            tracker.process_transcripts(video_ids)
        else:
            tracker.process_transcripts()
    
    else:
        print("""
🧹 Clean Video Tracker - No Dummy Files!

Usage:
  python3 clean_video_tracker.py [command]

Commands:
  --import              Import videos from old tracking files
  --scan                Scan existing files and update status
  --cleanup             Remove ALL dummy files and error files
  --status              Show status summary
  --failed [limit]      Show videos needing download
  --need-transcript [limit]  Show videos needing transcripts
  --completed [limit]   Show completed videos
  --export [file]       Export clean download list
  --process-transcripts Process transcripts for pending videos

Examples:
  python3 clean_video_tracker.py --import
  python3 clean_video_tracker.py --cleanup
  python3 clean_video_tracker.py --failed 20
""")

if __name__ == "__main__":
    main() 