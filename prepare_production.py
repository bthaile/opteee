#!/usr/bin/env python3
"""
Prepare Production Files - Creates files needed for HuggingFace deployment
Simulates GitHub Actions workflow without requiring Docker to be running
"""

import os
import json

def create_startup_script():
    """Create startup.sh script exactly like GitHub Actions"""
    print(" Creating startup.sh script...")
    
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
    os.chmod("startup.sh", 0o755)
    print("✅ startup.sh created and made executable")

def create_production_dockerfile():
    """Create Dockerfile for production deployment"""
    print(" Creating production Dockerfile...")
    
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

# Set environment variables
ENV VECTOR_STORE_PREBUILT=true
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV MPLCONFIGDIR=/app/cache/matplotlib
ENV TRANSFORMERS_CACHE=/app/cache/huggingface
ENV XDG_CACHE_HOME=/app/cache
ENV XDG_CONFIG_HOME=/app/cache

# Run the app using startup script
CMD ["/app/startup.sh"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("✅ Dockerfile created")

def create_huggingface_readme():
    """Create README.md for HuggingFace deployment"""
    print(" Creating HuggingFace README...")
    
    # Backup original README
    if os.path.exists("README.md"):
        os.rename("README.md", "README.md.backup")
        print("   Backed up original README.md")
    
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
    
    with open("README.md", "w") as f:
        f.write(huggingface_readme)
    
    print("✅ HuggingFace README.md created")

def ensure_required_directories():
    """Ensure all required directories exist"""
    print("📁 Ensuring required directories exist...")
    
    dirs_to_create = [
        "frontend/build",
        "static",
        "processed_transcripts"
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
    
    # Create minimal test data if processed_transcripts is empty
    if not os.listdir("processed_transcripts"):
        print("   Creating minimal test data in processed_transcripts...")
        test_chunk = {
            "video_id": "test123",
            "title": "Test Video",
            "content": "This is a test chunk for Docker testing",
            "start_timestamp_seconds": 0,
            "video_url_with_timestamp": "https://youtube.com/watch?v=test123&t=0"
        }
        
        with open("processed_transcripts/test_chunk.json", "w") as f:
            json.dump(test_chunk, f)
    
    print("✅ Required directories ensured")

def check_required_files():
    """Check that all required files exist"""
    print(" Checking required files...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "app/models/chat_models.py", 
        "app/services/rag_service.py",
        "vector_search.py",
        "rag_pipeline.py",
        "create_vector_store.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def main():
    """Main function to prepare production files"""
    print(" OPTEEE Production File Preparation")
    print("=" * 50)
    print(" Creating files needed for HuggingFace deployment")
    print()
    
    try:
        # Check required files exist
        if not check_required_files():
            return False
        
        # Ensure directories exist
        ensure_required_directories()
        
        # Create production files
        create_startup_script()
        create_production_dockerfile()
        create_huggingface_readme()
        
        print("\n" + "=" * 50)
        print("🎉 SUCCESS! Production files prepared")
        print("\n📋 Files created:")
        print("   ✅ startup.sh - Application startup script")
        print("   ✅ Dockerfile - Production Docker image")
        print("   ✅ README.md - HuggingFace format (original backed up)")
        print("\n Next steps:")
        print("   1. Start Docker Desktop")
        print("   2. Run: ./run_local.sh")
        print("   3. Test at http://localhost:7860")
        print("   4. If all works: git add . && git commit && git push")
        print("\n💡 Your existing run_local.sh script will handle the Docker build and run!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error preparing production files: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 