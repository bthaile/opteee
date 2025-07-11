#!/usr/bin/env python3
"""
Complete Pipeline Runner for Outlier Trading Video Processing

This script orchestrates the entire video processing pipeline:
1. Video discovery and metadata collection
2. Transcript retrieval (YouTube API + Whisper fallback)
3. Transcript preprocessing and chunking
4. Vector store creation

Usage:
    python3 run_pipeline.py [--step STEP_NAME] [--force-reprocess] [--non-interactive]

Options:
    --step: Run only a specific step (scrape, transcripts, preprocess, vectors)
    --force-reprocess: Force reprocessing of all videos (ignores progress)
    --non-interactive: Run without prompting for user input (useful for CI/CD)
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pipeline_config import (
    VIDEOS_JSON, METADATA_JSON, TRANSCRIPT_DIR, PROCESSED_DIR,
    CHUNK_SIZE, OVERLAP, MIN_CHUNK_WORDS, ensure_directories, validate_config
)

def print_banner(title):
    """Print a formatted banner"""
    print("\n" + "="*80)
    print(f"🚀 {title}")
    print("="*80)

def print_step(step_num, total_steps, description):
    """Print a formatted step header"""
    print(f"\n📋 Step {step_num}/{total_steps}: {description}")
    print("-" * 60)

def should_force_reprocess(directory, data_file, non_interactive=False):
    """Determine if we should force reprocessing based on new content"""
    if non_interactive:
        # In non-interactive mode, we want to process if:
        # 1. The data file is newer than the processed directory
        # 2. The processed directory is empty
        # 3. The data file doesn't exist yet (first run)
        
        if not os.path.exists(data_file):
            return True
            
        if not os.path.exists(directory):
            return True
            
        # Check if directory is empty
        files = [f for f in os.listdir(directory) if not f.startswith('.')]
        if not files:
            return True
            
        # Check if data file is newer than the directory
        data_mtime = os.path.getmtime(data_file)
        dir_mtime = max([os.path.getmtime(os.path.join(directory, f)) 
                        for f in files] + [0])
        
        return data_mtime > dir_mtime
    return False

def run_video_scraping(force=False, non_interactive=False):
    """Step 1: Scrape channel videos"""
    print_step(1, 4, "Video Discovery & Metadata Collection")
    
    # Check if we already have videos
    if os.path.exists(VIDEOS_JSON) and not force:
        with open(VIDEOS_JSON, 'r') as f:
            videos = json.load(f)
        print(f"✅ Found existing {VIDEOS_JSON} with {len(videos)} videos")
        
        if non_interactive:
            print("🤖 Non-interactive mode: Checking for new videos...")
            # In non-interactive mode, always scrape to check for new videos
            # This is lightweight and ensures we don't miss new content
        else:
            # Ask user if they want to re-scrape
            response = input("🤔 Re-scrape videos? (y/N): ").lower()
            if response != 'y':
                print("⏭️  Skipping video scraping")
                return
    
    print("🔍 Running video scraping...")
    import outlier_scraper
    print("✅ Video scraping complete")
    
    # Run metadata collection if we have a YouTube API key
    from pipeline_config import YOUTUBE_API_KEY
    if YOUTUBE_API_KEY:
        print("\n🔍 Running metadata collection...")
        import collect_video_metadata
        collect_video_metadata.main()
        print("✅ Metadata collection complete")
    else:
        print("⚠️  No YouTube API key found - using basic metadata only")

def run_transcript_processing(force=False, non_interactive=False):
    """Step 2: Process transcripts"""
    print_step(2, 4, "Transcript Generation")
    
    # Check what videos we have
    if not os.path.exists(VIDEOS_JSON):
        print("❌ No video data found. Please run video scraping first.")
        return False
    
    # Check if transcript directory exists and has files
    if os.path.exists(TRANSCRIPT_DIR) and not force:
        transcript_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith('.txt')]
        if transcript_files:
            print(f"✅ Found {len(transcript_files)} existing transcript files")
            
            if non_interactive:
                # In non-interactive mode, check if we need to process new videos
                should_reprocess = should_force_reprocess(TRANSCRIPT_DIR, VIDEOS_JSON, non_interactive)
                if should_reprocess:
                    print("🤖 Non-interactive mode: Detected new videos, processing transcripts...")
                else:
                    print("🤖 Non-interactive mode: No new videos detected, skipping transcript processing")
                    return True
            else:
                response = input("🤔 Re-process transcripts? (y/N): ").lower()
                if response != 'y':
                    print("⏭️  Skipping transcript processing")
                    return True
    
    # Load missing transcripts and process them
    print("🎯 Processing missing transcripts with Whisper...")
    import whisper_transcribe
    
    # Run the main function from whisper_transcribe
    whisper_transcribe.main()
    print("✅ Transcript processing complete")
    return True

def run_preprocessing(force=False, non_interactive=False):
    """Step 3: Preprocess transcripts into chunks"""
    print_step(3, 4, "Transcript Preprocessing & Chunking")
    
    # Check if we have transcripts
    if not os.path.exists(TRANSCRIPT_DIR):
        print("❌ No transcript directory found. Please run transcript processing first.")
        return False
    
    transcript_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith('.txt')]
    if not transcript_files:
        print("❌ No transcript files found. Please run transcript processing first.")
        return False
    
    # Check if we already have processed files
    if os.path.exists(PROCESSED_DIR) and not force:
        processed_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
        if processed_files:
            print(f"✅ Found {len(processed_files)} existing processed files")
            print(f"📊 Configuration: {CHUNK_SIZE} words/chunk, {OVERLAP} words overlap")
            
            if non_interactive:
                # In non-interactive mode, check if we need to reprocess based on newer transcripts
                should_reprocess = should_force_reprocess(PROCESSED_DIR, TRANSCRIPT_DIR, non_interactive)
                if should_reprocess:
                    print("🤖 Non-interactive mode: Detected new transcripts, reprocessing chunks...")
                else:
                    print("🤖 Non-interactive mode: No new transcripts detected, skipping preprocessing")
                    return True
            else:
                response = input("🤔 Re-process chunks? (y/N): ").lower()
                if response != 'y':
                    print("⏭️  Skipping preprocessing")
                    return True
    
    print(f"📝 Processing {len(transcript_files)} transcript files...")
    print(f"📊 Configuration: {CHUNK_SIZE} words/chunk, {OVERLAP} words overlap, min {MIN_CHUNK_WORDS} words")
    
    import preprocess_transcripts
    preprocess_transcripts.main()
    print("✅ Preprocessing complete")
    return True

def run_vector_creation(force=False, non_interactive=False):
    """Step 4: Create vector store"""
    print_step(4, 4, "Vector Store Creation")
    
    # Check if we have processed files
    if not os.path.exists(PROCESSED_DIR):
        print("❌ No processed transcript directory found. Please run preprocessing first.")
        return False
    
    processed_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
    if not processed_files:
        print("❌ No processed files found. Please run preprocessing first.")
        return False
    
    # Check if vector store already exists
    if os.path.exists('vector_store') and not force:
        print("✅ Found existing vector store")
        
        if non_interactive:
            # In non-interactive mode, check if we need to rebuild based on newer processed files
            should_rebuild = should_force_reprocess('vector_store', PROCESSED_DIR, non_interactive)
            if should_rebuild:
                print("🤖 Non-interactive mode: Detected new processed files, rebuilding vector store...")
            else:
                print("🤖 Non-interactive mode: No new processed files detected, skipping vector store creation")
                return True
        else:
            response = input("🤔 Rebuild vector store? (y/N): ").lower()
            if response != 'y':
                print("⏭️  Skipping vector store creation")
                return True
    
    print(f"🔮 Creating vector store from {len(processed_files)} processed files...")
    
    import create_vector_store
    import argparse
    
    # Create args for vector store creation
    vector_args = argparse.Namespace(
        model='all-MiniLM-L6-v2',
        batch_size=32,
        output_dir=None,  # Use default from config
        test_search=False
    )
    
    create_vector_store.main(vector_args)
    print("✅ Vector store creation complete")
    return True

def print_summary():
    """Print pipeline summary"""
    print_banner("Pipeline Summary")
    
    # Check what we have
    stats = {}
    
    if os.path.exists(VIDEOS_JSON):
        with open(VIDEOS_JSON, 'r') as f:
            videos = json.load(f)
        stats['videos'] = len(videos)
    
    if os.path.exists(TRANSCRIPT_DIR):
        transcript_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith('.txt')]
        stats['transcripts'] = len(transcript_files)
    
    if os.path.exists(PROCESSED_DIR):
        processed_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
        stats['processed_files'] = len(processed_files)
        
        # Count total chunks
        total_chunks = 0
        for filename in processed_files:
            file_path = os.path.join(PROCESSED_DIR, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_chunks += len(data) if isinstance(data, list) else 1
            except:
                pass
        stats['total_chunks'] = total_chunks
    
    vector_store_exists = os.path.exists('vector_store/index.faiss')
    stats['vector_store'] = vector_store_exists
    
    print("📊 Final Statistics:")
    print(f"  • Videos discovered: {stats.get('videos', 0)}")
    print(f"  • Transcripts generated: {stats.get('transcripts', 0)}")
    print(f"  • Processed files: {stats.get('processed_files', 0)}")
    print(f"  • Total chunks: {stats.get('total_chunks', 0)}")
    print(f"  • Vector store: {'✅ Created' if stats.get('vector_store') else '❌ Missing'}")
    
    print(f"\n🎯 Configuration Used:")
    print(f"  • Chunk size: {CHUNK_SIZE} words")
    print(f"  • Overlap: {OVERLAP} words")
    print(f"  • Min chunk words: {MIN_CHUNK_WORDS}")
    
    print(f"\n📁 Key Files:")
    print(f"  • Videos: {VIDEOS_JSON}")
    print(f"  • Metadata: {METADATA_JSON}")
    print(f"  • Transcripts: {TRANSCRIPT_DIR}/")
    print(f"  • Processed: {PROCESSED_DIR}/")
    print(f"  • Vector store: vector_store/")

def main():
    """Main pipeline runner"""
    parser = argparse.ArgumentParser(description='Run the complete video processing pipeline')
    parser.add_argument('--step', choices=['scrape', 'transcripts', 'preprocess', 'vectors'], 
                        help='Run only a specific step')
    parser.add_argument('--force-reprocess', action='store_true', 
                        help='Force reprocessing of all steps')
    parser.add_argument('--non-interactive', action='store_true',
                        help='Run without prompting for user input (useful for CI/CD)')
    
    args = parser.parse_args()
    
    print_banner("Outlier Trading Video Processing Pipeline")
    print(f"🗓️  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if args.non_interactive:
        print("🤖 Running in non-interactive mode (CI/CD friendly)")
    
    # Validate configuration (context-aware for specific steps)
    issues = validate_config(step=args.step)
    if issues:
        print("\n⚠️  Configuration Issues:")
        for issue in issues:
            print(f"  • {issue}")
        print("\nPlease fix these issues before running the pipeline.")
        return
    
    # Ensure directories exist
    ensure_directories()
    
    # Run specific step or full pipeline
    if args.step:
        force = args.force_reprocess
        if args.step == 'scrape':
            run_video_scraping(force, args.non_interactive)
        elif args.step == 'transcripts':
            run_transcript_processing(force, args.non_interactive)
        elif args.step == 'preprocess':
            run_preprocessing(force, args.non_interactive)
        elif args.step == 'vectors':
            run_vector_creation(force, args.non_interactive)
    else:
        # Run full pipeline
        print("\n🎯 Running complete pipeline...")
        force = args.force_reprocess
        
        success = True
        success &= run_video_scraping(force, args.non_interactive) is not False
        success &= run_transcript_processing(force, args.non_interactive) is not False
        success &= run_preprocessing(force, args.non_interactive) is not False
        success &= run_vector_creation(force, args.non_interactive) is not False
        
        if not success:
            print("\n❌ Pipeline failed! Check the errors above.")
            return
    
    print_summary()
    print(f"\n🎉 Pipeline completed successfully!")
    print(f"⏰ Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 