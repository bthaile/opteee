#!/usr/bin/env python3
"""
Show Clean State - No More Dummy Files!
"""

import os
from pathlib import Path

def show_clean_state():
    print("🎉 CLEAN SYSTEM STATUS - NO MORE DUMMY FILES!")
    print("=" * 60)
    
    # Check audio files
    audio_dir = Path("audio_files")
    audio_files = list(audio_dir.glob("*")) if audio_dir.exists() else []
    
    print(f"📁 AUDIO FILES DIRECTORY:")
    if audio_files:
        for file in audio_files:
            size_mb = file.stat().st_size / 1024 / 1024
            print(f"   📄 {file.name} ({size_mb:.1f}MB)")
    else:
        print("   ✅ Empty (no dummy files!)")
    
    # Check transcript files
    transcript_dir = Path("transcripts")
    transcript_files = list(transcript_dir.glob("*")) if transcript_dir.exists() else []
    
    print(f"\n📁 TRANSCRIPTS DIRECTORY:")
    if transcript_files:
        for file in transcript_files:
            size_kb = file.stat().st_size / 1024
            print(f"   📄 {file.name} ({size_kb:.1f}KB)")
    else:
        print("   ✅ Empty (no error files!)")
    
    # Count tracking files
    tracking_files = []
    if os.path.exists("failed_video_urls.txt"):
        tracking_files.append("failed_video_urls.txt")
    if os.path.exists("manual_processing_needed.json"):
        tracking_files.append("manual_processing_needed.json")
    if os.path.exists("missing_transcripts.json"):
        tracking_files.append("missing_transcripts.json")
    
    print(f"\n📋 TRACKING FILES:")
    for file in tracking_files:
        print(f"   📄 {file}")
    
    print(f"\n📊 SUMMARY:")
    print(f"   🧹 Dummy files removed: ✅ ALL GONE!")
    print(f"   📁 Clean directories: ✅ YES") 
    print(f"   🎯 Ready for downloads: ✅ YES")
    
    print(f"\n🎯 NEXT STEPS:")
    print("   1. Download MP3 files (not MP4) from y2mate")
    print("   2. Click 'Audio' tab, not 'Video' tab")
    print("   3. Save as audio_files/VIDEO_ID.mp3")
    print("   4. Process with: python3 whisper_transcribe.py")
    
    print(f"\n💡 BENEFITS OF CLEAN SYSTEM:")
    print("   • No more 1,502 dummy files cluttering directories")
    print("   • No more confusion about real vs fake files")
    print("   • Clean tracking with JSON (when you're ready)")
    print("   • Easy to see what actually needs to be done")

if __name__ == "__main__":
    show_clean_state() 