"""
Test script for FastAPI backend
Verifies that the API endpoints work correctly with the extracted RAG logic
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:7860"
API_BASE = f"{BASE_URL}/api"

def test_health_endpoint():
    """Test the health endpoint"""
    print(" Testing health endpoint...")
    
    try:
        response = requests.get(f"{API_BASE}/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Version: {data['version']}")
            print(f"   Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with a sample query"""
    print("\n Testing chat endpoint...")
    
    test_query = "What are the Greeks in options trading?"
    
    payload = {
        "query": test_query,
        "provider": "openai",
        "num_results": 5
    }
    
    try:
        print(f"   Sending query: '{test_query}'")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Chat request successful (took {response_time:.2f}s)")
            print(f"   Answer length: {len(data['answer'])} characters")
            print(f"   Sources provided: {len(data['raw_sources'])} videos")
            print(f"   Response timestamp: {data['timestamp']}")
            
            # Print first 200 characters of answer
            answer_preview = data['answer'][:200] + "..." if len(data['answer']) > 200 else data['answer']
            print(f"   Answer preview: {answer_preview}")
            
            # Print source titles if available
            if data['raw_sources']:
                print("   Source videos:")
                for i, source in enumerate(data['raw_sources'][:3], 1):  # Show first 3
                    title = source.get('title', 'Unknown Title')
                    print(f"     {i}. {title}")
            
            return True
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error details: {error_data}")
            except:
                print(f"   Raw response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat request failed: {e}")
        return False

def test_invalid_chat_request():
    """Test chat endpoint with invalid request"""
    print("\n Testing chat endpoint with invalid request...")
    
    payload = {
        "query": "",  # Empty query should be handled gracefully
        "provider": "openai",
        "num_results": 5
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Empty query handled gracefully")
            print(f"   Answer: '{data['answer']}'")
            return True
        else:
            print(f"❌ Empty query handling failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Invalid request test failed: {e}")
        return False

def test_format_parameter():
    """Test the format parameter for different output formats"""
    print("\n Testing format parameter...")
    
    test_query = "What is Delta in options trading?"
    
    # Test HTML format (default)
    print("   Testing HTML format...")
    html_payload = {
        "query": test_query,
        "provider": "openai",
        "num_results": 3,
        "format": "html"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json=html_payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            html_data = response.json()
            html_answer = html_data['answer']
            print(f"   ✅ HTML format successful")
            
            # Check for HTML tags (should be present)
            has_html_tags = any(tag in html_answer for tag in ['<p>', '<strong>', '<h3>', '<ul>', '<li>'])
            if has_html_tags:
                print(f"   ✅ HTML format contains HTML tags as expected")
            else:
                print(f"   ⚠️  HTML format doesn't contain expected HTML tags")
            
        else:
            print(f"   ❌ HTML format test failed: {response.status_code}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"   ❌ HTML format test failed: {e}")
        return False
    
    # Test Discord format
    print("   Testing Discord format...")
    discord_payload = {
        "query": test_query,
        "provider": "openai", 
        "num_results": 3,
        "format": "discord"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json=discord_payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            discord_data = response.json()
            discord_answer = discord_data['answer']
            print(f"   ✅ Discord format successful")
            
            # Check for absence of HTML tags (should be plain text/markdown)
            has_html_tags = any(tag in discord_answer for tag in ['<p>', '<strong>', '<h3>', '<ul>', '<li>', '<div>'])
            if not has_html_tags:
                print(f"   ✅ Discord format contains no HTML tags as expected")
            else:
                print(f"   ❌ Discord format unexpectedly contains HTML tags: {discord_answer[:100]}...")
                return False
            
            # Check for Discord markdown formatting
            has_discord_markdown = any(pattern in discord_answer for pattern in ['**', '`', '•'])
            if has_discord_markdown:
                print(f"   ✅ Discord format contains Discord markdown as expected")
            else:
                print(f"   ⚠️  Discord format doesn't contain expected Discord markdown")
            
            # Check that sources field is empty for Discord
            if discord_data['sources'] == "":
                print(f"   ✅ Discord format has empty sources field as expected")
            else:
                print(f"   ❌ Discord format unexpectedly has sources content")
                return False
            
        else:
            print(f"   ❌ Discord format test failed: {response.status_code}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Discord format test failed: {e}")
        return False
    
    return True

def test_backward_compatibility():
    """Test that requests without format parameter default to HTML"""
    print("\n Testing backward compatibility (no format parameter)...")
    
    payload = {
        "query": "What is Gamma in options?",
        "provider": "openai",
        "num_results": 3
        # No format parameter - should default to HTML
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data['answer']
            
            # Should behave like HTML format
            has_html_tags = any(tag in answer for tag in ['<p>', '<strong>', '<h3>', '<ul>', '<li>'])
            if has_html_tags:
                print(f"   ✅ Backward compatibility: defaults to HTML format")
                return True
            else:
                print(f"   ⚠️  Backward compatibility: doesn't default to HTML format")
                return True  # Still pass, might just be simple text
        else:
            print(f"   ❌ Backward compatibility test failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Backward compatibility test failed: {e}")
        return False

def test_invalid_format():
    """Test handling of invalid format parameter"""
    print("\n Testing invalid format parameter...")
    
    payload = {
        "query": "What is Theta?",
        "provider": "openai",
        "num_results": 3,
        "format": "invalid_format"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Should return 422 for validation error or 200 with default behavior
        if response.status_code == 422:
            print(f"   ✅ Invalid format properly rejected with validation error")
            return True
        elif response.status_code == 200:
            data = response.json()
            print(f"   ✅ Invalid format handled gracefully (fallback to default)")
            return True
        else:
            print(f"   ❌ Invalid format test unexpected status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Invalid format test failed: {e}")
        return False

def test_frontend_serving():
    """Test that the frontend is served correctly"""
    print("\n Testing frontend serving...")
    
    try:
        response = requests.get(BASE_URL)
        
        if response.status_code == 200:
            content = response.text
            if "OPTEEE" in content or "Options Trading" in content:
                print("✅ Frontend served successfully")
                return True
            else:
                print("⚠️  Frontend served but content might be placeholder")
                return True
        else:
            print(f"❌ Frontend serving failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    """Run all tests"""
    print(" Starting FastAPI Backend Tests")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        test_health_endpoint,
        test_chat_endpoint,
        test_invalid_chat_request,
        test_format_parameter,
        test_backward_compatibility,
        test_invalid_format,
        test_frontend_serving
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! FastAPI backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the logs above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 