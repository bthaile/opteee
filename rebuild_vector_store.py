"""
Rebuild Vector Store

This script checks if transcripts are newer than the vector store and rebuilds it if needed.
It's designed to run at app startup on Hugging Face Spaces.
"""
import os
import sys
import time
import glob
import json
import pickle
from datetime import datetime
import argparse  # Import argparse for creating an args object

# Import vector store creation function directly
try:
    # First try to import as a module
    import create_vector_store
    create_vector_store_main = create_vector_store.main
except (ImportError, AttributeError) as e:
    print(f"❌ Could not import create_vector_store module: {str(e)}")
    try:
        # If that fails, try to import the main function directly
        from create_vector_store import main as create_vector_store_main
    except ImportError as e:
        print(f"❌ Could not import main from create_vector_store: {str(e)}")
        create_vector_store_main = None

# Paths
VECTOR_STORE_DIR = "vector_store"
VECTOR_STORE_META_FILE = os.path.join(VECTOR_STORE_DIR, "transcript_metadata.pkl")
TRANSCRIPTS_DIR = "processed_transcripts"
VECTOR_STORE_TIMESTAMP_FILE = os.path.join(VECTOR_STORE_DIR, "last_updated.txt")

def get_latest_transcript_timestamp():
    """Get the timestamp of the most recently modified transcript file"""
    transcript_files = glob.glob(os.path.join(TRANSCRIPTS_DIR, "*.json"))
    
    if not transcript_files:
        print("⚠️ No transcript files found")
        return 0
    
    # Get the latest modification time of any transcript file
    latest_timestamp = 0
    for file_path in transcript_files:
        mtime = os.path.getmtime(file_path)
        if mtime > latest_timestamp:
            latest_timestamp = mtime
    
    return latest_timestamp

def get_vector_store_timestamp():
    """Get the timestamp when the vector store was last updated"""
    if not os.path.exists(VECTOR_STORE_TIMESTAMP_FILE):
        return 0
    
    try:
        with open(VECTOR_STORE_TIMESTAMP_FILE, 'r') as f:
            timestamp_str = f.read().strip()
            return float(timestamp_str)
    except (ValueError, IOError):
        return 0

def update_vector_store_timestamp():
    """Update the timestamp file with the current time"""
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    
    with open(VECTOR_STORE_TIMESTAMP_FILE, 'w') as f:
        f.write(str(time.time()))

def is_rebuild_needed():
    """Check if the vector store needs to be rebuilt"""
    # If the vector store doesn't exist, it needs to be built
    if not os.path.exists(VECTOR_STORE_META_FILE):
        print("⚠️ Vector store doesn't exist, rebuild needed")
        return True
    
    # Get timestamps
    vector_store_time = get_vector_store_timestamp()
    transcript_time = get_latest_transcript_timestamp()
    
    # Convert to human-readable format for logging
    vector_time_str = datetime.fromtimestamp(vector_store_time).strftime('%Y-%m-%d %H:%M:%S') if vector_store_time > 0 else "never"
    transcript_time_str = datetime.fromtimestamp(transcript_time).strftime('%Y-%m-%d %H:%M:%S') if transcript_time > 0 else "none found"
    
    print(f"Vector store last updated: {vector_time_str}")
    print(f"Latest transcript modified: {transcript_time_str}")
    
    # If transcripts are newer than the vector store, rebuild is needed
    return transcript_time > vector_store_time

def count_transcripts():
    """Count the number of transcript files"""
    transcript_files = glob.glob(os.path.join(TRANSCRIPTS_DIR, "*.json"))
    return len(transcript_files)

def main():
    """Main function to check and rebuild the vector store if needed"""
    print("=" * 50)
    print("CHECKING VECTOR STORE STATUS")
    print("=" * 50)
    
    # Check if transcripts directory exists
    if not os.path.exists(TRANSCRIPTS_DIR):
        print(f"❌ Transcripts directory ({TRANSCRIPTS_DIR}) not found")
        return False
    
    # Count transcripts
    num_transcripts = count_transcripts()
    print(f"Found {num_transcripts} transcript files")
    
    if num_transcripts == 0:
        print("❌ No transcript files found, cannot build vector store")
        return False
    
    # Check if rebuild is needed
    if not is_rebuild_needed():
        print("✅ Vector store is up to date")
        return True
    
    print("\n" + "=" * 50)
    print("REBUILDING VECTOR STORE")
    print("=" * 50)
    
    # Make sure vector store directory exists
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    
    # Rebuild vector store
    try:
        # Create an argparse.Namespace object with default values
        args = argparse.Namespace()
        args.model = "all-MiniLM-L6-v2"  # Default model
        args.batch_size = 32  # Default batch size
        args.test_search = False  # Don't run test search during rebuild
        
        if create_vector_store_main is None:
            raise ImportError("No create_vector_store function available")
            
        create_vector_store_main(args)
        update_vector_store_timestamp()
        print("✅ Vector store rebuilt successfully")
        return True
    except Exception as e:
        print(f"❌ Error rebuilding vector store: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 