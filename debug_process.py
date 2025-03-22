import os
import json
import re
from tqdm import tqdm

# Configuration
TRANSCRIPT_DIR = "transcripts"
PROCESSED_DIR = "processed_transcripts"
METADATA_FILE = "outlier_trading_videos_metadata.json"

def main():
    print("="*80)
    print("DEBUG SCRIPT STARTING")
    print("="*80)
    
    # Check directories
    print(f"Current directory: {os.getcwd()}")
    print(f"Transcript dir exists: {os.path.exists(TRANSCRIPT_DIR)}")
    print(f"Processed dir exists: {os.path.exists(PROCESSED_DIR)}")
    print(f"Metadata file exists: {os.path.exists(METADATA_FILE)}")
    
    # List transcript files
    if os.path.exists(TRANSCRIPT_DIR):
        transcript_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith('.txt')]
        print(f"Found {len(transcript_files)} transcript files: {transcript_files}")
        
        # Check content of each file
        for filename in transcript_files:
            file_path = os.path.join(TRANSCRIPT_DIR, filename)
            file_size = os.path.getsize(file_path)
            print(f"File: {filename}, Size: {file_size} bytes")
            
            # Try to extract video ID
            base_name = os.path.splitext(filename)[0]
            youtube_id_match = re.search(r'([-\w]{11})', base_name)
            video_id = youtube_id_match.group(1) if youtube_id_match else base_name
            print(f"Extracted video ID: {video_id}")
            
            # Read part of the file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_lines = ''.join([f.readline() for _ in range(3)])
                    print(f"First few lines:\n{first_lines}")
            except Exception as e:
                print(f"Error reading file: {e}")
    
    # Check metadata
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                print(f"Loaded metadata with {len(metadata)} entries")
                print(f"First entry: {next(iter(metadata.items()))}")
        except Exception as e:
            print(f"Error loading metadata: {e}")
    
    print("="*80)
    print("DEBUG SCRIPT COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main() 