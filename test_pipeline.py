#!/usr/bin/env python3
"""
Pipeline Testing Script

This script helps test the new pipeline functionality with various scenarios.
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n🔬 {step}: {description}")
    print("-" * 50)

def run_command(cmd, description=""):
    """Run a command and capture output"""
    print(f"💻 Running: {cmd}")
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Success ({elapsed:.1f}s)")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ Failed ({elapsed:.1f}s)")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False, "", str(e)

def check_file_exists(filepath, description=""):
    """Check if a file exists"""
    if os.path.exists(filepath):
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {description or filepath}: {size:,} bytes")
        else:
            count = len([f for f in os.listdir(filepath) if not f.startswith('.')])
            print(f"✅ {description or filepath}: {count} files")
        return True
    else:
        print(f"❌ {description or filepath}: Not found")
        return False

def count_files_in_dir(directory, extension=""):
    """Count files in directory"""
    if not os.path.exists(directory):
        return 0
    
    if extension:
        return len([f for f in os.listdir(directory) if f.endswith(extension)])
    else:
        return len([f for f in os.listdir(directory) if not f.startswith('.')])

def get_video_count():
    """Get video count from JSON file"""
    try:
        with open('outlier_trading_videos.json', 'r') as f:
            data = json.load(f)
        return len(data)
    except:
        return 0

def test_basic_functionality():
    """Test basic pipeline functionality"""
    print_header("Basic Functionality Test")
    
    # Test video scraping
    print_step("1", "Testing video discovery")
    success, _, _ = run_command("python3 run_pipeline.py --step scrape --non-interactive")
    
    if success:
        video_count = get_video_count()
        print(f"📊 Videos discovered: {video_count}")
    
    # Test system validation
    print_step("2", "Testing system validation")
    run_command("python3 validate_system.py")
    
    return success

def test_non_interactive_mode():
    """Test non-interactive mode"""
    print_header("Non-Interactive Mode Test")
    
    print_step("1", "Testing complete pipeline in non-interactive mode")
    success, stdout, stderr = run_command("python3 run_pipeline.py --non-interactive")
    
    # Check for user prompts (should be none)
    if "🤔" in stdout or "input" in stderr.lower():
        print("❌ Non-interactive mode failed: Found user prompts")
        return False
    
    print_step("2", "Testing smart processing logic")
    print("Running pipeline again to test change detection...")
    success2, stdout2, stderr2 = run_command("python3 run_pipeline.py --non-interactive")
    
    if "No new" in stdout2 or "Skipping" in stdout2:
        print("✅ Smart processing logic working: Detected no changes")
    else:
        print("⚠️ Smart processing logic unclear: Check logs")
    
    return success

def test_individual_steps():
    """Test individual pipeline steps"""
    print_header("Individual Steps Test")
    
    steps = [
        ("scrape", "Video discovery"),
        ("transcripts", "Transcript generation"),
        ("preprocess", "Text processing"),
        ("vectors", "Vector store creation")
    ]
    
    results = []
    for step, description in steps:
        print_step(step, f"Testing {description}")
        success, _, _ = run_command(f"python3 run_pipeline.py --step {step} --non-interactive")
        results.append(success)
    
    return all(results)

def test_file_outputs():
    """Test that expected files are created"""
    print_header("File Output Verification")
    
    # Check expected files/directories
    checks = [
        ("outlier_trading_videos.json", "Video metadata"),
        ("transcripts/", "Transcript directory"),
        ("processed_transcripts/", "Processed transcript directory"),
        ("vector_store/", "Vector store directory")
    ]
    
    results = []
    for filepath, description in checks:
        result = check_file_exists(filepath, description)
        results.append(result)
    
    # Count files
    print_step("Counts", "File counts")
    video_count = get_video_count()
    transcript_count = count_files_in_dir("transcripts", ".txt")
    processed_count = count_files_in_dir("processed_transcripts", ".json")
    vector_files = count_files_in_dir("vector_store")
    
    print(f"📊 Statistics:")
    print(f"  - Videos: {video_count}")
    print(f"  - Transcripts: {transcript_count}")
    print(f"  - Processed files: {processed_count}")
    print(f"  - Vector store files: {vector_files}")
    
    return all(results)

def test_end_to_end():
    """Test end-to-end functionality"""
    print_header("End-to-End Test")
    
    print_step("1", "Testing RAG pipeline")
    success, stdout, stderr = run_command('python3 rag_pipeline.py "What is gamma in options trading?" --provider claude')
    
    if success and len(stdout) > 100:  # Reasonable answer length
        print("✅ RAG pipeline working: Generated response")
    else:
        print("❌ RAG pipeline issue: Short or no response")
    
    print_step("2", "Testing search functionality")
    success2, stdout2, stderr2 = run_command('python3 search_transcripts.py "covered calls" --top-k 3')
    
    if success2 and "youtube.com" in stdout2:
        print("✅ Search working: Found video links")
    else:
        print("❌ Search issue: No video links found")
    
    return success and success2

def test_github_actions_simulation():
    """Simulate GitHub Actions environment"""
    print_header("GitHub Actions Simulation")
    
    print_step("1", "Setting up CI/CD environment variables")
    
    # Check for required environment variables
    env_vars = ["YOUTUBE_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    missing_vars = []
    
    for var in env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("Add these to your .env file for full testing")
    
    print_step("2", "Running pipeline in CI/CD mode")
    
    # Create a test environment
    start_time = time.time()
    success, stdout, stderr = run_command("python3 run_pipeline.py --non-interactive")
    elapsed = time.time() - start_time
    
    print(f"📊 Pipeline completed in {elapsed:.1f}s")
    
    if elapsed > 3600:  # 1 hour
        print("⚠️ Pipeline took over 1 hour (GitHub Actions has 3 hour timeout)")
    
    return success

def run_all_tests():
    """Run all tests"""
    print_header("Complete Pipeline Test Suite")
    print(f"🗓️ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Non-Interactive Mode", test_non_interactive_mode),
        ("Individual Steps", test_individual_steps),
        ("File Outputs", test_file_outputs),
        ("End-to-End", test_end_to_end),
        ("GitHub Actions Simulation", test_github_actions_simulation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n🚀 Running {test_name} test...")
        try:
            result = test_func()
            results[test_name] = result
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"📊 {test_name}: {status}")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results[test_name] = False
    
    # Summary
    print_header("Test Results Summary")
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"📊 Overall Results: {passed}/{total} tests passed")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    if passed == total:
        print(f"\n🎉 All tests passed! Pipeline is ready for production.")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Check the logs above.")
    
    print(f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == "basic":
            test_basic_functionality()
        elif test_type == "non-interactive":
            test_non_interactive_mode()
        elif test_type == "steps":
            test_individual_steps()
        elif test_type == "files":
            test_file_outputs()
        elif test_type == "end-to-end":
            test_end_to_end()
        elif test_type == "github":
            test_github_actions_simulation()
        else:
            print("Available test types: basic, non-interactive, steps, files, end-to-end, github")
    else:
        run_all_tests()

if __name__ == "__main__":
    main() 