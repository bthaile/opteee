#!/usr/bin/env python3
"""
Organize processed audio files by moving them to a separate directory.
Only moves audio files that have corresponding transcripts.
"""

import os
import shutil
import json
from pathlib import Path

def load_video_metadata():
    """Load video metadata from JSON file"""
    if os.path.exists("outlier_trading_videos_metadata.json"):
        with open("outlier_trading_videos_metadata.json", 'r') as f:
            return json.load(f)
    return {}

def get_video_title(video_id, metadata):
    """Get video title from metadata"""
    for video in metadata:
        if video.get('video_id') == video_id:
            return video.get('title', 'Unknown Title')
    return 'Unknown Title'

def organize_processed_audio():
    """Move processed audio files to a separate directory"""
    
    # Create processed directory
    processed_dir = Path("audio_files_processed")
    processed_dir.mkdir(exist_ok=True)
    
    # Load metadata for titles
    metadata = load_video_metadata()
    
    # Get all MP3 files in audio_files
    audio_files = list(Path("audio_files").glob("*.mp3"))
    
    moved_count = 0
    skipped_count = 0
    
    print(f"🔍 Found {len(audio_files)} MP3 files in audio_files/")
    print(f"📁 Moving processed files to: {processed_dir}")
    print("="*60)
    
    for audio_file in audio_files:
        video_id = audio_file.stem  # filename without extension
        transcript_file = Path(f"transcripts/{video_id}.txt")
        
        # Check if transcript exists
        if transcript_file.exists():
            # Move the audio file
            dest_path = processed_dir / audio_file.name
            shutil.move(str(audio_file), str(dest_path))
            
            # Get video title for display
            title = get_video_title(video_id, metadata)
            title_display = title[:50] + "..." if len(title) > 50 else title
            
            print(f"✅ {video_id} - {title_display}")
            moved_count += 1
        else:
            print(f"⏸️ {video_id} - No transcript found, keeping in audio_files/")
            skipped_count += 1
    
    print("="*60)
    print(f"📊 SUMMARY:")
    print(f"✅ Moved to processed: {moved_count} files")
    print(f"⏸️ Kept in audio_files: {skipped_count} files")
    print(f"📁 Processed files location: {processed_dir}")
    
    return moved_count, skipped_count

def show_directory_status():
    """Show current status of audio directories"""
    
    audio_files = list(Path("audio_files").glob("*.mp3"))
    processed_files = list(Path("audio_files_processed").glob("*.mp3")) if Path("audio_files_processed").exists() else []
    note_files = list(Path("audio_files").glob("*.note.txt"))
    
    print("📊 AUDIO FILES DIRECTORY STATUS")
    print("="*50)
    print(f"📁 audio_files/")
    print(f"   🎵 MP3 files: {len(audio_files)}")
    print(f"   📝 Note files (failed): {len(note_files)}")
    print(f"📁 audio_files_processed/")
    print(f"   🎵 Processed MP3 files: {len(processed_files)}")
    print()
    
    if audio_files:
        print(f"💡 You have {len(audio_files)} MP3 files that can be organized")
        print("   Run: python3 organize_processed_audio.py --move")
    else:
        print("✅ All MP3 files are already organized!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--move":
        organize_processed_audio()
    else:
        show_directory_status()
        print("\n🔧 Commands:")
        print("   python3 organize_processed_audio.py        # Show status")
        print("   python3 organize_processed_audio.py --move # Move processed files") 