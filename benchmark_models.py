#!/usr/bin/env python3
"""
Whisper Model Benchmark for Parallel Processing

Test different models with parallel processing to find optimal configuration
for your specific hardware.

Usage:
    python3 benchmark_models.py [--test-files N] [--max-workers N]
"""

import os
import time
import argparse
import multiprocessing
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import whisper
import subprocess
import json
import psutil

def get_system_metrics():
    """Get current system resource usage"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "memory_used_gb": psutil.virtual_memory().used / (1024**3)
    }

def transcribe_benchmark_worker(args):
    """Worker function for benchmarking"""
    audio_file, model_name, worker_id = args
    
    start_time = time.time()
    try:
        # Load model
        model_load_start = time.time()
        model = whisper.load_model(model_name)
        model_load_time = time.time() - model_load_start
        
        # Transcribe
        transcribe_start = time.time()
        result = model.transcribe(str(audio_file))
        transcribe_time = time.time() - transcribe_start
        
        total_time = time.time() - start_time
        
        # Get audio duration
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', 
                   '-of', 'csv=p=0', str(audio_file)]
            duration_result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            audio_duration = float(duration_result.stdout.strip()) if duration_result.returncode == 0 else 0
        except:
            audio_duration = 0
        
        return {
            "success": True,
            "worker_id": worker_id,
            "file": str(audio_file),
            "model": model_name,
            "total_time": total_time,
            "model_load_time": model_load_time,
            "transcribe_time": transcribe_time,
            "audio_duration": audio_duration,
            "realtime_factor": transcribe_time / audio_duration if audio_duration > 0 else 0,
            "text_length": len(result.get("text", "")),
            "segments": len(result.get("segments", []))
        }
        
    except Exception as e:
        return {
            "success": False,
            "worker_id": worker_id,
            "file": str(audio_file),
            "model": model_name,
            "error": str(e),
            "total_time": time.time() - start_time
        }

def benchmark_model(audio_files, model_name, num_workers):
    """Benchmark a specific model with given number of workers"""
    print(f"\n🧪 Testing {model_name} model with {num_workers} workers...")
    
    # Limit files for benchmarking
    test_files = audio_files[:min(len(audio_files), num_workers * 2)]  # 2 files per worker
    
    # Prepare worker arguments
    worker_args = [(file, model_name, i % num_workers) for i, file in enumerate(test_files)]
    
    # Get initial system metrics
    initial_metrics = get_system_metrics()
    
    # Run benchmark
    start_time = time.time()
    results = []
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_args = {executor.submit(transcribe_benchmark_worker, args): args 
                          for args in worker_args}
        
        for future in as_completed(future_to_args):
            result = future.result()
            results.append(result)
            
            if result["success"]:
                print(f"  ✅ Worker {result['worker_id']}: {result['transcribe_time']:.1f}s "
                      f"(RTF: {result['realtime_factor']:.2f})")
            else:
                print(f"  ❌ Worker {result['worker_id']}: {result['error']}")
    
    total_time = time.time() - start_time
    final_metrics = get_system_metrics()
    
    # Calculate statistics
    successful_results = [r for r in results if r["success"]]
    
    if successful_results:
        avg_transcribe_time = sum(r["transcribe_time"] for r in successful_results) / len(successful_results)
        avg_realtime_factor = sum(r["realtime_factor"] for r in successful_results) / len(successful_results)
        total_audio_duration = sum(r["audio_duration"] for r in successful_results)
        throughput = len(successful_results) / total_time  # files per second
        
        return {
            "model": model_name,
            "workers": num_workers,
            "files_processed": len(successful_results),
            "total_time": total_time,
            "avg_transcribe_time": avg_transcribe_time,
            "avg_realtime_factor": avg_realtime_factor,
            "throughput": throughput,
            "total_audio_duration": total_audio_duration,
            "cpu_usage": final_metrics["cpu_percent"],
            "memory_usage_gb": final_metrics["memory_used_gb"],
            "efficiency": total_audio_duration / total_time,  # audio minutes per wall-clock minute
            "success_rate": len(successful_results) / len(results)
        }
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description='Benchmark Whisper models for parallel processing')
    parser.add_argument('--test-files', type=int, default=10, help='Number of files to test')
    parser.add_argument('--max-workers', type=int, default=8, help='Maximum workers to test')
    parser.add_argument('--models', default='tiny,base', help='Models to test (comma-separated)')
    parser.add_argument('--audio-dir', default='audio_files', help='Audio files directory')
    
    args = parser.parse_args()
    
    # Find audio files
    audio_dir = Path(args.audio_dir)
    audio_extensions = ['.mp3', '.wav', '.m4a', '.flac']
    audio_files = []
    
    for ext in audio_extensions:
        audio_files.extend(audio_dir.glob(f"*{ext}"))
    
    if len(audio_files) < args.test_files:
        print(f"⚠️  Only found {len(audio_files)} audio files, using all of them")
        args.test_files = len(audio_files)
    
    audio_files = audio_files[:args.test_files]
    models = args.models.split(',')
    
    print(f"🚀 Benchmarking Whisper Models")
    print(f"   Audio files: {len(audio_files)}")
    print(f"   Models: {models}")
    print(f"   Max workers: {args.max_workers}")
    
    # System info
    print(f"\n🖥️  System Info:")
    print(f"   CPU cores: {multiprocessing.cpu_count()}")
    print(f"   Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    
    # Run benchmarks
    all_results = []
    
    for model in models:
        for workers in [1, 2, 4, 6, 8, min(args.max_workers, 10)]:
            if workers > args.max_workers:
                continue
                
            result = benchmark_model(audio_files, model.strip(), workers)
            if result:
                all_results.append(result)
                
                print(f"\n📊 {model} model, {workers} workers:")
                print(f"   Throughput: {result['throughput']:.2f} files/sec")
                print(f"   Efficiency: {result['efficiency']:.2f} audio minutes/wall minute")
                print(f"   CPU usage: {result['cpu_usage']:.1f}%")
                print(f"   Memory: {result['memory_usage_gb']:.1f} GB")
    
    # Final analysis
    if all_results:
        print(f"\n🏆 BENCHMARK RESULTS SUMMARY")
        print("="*80)
        
        best_throughput = max(all_results, key=lambda x: x['throughput'])
        best_efficiency = max(all_results, key=lambda x: x['efficiency'])
        
        print(f"\n🚀 Best Throughput:")
        print(f"   {best_throughput['model']} model with {best_throughput['workers']} workers")
        print(f"   {best_throughput['throughput']:.2f} files/sec")
        
        print(f"\n⚡ Best Efficiency:")
        print(f"   {best_efficiency['model']} model with {best_efficiency['workers']} workers") 
        print(f"   {best_efficiency['efficiency']:.2f}x real-time")
        
        print(f"\n📈 All Results:")
        print(f"{'Model':<8} {'Workers':<8} {'Files/sec':<10} {'Efficiency':<12} {'CPU%':<8} {'Memory GB':<10}")
        print("-" * 70)
        
        for result in sorted(all_results, key=lambda x: x['throughput'], reverse=True):
            print(f"{result['model']:<8} {result['workers']:<8} "
                  f"{result['throughput']:<10.2f} {result['efficiency']:<12.2f} "
                  f"{result['cpu_usage']:<8.1f} {result['memory_usage_gb']:<10.1f}")

if __name__ == "__main__":
    main() 