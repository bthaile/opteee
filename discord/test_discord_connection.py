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
        # Try alternative test
        try:
            import subprocess
            result = subprocess.run(['nslookup', 'discord.com'], capture_output=True, text=True, timeout=5)
            output = result.stdout + result.stderr
            
            # Check if nslookup actually resolved (not just exit code)
            if "No answer" in output or "can't find" in output or "NXDOMAIN" in output:
                print(f"❌ nslookup failed to resolve: {output.strip()}")
                return False
            elif "Address:" in output and any(c.isdigit() for c in output):
                print(f"✅ nslookup resolved discord.com successfully")
                return True
            else:
                print(f"❌ nslookup unclear result: {output.strip()}")
                return False
        except Exception as ns_error:
            print(f"❌ nslookup test failed: {ns_error}")
        return False

def test_discord_api():
    """Test Discord API connectivity"""
    try:
        # Simple GET request to Discord API
        response = requests.get('https://discord.com/api/v10/gateway', timeout=5)
        print(f"✅ Discord API: Status {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Discord Gateway URL: {response.json().get('url', 'Unknown')}")
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
    
    if not discord_ok and https_ok and not dns_ok:
        print("\n🚫 CONCLUSION: HuggingFace DNS server cannot resolve discord.com")
        print("💡 DNS server responds but says 'No answer' for Discord domains")
        print("🔧 Attempting /etc/hosts fallback in startup script")
        sys.exit(1)
    elif not discord_ok and https_ok and dns_ok:
        print("\n🚫 CONCLUSION: Discord API blocked (DNS works but API fails)")
        sys.exit(1)
    elif not https_ok:
        print("\n🌐 CONCLUSION: General network connectivity issue")  
        sys.exit(1)
    else:
        print("\n✅ CONCLUSION: Discord should work!")
        sys.exit(0) 