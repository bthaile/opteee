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
    print("🔍 Testing health endpoint...")
    
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
    print("\n🔍 Testing chat endpoint...")
    
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
    print("\n🔍 Testing chat endpoint with invalid request...")
    
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

def test_frontend_serving():
    """Test that the frontend is served correctly"""
    print("\n🔍 Testing frontend serving...")
    
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
    print("🚀 Starting FastAPI Backend Tests")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        test_health_endpoint,
        test_chat_endpoint,
        test_invalid_chat_request,
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