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
import json

# Import our vector search module
from config import PROCESSED_DIR, VECTOR_DIR
from vector_search import semantic_search, vector_store_exists, build_vector_store

# Create Flask app
app = Flask(__name__)

# Sample data for demonstration
SAMPLE_TRANSCRIPTS = [
    # ... existing sample transcripts ...
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

# Check if there's any file that might be auto-imported
for filename in os.listdir():
    if filename.endswith('.py') and filename != 'app.py':
        print(f"Potential import file found: {filename}")

# Try to create a minimal Flask app without any problematic imports
try:
    from flask import Flask, render_template
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return render_template('index.html', 
                             flask_version="2.0.1",
                             python_version=sys.version.split()[0],
                             timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             file_list="Debug mode",
                             static_files="Debug mode",
                             template_files="Debug mode",
                             vector_status="Debug mode",
                             transcript_count=0,
                             building_vector_store=False)
    
    # No problematic imports here
    if __name__ == '__main__':
        print("Starting minimal Flask app...")
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 7860)))

except Exception as e:
    print(f"Error in minimal Flask app: {e}")
    import traceback
    traceback.print_exc() 