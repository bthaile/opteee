#!/usr/bin/env python3
"""
Advanced test script that uses selenium to extract cookies and session data
from a real browser session, then passes that to yt-dlp for downloads.
"""

import os
import time
import json
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yt_dlp

def setup_realistic_browser():
    """Set up Chrome with realistic settings to avoid detection."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    # Enhanced anti-detection measures
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # Hide webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"❌ Could not start Chrome: {e}")
        return None

def extract_cookies_from_browser(video_url):
    """Extract cookies from a browser session accessing the video."""
    print(f"🍪 Extracting cookies from browser session...")
    
    driver = setup_realistic_browser()
    if not driver:
        return None
    
    try:
        # Navigate to YouTube main page first
        driver.get("https://www.youtube.com")
        time.sleep(2)
        
        # Then navigate to the specific video
        driver.get(video_url)
        time.sleep(3)
        
        # Extract cookies
        cookies = driver.get_cookies()
        
        # Create a temporary cookie file
        cookie_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        
        # Write cookies in Netscape format for yt-dlp
        cookie_file.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            domain = cookie.get('domain', '.youtube.com')
            if not domain.startswith('.'):
                domain = '.' + domain
            
            line = f"{domain}\tTRUE\t/\t{str(cookie.get('secure', False)).upper()}\t0\t{cookie['name']}\t{cookie['value']}\n"
            cookie_file.write(line)
        
        cookie_file.close()
        print(f" Extracted {len(cookies)} cookies to {cookie_file.name}")
        return cookie_file.name
        
    except Exception as e:
        print(f"❌ Cookie extraction failed: {e}")
        return None
    finally:
        driver.quit()

def test_with_fresh_cookies(video_url, video_id):
    """Test yt-dlp with fresh cookies from browser session."""
    print(f"\n🍪 Testing with fresh browser cookies...")
    
    # Extract cookies first
    cookie_file = extract_cookies_from_browser(video_url)
    if not cookie_file:
        print("❌ Could not extract cookies")
        return False
    
    audio_path = f"test_audio_{video_id}.mp3"
    
    try:
        # Try with fresh cookies
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'outtmpl': audio_path,
            'cookiefile': cookie_file,
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'sleep_interval': 2,
            'max_sleep_interval': 5,
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("      🔄 Trying to extract info...")
            info = ydl.extract_info(video_url, download=False)
            print(f"       Info extracted: {info.get('title', 'Unknown')}")
            
            print("      🔄 Trying to download...")
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
                return False
                
    except Exception as e:
        print(f"      ❌ Failed: {e}")
        return False
    finally:
        # Clean up cookie file
        if os.path.exists(cookie_file):
            os.remove(cookie_file)

def test_alternative_formats(video_url, video_id):
    """Test alternative format selection strategies."""
    print(f"\n🎯 Testing alternative format strategies...")
    
    audio_path = f"test_audio_{video_id}.mp3"
    
    format_strategies = [
        {
            'name': 'Worst Quality Audio Only',
            'format': 'worstaudio/worst',
            'quality': '96'
        },
        {
            'name': 'Best Audio, Any Container',
            'format': 'bestaudio',
            'quality': '128'
        },
        {
            'name': 'Specific Audio Codec',
            'format': 'bestaudio[acodec^=mp4a]/bestaudio[acodec^=aac]/bestaudio',
            'quality': '128'
        },
        {
            'name': 'Low Quality Video to Audio',
            'format': 'worst[height<=480]/worst',
            'quality': '96'
        }
    ]
    
    for strategy in format_strategies:
        print(f"  🔄 Trying: {strategy['name']}")
        
        try:
            ydl_opts = {
                'format': strategy['format'],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': strategy['quality'],
                }],
                'outtmpl': audio_path,
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'referer': 'https://www.youtube.com/',
                'sleep_interval': 3,
                'max_sleep_interval': 8,
                'socket_timeout': 30,
                'retries': 3,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Just try to download directly
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
            
            # Clean analysis
            if "403" in error_msg or "Forbidden" in error_msg:
                print(f"          🚫 Still blocked")
            elif "format" in error_msg.lower():
                print(f"          📹 Format not available")
            elif "throttl" in error_msg.lower():
                print(f"          ⏳ Being throttled")
    
    return False

def main():
    """Test advanced download strategies."""
    # Load a test video
    try:
        with open('outlier_trading_videos.json', 'r') as f:
            videos = json.load(f)
        
        # Pick a different video to test
        test_video = None
        for video in videos[5:15]:  # Try videos 6-15
            if video.get('video_id'):
                test_video = video
                break
        
        if not test_video:
            print("❌ No suitable test video found")
            return
        
        video_id = test_video['video_id']
        video_url = test_video['url']
        
        print(f"🧪 Testing Advanced Download Strategies")
        print(f"📹 Video ID: {video_id}")
        print(f"🔗 URL: {video_url}")
        print(f" Title: {test_video.get('title', 'Unknown')}")
        print(f"🔄 Using updated yt-dlp version")
        
        # Test 1: Fresh cookies from browser
        success1 = test_with_fresh_cookies(video_url, video_id)
        
        # Test 2: Alternative formats
        if not success1:
            success2 = test_alternative_formats(video_url, video_id)
            
            if success2:
                print(f"\n SUCCESS! Alternative format worked for {video_id}")
            else:
                print(f"\n❌ All advanced strategies failed for {video_id}")
                print(f"💡 YouTube may have completely blocked automated access")
        else:
            print(f"\n SUCCESS! Cookie-based approach worked for {video_id}")
            
    except FileNotFoundError:
        print("❌ outlier_trading_videos.json not found. Run outlier_scraper.py first.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 