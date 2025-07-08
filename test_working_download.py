#!/usr/bin/env python3
"""
Test script that uses the working cookie-based approach with fixed file naming.
"""

import os
import time
import json
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yt_dlp

def setup_browser():
    """Set up Chrome for cookie extraction."""
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
        return None

def extract_cookies_from_browser(video_url):
    """Extract cookies from a browser session."""
    print(f"🍪 Extracting cookies from browser session...")
    
    driver = setup_browser()
    if not driver:
        return None
    
    try:
        # Navigate to YouTube first
        driver.get("https://www.youtube.com")
        time.sleep(2)
        
        # Then to the video
        driver.get(video_url)
        time.sleep(3)
        
        # Extract cookies
        cookies = driver.get_cookies()
        
        # Create cookie file
        cookie_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        cookie_file.write("# Netscape HTTP Cookie File\n")
        
        for cookie in cookies:
            domain = cookie.get('domain', '.youtube.com')
            if not domain.startswith('.'):
                domain = '.' + domain
            
            line = f"{domain}\tTRUE\t/\t{str(cookie.get('secure', False)).upper()}\t0\t{cookie['name']}\t{cookie['value']}\n"
            cookie_file.write(line)
        
        cookie_file.close()
        print(f"✅ Extracted {len(cookies)} cookies")
        return cookie_file.name
        
    except Exception as e:
        print(f"❌ Cookie extraction failed: {e}")
        return None
    finally:
        driver.quit()

def download_single_video(video_url, video_id, output_dir="audio_files"):
    """Download a single video with the working approach."""
    print(f"📥 Testing download for {video_id}")
    
    # Extract cookies
    cookie_file = extract_cookies_from_browser(video_url)
    if not cookie_file:
        print("❌ Could not extract cookies")
        return False
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Fixed output template (no extension in template)
    output_template = os.path.join(output_dir, f"{video_id}.%(ext)s")
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'outtmpl': output_template,
            'cookiefile': cookie_file,
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'sleep_interval': 2,
            'max_sleep_interval': 5,
            'extract_flat': False,
            'writesubtitles': False,
            'writeautomaticsub': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("  🔄 Downloading...")
            ydl.download([video_url])
            
            # Check what files were created
            expected_file = os.path.join(output_dir, f"{video_id}.mp3")
            if os.path.exists(expected_file):
                size_mb = os.path.getsize(expected_file) / (1024 * 1024)
                print(f"  ✅ Downloaded: {expected_file} ({size_mb:.1f} MB)")
                return True
            else:
                # Check for other possible filenames
                for ext in ['mp3', 'webm', 'm4a', 'ogg']:
                    alt_file = os.path.join(output_dir, f"{video_id}.{ext}")
                    if os.path.exists(alt_file):
                        size_mb = os.path.getsize(alt_file) / (1024 * 1024)
                        print(f"  ✅ Downloaded: {alt_file} ({size_mb:.1f} MB)")
                        return True
                
                print(f"  ❌ No output file found")
                return False
                
    except Exception as e:
        print(f"  ❌ Download failed: {e}")
        return False
    finally:
        # Clean up cookie file
        if os.path.exists(cookie_file):
            os.remove(cookie_file)

def main():
    """Test the working download approach."""
    try:
        with open('outlier_trading_videos.json', 'r') as f:
            videos = json.load(f)
        
        # Test with a few different videos
        test_videos = []
        for video in videos[1:6]:  # Test videos 2-6
            if video.get('video_id'):
                test_videos.append(video)
        
        print(f"🧪 Testing Working Download Approach")
        print(f"📹 Testing {len(test_videos)} videos with updated yt-dlp")
        print(f"🔄 Using cookie-based approach (no more 403 errors!)")
        
        successes = 0
        for i, video in enumerate(test_videos, 1):
            video_id = video['video_id']
            video_url = video['url']
            title = video.get('title', 'Unknown')
            
            print(f"\n📹 Video {i}/{len(test_videos)}: {video_id}")
            print(f"   📝 Title: {title}")
            
            success = download_single_video(video_url, video_id)
            if success:
                successes += 1
                print(f"   ✅ SUCCESS!")
            else:
                print(f"   ❌ Failed")
            
            # Small delay between videos
            time.sleep(5)
        
        print(f"\n📊 Results: {successes}/{len(test_videos)} videos downloaded successfully")
        
        if successes > 0:
            print(f"🎉 BREAKTHROUGH! Found working approach!")
            print(f"💡 Key factors:")
            print(f"   - Updated yt-dlp to latest version")
            print(f"   - Extract cookies from real browser session")
            print(f"   - Use proper output template")
            print(f"   - Anti-detection browser settings")
            
            # Show files created
            print(f"\n📁 Files created:")
            for file in os.listdir("audio_files"):
                if file.endswith('.mp3'):
                    size_mb = os.path.getsize(os.path.join("audio_files", file)) / (1024 * 1024)
                    print(f"   - {file} ({size_mb:.1f} MB)")
        else:
            print(f"❌ No downloads succeeded")
            
    except FileNotFoundError:
        print("❌ outlier_trading_videos.json not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 