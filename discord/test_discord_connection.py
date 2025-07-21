#!/usr/bin/env python3
"""
Simple test to check if Discord API is reachable from this environment
"""
import requests
import socket
import sys

def test_dns_resolution():
    """Test DNS resolution for discord.com"""
    try:
        result = socket.gethostbyname('discord.com')
        print(f"✅ DNS Resolution: discord.com -> {result}")
        return True
    except Exception as e:
        print(f"❌ DNS Resolution Failed: {e}")
        return False

def test_discord_api():
    """Test Discord API connectivity"""
    try:
        response = requests.get('https://discord.com/api/v10/gateway', timeout=10)
        print(f"✅ Discord API: Status {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Discord API Failed: {e}")
        return False

def test_generic_https():
    """Test generic HTTPS connectivity"""
    try:
        response = requests.get('https://httpbin.org/get', timeout=10)
        print(f"✅ HTTPS Works: Status {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ HTTPS Failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Discord Connectivity from Container...")
    print("=" * 50)
    
    dns_ok = test_dns_resolution()
    https_ok = test_generic_https() 
    discord_ok = test_discord_api()
    
    print("\n📋 Results:")
    print(f"DNS Resolution: {'✅' if dns_ok else '❌'}")
    print(f"HTTPS General: {'✅' if https_ok else '❌'}")  
    print(f"Discord API: {'✅' if discord_ok else '❌'}")
    
    if not discord_ok and https_ok:
        print("\n🚫 CONCLUSION: Discord specifically blocked by platform")
        sys.exit(1)
    elif not https_ok:
        print("\n🌐 CONCLUSION: General network connectivity issue")  
        sys.exit(1)
    else:
        print("\n✅ CONCLUSION: Discord should work!")
        sys.exit(0) 