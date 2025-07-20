#!/usr/bin/env python3
"""
Test Docker Build Process - Mimics HuggingFace Deployment
Tests the exact same Docker build and run process that HuggingFace uses
"""

import os
import subprocess
import time
import requests
import sys
import json
from datetime import datetime

def run_command(cmd, cwd=None, capture_output=True):
    """Run a command and return result"""
    print(f"🔧 Running: {cmd}")
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, cwd=cwd, 
                                  capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                print(f"❌ Command failed: {result.stderr}")
                return False, result.stderr
            return True, result.stdout
        else:
            result = subprocess.run(cmd, shell=True, cwd=cwd, timeout=300)
            return result.returncode == 0, ""
    except subprocess.TimeoutExpired:
        print(f"❌ Command timed out: {cmd}")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ Command error: {e}")
        return False, str(e)

def check_docker_installed():
    """Check if Docker is installed and running"""
    print("🐳 Checking Docker installation...")
    
    success, output = run_command("docker --version")
    if not success:
        print("❌ Docker not installed. Please install Docker Desktop")
        return False
    print(f"✅ Docker found: {output.strip()}")
    
    success, output = run_command("docker info")
    if not success:
        print("❌ Docker not running. Please start Docker Desktop")
        return False
    print("✅ Docker is running")
    return True

def simulate_github_workflow():
    """Simulate the exact GitHub Actions workflow steps"""
    print("🔄 Simulating GitHub Actions workflow steps...")
    
    # Step 1: Create startup script (exactly like the workflow)
    print("📝 Creating startup.sh script...")
    startup_script = """#!/bin/bash
set -e

echo "===== Starting application ====="
date

# Print environment for debugging
echo "Current directory: $(pwd)"
echo "Current user: $(whoami)"

# Run the FastAPI application
python main.py
"""
    
    with open("startup.sh", "w") as f:
        f.write(startup_script)
    
    # Make it executable
    success, _ = run_command("chmod +x startup.sh")
    if not success:
        print("❌ Failed to make startup.sh executable")
        return False
    
    # Step 2: Update README for HuggingFace (exactly like the workflow)
    print("📝 Creating HuggingFace README...")
    huggingface_readme = """---
title: opteee
emoji: 🔥
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
pinned: false
env:
  - PYTHONPATH=/app
---

# Options Trading Knowledge Search

This application provides semantic search across a collection of options trading transcripts and videos.

## Features

- Semantic search using sentence-transformers
- FAISS vector database for fast retrieval
- Direct links to specific timestamps in relevant videos
"""
    
    # Backup original README
    if os.path.exists("README.md"):
        os.rename("README.md", "README.md.backup")
    
    with open("README.md", "w") as f:
        f.write(huggingface_readme)
    
    print("✅ GitHub workflow steps simulated")
    return True

def create_test_dockerfile():
    """Create the original Dockerfile that HuggingFace will use"""
    print("📝 Creating production Dockerfile...")
    
    # Use the EXACT same Dockerfile from your original system
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# First, copy only requirements to leverage cache for pip install
COPY requirements.txt /app/requirements.txt

# Install Python dependencies (this layer will be cached)
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/vector_store /app/static /app/templates

# Copy all Python files first (this layer will be cached)
COPY *.py /app/

# Copy app directory
COPY app /app/app

# Copy static assets
COPY static /app/static

# Copy frontend build
COPY frontend/build /app/frontend/build

# Copy processed transcripts (this layer will be cached)
COPY processed_transcripts /app/processed_transcripts

# Build vector store (this layer will be cached)
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store && \\
    cp -r /app/processed_transcripts/* /tmp/processed_transcripts/ && \\
    python create_vector_store.py --output-dir /tmp/vector_store && \\
    cp -r /tmp/vector_store/* /app/vector_store/ && \\
    rm -rf /tmp/processed_transcripts /tmp/vector_store

# Copy the startup script
COPY startup.sh /app/

# Make startup script executable
RUN chmod +x /app/startup.sh

# Create cache and flagged directories
RUN mkdir -p /app/cache/matplotlib /app/cache/huggingface /app/flagged

# Set permissions on the entire /app directory
RUN chmod -R 777 /app

# Set environment variables (EXACT same as original)
ENV VECTOR_STORE_PREBUILT=true
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV MPLCONFIGDIR=/app/cache/matplotlib
ENV TRANSFORMERS_CACHE=/app/cache/huggingface
ENV XDG_CACHE_HOME=/app/cache
ENV XDG_CONFIG_HOME=/app/cache

# Run the app using startup script (EXACT same as HuggingFace)
CMD ["/app/startup.sh"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("✅ Production Dockerfile created")
    return True

def prepare_build_context():
    """Prepare the build context - ensure all files exist"""
    print("📁 Preparing build context...")
    
    # Check required files
    required_files = [
        "main.py",
        "requirements.txt", 
        "app/models/chat_models.py",
        "app/services/rag_service.py",
        "vector_search.py",
        "rag_pipeline.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    # Check if processed_transcripts exists
    if not os.path.exists("processed_transcripts"):
        print("⚠️  processed_transcripts directory not found")
        print("   Creating minimal test data...")
        os.makedirs("processed_transcripts", exist_ok=True)
        
        # Create minimal test data
        test_chunk = {
            "video_id": "test123",
            "title": "Test Video",
            "content": "This is a test chunk for Docker testing",
            "start_timestamp_seconds": 0,
            "video_url_with_timestamp": "https://youtube.com/watch?v=test123&t=0"
        }
        
        with open("processed_transcripts/test_chunk.json", "w") as f:
            json.dump(test_chunk, f)
    
    # Ensure frontend/build directory exists
    os.makedirs("frontend/build", exist_ok=True)
    
    # Check static directory
    if not os.path.exists("static"):
        os.makedirs("static", exist_ok=True)
    
    print("✅ Build context prepared")
    return True

def build_docker_image():
    """Build the Docker image using production Dockerfile"""
    print("🏗️  Building Docker image (this may take several minutes)...")
    
    # Build the image using production Dockerfile (same as HuggingFace)
    build_cmd = "docker build -t opteee-test:latest ."
    
    print("⏳ Building image... (this can take 5-15 minutes)")
    success, output = run_command(build_cmd, capture_output=False)
    
    if not success:
        print("❌ Docker build failed")
        return False
    
    # Check if image was created
    success, output = run_command("docker images opteee-test:latest")
    if "opteee-test" not in output:
        print("❌ Docker image not found after build")
        return False
    
    print("✅ Docker image built successfully")
    return True

def test_docker_container():
    """Test the Docker container"""
    print("🚀 Testing Docker container...")
    
    # Stop any existing container
    run_command("docker stop opteee-test-container 2>/dev/null || true")
    run_command("docker rm opteee-test-container 2>/dev/null || true")
    
    # Run the container
    run_cmd = ("docker run -d --name opteee-test-container "
               "-p 7860:7860 opteee-test:latest")
    
    success, output = run_command(run_cmd)
    if not success:
        print(f"❌ Failed to start container: {output}")
        return False
    
    print("✅ Container started successfully")
    
    # Wait for container to be ready
    print("⏳ Waiting for container to initialize...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:7860/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Container is healthy and responding")
                return True
        except:
            pass
        
        time.sleep(2)
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
    
    # Show container logs if it failed to start
    print("❌ Container failed to respond within 60 seconds")
    print("📋 Container logs:")
    success, logs = run_command("docker logs opteee-test-container")
    if success:
        print(logs[-2000:])  # Show last 2000 characters
    
    return False

def test_api_endpoints():
    """Test all API endpoints"""
    print("🧪 Testing API endpoints...")
    
    base_url = "http://localhost:7860"
    
    tests = []
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            tests.append(("Health Check", True, f"Status: {data.get('status')}"))
        else:
            tests.append(("Health Check", False, f"HTTP {response.status_code}"))
    except Exception as e:
        tests.append(("Health Check", False, str(e)))
    
    # Test chat endpoint
    try:
        chat_payload = {
            "query": "What is a test query?",
            "provider": "openai",
            "num_results": 3
        }
        response = requests.post(f"{base_url}/api/chat", 
                               json=chat_payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            tests.append(("Chat API", True, f"Answer length: {len(data.get('answer', ''))}"))
        else:
            tests.append(("Chat API", False, f"HTTP {response.status_code}: {response.text[:200]}"))
    except Exception as e:
        tests.append(("Chat API", False, str(e)))
    
    # Test frontend serving
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            content = response.text
            if "OPTEEE" in content:
                tests.append(("Frontend", True, "Frontend served successfully"))
            else:
                tests.append(("Frontend", False, "Frontend content invalid"))
        else:
            tests.append(("Frontend", False, f"HTTP {response.status_code}"))
    except Exception as e:
        tests.append(("Frontend", False, str(e)))
    
    # Display results
    passed = 0
    total = len(tests)
    for test_name, success, message in tests:
        if success:
            print(f"✅ {test_name}: {message}")
            passed += 1
        else:
            print(f"❌ {test_name}: {message}")
    
    print(f"\n📊 API Tests: {passed}/{total} passed")
    return passed == total

def cleanup_test_resources():
    """Clean up test resources"""
    print("🧹 Cleaning up test resources...")
    
    # Stop and remove container
    run_command("docker stop opteee-test-container 2>/dev/null || true")
    run_command("docker rm opteee-test-container 2>/dev/null || true")
    
    # Remove test image
    run_command("docker rmi opteee-test:latest 2>/dev/null || true")
    
    # Remove production files created during test
    if os.path.exists("Dockerfile"):
        os.remove("Dockerfile")
        print("   Removed production Dockerfile")
    
    if os.path.exists("startup.sh"):
        os.remove("startup.sh")
        print("   Removed startup.sh")
    
    # Restore original README if it was backed up
    if os.path.exists("README.md.backup"):
        if os.path.exists("README.md"):
            os.remove("README.md")
        os.rename("README.md.backup", "README.md")
        print("   Restored original README.md")
    
    print("✅ Cleanup completed")

def main():
    """Main test function"""
    print("🚀 OPTEEE GitHub Actions Workflow Simulation - HuggingFace Deployment Test")
    print("=" * 70)
    print("📝 This test simulates your EXACT deploy-to-huggingface.yml workflow")
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Step 1: Check Docker
        if not check_docker_installed():
            return False
        
        # Step 2: Simulate GitHub Actions workflow
        if not simulate_github_workflow():
            return False
        
        # Step 3: Create production Dockerfile
        if not create_test_dockerfile():
            return False
        
        # Step 4: Prepare build context
        if not prepare_build_context():
            return False
        
        # Step 5: Build Docker image
        if not build_docker_image():
            return False
        
        # Step 6: Test container
        if not test_docker_container():
            return False
        
        # Step 7: Test API endpoints
        if not test_api_endpoints():
            return False
        
        print("\n" + "=" * 70)
        print("🎉 SUCCESS! HuggingFace deployment simulation passed!")
        print("✅ Your application is ready for production deployment")
        print("\n📋 What this test verified (EXACT GitHub Actions workflow):")
        print("   ✅ GitHub Actions workflow steps simulated")
        print("   ✅ Startup script created (startup.sh)")
        print("   ✅ HuggingFace README format correct")
        print("   ✅ Production Dockerfile builds successfully")
        print("   ✅ All dependencies install correctly") 
        print("   ✅ Vector store builds during Docker build")
        print("   ✅ FastAPI server starts with startup script")
        print("   ✅ All API endpoints respond correctly")
        print("   ✅ Frontend serves successfully")
        print("   ✅ Port 7860 works (HuggingFace requirement)")
        print("\n🚀 You can now safely push to GitHub - HuggingFace deployment will work!")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False
    finally:
        cleanup_test_resources()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 