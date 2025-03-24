"""
Entry point for Hugging Face Spaces.
This file checks and rebuilds the vector store if needed, then runs the Gradio app.
"""
import os
import sys
import subprocess
from flask import Flask, request, render_template, jsonify
from datetime import datetime
import random
import threading

# First, check if vector store needs rebuilding
print("Checking and updating vector store...")
try:
    import rebuild_vector_store
    rebuild_success = rebuild_vector_store.main()
    if not rebuild_success:
        print("⚠️ Vector store rebuild failed or not needed. This might affect app functionality.")
    else:
        print("✅ Vector store is ready")
except Exception as e:
    print(f"⚠️ Warning: Vector store check error: {str(e)}")

# Then import and run the Gradio app
try:
    from gradio_app import demo
    
    # Launch the app
    if __name__ == "__main__":
        demo.launch()
except Exception as e:
    print(f"❌ Error starting Gradio app: {str(e)}")
    sys.exit(1)

# Flask application with detailed error logging
import sys
import os

# Debug startup
print("===== Application Startup at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "=====")
print("Python version:", sys.version)
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

try:
    from flask import Flask, request, render_template, jsonify
    import json
    from datetime import datetime
    import random
    import threading
    
    # Print modules before potential error
    print("Successfully imported Flask modules")
    
    try:
        # Import our vector search module
        from config import PROCESSED_DIR, VECTOR_DIR
        from vector_search import semantic_search, vector_store_exists, build_vector_store
        print("Successfully imported vector search modules")
    except ImportError as e:
        print(f"⚠️ Warning: Vector search module import error: {e}")
        # Create fallback variables if imports fail
        PROCESSED_DIR = "processed_transcripts"
        VECTOR_DIR = "vector_store"
        
    # Create Flask app
    app = Flask(__name__)

    # Sample data for demonstration
    SAMPLE_TRANSCRIPTS = [
        # ... existing code ...
    ]

    # Application status tracking
    app_status = {
        "vector_store_available": False,
        "building_vector_store": False,
        "transcript_count": 0,
        "vector_count": 0,
        "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    def check_and_build_vector_store():
        """Check vector store status and build if needed"""
        app_status["vector_store_available"] = vector_store_exists()
        
        # If vector store doesn't exist and we're not already building it
        if not app_status["vector_store_available"] and not app_status["building_vector_store"]:
            # Start a background thread to build the vector store
            threading.Thread(target=build_vector_store_background).start()

    def build_vector_store_background():
        """Build vector store in a background thread"""
        try:
            app_status["building_vector_store"] = True
            success = build_vector_store()
            app_status["vector_store_available"] = success
        finally:
            app_status["building_vector_store"] = False
            app_status["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check vector store on startup
    @app.route('/')
    def home():
        """Render the home page"""
        # Check vector store status
        try:
            check_and_build_vector_store()
        except Exception as e:
            print(f"⚠️ Warning: Vector store check error: {e}")
        
        # Get system info for the Info tab
        flask_version = "2.0.1"  # Hardcoded for simplicity
        python_version = sys.version.split()[0]
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get directory listing
        app_files = sorted([f for f in os.listdir() if os.path.isfile(f)])
        static_files = []
        if os.path.exists('static'):
            static_files = sorted(os.listdir('static'))
        template_files = []
        if os.path.exists('templates'):
            template_files = sorted(os.listdir('templates'))
        
        # Check vector store
        vector_status = "✅ Available" if vector_store_exists() else "🚧 Building" if app_status["building_vector_store"] else "❌ Not Available"
        
        # Count transcript files
        transcript_count = 0
        if os.path.exists(PROCESSED_DIR):
            transcript_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
            transcript_count = len(transcript_files)
        
        return render_template(
            'index.html', 
            flask_version=flask_version,
            python_version=python_version,
            timestamp=timestamp,
            file_list=', '.join(app_files[:10]) + ('...' if len(app_files) > 10 else ''),
            static_files=', '.join(static_files[:5]) + ('...' if len(static_files) > 5 else ''),
            template_files=', '.join(template_files[:5]) + ('...' if len(template_files) > 5 else ''),
            vector_status=vector_status,
            transcript_count=transcript_count,
            building_vector_store=app_status["building_vector_store"]
        ) 

except Exception as e:
    print(f"❌ Critical error in app initialization: {e}")
    import traceback
    traceback.print_exc() 