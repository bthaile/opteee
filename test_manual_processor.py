#!/usr/bin/env python3

import json
import os
from pathlib import Path

def test_basic_functionality():
    print(" Testing manual video processor...")
    
    # Check if tracking files exist
    files_to_check = [
        "failed_video_urls.txt",
        "manual_processing_needed.json", 
        "missing_transcripts.json"
    ]
    
    print("\n📁 Checking tracking files:")
    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f" {file} - {size} bytes")
        else:
            print(f"❌ {file} - not found")
    
    # Check audio_files directory
    audio_dir = Path("audio_files")
    if audio_dir.exists():
        mp3_files = list(audio_dir.glob("*.mp3"))
        mp4_files = list(audio_dir.glob("*.mp4"))
        print(f"\n🎵 audio_files directory:")
        print(f"   MP3 files: {len(mp3_files)}")
        print(f"   MP4 files: {len(mp4_files)}")
        
        # Show first few files
        if mp3_files:
            print("   Sample MP3 files:")
            for file in mp3_files[:5]:
                size_kb = file.stat().st_size // 1024
                status = "real" if size_kb > 50 else "dummy"
                print(f"     {file.name} - {size_kb}KB ({status})")
    else:
        print("❌ audio_files directory not found")
    
    # Check transcripts directory
    transcript_dir = Path("transcripts")
    if transcript_dir.exists():
        txt_files = list(transcript_dir.glob("*.txt"))
        print(f"\n📄 transcripts directory:")
        print(f"   TXT files: {len(txt_files)}")
    else:
        print("❌ transcripts directory not found")

if __name__ == "__main__":
    test_basic_functionality() 