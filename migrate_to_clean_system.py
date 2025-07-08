#!/usr/bin/env python3
"""
Migration Script: Dummy Files → Clean JSON Tracking

This script helps you migrate from the messy dummy file system
to the clean JSON-based tracking system.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def analyze_current_mess():
    """Analyze the current state of dummy files and tracking mess"""
    print("🔍 ANALYZING CURRENT DUMMY FILE MESS...")
    print("=" * 50)
    
    audio_dir = Path("audio_files")
    transcript_dir = Path("transcripts")
    
    # Count dummy files
    dummy_audio = 0
    real_audio = 0
    note_files = 0
    
    if audio_dir.exists():
        for file in audio_dir.glob("*.mp3"):
            size = file.stat().st_size
            if size <= 50000:  # 50KB or less = dummy
                dummy_audio += 1
            else:
                real_audio += 1
        
        note_files = len(list(audio_dir.glob("*.note.txt")))
    
    # Count transcript files
    dummy_transcripts = 0
    real_transcripts = 0
    
    if transcript_dir.exists():
        for file in transcript_dir.glob("*.txt"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "DOWNLOAD FAILED" in content or "This transcript is a placeholder" in content:
                        dummy_transcripts += 1
                    else:
                        real_transcripts += 1
            except:
                dummy_transcripts += 1
    
    # Count tracking files
    tracking_files = []
    if os.path.exists("failed_video_urls.txt"):
        tracking_files.append("failed_video_urls.txt")
    if os.path.exists("manual_processing_needed.json"):
        tracking_files.append("manual_processing_needed.json")
    if os.path.exists("missing_transcripts.json"):
        tracking_files.append("missing_transcripts.json")
    
    print(f"📁 DUMMY FILE ANALYSIS:")
    print(f"   🗑️  Dummy audio files: {dummy_audio}")
    print(f"   🗑️  Dummy transcripts: {dummy_transcripts}")
    print(f"   🗑️  Error note files: {note_files}")
    print(f"   ✅  Real audio files: {real_audio}")
    print(f"   ✅  Real transcripts: {real_transcripts}")
    print(f"   📋  Tracking files: {len(tracking_files)}")
    
    total_dummy = dummy_audio + dummy_transcripts + note_files
    total_real = real_audio + real_transcripts
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total dummy/error files: {total_dummy}")
    print(f"   Total real files: {total_real}")
    print(f"   Total tracking files: {len(tracking_files)}")
    
    if total_dummy > 0:
        print(f"\n💡 You have {total_dummy} dummy files cluttering your directories!")
        print("   The clean system will eliminate ALL of these.")
    
    return {
        "dummy_audio": dummy_audio,
        "dummy_transcripts": dummy_transcripts,
        "note_files": note_files,
        "real_audio": real_audio,
        "real_transcripts": real_transcripts,
        "tracking_files": tracking_files
    }

def show_migration_plan():
    """Show what the migration will do"""
    print("\n🚀 MIGRATION PLAN: DUMMY FILES → CLEAN JSON TRACKING")
    print("=" * 60)
    
    print("📋 STEP 1: Import all tracking data into clean JSON")
    print("   • Read failed_video_urls.txt")
    print("   • Read manual_processing_needed.json")
    print("   • Read missing_transcripts.json")
    print("   • Create single video_state.json file")
    
    print("\n📋 STEP 2: Scan existing files and update status")
    print("   • Identify real audio files (>50KB)")
    print("   • Identify real transcripts (>1000 chars, no errors)")
    print("   • Update status for each video")
    
    print("\n📋 STEP 3: Clean up ALL dummy files")
    print("   • Remove dummy audio files (<50KB)")
    print("   • Remove error transcripts")
    print("   • Remove .note.txt files")
    print("   • Keep only real files")
    
    print("\n📋 STEP 4: Pure JSON tracking")
    print("   • No more dummy files")
    print("   • No more scattered tracking files")
    print("   • Single video_state.json with all info")
    print("   • Clean directories with only real files")

def show_benefits():
    """Show benefits of clean system"""
    print("\n✅ BENEFITS OF CLEAN SYSTEM:")
    print("=" * 40)
    
    print("🧹 CLEANER DIRECTORIES:")
    print("   • No more 502 dummy MP3 files")
    print("   • No more 502 .note.txt error files")
    print("   • Only real audio and transcript files")
    
    print("\n📊 BETTER TRACKING:")
    print("   • Single video_state.json file")
    print("   • Clear status for each video")
    print("   • Progress tracking and statistics")
    
    print("\n🎯 EASIER WORKFLOW:")
    print("   • Know exactly what needs to be done")
    print("   • No confusion about dummy vs real files")
    print("   • Resume processing from any point")
    
    print("\n💡 BETTER MAINTENANCE:")
    print("   • Easy to backup (one JSON file)")
    print("   • Easy to understand state")
    print("   • No file size checking needed")

def migrate_now():
    """Perform the migration"""
    print("\n🚀 PERFORMING MIGRATION...")
    print("=" * 40)
    
    # Run the clean video tracker
    os.system("python3 clean_video_tracker.py --import")
    os.system("python3 clean_video_tracker.py --scan")
    
    print("\n✅ MIGRATION COMPLETE!")
    print("Your system now uses clean JSON tracking.")
    
    # Show new status
    print("\n📊 NEW CLEAN STATUS:")
    os.system("python3 clean_video_tracker.py --status")

def main():
    print("🔄 MIGRATION ASSISTANT: DUMMY FILES → CLEAN JSON TRACKING")
    print("=" * 70)
    
    # Analyze current state
    analysis = analyze_current_mess()
    
    # Show migration plan
    show_migration_plan()
    
    # Show benefits
    show_benefits()
    
    # Ask if they want to migrate
    if analysis["dummy_audio"] > 0 or analysis["dummy_transcripts"] > 0:
        print(f"\n❓ You have {analysis['dummy_audio'] + analysis['dummy_transcripts']} dummy files.")
        print("   Would you like to migrate to the clean system now?")
        
        response = input("\n   Type 'yes' to migrate, 'no' to just analyze: ").strip().lower()
        
        if response == 'yes':
            migrate_now()
            
            print("\n🎉 MIGRATION COMPLETE!")
            print("You can now use the clean system:")
            print("   python3 clean_video_tracker.py --status")
            print("   python3 clean_video_tracker.py --failed 10")
            print("   python3 clean_video_tracker.py --cleanup")
        else:
            print("\n👍 No migration performed.")
            print("Run 'python3 clean_video_tracker.py --import' when ready.")
    else:
        print("\n✅ No dummy files found - you may already be using a clean system!")

if __name__ == "__main__":
    main() 