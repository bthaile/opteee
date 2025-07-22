#!/usr/bin/env python3
"""
Find Audio Files - Locate and organize audio files for transcription

This script will:
1. Search for audio files in various locations
2. Move them to the correct audio_files/ directory
3. Show which videos have audio available for transcription
4. Help prepare for the complete timestamp fix

Usage:
    python3 find_audio_files.py
"""

import os
import glob
import shutil
from pathlib import Path

def find_audio_files():
    """
    Search for audio files in common locations
    """
    print(" Searching for audio files...")
    
    # Common audio file extensions
    audio_extensions = ['.mp3', '.wav', '.m4a', '.mp4', '.mkv', '.webm']
    
    # Search locations
    search_locations = [
        '.',  # Current directory
        'audio_files_processed/',
        'Downloads/',
        '~/Downloads/',
        'audio/',
        'audio_files/',
    ]
    
    found_files = []
    
    for location in search_locations:
        # Expand ~ for home directory
        location = os.path.expanduser(location)
        
        if not os.path.exists(location):
            continue
            
        print(f"📂 Searching in: {location}")
        
        for ext in audio_extensions:
            pattern = os.path.join(location, f"*{ext}")
            files = glob.glob(pattern)
            
            for file in files:
                # Check if it looks like a YouTube video ID
                filename = os.path.basename(file)
                name_without_ext = os.path.splitext(filename)[0]
                
                # YouTube video IDs are typically 11 characters
                if len(name_without_ext) == 11 and name_without_ext.replace('-', '').replace('_', '').isalnum():
                    found_files.append(file)
                    print(f"   Found: {file}")
                elif any(char in name_without_ext for char in ['youtube', 'video', 'outlier']):
                    found_files.append(file)
                    print(f"   Found: {file}")
    
    return found_files

def organize_audio_files(found_files):
    """
    Move audio files to the correct location
    """
    if not found_files:
        print("❌ No audio files found")
        return 0
    
    print(f"\n📁 Organizing {len(found_files)} audio files...")
    
    # Ensure audio_files directory exists
    audio_dir = "audio_files"
    os.makedirs(audio_dir, exist_ok=True)
    
    moved_count = 0
    
    for file_path in found_files:
        try:
            filename = os.path.basename(file_path)
            name_without_ext = os.path.splitext(filename)[0]
            
            # Convert to .mp3 extension for consistency
            new_filename = f"{name_without_ext}.mp3"
            destination = os.path.join(audio_dir, new_filename)
            
            # Don't move if it's already in the right place
            if os.path.abspath(file_path) == os.path.abspath(destination):
                print(f"   Already in place: {new_filename}")
                continue
            
            # Don't overwrite existing files
            if os.path.exists(destination):
                print(f"  ⚠️  File already exists: {new_filename}")
                continue
            
            # Move the file
            shutil.move(file_path, destination)
            print(f"  📁 Moved: {filename} → {new_filename}")
            moved_count += 1
            
        except Exception as e:
            print(f"  ❌ Error moving {file_path}: {e}")
    
    return moved_count

def check_current_audio_status():
    """
    Check what audio files are currently available
    """
    print("\n📊 Current Audio Status:")
    
    audio_files = glob.glob("audio_files/*.mp3")
    note_files = glob.glob("audio_files/*.note.txt")
    
    print(f"  🎵 Audio files available: {len(audio_files)}")
    print(f"   Note files (failed downloads): {len(note_files)}")
    
    if audio_files:
        print("\n🎵 Available audio files:")
        for file in audio_files[:10]:  # Show first 10
            video_id = os.path.basename(file).replace('.mp3', '')
            print(f"  - {video_id}")
        if len(audio_files) > 10:
            print(f"  ... and {len(audio_files) - 10} more")
    
    if note_files:
        print("\n Failed downloads (need manual download):")
        for file in note_files[:5]:  # Show first 5
            video_id = os.path.basename(file).replace('.note.txt', '')
            print(f"  - {video_id}")
        if len(note_files) > 5:
            print(f"  ... and {len(note_files) - 5} more")
    
    return len(audio_files)

def show_next_steps(audio_count):
    """
    Show next steps based on current situation
    """
    print(f"\n🎯 Next Steps:")
    
    if audio_count > 0:
        print(f" You have {audio_count} audio files ready for transcription!")
        print("\n📋 To get exact timestamps, run:")
        print("   python3 fix_timestamp_issue.py")
        print("\n Or to transcribe new/missing files only:")
        print("   python3 whisper_transcribe.py")
    else:
        print("❌ No audio files found.")
        print("\n📥 To get audio files, you can:")
        print("   1. Run the downloader: python3 whisper_focused_downloader.py")
        print("   2. Manually download using: python3 generate_tracker_page.py")
        print("   3. Move audio files from other locations to audio_files/")
    
    print("\n📚 After transcription, the system will:")
    print("    Generate transcripts with exact timestamps")
    print("    Process chunks with proper timestamp metadata") 
    print("    Rebuild vector store with correct video links")
    print("    Enable precise video navigation")

def main():
    """
    Main function to find and organize audio files
    """
    print("🎵 Audio File Finder & Organizer")
    print("="*50)
    
    # Step 1: Find audio files
    found_files = find_audio_files()
    
    # Step 2: Organize them
    moved_count = organize_audio_files(found_files)
    
    # Step 3: Check current status
    audio_count = check_current_audio_status()
    
    # Step 4: Show next steps
    show_next_steps(audio_count)
    
    print(f"\n🎉 Audio file organization complete!")
    if moved_count > 0:
        print(f"📁 Moved {moved_count} files to audio_files/")

if __name__ == "__main__":
    main() 