#!/usr/bin/env python3
"""
Fix Timestamp Issue - Regenerate transcripts with proper timestamps

This script will:
1. Re-transcribe audio files using Whisper with timestamps
2. Save transcripts in the correct format (XX.XXs: content)
3. Reprocess chunks with proper timestamps
4. Rebuild the vector store with correct timestamps

Usage:
    python3 fix_timestamp_issue.py [--parallel] [--workers N]
    
Options:
    --parallel: Enable parallel processing (default: sequential)
    --workers N: Number of parallel workers (default: CPU count)
"""

import os
import json
import whisper
import subprocess
import multiprocessing
import argparse
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import glob
from pathlib import Path

def transcribe_single_file(audio_file_path):
    """
    Transcribe a single audio file with Whisper
    This function will be run in parallel processes
    """
    try:
        # Each process loads its own model to avoid sharing issues
        model = whisper.load_model("tiny")
        
        video_id = os.path.basename(audio_file_path).replace('.mp3', '')
        output_file = f"transcripts/{video_id}.txt"
        
        # Skip if already exists
        if os.path.exists(output_file):
            return {"success": True, "video_id": video_id, "message": "Already exists", "skipped": True}
        
        # Transcribe with Whisper
        result = model.transcribe(audio_file_path)
        
        # Save transcript with timestamps in correct format
        os.makedirs("transcripts", exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            for segment in result["segments"]:
                start_time = segment["start"]
                text = segment["text"].strip()
                if text:  # Only write non-empty segments
                    f.write(f"{start_time:.2f}s: {text}\n")
        
        return {"success": True, "video_id": video_id, "message": "Transcribed successfully", "skipped": False}
        
    except Exception as e:
        return {"success": False, "video_id": video_id, "message": str(e), "skipped": False}

def regenerate_transcripts_with_timestamps(use_parallel=False, num_workers=None):
    """
    Regenerate transcript files with proper timestamps
    """
    print("🔧 Regenerating transcripts with proper timestamps...")
    
    # Find all audio files
    audio_files = glob.glob("audio_files/*.mp3")
    
    if not audio_files:
        print("❌ No audio files found in audio_files/ directory")
        return False
    
    print(f"📁 Found {len(audio_files)} audio files")
    
    if use_parallel:
        # Parallel processing
        if num_workers is None:
            num_workers = min(multiprocessing.cpu_count(), len(audio_files))
        
        print(f"🚀 Using parallel processing with {num_workers} workers")
        
        # Process files in parallel
        successful = 0
        failed = 0
        skipped = 0
        
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            # Submit all tasks
            future_to_file = {executor.submit(transcribe_single_file, audio_file): audio_file 
                              for audio_file in audio_files}
            
            # Process results as they complete
            for future in tqdm(as_completed(future_to_file), total=len(audio_files), desc="Processing"):
                audio_file = future_to_file[future]
                try:
                    result = future.result()
                    if result["success"]:
                        if result["skipped"]:
                            skipped += 1
                        else:
                            successful += 1
                        print(f"✅ {result['video_id']}: {result['message']}")
                    else:
                        failed += 1
                        print(f"❌ {result['video_id']}: {result['message']}")
                except Exception as e:
                    failed += 1
                    print(f"❌ {os.path.basename(audio_file)}: {str(e)}")
                    
    else:
        # Sequential processing (original method)
        print("🐌 Using sequential processing (use --parallel for speed)")
        
        # Load Whisper model once for sequential processing
        print("📥 Loading Whisper model...")
        model = whisper.load_model("tiny")
        
        successful = 0
        failed = 0
        skipped = 0
        
        # Process each audio file
        for audio_file in tqdm(audio_files, desc="Processing audio files"):
            video_id = os.path.basename(audio_file).replace('.mp3', '')
            output_file = f"transcripts/{video_id}.txt"
            
            # Skip if already exists
            if os.path.exists(output_file):
                skipped += 1
                continue
            
            print(f"🎤 Transcribing {video_id}...")
            
            try:
                # Transcribe with Whisper
                result = model.transcribe(audio_file)
                
                # Save transcript with timestamps in correct format
                with open(output_file, 'w', encoding='utf-8') as f:
                    for segment in result["segments"]:
                        start_time = segment["start"]
                        text = segment["text"].strip()
                        if text:  # Only write non-empty segments
                            f.write(f"{start_time:.2f}s: {text}\n")
                
                print(f"✅ Saved {output_file}")
                successful += 1
                
            except Exception as e:
                print(f"❌ Error processing {audio_file}: {e}")
                failed += 1
                continue
    
    # Summary
    print(f"\n📊 Processing Summary:")
    print(f"  ✅ Successful: {successful}")
    print(f"  ⏭️  Skipped: {skipped}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📁 Total: {len(audio_files)}")
    
    print("✅ Transcript regeneration complete!")
    return True

def reprocess_chunks():
    """
    Reprocess transcripts into chunks with proper timestamps
    """
    print("🔄 Reprocessing transcripts into chunks...")
    
    try:
        # Run the preprocessing script
        result = subprocess.run(
            ["python3", "preprocess_transcripts.py"],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Chunk processing complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during chunk processing: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def rebuild_vector_store():
    """
    Rebuild the vector store with corrected timestamps
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
            timestamps[ts] = timestamps.get(ts, 0) + 1
        
        print(f"📊 Results:")
        print(f"  Total chunks: {len(metadata)}")
        print(f"  Unique timestamps: {len(timestamps)}")
        print(f"  Chunks with timestamp 0: {timestamps.get(0, 0)}")
        print(f"  Chunks with non-zero timestamps: {len(metadata) - timestamps.get(0, 0)}")
        
        # Show some examples
        non_zero_examples = [
            entry for entry in metadata[:10] 
            if entry.get('start_timestamp_seconds', 0) > 0
        ]
        
        if non_zero_examples:
            print(f"\n✅ Success! Found {len(non_zero_examples)} examples with proper timestamps:")
            for i, entry in enumerate(non_zero_examples[:3]):
                print(f"  {i+1}. {entry['title'][:50]}...")
                print(f"     Timestamp: {entry['start_timestamp_seconds']}s")
                print(f"     URL: {entry['video_url_with_timestamp']}")
        else:
            print("❌ Still no proper timestamps found")
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")

def main():
    """
    Main function to fix the timestamp issue
    """
    parser = argparse.ArgumentParser(description='Fix timestamp issue with parallel processing support')
    parser.add_argument('--parallel', action='store_true', help='Enable parallel processing')
    parser.add_argument('--workers', type=int, help='Number of parallel workers (default: CPU count)')
    
    args = parser.parse_args()
    
    print("🚀 Starting timestamp fix process...")
    print("="*60)
    
    # Step 1: Regenerate transcripts with timestamps
    if not regenerate_transcripts_with_timestamps(use_parallel=args.parallel, num_workers=args.workers):
        print("❌ Failed to regenerate transcripts. Exiting.")
        return
    
    # Step 2: Reprocess chunks
    if not reprocess_chunks():
        print("❌ Failed to reprocess chunks. Exiting.")
        return
    
    # Step 3: Rebuild vector store
    if not rebuild_vector_store():
        print("❌ Failed to rebuild vector store. Exiting.")
        return
    
    # Step 4: Verify the fix
    verify_fix()
    
    print("\n🎉 Timestamp fix process complete!")
    print("🔗 Video links should now point to the correct timestamps!")

if __name__ == "__main__":
    main() 