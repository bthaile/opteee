#!/usr/bin/env python3
"""
Test script for downloading YouTube videos using headless browser approach.
This simulates a real user session to avoid YouTube's anti-bot detection.
"""

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yt_dlp

def setup_browser():
    """Set up Chrome in headless mode with realistic settings."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Anti-detection measures
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"❌ Could not start Chrome: {e}")
        print("💡 Install ChromeDriver: brew install chromedriver")
        return None

def test_browser_access(video_url):
    """Test if we can access YouTube video with browser."""
    print(f"🌐 Testing browser access to: {video_url}")
    
    driver = setup_browser()
    if not driver:
        return False
    
    try:
        # Navigate to video
        driver.get(video_url)
        time.sleep(3)
        
        # Check if page loaded successfully
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ytd-video-primary-info-renderer"))
            )
            title = title_element.text
            print(f" Successfully accessed video: {title}")
            
            # Check if there are any error messages
            error_messages = driver.find_elements(By.CSS_SELECTOR, ".yt-alert-message")
            if error_messages:
                for msg in error_messages:
                    print(f"⚠️ Warning: {msg.text}")
            
            return True
            
        except Exception as e:
            print(f"❌ Could not find video title: {e}")
            # Check for specific error pages
            page_source = driver.page_source
            if "Video unavailable" in page_source:
                print("❌ Video is unavailable")
            elif "private video" in page_source.lower():
                print("❌ Video is private")
            elif "removed" in page_source.lower():
                print("❌ Video has been removed")
            return False
            
    except Exception as e:
        print(f"❌ Browser access failed: {e}")
        return False
    finally:
        driver.quit()

def test_yt_dlp_strategies(video_url, video_id):
    """Test different yt-dlp strategies with realistic browser simulation."""
    print(f"\n🔧 Testing yt-dlp strategies for: {video_id}")
    
    audio_path = f"test_audio_{video_id}.mp3"
    
    strategies = [
        {
            'name': 'Standard with Browser Headers',
            'options': {
                'format': 'bestaudio[ext=mp3]/bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',
                }],
                'outtmpl': audio_path,
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'referer': 'https://www.youtube.com/',
            }
        },
        {
            'name': 'With Cookies and Headers',
            'options': {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',
                }],
                'outtmpl': audio_path,
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'referer': 'https://www.youtube.com/',
                'cookiefile': 'youtube_cookies.txt' if os.path.exists('youtube_cookies.txt') else None,
                'sleep_interval': 2,
                'max_sleep_interval': 5,
            }
        },
        {
            'name': 'Mobile User Agent',
            'options': {
                'format': 'bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '96',
                }],
                'outtmpl': audio_path,
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
                'sleep_interval': 3,
                'max_sleep_interval': 8,
            }
        }
    ]
    
    for strategy in strategies:
        print(f"\n  🔄 Trying: {strategy['name']}")
        
        try:
            with yt_dlp.YoutubeDL(strategy['options']) as ydl:
                # First, try to extract info without downloading
                info = ydl.extract_info(video_url, download=False)
                print(f"       Successfully extracted video info")
                print(f"      📹 Title: {info.get('title', 'Unknown')}")
                print(f"      ⏱️ Duration: {info.get('duration', 'Unknown')} seconds")
                
                # Now try to download
                ydl.download([video_url])
                
                # Check if file was created
                if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
                    size_mb = os.path.getsize(audio_path) / (1024 * 1024)
                    print(f"       Downloaded successfully: {size_mb:.1f} MB")
                    
                    # Clean up test file
                    os.remove(audio_path)
                    return True
                else:
                    print(f"      ❌ File not created or too small")
                    
        except Exception as e:
            error_msg = str(e)
            print(f"      ❌ Failed: {error_msg}")
            
            # Analyze error type
            if "403" in error_msg or "Forbidden" in error_msg:
                print(f"          🚫 HTTP 403 - Still being blocked")
            elif "429" in error_msg:
                print(f"          ⏳ Rate limited")
            elif "unavailable" in error_msg.lower():
                print(f"          📹 Video unavailable")
            elif "private" in error_msg.lower():
                print(f"          🔒 Video is private")
    
    return False

def main():
    """Test single video download with different approaches."""
    # Load a test video from our list
    try:
        with open('outlier_trading_videos.json', 'r') as f:
            videos = json.load(f)
        
        # Pick a video that should work (not one of the known failures)
        test_video = None
        for video in videos[:10]:  # Check first 10 videos
            if video.get('video_id') and video.get('video_id') not in ['nLC0tmrc_ao', 'CzPirDlJWgM', '2jG5SD-3F0w', 'hny9FtaPG9o', 'dBD1IkHNlGY']:
                test_video = video
                break
        
        if not test_video:
            print("❌ No suitable test video found")
            return
        
        video_id = test_video['video_id']
        video_url = test_video['url']
        
        print(f"🧪 Testing single video download")
        print(f"📹 Video ID: {video_id}")
        print(f"🔗 URL: {video_url}")
        print(f" Title: {test_video.get('title', 'Unknown')}")
        
        # Test 1: Browser access
        browser_success = test_browser_access(video_url)
        
        # Test 2: yt-dlp strategies
        if browser_success:
            print(f"\n🔧 Browser access successful, testing yt-dlp...")
            ytdlp_success = test_yt_dlp_strategies(video_url, video_id)
            
            if ytdlp_success:
                print(f"\n SUCCESS! Found working approach for {video_id}")
            else:
                print(f"\n❌ All yt-dlp strategies failed for {video_id}")
        else:
            print(f"\n❌ Browser access failed - video may be unavailable")
            
    except FileNotFoundError:
        print("❌ outlier_trading_videos.json not found. Run outlier_scraper.py first.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 