#!/usr/bin/env python3
"""
Video Processing Pipeline Runner

This script orchestrates the complete video processing pipeline:
1. Scrape - Discover videos from the YouTube channel
2. Transcripts - Fetch transcripts via YouTube API (marks failures for Whisper)
3. Whisper - Second pass: download audio and transcribe failed videos with Whisper
4. Preprocess - Chunk transcripts for vector search
5. Vectors - Build the vector store for semantic search

Usage:
    python3 run_pipeline.py                          # Run complete pipeline
    python3 run_pipeline.py --step scrape            # Run only video discovery
    python3 run_pipeline.py --step transcripts       # Run only transcript generation
    python3 run_pipeline.py --step whisper           # Run Whisper on failed videos only
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
    CHANNEL_URLS, YOUTUBE_API_KEY, TRANSCRIPT_REQUEST_DELAY,
    ensure_directories, validate_config
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
    """Step 2: Generate transcripts for videos using yt-dlp (primary) with youtube-transcript-api fallback"""
    print_banner("STEP 2: TRANSCRIPT GENERATION")

    try:
        import yt_dlp
    except ImportError:
        print("❌ yt_dlp not installed. Run: pip install yt-dlp")
        return False

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import CouldNotRetrieveTranscript
        ytt_api = YouTubeTranscriptApi()
        has_ytt = True
    except ImportError:
        has_ytt = False

    # Load video list
    if not os.path.exists(VIDEOS_JSON):
        print(f"❌ {VIDEOS_JSON} not found. Run with --step scrape first.")
        return False

    with open(VIDEOS_JSON, 'r', encoding='utf-8') as f:
        videos = json.load(f)

    print(f"📚 Found {len(videos)} videos to process")

    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

    # Track progress
    progress_file = "transcript_progress.json"
    if os.path.exists(progress_file) and not args.force_reprocess:
        with open(progress_file, 'r') as f:
            progress = json.load(f)
        # Deduplicate on load
        progress['processed'] = list(set(progress.get('processed', [])))
        progress['failed'] = list(set(progress.get('failed', [])))
        progress['whisper_processed'] = list(set(progress.get('whisper_processed', [])))
    else:
        progress = {'processed': [], 'failed': [], 'whisper_processed': []}

    if not args.force_reprocess:
        all_processed = set(progress.get('processed', []) + progress.get('whisper_processed', []))
        progress['failed'] = [u for u in progress['failed'] if u not in all_processed]
        videos_to_process = [v for v in videos if v.get('url') not in all_processed]
        print(f"  ⏭️  Skipping {len(videos) - len(videos_to_process)} already processed videos")
    else:
        videos_to_process = videos

    successful = 0
    failed = 0

    def fetch_via_ytdlp(video_id):
        """Download subtitles via yt-dlp, return list of {start, text} dicts or None."""
        import tempfile, glob, re
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en', 'en-orig'],
                'skip_download': True,
                'outtmpl': os.path.join(tmpdir, '%(id)s'),
                'quiet': True,
                'no_warnings': True,
            }
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            except Exception:
                return None

            vtt_files = glob.glob(os.path.join(tmpdir, '*.vtt'))
            if not vtt_files:
                return None

            # Parse VTT — pick the cleanest file (en-orig preferred)
            vtt_files.sort(key=lambda f: (0 if 'en-orig' in f else 1))
            vtt_path = vtt_files[0]

            segments = []
            seen_texts = set()
            with open(vtt_path, encoding='utf-8') as f:
                content = f.read()

            # Extract timestamp + text blocks
            blocks = re.split(r'\n\n+', content)
            for block in blocks:
                lines = block.strip().splitlines()
                # Find timestamp line
                ts_line = next((l for l in lines if '-->' in l), None)
                if not ts_line:
                    continue
                start_str = ts_line.split('-->')[0].strip()
                # Convert HH:MM:SS.mmm to seconds
                parts = start_str.replace(',', '.').split(':')
                try:
                    if len(parts) == 3:
                        start = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
                    else:
                        start = float(parts[0])*60 + float(parts[1])
                except ValueError:
                    continue
                # Get text lines (skip timestamp, strip inline tags)
                text_lines = [l for l in lines if '-->' not in l and l.strip()]
                text = ' '.join(re.sub(r'<[^>]+>', '', l).strip() for l in text_lines).strip()
                if text and text not in seen_texts:
                    seen_texts.add(text)
                    segments.append({'start': start, 'text': text})

            return segments if segments else None

    for video in videos_to_process:
        video_id = video.get('video_id')
        title = video.get('title', 'Untitled')
        url = video.get('url')

        if not video_id:
            continue

        filename = os.path.join(TRANSCRIPT_DIR, f"{video_id}.txt")
        transcript = None
        method = None

        # --- Primary: yt-dlp subtitle extraction (handles IP blocks better) ---
        transcript = fetch_via_ytdlp(video_id)
        if transcript:
            method = 'yt-dlp'

        # --- Fallback: youtube-transcript-api ---
        if transcript is None and has_ytt:
            try:
                raw = ytt_api.fetch(video_id).to_raw_data()
                transcript = [{'start': e['start'], 'text': e['text']} for e in raw]
                method = 'youtube-transcript-api'
            except Exception:
                transcript = None

        if transcript:
            with open(filename, 'w', encoding='utf-8') as f:
                for entry in transcript:
                    text = entry['text'].strip()
                    if text:
                        f.write(f"{entry['start']:.2f}s: {text}\n")
            print(f"  ✅ [{method}] {title[:50]}...")
            if url not in progress.get('processed', []):
                progress['processed'].append(url)
            successful += 1
        else:
            print(f"  ⚠️  No captions found for {title[:50]}... (will use Whisper)")
            if url not in progress.get('failed', []):
                progress['failed'].append(url)
            failed += 1

        # Save progress after each video
        with open(progress_file, 'w') as f:
            json.dump(progress, f, indent=2)

        time.sleep(TRANSCRIPT_REQUEST_DELAY)

    print(f"\n📊 Transcript Results:")
    print(f"  ✅ Successfully processed: {successful}")
    print(f"  ❌ Failed/Need Whisper: {failed}")
    print(f"  📁 Transcripts saved to: {TRANSCRIPT_DIR}/")

    return True


def run_whisper(args):
    """Step 3: Second pass — download audio and transcribe failed videos with Whisper"""
    print_banner("STEP 3: WHISPER (failed videos)")
    
    import subprocess
    script_dir = os.path.dirname(os.path.abspath(__file__))
    retry_script = os.path.join(script_dir, 'retry_and_whisper.py')
    
    if not os.path.exists(retry_script):
        print(f"❌ {retry_script} not found")
        return False
    
    cmd = [sys.executable, retry_script, '--whisper-only']
    if getattr(args, 'max_whisper', None):
        cmd.extend(['--max-whisper', str(args.max_whisper)])
    
    try:
        result = subprocess.run(cmd, cwd=script_dir)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Whisper step failed: {e}")
        return False


def run_preprocess(args):
    """Step 4: Preprocess transcripts into chunks"""
    print_banner("STEP 4: TRANSCRIPT PREPROCESSING")
    
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
    """Step 5: Create vector store"""
    print_banner("STEP 5: VECTOR STORE CREATION")
    
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
  python3 run_pipeline.py --step whisper           # Run Whisper on failed videos
  python3 run_pipeline.py --step preprocess        # Run only preprocessing
  python3 run_pipeline.py --step vectors           # Run only vector store creation
  python3 run_pipeline.py --non-interactive        # Run without prompts (for CI/CD)
  python3 run_pipeline.py --force-reprocess        # Force reprocessing of all files
        """
    )
    
    parser.add_argument(
        '--step', 
        choices=['scrape', 'transcripts', 'whisper', 'preprocess', 'vectors'],
        help='Run a specific step only'
    )
    parser.add_argument(
        '--max-whisper',
        type=int,
        default=None,
        help='Limit Whisper to N videos (for testing)'
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
        'whisper': ('Whisper (failed videos)', run_whisper),
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

