#!/usr/bin/env python3
"""
Parallel Audio Transcription Script

This script processes multiple audio files simultaneously using Whisper,
with various optimization options for maximum speed.

Usage:
    python3 parallel_transcribe.py [options]

Options:
    --workers N          Number of parallel workers (default: CPU count)
    --model tiny|base    Whisper model to use (default: tiny)
    --batch-size N       Batch size for processing (default: 10)
    --gpu                Use GPU if available
    --resume             Resume from previous run
    --output-dir DIR     Output directory (default: transcripts)
    --input-dir DIR      Input directory (default: audio_files)
    --format txt|json    Output format (default: txt)
"""

import os
import json
import whisper
import torch
import argparse
import multiprocessing
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import time
import sys
import subprocess

# Configuration
PROGRESS_FILE = "parallel_transcription_progress.json"

def get_system_info():
    """Get system information for optimization"""
    import psutil
    import torch
    
    info = {
        "cpu_count": multiprocessing.cpu_count(),
        "memory_gb": round(psutil.virtual_memory().total / (1024**3), 1),
        "gpu_available": torch.cuda.is_available(),
        "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0
    }
    
    if info["gpu_available"]:
        info["gpu_memory_gb"] = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 1)
    
    return info

def suggest_optimal_workers(model_size="tiny"):
    """Suggest optimal number of workers based on system resources"""
    info = get_system_info()
    
    # Memory requirements per worker (approximate)
    memory_per_worker = {
        "tiny": 1.0,    # GB
        "base": 1.5,    # GB
        "small": 2.0,   # GB
        "medium": 4.0,  # GB
        "large": 8.0    # GB
    }
    
    # CPU-based limit
    cpu_limit = info["cpu_count"]
    
    # Memory-based limit
    memory_limit = int(info["memory_gb"] * 0.8 / memory_per_worker.get(model_size, 1.0))
    
    # Conservative limit to avoid system overload
    suggested = min(cpu_limit, memory_limit, 8)  # Cap at 8 workers
    
    return max(1, suggested)

def validate_audio_file(audio_file):
    """Validate that the file is a proper audio file"""
    try:
        # Use ffprobe to check if file has audio streams
        cmd = [
            'ffprobe', '-v', 'quiet', '-select_streams', 'a:0',
            '-show_entries', 'stream=codec_type', '-of', 'csv=p=0',
            str(audio_file)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        # Check if we found an audio stream
        return 'audio' in result.stdout
        
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, Exception):
        return False

def transcribe_file_worker(args):
    """Worker function for parallel transcription"""
    audio_file, model_name, output_dir, output_format, use_gpu = args
    
    try:
        # Validate audio file first
        if not validate_audio_file(audio_file):
            return {
                "success": False,
                "file": audio_file,
                "output": "",
                "message": "Invalid audio file (may be video or corrupted)",
                "skipped": False,
                "duration": 0
            }

        # Load model in each worker process
        device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        model = whisper.load_model(model_name, device=device)
        
        # Prepare output file
        file_stem = Path(audio_file).stem
        if output_format == "json":
            output_file = Path(output_dir) / f"{file_stem}.json"
        else:
            output_file = Path(output_dir) / f"{file_stem}.txt"
        
        # Skip if already exists
        if output_file.exists():
            return {
                "success": True,
                "file": audio_file,
                "output": str(output_file),
                "message": "Already exists",
                "skipped": True,
                "duration": 0
            }
        
        # Transcribe
        start_time = time.time()
        result = model.transcribe(audio_file)
        duration = time.time() - start_time
        
        # Save results
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if output_format == "json":
            # Save full JSON result
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        else:
            # Save timestamped text format
            with open(output_file, 'w', encoding='utf-8') as f:
                for segment in result["segments"]:
                    start_time = segment["start"]
                    text = segment["text"].strip()
                    if text:
                        f.write(f"{start_time:.2f}s: {text}\n")
        
        return {
            "success": True,
            "file": audio_file,
            "output": str(output_file),
            "message": "Transcribed successfully",
            "skipped": False,
            "duration": duration
        }
        
    except Exception as e:
        return {
            "success": False,
            "file": audio_file,
            "output": "",
            "message": str(e),
            "skipped": False,
            "duration": 0
        }

def load_progress():
    """Load previous progress if exists"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {"completed": [], "failed": [], "skipped": []}

def save_progress(progress):
    """Save progress to file"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def parallel_transcribe(input_dir, output_dir, model_name="tiny", num_workers=None, 
                       use_gpu=False, resume=False, output_format="txt"):
    """Main parallel transcription function"""
    
    # System information
    system_info = get_system_info()
    print(f"🖥️  System Info:")
    print(f"   CPU cores: {system_info['cpu_count']}")
    print(f"   Memory: {system_info['memory_gb']} GB")
    print(f"   GPU: {'✅' if system_info['gpu_available'] else '❌'}")
    
    # Determine optimal workers
    if num_workers is None:
        num_workers = suggest_optimal_workers(model_name)
    
    suggested = suggest_optimal_workers(model_name)
    if num_workers > suggested:
        print(f"⚠️  Warning: {num_workers} workers might be too many for your system.")
        print(f"   Suggested: {suggested} workers")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            num_workers = suggested
    
    print(f" Using {num_workers} workers with '{model_name}' model")
    
    # Find audio files
    input_path = Path(input_dir)
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
    audio_files = []
    
    for ext in audio_extensions:
        audio_files.extend(input_path.glob(f"*{ext}"))
    
    if not audio_files:
        print(f"❌ No audio files found in {input_dir}")
        return False
    
    print(f"📁 Found {len(audio_files)} audio files")
    
    # Load progress
    progress = load_progress() if resume else {"completed": [], "failed": [], "skipped": []}
    
    # Filter files if resuming
    if resume:
        completed_files = set(progress["completed"] + progress["failed"] + progress["skipped"])
        audio_files = [f for f in audio_files if str(f) not in completed_files]
        print(f"📋 Resume mode: {len(audio_files)} files remaining")
    
    if not audio_files:
        print("✅ All files already processed!")
        return True
    
    # Prepare arguments for workers
    worker_args = [
        (str(audio_file), model_name, output_dir, output_format, use_gpu)
        for audio_file in audio_files
    ]
    
    # Process files in parallel
    successful = 0
    failed = 0
    skipped = 0
    total_duration = 0
    
    print(f"🎯 Processing {len(audio_files)} files...")
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Submit all tasks
        future_to_file = {executor.submit(transcribe_file_worker, args): args[0] 
                          for args in worker_args}
        
        # Process results as they complete
        for future in tqdm(as_completed(future_to_file), total=len(audio_files), desc="Transcribing"):
            audio_file = future_to_file[future]
            try:
                result = future.result()
                
                if result["success"]:
                    if result["skipped"]:
                        skipped += 1
                        progress["skipped"].append(audio_file)
                    else:
                        successful += 1
                        progress["completed"].append(audio_file)
                        total_duration += result["duration"]
                    
                    # Print progress (optional - can be noisy)
                    if not result["skipped"]:
                        print(f"✅ {Path(audio_file).name}: {result['duration']:.1f}s")
                else:
                    failed += 1
                    progress["failed"].append(audio_file)
                    print(f"❌ {Path(audio_file).name}: {result['message']}")
                
                # Save progress periodically
                if (successful + failed + skipped) % 10 == 0:
                    save_progress(progress)
                    
            except Exception as e:
                failed += 1
                progress["failed"].append(audio_file)
                print(f"❌ {Path(audio_file).name}: {str(e)}")
    
    # Final progress save
    save_progress(progress)
    
    # Summary
    print(f"\n📊 Processing Summary:")
    print(f"  ✅ Successful: {successful}")
    print(f"  ⏭️  Skipped: {skipped}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📁 Total: {len(audio_files)}")
    
    if successful > 0:
        avg_time = total_duration / successful
        print(f"  ⏱️  Average time per file: {avg_time:.1f}s")
        print(f"   Total processing time: {total_duration:.1f}s")
    
    return True

def main():
    # Get defaults from pipeline configuration
    try:
        from pipeline_config import WHISPER_MODEL_PARALLEL, PARALLEL_WORKERS
        default_model = WHISPER_MODEL_PARALLEL
        default_workers = PARALLEL_WORKERS
        print(f"📋 Using pipeline config defaults: {default_model} model, {default_workers} workers")
    except ImportError:
        default_model = "tiny"
        default_workers = None
        print("📋 Pipeline config not found, using built-in defaults")
    
    parser = argparse.ArgumentParser(description='Parallel audio transcription with Whisper')
    parser.add_argument('--workers', type=int, default=default_workers, 
                        help=f'Number of parallel workers (default: {default_workers or "auto"})')
    parser.add_argument('--model', choices=['tiny', 'base', 'small', 'medium', 'large'], 
                        default=default_model, help=f'Whisper model to use (default: {default_model})')
    parser.add_argument('--gpu', action='store_true', help='Use GPU if available')
    parser.add_argument('--resume', action='store_true', help='Resume from previous run')
    parser.add_argument('--output-dir', default='transcripts', help='Output directory')
    parser.add_argument('--input-dir', default='audio_files', help='Input directory')
    parser.add_argument('--format', choices=['txt', 'json'], default='txt', help='Output format')
    parser.add_argument('--info', action='store_true', help='Show system info and exit')
    
    args = parser.parse_args()
    
    if args.info:
        system_info = get_system_info()
        print("🖥️  System Information:")
        print(f"   CPU cores: {system_info['cpu_count']}")
        print(f"   Memory: {system_info['memory_gb']} GB")
        print(f"   GPU available: {'✅' if system_info['gpu_available'] else '❌'}")
        if system_info['gpu_available']:
            print(f"   GPU memory: {system_info['gpu_memory_gb']} GB")
        
        suggested = suggest_optimal_workers(args.model)
        print(f"\n🎯 Suggested workers for '{args.model}' model: {suggested}")
        return
    
    print(" Starting parallel audio transcription...")
    print("=" * 60)
    
    start_time = time.time()
    
    success = parallel_transcribe(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        model_name=args.model,
        num_workers=args.workers,
        use_gpu=args.gpu,
        resume=args.resume,
        output_format=args.format
    )
    
    total_time = time.time() - start_time
    
    if success:
        print(f"\n🎉 Transcription complete! Total time: {total_time:.1f}s")
        print(f"📁 Results saved to: {args.output_dir}")
    else:
        print(f"\n❌ Transcription failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 