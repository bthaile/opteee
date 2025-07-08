#!/usr/bin/env python3
"""
Generate YouTube URLs from failed video IDs for manual download
"""

import os
import glob

def generate_urls_from_note_files():
    """Generate YouTube URLs from .note.txt files"""
    
    print("🔗 Generating YouTube URLs from failed downloads...")
    print("="*70)
    
    # Get all .note.txt files
    note_files = glob.glob("audio_files/*.note.txt")
    
    if not note_files:
        print("❌ No .note.txt files found in audio_files/")
        return
    
    print(f"📋 Found {len(note_files)} failed downloads")
    print()
    
    # Generate URLs
    urls = []
    for note_file in sorted(note_files):
        # Extract video ID from filename
        video_id = os.path.basename(note_file).replace('.note.txt', '')
        url = f"https://www.youtube.com/watch?v={video_id}"
        urls.append(url)
        print(f"• {video_id} → {url}")
    
    print()
    print("="*70)
    print(f"✅ Generated {len(urls)} YouTube URLs")
    
    # Save to file
    with open("failed_video_urls.txt", "w") as f:
        f.write("# YouTube URLs for Manual Download\n")
        f.write(f"# Generated from {len(note_files)} failed downloads\n")
        f.write("# Copy and paste these URLs into your download tool\n\n")
        
        for url in urls:
            f.write(url + "\n")
    
    print(f"📁 Saved all URLs to: failed_video_urls.txt")
    print()
    print("🛠️ NEXT STEPS:")
    print("1. Copy URLs from failed_video_urls.txt")
    print("2. Download audio files using yt-dlp or online tools")
    print("3. Save as: audio_files/{VIDEO_ID}.mp3")
    print("4. Run: python3 run_pipeline.py --step transcripts")

if __name__ == "__main__":
    generate_urls_from_note_files() 