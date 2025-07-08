#!/bin/bash
# Batch download script for failed videos
# This script downloads all failed videos using yt-dlp

echo "🎵 Downloading failed videos using yt-dlp..."
echo "================================================"

# Check if yt-dlp is installed
if ! command -v yt-dlp &> /dev/null; then
    echo "❌ yt-dlp not found. Installing..."
    pip install yt-dlp
fi

# Create audio_files directory if it doesn't exist
mkdir -p audio_files

# Count total failed videos
total_videos=$(ls audio_files/*.note.txt 2>/dev/null | wc -l)
echo "📊 Found $total_videos failed videos to download"
echo

# Download each failed video
count=0
for note_file in audio_files/*.note.txt; do
    if [ -f "$note_file" ]; then
        # Extract video ID from filename
        video_id=$(basename "$note_file" .note.txt)
        url="https://www.youtube.com/watch?v=$video_id"
        
        count=$((count + 1))
        echo "[$count/$total_videos] Downloading: $video_id"
        
        # Download audio only, save as MP3
        yt-dlp --extract-audio --audio-format mp3 \
               --output "audio_files/%(id)s.%(ext)s" \
               "$url" 2>/dev/null
        
        # Check if download was successful
        if [ -f "audio_files/$video_id.mp3" ]; then
            # Get file size
            size=$(stat -f%z "audio_files/$video_id.mp3" 2>/dev/null || stat -c%s "audio_files/$video_id.mp3" 2>/dev/null)
            if [ "$size" -gt 10000 ]; then
                echo "  ✅ Success: $video_id.mp3 (${size} bytes)"
                # Remove the note file since we succeeded
                rm "$note_file"
            else
                echo "  ⚠️ Small file: $video_id.mp3 (${size} bytes) - may be dummy"
            fi
        else
            echo "  ❌ Failed: $video_id"
        fi
        
        # Small delay to avoid rate limiting
        sleep 1
    fi
done

echo
echo "================================================"
echo "✅ Download process complete!"
echo "📊 Check audio_files/ directory for downloaded files"
echo "🔄 Run 'python3 run_pipeline.py --step transcripts' to process" 