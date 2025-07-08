#!/usr/bin/env python3
"""
MP4 to MP3 Converter

Converts MP4 video files to MP3 audio files for transcript processing.
Useful when you accidentally download video files instead of audio files.
"""

import os
import sys
import subprocess
from pathlib import Path
import glob

def convert_mp4_to_mp3(mp4_file: Path, mp3_file: Path) -> bool:
    """Convert a single MP4 file to MP3"""
    try:
        cmd = [
            'ffmpeg', '-i', str(mp4_file),
            '-vn',  # No video
            '-acodec', 'mp3',
            '-ab', '128k',  # Audio bitrate
            '-y',  # Overwrite output file
            str(mp3_file)
        ]
        
        # Run conversion
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Converted: {mp4_file.name} → {mp3_file.name}")
            return True
        else:
            print(f"❌ Failed to convert {mp4_file.name}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error converting {mp4_file.name}: {e}")
        return False

def find_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def main():
    if not find_ffmpeg():
        print("❌ ffmpeg not found. Please install ffmpeg first:")
        print("   brew install ffmpeg  (on macOS)")
        print("   sudo apt install ffmpeg  (on Ubuntu/Debian)")
        return
    
    audio_dir = Path("audio_files")
    if not audio_dir.exists():
        print("❌ audio_files directory not found")
        return
    
    # Find all MP4 files in audio_files directory
    mp4_files = list(audio_dir.glob("*.mp4"))
    
    if not mp4_files:
        print("✅ No MP4 files found in audio_files directory")
        return
    
    print(f"🎬 Found {len(mp4_files)} MP4 files to convert")
    
    converted = 0
    failed = 0
    
    for mp4_file in mp4_files:
        # Create corresponding MP3 filename
        mp3_file = mp4_file.with_suffix('.mp3')
        
        print(f"\n🔄 Converting: {mp4_file.name}")
        
        if convert_mp4_to_mp3(mp4_file, mp3_file):
            converted += 1
            
            # Remove the original MP4 file
            try:
                mp4_file.unlink()
                print(f"🗑️  Removed original: {mp4_file.name}")
            except Exception as e:
                print(f"⚠️  Could not remove {mp4_file.name}: {e}")
        else:
            failed += 1
    
    print(f"\n📊 Conversion complete:")
    print(f"   ✅ Converted: {converted} files")
    print(f"   ❌ Failed: {failed} files")
    
    if converted > 0:
        print(f"\n🎵 Ready to process transcripts! Run:")
        print(f"   python3 manual_video_processor.py --process-transcripts")

if __name__ == "__main__":
    main() 