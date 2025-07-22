#!/usr/bin/env python3
"""
Test script to verify transcript downloading methods work correctly.
Tests a single video with all available methods.
"""

import os
import json
from dotenv import load_dotenv
from transcript_downloader import TranscriptDownloader

# Load environment variables
load_dotenv()

def test_single_video():
    """Test transcript downloading with a single video."""
    
    # Use a known public video for testing
    test_video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - widely available
    test_video_id = "dQw4w9WgXcQ"
    
    print("🧪 Testing Transcript Downloader")
    print("=" * 50)
    print(f"Test video: {test_video_url}")
    print(f"Video ID: {test_video_id}")
    
    # Create downloader instance
    downloader = TranscriptDownloader()
    
    # Test each method individually
    print("\n Testing YouTube Transcript API...")
    transcript_api_result = downloader.get_transcript_via_transcript_api(test_video_id)
    if transcript_api_result:
        print(f" Success! Found {len(transcript_api_result)} segments")
        print(f"First segment: {transcript_api_result[0]['text'][:100]}...")
    else:
        print("❌ No transcript found via YouTube Transcript API")
    
    print("\n Testing yt-dlp subtitle extraction...")
    ytdlp_result = downloader.get_transcript_via_yt_dlp(test_video_url)
    if ytdlp_result:
        print(f" Success! Found {len(ytdlp_result)} segments")
        print(f"First segment: {ytdlp_result[0]['text'][:100]}...")
    else:
        print("❌ No transcript found via yt-dlp")
    
    print("\n Testing Whisper transcription...")
    if downloader.whisper_model:
        whisper_result = downloader.download_audio_and_transcribe(test_video_url, test_video_id)
        if whisper_result:
            print(f" Success! Found {len(whisper_result)} segments")
            print(f"First segment: {whisper_result[0]['text'][:100]}...")
        else:
            print("❌ Whisper transcription failed")
    else:
        print("⚠️  Whisper not available")
    
    print("\n📊 Test Summary:")
    print(f"YouTube Transcript API: {'' if transcript_api_result else '❌'}")
    print(f"yt-dlp subtitles: {'' if ytdlp_result else '❌'}")
    print(f"Whisper: {'' if downloader.whisper_model and whisper_result else '❌'}")

def test_with_your_videos():
    """Test with a few videos from your collection."""
    
    if not os.path.exists("outlier_trading_videos.json"):
        print("❌ outlier_trading_videos.json not found. Please run outlier_scraper.py first.")
        return
    
    with open("outlier_trading_videos.json", 'r', encoding='utf-8') as f:
        videos = json.load(f)
    
    print(f"\n🎯 Testing with your videos ({len(videos)} total)")
    print("=" * 50)
    
    # Test first 3 videos
    test_videos = videos[:3]
    
    downloader = TranscriptDownloader()
    
    for i, video in enumerate(test_videos):
        video_id = downloader.get_video_id(video.get('url'))
        print(f"\n📹 Test {i+1}: {video.get('title', 'Unknown')}")
        print(f"Video ID: {video_id}")
        
        # Test transcript API
        transcript = downloader.get_transcript_via_transcript_api(video_id)
        if transcript:
            print(f" YouTube Transcript API: {len(transcript)} segments")
        else:
            print("❌ YouTube Transcript API: No transcript")
        
        # Test yt-dlp
        transcript = downloader.get_transcript_via_yt_dlp(video.get('url'))
        if transcript:
            print(f" yt-dlp subtitles: {len(transcript)} segments")
        else:
            print("❌ yt-dlp subtitles: No transcript")

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Test with sample video")
    print("2. Test with your videos")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_single_video()
    elif choice == "2":
        test_with_your_videos()
    else:
        print("Invalid choice. Running both tests...")
        test_single_video()
        test_with_your_videos() 