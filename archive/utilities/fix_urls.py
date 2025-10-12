import os
import json
import re
import glob

PROCESSED_DIR = "processed_transcripts"

def fix_urls_in_file(file_path):
    print(f"Processing file: {file_path}")
    
    # Load the JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get video ID from filename
    filename = os.path.basename(file_path)
    video_id_match = re.search(r'([-\w]{11})_processed\.json', filename)
    video_id = video_id_match.group(1) if video_id_match else None
    
    if not video_id:
        print(f"Could not extract video ID from filename: {filename}")
        return False
    
    changes_made = False
    
    # Process each chunk in the file
    for chunk in data:
        metadata = chunk.get('metadata', {})
        
        # Fix video_id if needed
        if metadata.get('video_id') != video_id:
            metadata['video_id'] = video_id
            changes_made = True
        
        # Fix main URL if needed
        correct_url = f"https://www.youtube.com/watch?v={video_id}"
        if metadata.get('url') != correct_url:
            metadata['url'] = correct_url
            changes_made = True
        
        # Fix timestamp URL
        timestamp_seconds = metadata.get('start_timestamp_seconds', 0)
        correct_ts_url = f"https://www.youtube.com/watch?v={video_id}&t={int(timestamp_seconds)}"
        if metadata.get('video_url_with_timestamp') != correct_ts_url:
            metadata['video_url_with_timestamp'] = correct_ts_url
            changes_made = True
    
    # Save changes if needed
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Fixed URLs in {file_path}")
        return True
    else:
        print(f"No changes needed for {file_path}")
        return False

def main():
    print("Starting URL fixing process...")
    
    if not os.path.exists(PROCESSED_DIR):
        print(f"Directory {PROCESSED_DIR} does not exist!")
        return
    
    # Get all JSON files in the processed directory
    json_files = glob.glob(os.path.join(PROCESSED_DIR, "*_processed.json"))
    print(f"Found {len(json_files)} processed transcript files")
    
    if not json_files:
        print("No files to process. Exiting.")
        return
    
    # Process each file
    fixed_count = 0
    for file_path in json_files:
        if fix_urls_in_file(file_path):
            fixed_count += 1
    
    print(f"Fixed URLs in {fixed_count} out of {len(json_files)} files")

if __name__ == "__main__":
    main() 