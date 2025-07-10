#!/usr/bin/env python3
"""
Quick Timestamp Fix - Estimate timestamps based on text position

This script provides a faster alternative that:
1. Estimates timestamps based on chunk position in the transcript
2. Uses video duration metadata to calculate proportional timestamps
3. Updates existing processed chunks with estimated timestamps
4. Rebuilds the vector store with estimated timestamps

Usage:
    python3 quick_timestamp_fix.py
"""

import os
import json
import pickle
import subprocess
from tqdm import tqdm
import glob

def load_video_metadata():
    """Load video metadata to get durations"""
    try:
        with open('outlier_trading_videos_metadata.json', 'r') as f:
            return json.load(f)
    except:
        try:
            with open('outlier_trading_videos.json', 'r') as f:
                return json.load(f)
        except:
            print("❌ No video metadata found")
            return {}

def estimate_timestamps_for_chunks():
    """
    Estimate timestamps for existing chunks based on position and video duration
    """
    print("🔧 Estimating timestamps for existing chunks...")
    
    # Load video metadata
    video_metadata = load_video_metadata()
    metadata_by_id = {video.get('id', ''): video for video in video_metadata}
    
    # Find all processed transcript files
    processed_files = glob.glob("processed_transcripts/*.json")
    
    if not processed_files:
        print("❌ No processed transcript files found")
        return False
    
    updated_files = 0
    
    for file_path in tqdm(processed_files, desc="Updating chunks"):
        try:
            # Extract video ID from filename
            video_id = os.path.basename(file_path).replace('_processed.json', '')
            
            # Load the chunks
            with open(file_path, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            
            if not chunks:
                continue
            
            # Get video duration
            video_info = metadata_by_id.get(video_id, {})
            duration = video_info.get('duration', 0)
            
            # If we don't have duration, estimate from content length
            if not duration:
                # Estimate ~150 words per minute of speech
                total_words = sum(len(chunk['text'].split()) for chunk in chunks)
                duration = (total_words / 150) * 60  # Convert to seconds
            
            # Update chunks with estimated timestamps
            total_chunks = len(chunks)
            for i, chunk in enumerate(chunks):
                # Estimate timestamp based on position in the transcript
                estimated_seconds = (i / total_chunks) * duration if total_chunks > 1 else 0
                
                # Update the metadata
                chunk['metadata']['start_timestamp_seconds'] = estimated_seconds
                chunk['metadata']['start_timestamp'] = format_timestamp(estimated_seconds)
                
                # Update the URL with timestamp
                video_url_base = chunk['metadata'].get('url', f"https://www.youtube.com/watch?v={video_id}")
                if '&t=' in video_url_base:
                    video_url_base = video_url_base.split('&t=')[0]
                
                chunk['metadata']['video_url_with_timestamp'] = f"{video_url_base}&t={int(estimated_seconds)}"
            
            # Save the updated chunks
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2)
            
            updated_files += 1
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            continue
    
    print(f"✅ Updated {updated_files} files with estimated timestamps")
    return updated_files > 0

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def rebuild_vector_store():
    """
    Rebuild the vector store with estimated timestamps
    """
    print("🔨 Rebuilding vector store...")
    
    try:
        # Remove old vector store
        if os.path.exists("vector_store"):
            import shutil
            shutil.rmtree("vector_store")
        
        # Rebuild vector store
        result = subprocess.run(
            ["python3", "create_vector_store.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Vector store rebuild complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during vector store rebuild: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def verify_fix():
    """
    Verify that the fix worked by checking some timestamps
    """
    print("🔍 Verifying timestamp fix...")
    
    try:
        import pickle
        with open('vector_store/transcript_metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
        
        # Check timestamp distribution
        timestamps = {}
        for entry in metadata:
            ts = entry.get('start_timestamp_seconds', 0)
            ts_rounded = int(ts / 10) * 10  # Group by 10-second intervals
            timestamps[ts_rounded] = timestamps.get(ts_rounded, 0) + 1
        
        print(f"📊 Results:")
        print(f"  Total chunks: {len(metadata)}")
        print(f"  Chunks with timestamp 0: {sum(1 for e in metadata if e.get('start_timestamp_seconds', 0) == 0)}")
        print(f"  Chunks with non-zero timestamps: {sum(1 for e in metadata if e.get('start_timestamp_seconds', 0) > 0)}")
        print(f"  Timestamp distribution (10s intervals): {len(timestamps)} intervals")
        
        # Show some examples
        non_zero_examples = [
            entry for entry in metadata 
            if entry.get('start_timestamp_seconds', 0) > 0
        ][:5]
        
        if non_zero_examples:
            print(f"\n✅ Success! Examples with estimated timestamps:")
            for i, entry in enumerate(non_zero_examples):
                print(f"  {i+1}. {entry['title'][:50]}...")
                print(f"     Timestamp: {entry['start_timestamp_seconds']:.1f}s ({entry['start_timestamp']})")
                print(f"     URL: {entry['video_url_with_timestamp']}")
        else:
            print("❌ Still no proper timestamps found")
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")

def main():
    """
    Main function for quick timestamp fix
    """
    print("🚀 Starting quick timestamp fix...")
    print("="*60)
    print("ℹ️  This creates estimated timestamps based on chunk position.")
    print("ℹ️  For exact timestamps, use fix_timestamp_issue.py instead.")
    print("="*60)
    
    # Step 1: Estimate timestamps for existing chunks
    if not estimate_timestamps_for_chunks():
        print("❌ Failed to estimate timestamps. Exiting.")
        return
    
    # Step 2: Rebuild vector store
    if not rebuild_vector_store():
        print("❌ Failed to rebuild vector store. Exiting.")
        return
    
    # Step 3: Verify the fix
    verify_fix()
    
    print("\n🎉 Quick timestamp fix complete!")
    print("📍 Video links now point to estimated timestamps!")
    print("💡 Note: These are estimated positions, not exact timestamps.")

if __name__ == "__main__":
    main() 