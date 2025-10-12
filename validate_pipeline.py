#!/usr/bin/env python3
"""
Pipeline Validation Script

This script validates that the video processing pipeline is correctly organized
and ready for execution. It checks for:
- Script organization and dependencies
- Configuration consistency
- File structure
- API keys and environment setup
- Common issues and fixes

Usage:
    python3 validate_pipeline.py
"""

import os
import sys
import json
import importlib.util
from datetime import datetime

def check_mark(condition, message):
    """Print a formatted check message"""
    status = "" if condition else "❌"
    print(f"{status} {message}")
    return condition

def warning_mark(condition, message):
    """Print a formatted warning message"""
    status = "⚠️ " if condition else ""
    print(f"{status} {message}")
    return condition

def print_section(title):
    """Print a formatted section header"""
    print(f"\n📋 {title}")
    print("-" * 50)

def validate_scripts():
    """Validate that all required scripts exist and are importable"""
    print_section("Script Organization & Dependencies")
    
    required_scripts = [
        'pipeline_config.py',
        'outlier_scraper.py', 
        'collect_video_metadata.py',
        'save_youtube_transcript.py',
        'whisper_transcribe.py',
        'preprocess_transcripts.py',
        'create_vector_store.py',
        'run_pipeline.py'
    ]
    
    all_present = True
    for script in required_scripts:
        exists = os.path.exists(script)
        check_mark(exists, f"Required script: {script}")
        if not exists:
            all_present = False
    
    # Test imports
    print(f"\n Testing imports...")
    try:
        import pipeline_config
        check_mark(True, "pipeline_config module imports successfully")
        
        # Test configuration validation
        issues = pipeline_config.validate_config()
        if issues:
            print(f"⚠️  Configuration issues found:")
            for issue in issues:
                print(f"    • {issue}")
        else:
            check_mark(True, "Configuration validation passes")
            
    except Exception as e:
        check_mark(False, f"pipeline_config import failed: {e}")
        all_present = False
    
    try:
        import preprocess_transcripts
        check_mark(True, "preprocess_transcripts module imports successfully")
    except Exception as e:
        check_mark(False, f"preprocess_transcripts import failed: {e}")
        all_present = False
    
    return all_present

def validate_file_structure():
    """Validate directory structure and key files"""
    print_section("File Structure & Organization")
    
    # Check directories
    from pipeline_config import TRANSCRIPT_DIR, PROCESSED_DIR, AUDIO_DIR, VECTOR_STORE_DIR
    
    dirs_to_check = [
        (TRANSCRIPT_DIR, "Transcript storage"),
        (PROCESSED_DIR, "Processed chunks"),
        (AUDIO_DIR, "Temporary audio files"),
        (VECTOR_STORE_DIR, "Vector database")
    ]
    
    structure_ok = True
    for dir_path, description in dirs_to_check:
        exists = os.path.exists(dir_path)
        check_mark(exists, f"Directory {dir_path}/ ({description})")
        if not exists:
            structure_ok = False
    
    # Check for conflicting files
    conflicting_files = [
        ('outlier_trading_videos.csv', 'Should use .json format instead'),
        ('gradio_app.py', 'Redundant - use app.py'),
        ('main.py', 'Redundant - use app.py'),
        ('start_app.py', 'Redundant - use app.py')
    ]
    
    for file_path, reason in conflicting_files:
        exists = os.path.exists(file_path)
        if exists:
            print(f"⚠️  Found conflicting file: {file_path} ({reason})")
            structure_ok = False
    
    return structure_ok

def validate_configuration():
    """Validate pipeline configuration"""
    print_section("Configuration Validation")
    
    try:
        from pipeline_config import (
            CHUNK_SIZE, OVERLAP, MIN_CHUNK_WORDS, 
            VIDEOS_JSON, METADATA_JSON, YOUTUBE_API_KEY
        )
        
        config_valid = True
        
        # Check chunk configuration
        config_valid &= check_mark(
            CHUNK_SIZE > OVERLAP, 
            f"Chunk size ({CHUNK_SIZE}) > overlap ({OVERLAP})"
        )
        
        config_valid &= check_mark(
            MIN_CHUNK_WORDS > 0, 
            f"Min chunk words ({MIN_CHUNK_WORDS}) > 0"
        )
        
        config_valid &= check_mark(
            OVERLAP >= 0, 
            f"Overlap ({OVERLAP}) >= 0"
        )
        
        # Check file paths
        config_valid &= check_mark(
            VIDEOS_JSON.endswith('.json'), 
            f"Videos file uses JSON format: {VIDEOS_JSON}"
        )
        
        config_valid &= check_mark(
            METADATA_JSON.endswith('.json'), 
            f"Metadata file uses JSON format: {METADATA_JSON}"
        )
        
        # Check API key
        has_api_key = YOUTUBE_API_KEY is not None and len(YOUTUBE_API_KEY) > 0
        warning_mark(
            not has_api_key, 
            "YouTube API key not found (metadata will be limited)"
        )
        
        if has_api_key:
            # Basic API key validation
            valid_format = not YOUTUBE_API_KEY.endswith('.apps.googleusercontent.com')
            config_valid &= check_mark(
                valid_format, 
                "YouTube API key format looks correct"
            )
        
        return config_valid
        
    except Exception as e:
        check_mark(False, f"Configuration validation failed: {e}")
        return False

def validate_existing_data():
    """Validate existing data files"""
    print_section("Existing Data Validation")
    
    from pipeline_config import VIDEOS_JSON, METADATA_JSON, TRANSCRIPT_DIR, PROCESSED_DIR
    
    data_status = {}
    
    # Check videos file
    if os.path.exists(VIDEOS_JSON):
        try:
            with open(VIDEOS_JSON, 'r') as f:
                videos = json.load(f)
            data_status['videos'] = len(videos)
            check_mark(True, f"Videos file: {len(videos)} videos found")
        except Exception as e:
            check_mark(False, f"Videos file corrupted: {e}")
    else:
        print(f"ℹ️  No videos file found - will be created on first run")
    
    # Check metadata file
    if os.path.exists(METADATA_JSON):
        try:
            with open(METADATA_JSON, 'r') as f:
                metadata = json.load(f)
            data_status['metadata'] = len(metadata) if isinstance(metadata, list) else len(metadata.keys())
            check_mark(True, f"Metadata file: {data_status['metadata']} entries found")
        except Exception as e:
            check_mark(False, f"Metadata file corrupted: {e}")
    else:
        print(f"ℹ️  No metadata file found - will be created if API key is available")
    
    # Check transcripts
    if os.path.exists(TRANSCRIPT_DIR):
        transcript_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith('.txt')]
        data_status['transcripts'] = len(transcript_files)
        check_mark(True, f"Transcripts: {len(transcript_files)} files found")
    else:
        print(f"ℹ️  No transcripts directory found - will be created")
    
    # Check processed files
    if os.path.exists(PROCESSED_DIR):
        processed_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
        data_status['processed'] = len(processed_files)
        check_mark(True, f"Processed files: {len(processed_files)} files found")
        
        # Sample a few files for validation
        sample_files = processed_files[:3]
        for filename in sample_files:
            file_path = os.path.join(PROCESSED_DIR, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    # Check if chunks have required fields
                    sample_chunk = data[0]
                    required_fields = ['video_id', 'title', 'text', 'start_timestamp_seconds']
                    has_all_fields = all(field in sample_chunk for field in required_fields)
                    check_mark(has_all_fields, f"Sample file {filename} has required fields")
                else:
                    check_mark(False, f"Sample file {filename} is empty or invalid")
            except Exception as e:
                check_mark(False, f"Sample file {filename} corrupted: {e}")
    else:
        print(f"ℹ️  No processed files found - will be created during preprocessing")
    
    return data_status

def validate_dependencies():
    """Validate Python dependencies"""
    print_section("Python Dependencies")
    
    required_packages = [
        'yt_dlp',
        'youtube_transcript_api', 
        'whisper',
        'sentence_transformers',
        'faiss',
        'tqdm',
        'pandas',
        'numpy',
        'transformers',
        'torch'
    ]
    
    deps_ok = True
    for package in required_packages:
        try:
            __import__(package)
            check_mark(True, f"Package {package} available")
        except ImportError:
            check_mark(False, f"Package {package} missing - install with: pip install {package}")
            deps_ok = False
    
    return deps_ok

def print_recommendations():
    """Print recommendations for optimal pipeline execution"""
    print_section("Recommendations")
    
    print("🎯 To run the complete pipeline:")
    print("   python3 run_pipeline.py")
    print("")
    print("🔧 To run specific steps:")
    print("   python3 run_pipeline.py --step scrape")
    print("   python3 run_pipeline.py --step transcripts")
    print("   python3 run_pipeline.py --step preprocess")
    print("   python3 run_pipeline.py --step vectors")
    print("")
    print("🔄 To force reprocessing:")
    print("   python3 run_pipeline.py --force-reprocess")
    print("")
    print("📊 To check configuration:")
    print("   python3 pipeline_config.py")
    print("")
    print("🧪 To test the RAG system:")
    print("   python3 app.py")

def main():
    """Main validation function"""
    print(" PIPELINE VALIDATION REPORT")
    print("=" * 80)
    print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all validations
    scripts_ok = validate_scripts()
    structure_ok = validate_file_structure()
    config_ok = validate_configuration()
    data_status = validate_existing_data()
    deps_ok = validate_dependencies()
    
    # Summary
    print_section("Validation Summary")
    
    all_checks = [
        ("Scripts & imports", scripts_ok),
        ("File structure", structure_ok),
        ("Configuration", config_ok),
        ("Dependencies", deps_ok)
    ]
    
    overall_status = all(status for _, status in all_checks)
    
    for name, status in all_checks:
        check_mark(status, f"{name} validation")
    
    if data_status:
        print(f"\n📊 Current Data Status:")
        for key, value in data_status.items():
            print(f"   • {key.title()}: {value}")
    
    print(f"\n🎯 Overall Status: {' READY' if overall_status else '❌ NEEDS FIXES'}")
    
    if overall_status:
        print("\n Pipeline is ready for execution!")
        print_recommendations()
    else:
        print("\n🔧 Please fix the issues above before running the pipeline.")
    
    return overall_status

if __name__ == "__main__":
    main() 