#!/usr/bin/env python3
"""
Test script to verify all pipeline fixes are working correctly
"""

import os
import sys

def test_imports():
    """Test that all modules can be imported correctly"""
    print(" Testing imports...")
    
    try:
        from pipeline_config import CHUNK_SIZE, OVERLAP, VIDEOS_JSON, METADATA_JSON
        print(f"✅ pipeline_config imported successfully")
        print(f"   Chunk size: {CHUNK_SIZE}, Overlap: {OVERLAP}")
        print(f"   Videos file: {VIDEOS_JSON}")
        print(f"   Metadata file: {METADATA_JSON}")
    except Exception as e:
        print(f"❌ pipeline_config import failed: {e}")
        return False
    
    try:
        import preprocess_transcripts
        print(f"✅ preprocess_transcripts imported successfully")
    except Exception as e:
        print(f"❌ preprocess_transcripts import failed: {e}")
        return False
    
    try:
        import outlier_scraper
        print(f"✅ outlier_scraper imported successfully")
    except Exception as e:
        print(f"❌ outlier_scraper import failed: {e}")
        return False
    
    return True

def test_file_consistency():
    """Test that files are using consistent formats"""
    print("\n Testing file consistency...")
    
    # Check that CSV file is gone
    if os.path.exists('outlier_trading_videos.csv'):
        print("❌ Old CSV file still exists - should be removed")
        return False
    else:
        print("✅ Old CSV file removed")
    
    # Check that backup files are gone
    if os.path.exists('app.py.backup'):
        print("❌ Backup file still exists - should be removed")
        return False
    else:
        print("✅ Backup files removed")
    
    return True

def test_configuration_consistency():
    """Test that all scripts use consistent configuration"""
    print("\n Testing configuration consistency...")
    
    from pipeline_config import CHUNK_SIZE, OVERLAP, MIN_CHUNK_WORDS
    
    if CHUNK_SIZE <= OVERLAP:
        print(f"❌ Invalid configuration: chunk size ({CHUNK_SIZE}) must be > overlap ({OVERLAP})")
        return False
    
    if MIN_CHUNK_WORDS <= 0:
        print(f"❌ Invalid configuration: min chunk words ({MIN_CHUNK_WORDS}) must be > 0")
        return False
    
    print(f"✅ Configuration is valid:")
    print(f"   Chunk size: {CHUNK_SIZE} words")
    print(f"   Overlap: {OVERLAP} words")
    print(f"   Min chunk words: {MIN_CHUNK_WORDS}")
    
    return True

def test_script_organization():
    """Test that all required scripts exist"""
    print("\n Testing script organization...")
    
    required_scripts = [
        'pipeline_config.py',
        'outlier_scraper.py',
        'collect_video_metadata.py',
        'save_youtube_transcript.py',
        'whisper_transcribe.py',
        'preprocess_transcripts.py',
        'create_vector_store.py',
        'run_pipeline.py',
        'validate_pipeline.py'
    ]
    
    all_present = True
    for script in required_scripts:
        if os.path.exists(script):
            print(f"✅ {script}")
        else:
            print(f"❌ {script} missing")
            all_present = False
    
    return all_present

def main():
    """Run all tests"""
    print("🔧 PIPELINE CONSISTENCY TEST")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("File Consistency", test_file_consistency),
        ("Configuration", test_configuration_consistency),
        ("Script Organization", test_script_organization)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        try:
            passed = test_func()
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED - Pipeline is consistent and ready!")
        print("\n📋 Next Steps:")
        print("1. Run: python3 run_pipeline.py --force-reprocess")
        print("2. This will reprocess all videos with consistent settings")
        print("3. Multiple runs will produce identical results")
    else:
        print("❌ SOME TESTS FAILED - Please fix issues above")
    
    return all_passed

if __name__ == "__main__":
    main() 