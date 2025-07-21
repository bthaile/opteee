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

def test_custom_dns_resolver():
    """Test comprehensive custom DNS resolver approach with proper async context"""
    try:
        import asyncio
        import aiohttp
        from aiohttp.resolver import AsyncResolver
        
        async def test_comprehensive_resolver():
            print("🔧 Setting up custom DNS resolver in async context...")
            
            # Create custom DNS resolver with multiple servers
            resolver = AsyncResolver(nameservers=['8.8.8.8', '8.8.4.4', '1.1.1.1'])
            connector = aiohttp.TCPConnector(
                resolver=resolver,
                ttl_dns_cache=300,
                use_dns_cache=True,
                limit=100,
                limit_per_host=30,
                enable_cleanup_closed=True
            )
            
            print("✅ Custom DNS resolver created in async context")
            
            try:
                # Create session with our custom DNS resolver
                session = aiohttp.ClientSession(
                    connector=connector,
                    timeout=aiohttp.ClientTimeout(total=30)
                )
                
                print("✅ Custom DNS session created")
                
                try:
                    # Test 1: Discord API endpoint
                    print("🔍 Testing Discord API with custom DNS resolver...")
                    async with session.get('https://discord.com/api/v10/gateway', timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            print(f"✅ Custom DNS: Discord API reachable (Status {response.status})")
                            gateway_url = data.get('url', '')
                            print(f"✅ Gateway URL: {gateway_url}")
                            
                            # Test 2: Gateway WebSocket endpoint hostname resolution
                            if gateway_url:
                                import urllib.parse
                                parsed = urllib.parse.urlparse(gateway_url)
                                gateway_host = parsed.hostname
                                
                                print(f"🔍 Testing gateway hostname resolution: {gateway_host}")
                                
                                # Test direct hostname resolution with our resolver
                                try:
                                    # Use the resolver directly to test hostname resolution
                                    resolved_hosts = await resolver.resolve(gateway_host, 443)
                                    if resolved_hosts:
                                        print(f"✅ Custom DNS: Gateway {gateway_host} resolved successfully")
                                        # Try to show some IP addresses if available
                                        for i, host_info in enumerate(resolved_hosts[:3]):  # Show first 3
                                            if hasattr(host_info, 'host'):
                                                print(f"   → IP {i+1}: {host_info.host}")
                                            else:
                                                print(f"   → Record {i+1}: {host_info}")
                                    else:
                                        print(f"⚠️ Custom DNS: Gateway {gateway_host} resolved but no hosts returned")
                                        
                                except Exception as gateway_error:
                                    print(f"⚠️ Custom DNS: Gateway resolution error: {gateway_error}")
                                    # Try simpler approach - just test if we can make a basic request to the gateway
                                    try:
                                        # Extract just the base URL for testing
                                        test_url = f"https://{gateway_host}/"
                                        async with session.get(test_url, timeout=5) as gw_response:
                                            print(f"✅ Custom DNS: Gateway {gateway_host} accessible via HTTP (Status: {gw_response.status})")
                                    except Exception as simple_test_error:
                                        print(f"⚠️ Custom DNS: Gateway {gateway_host} not accessible: {simple_test_error}")
                            
                            return True
                        else:
                            print(f"❌ Custom DNS: Discord API returned status {response.status}")
                            return False
                            
                except asyncio.TimeoutError:
                    print(f"❌ Custom DNS Resolver: Connection timeout to Discord API")
                    return False
                except Exception as e:
                    print(f"❌ Custom DNS Resolver request failed: {e}")
                    return False
                
                finally:
                    # Clean up session
                    if not session.closed:
                        await session.close()
                        print("✅ Cleaned up custom DNS session")
                        
            finally:
                # Clean up connector
                await connector.close()
                print("✅ Cleaned up custom DNS connector")
            
        # Run the comprehensive async test with proper event loop handling
        try:
            # Try to use existing event loop if available
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Create a new loop for our test if one is already running
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, test_comprehensive_resolver())
                    return future.result()
            else:
                return loop.run_until_complete(test_comprehensive_resolver())
        except RuntimeError:
            # No event loop exists, create a new one
            return asyncio.run(test_comprehensive_resolver())
        
    except ImportError as e:
        print(f"❌ Custom DNS Resolver dependencies not available: {e}")
        print(f"💡 Required: pip install aiohttp aiodns")
        return False
    except Exception as e:
        print(f"❌ Custom DNS Resolver test setup failed: {e}")
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
    
    print("\n🧪 Testing Custom DNS Resolver Approach...")
    custom_dns_ok = test_custom_dns_resolver()
    
    print("\n📋 Results:")
    print(f"DNS Resolution: {'✅' if dns_ok else '❌'}")
    print(f"HTTPS General: {'✅' if https_ok else '❌'}")  
    print(f"Discord API: {'✅' if discord_ok else '❌'}")
    print(f"Custom DNS Resolver: {'✅' if custom_dns_ok else '❌'}")
    
    if custom_dns_ok:
        print("\n🎉 CONCLUSION: Custom DNS resolver successfully bypassed system DNS!")
        print("💡 Discord bot should work with custom aiohttp resolver")
        sys.exit(0)
    elif not discord_ok and https_ok and not dns_ok:
        print("\n🚫 CONCLUSION: System DNS cannot resolve discord.com")
        print("💡 Custom DNS resolver also failed - may need different approach")
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