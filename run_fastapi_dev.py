#!/usr/bin/env python3
"""
Development script to run the FastAPI version of OPTEEE
This replaces the original Gradio app for testing
"""

import os
import sys
import subprocess
import threading
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        print(" FastAPI dependencies found")
        return True
    except ImportError:
        print("❌ FastAPI dependencies not found")
        print("   Please install with: pip install -r requirements-fastapi.txt")
        return False

def check_rag_dependencies():
    """Check if RAG dependencies are available"""
    try:
        import vector_search
        import rag_pipeline
        print(" RAG dependencies found")
        return True
    except ImportError as e:
        print(f"❌ RAG dependencies not found: {e}")
        print("   Make sure vector_search.py and rag_pipeline.py are available")
        return False

def check_vector_store():
    """Check if vector store exists"""
    vector_store_path = "/app/vector_store/faiss.index"
    local_vector_store_path = "vector_store"
    
    if os.path.exists(vector_store_path) or os.path.exists(local_vector_store_path):
        print(" Vector store found")
        return True
    else:
        print("⚠️  Vector store not found")
        print("   The app will warn about this but should still start")
        return True  # Don't fail, just warn

def run_fastapi_server():
    """Run the FastAPI server"""
    print(" Starting FastAPI server...")
    
    try:
        import uvicorn
        from main import app
        
        # Run uvicorn server
        uvicorn.run(
            app,
            host="0.0.0.0", 
            port=7860,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start FastAPI server: {e}")
        return False

def run_tests_after_startup():
    """Run tests after server startup"""
    print("⏳ Waiting for server to start...")
    time.sleep(5)  # Wait for server to be ready
    
    print("🧪 Running API tests...")
    try:
        result = subprocess.run([sys.executable, "test_fastapi.py"], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        if result.returncode == 0:
            print(" All tests passed!")
        else:
            print("⚠️  Some tests failed")
            
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")

def main():
    """Main development script"""
    print(" OPTEEE FastAPI Development Server")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return False
        
    if not check_rag_dependencies():
        return False
        
    check_vector_store()
    
    print("\n🌐 Starting server on http://localhost:7860")
    print("📚 API documentation will be available at http://localhost:7860/docs")
    print(" Health check: http://localhost:7860/api/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start tests in background thread
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_thread = threading.Thread(target=run_tests_after_startup)
        test_thread.daemon = True
        test_thread.start()
    
    try:
        # Run the server
        run_fastapi_server()
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
        return True
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 