#!/usr/bin/env python3
"""
Video Processing Pipeline Runner

This script orchestrates the complete video processing pipeline:
1. Scrape - Discover videos from the YouTube channel
2. Transcripts - Download/generate transcripts for videos
3. Preprocess - Chunk transcripts for vector search
4. Vectors - Build the vector store for semantic search

Usage:
    python3 run_pipeline.py                          # Run complete pipeline
    python3 run_pipeline.py --step scrape            # Run only video discovery
    python3 run_pipeline.py --step transcripts       # Run only transcript generation
    python3 run_pipeline.py --step preprocess        # Run only preprocessing
    python3 run_pipeline.py --step vectors           # Run only vector store creation
    python3 run_pipeline.py --non-interactive        # Run without prompts (for CI/CD)
    python3 run_pipeline.py --force-reprocess        # Force reprocessing of all files
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime

# Import configuration
from pipeline_config import (
    VIDEOS_JSON, TRANSCRIPT_DIR, PROCESSED_DIR, VECTOR_STORE_DIR,
    CHANNEL_URLS, YOUTUBE_API_KEY, ensure_directories, validate_config
)


def print_banner(step_name):
    """Print a formatted banner for each step"""
    print("\n" + "=" * 60)
    print(f"🚀 {step_name}")
    print("=" * 60 + "\n")


def run_scrape(args):
    """Step 1: Discover videos from YouTube channel"""
    print_banner("STEP 1: VIDEO DISCOVERY")
    
    try:
        import yt_dlp
    except ImportError:
        print("❌ yt_dlp not installed. Run: pip install yt-dlp")
        return False
    
    ydl_opts = {
        'ignoreerrors': True,
        'quiet': not args.verbose if hasattr(args, 'verbose') else True,
        'extract_flat': True,
        'playlistend': 10000,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'no_warnings': True,
    }
    
    all_videos_data = []
    url_stats = {}
    
    for channel_url in CHANNEL_URLS:
        print(f"📺 Processing: {channel_url}")
        url_stats[channel_url] = {'found': 0, 'errors': 0}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                data = ydl.extract_info(channel_url, download=False)
                if not data:
                    print(f"  ❌ No data returned for {channel_url}")
                    url_stats[channel_url]['errors'] += 1
                    continue
                
                video_entries = data.get('entries', [])
                print(f"  📹 Found {len(video_entries)} videos")
                
                for entry in video_entries:
                    if entry:
                        video_info = {
                            'video_id': entry.get('id'),
                            'title': entry.get('title', 'No Title'),
                            'url': f"https://www.youtube.com/watch?v={entry.get('id')}" if entry.get('id') else None,
                            'upload_date': entry.get('upload_date'),
                            'duration': entry.get('duration'),
                            'description': entry.get('description'),
                            'view_count': entry.get('view_count'),
                            'like_count': entry.get('like_count'),
                            'source_url': channel_url
                        }
                        all_videos_data.append(video_info)
                        url_stats[channel_url]['found'] += 1
                        
            except Exception as e:
                print(f"  ❌ Error processing {channel_url}: {e}")
                url_stats[channel_url]['errors'] += 1
    
    # Remove duplicates based on video_id
    seen_ids = set()
    unique_videos = []
    duplicate_count = 0
    
    for video in all_videos_data:
        if video['video_id'] and video['video_id'] not in seen_ids:
            seen_ids.add(video['video_id'])
            unique_videos.append(video)
        else:
            duplicate_count += 1
    
    # Save results
    with open(VIDEOS_JSON, 'w', encoding='utf-8') as jsonfile:
        json.dump(unique_videos, jsonfile, indent=4, ensure_ascii=False)
    
    print(f"\n📊 Discovery Results:")
    print(f"  ✅ {len(unique_videos)} unique videos saved to {VIDEOS_JSON}")
    print(f"  🔄 {duplicate_count} duplicates removed")
    
    return True


def run_transcripts(args):
    """Step 2: Generate transcripts for videos"""
    print_banner("STEP 2: TRANSCRIPT GENERATION")
    
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    except ImportError:
        print("❌ youtube_transcript_api not installed. Run: pip install youtube-transcript-api")
        return False
    
    # Load video list
    if not os.path.exists(VIDEOS_JSON):
        print(f"❌ {VIDEOS_JSON} not found. Run with --step scrape first.")
        return False
    
    with open(VIDEOS_JSON, 'r', encoding='utf-8') as f:
        videos = json.load(f)
    
    print(f"📚 Found {len(videos)} videos to process")
    
    # Create transcript directory
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    
    # Track progress
    progress_file = "transcript_progress.json"
    if os.path.exists(progress_file) and not args.force_reprocess:
        with open(progress_file, 'r') as f:
            progress = json.load(f)
    else:
        progress = {'processed': [], 'failed': [], 'whisper_processed': []}
    
    # Filter already processed videos
    if not args.force_reprocess:
        all_processed = set(progress.get('processed', []) + progress.get('whisper_processed', []))
        videos_to_process = [v for v in videos if v.get('url') not in all_processed]
        print(f"  ⏭️  Skipping {len(videos) - len(videos_to_process)} already processed videos")
    else:
        videos_to_process = videos
    
    successful = 0
    failed = 0
    
    for video in videos_to_process:
        video_id = video.get('video_id')
        title = video.get('title', 'Untitled')
        url = video.get('url')
        
        if not video_id:
            continue
        
        # Clean title for filename
        safe_title = "".join(c if c.isalnum() or c in ' -_' else '_' for c in title)[:100]
        filename = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
        
        try:
            # Try to get YouTube transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in transcript:
                    text = entry['text'].strip()
                    if text:
                        f.write(f"{entry['start']:.2f}s: {text}\n")
            
            print(f"  ✅ {title[:50]}...")
            progress['processed'].append(url)
            successful += 1
            
        except (TranscriptsDisabled, NoTranscriptFound) as e:
            # Try Whisper if YouTube transcript not available
            print(f"  ⚠️  No YouTube transcript for {title[:50]}... (will need Whisper)")
            progress['failed'].append(url)
            failed += 1
            
        except Exception as e:
            print(f"  ❌ Error: {title[:50]}... - {str(e)[:50]}")
            progress['failed'].append(url)
            failed += 1
        
        # Save progress periodically
        with open(progress_file, 'w') as f:
            json.dump(progress, f, indent=2)
    
    print(f"\n📊 Transcript Results:")
    print(f"  ✅ Successfully processed: {successful}")
    print(f"  ❌ Failed/Need Whisper: {failed}")
    print(f"  📁 Transcripts saved to: {TRANSCRIPT_DIR}/")
    
    return True


def run_preprocess(args):
    """Step 3: Preprocess transcripts into chunks"""
    print_banner("STEP 3: TRANSCRIPT PREPROCESSING")
    
    # Import the preprocessing module
    try:
        import preprocess_transcripts
        return preprocess_transcripts.main(force_reprocess=args.force_reprocess)
    except ImportError:
        print("❌ preprocess_transcripts module not found")
        return False
    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
        return False


def run_vectors(args):
    """Step 4: Create vector store"""
    print_banner("STEP 4: VECTOR STORE CREATION")
    
    try:
        import create_vector_store
        
        # Create args namespace for the vector store script
        vector_args = argparse.Namespace()
        vector_args.model = "all-MiniLM-L6-v2"
        vector_args.batch_size = 32
        vector_args.output_dir = None
        vector_args.test_search = False
        
        create_vector_store.main(vector_args)
        return True
        
    except ImportError as e:
        print(f"❌ create_vector_store module not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        return False


def main():
    """Main entry point for the pipeline"""
    parser = argparse.ArgumentParser(
        description='Video Processing Pipeline Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 run_pipeline.py                          # Run complete pipeline
  python3 run_pipeline.py --step scrape            # Run only video discovery
  python3 run_pipeline.py --step transcripts       # Run only transcript generation
  python3 run_pipeline.py --step preprocess        # Run only preprocessing
  python3 run_pipeline.py --step vectors           # Run only vector store creation
  python3 run_pipeline.py --non-interactive        # Run without prompts (for CI/CD)
  python3 run_pipeline.py --force-reprocess        # Force reprocessing of all files
        """
    )
    
    parser.add_argument(
        '--step', 
        choices=['scrape', 'transcripts', 'preprocess', 'vectors'],
        help='Run a specific step only'
    )
    parser.add_argument(
        '--non-interactive', 
        action='store_true',
        help='Run without user prompts (for CI/CD environments)'
    )
    parser.add_argument(
        '--force-reprocess', 
        action='store_true',
        help='Force reprocessing of all files'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("\n" + "=" * 60)
    print("🎬 VIDEO PROCESSING PIPELINE")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Ensure directories exist
    ensure_directories()
    
    # Validate configuration for the specified step
    issues = validate_config(step=args.step)
    if issues:
        print("\n⚠️  Configuration warnings:")
        for issue in issues:
            print(f"  • {issue}")
        
        if not args.non_interactive:
            response = input("\nContinue anyway? (y/n): ")
            if response.lower() != 'y':
                print("Aborted by user.")
                sys.exit(1)
    
    # Define pipeline steps
    steps = {
        'scrape': ('Video Discovery', run_scrape),
        'transcripts': ('Transcript Generation', run_transcripts),
        'preprocess': ('Transcript Preprocessing', run_preprocess),
        'vectors': ('Vector Store Creation', run_vectors),
    }
    
    # Determine which steps to run
    if args.step:
        steps_to_run = [args.step]
    else:
        steps_to_run = list(steps.keys())
    
    # Run the selected steps
    start_time = time.time()
    results = {}
    
    for step_name in steps_to_run:
        step_title, step_func = steps[step_name]
        try:
            success = step_func(args)
            results[step_name] = success
            if not success:
                print(f"\n❌ {step_title} failed")
                if not args.non_interactive:
                    response = input("Continue to next step? (y/n): ")
                    if response.lower() != 'y':
                        break
        except KeyboardInterrupt:
            print("\n\n⚠️  Pipeline interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error in {step_title}: {e}")
            results[step_name] = False
            if not args.non_interactive:
                response = input("Continue to next step? (y/n): ")
                if response.lower() != 'y':
                    break
    
    # Print summary
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("📊 PIPELINE SUMMARY")
    print("=" * 60)
    
    for step_name, success in results.items():
        status = "✅" if success else "❌"
        step_title = steps[step_name][0]
        print(f"  {status} {step_title}")
    
    print(f"\n⏱️  Total time: {elapsed_time:.1f} seconds")
    
    # Return appropriate exit code
    all_success = all(results.values())
    if all_success:
        print("\n🎉 Pipeline completed successfully!")
        sys.exit(0)
    else:
        print("\n⚠️  Pipeline completed with some failures")
        sys.exit(1)


if __name__ == "__main__":
    main()

