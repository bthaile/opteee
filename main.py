# Brand new entry point to avoid any caching issues
from flask import Flask, request, render_template, jsonify
import os
import sys
import json
from datetime import datetime
import random
import threading

# Print diagnostic information
print(f"===== NEW ENTRY POINT at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir()}")

# ===== Configuration (formerly in config.py) =====
PROCESSED_DIR = "processed_transcripts"
VECTOR_DIR = "vector_store"
MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 5
BATCH_SIZE = 32

# Ensure directories exist
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)

# ===== Vector Search Functions (simplified) =====
def vector_store_exists():
    """Check if vector store files exist"""
    # Simplified implementation
    return False

def build_vector_store():
    """Build or rebuild the vector store from processed transcripts"""
    # Simplified implementation
    print("Building vector store (simplified implementation)")
    return True

def semantic_search(query, top_k=5):
    """Perform semantic search using the vector store"""
    # Simplified implementation - return empty results
    return []

# Create Flask app
app = Flask(__name__)

# Sample data for demonstration
SAMPLE_TRANSCRIPTS = [
    {
        "title": "Options Trading Basics",
        "timestamp": "05:23",
        "video_url": "https://example.com/video1?t=323",
        "content": "Options give you the right, but not the obligation, to buy or sell an underlying asset."
    }
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

# Routes
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

def simple_search(query, data, top_k=5):
    """Simple keyword-based search on the sample data"""
    if not query or not data:
        return []
    
    # Split query into terms
    terms = query.lower().split()
    
    results = []
    for item in data:
        # Simple scoring based on term frequency
        score = 0
        content_lower = item["content"].lower()
        title_lower = item["title"].lower()
        
        for term in terms:
            if len(term) > 2:  # Only consider terms with more than 2 characters
                # Give more weight to title matches
                title_count = title_lower.count(term)
                content_count = content_lower.count(term)
                score += (title_count * 2) + content_count
        
        if score > 0:
            results.append({
                "title": item["title"],
                "timestamp": item["timestamp"],
                "video_url": item["video_url"],
                "content": item["content"],
                "score": score / max(1, len(terms))  # Normalize by number of terms
            })
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Return top k results
    return results[:top_k]

@app.route('/api/search')
def search_api():
    """Enhanced search endpoint that tries vector search first, then fallback to simple search"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            "results": [],
            "message": "Please provide a search query"
        })
    
    # Fallback to simple search
    results = simple_search(query, SAMPLE_TRANSCRIPTS)
    
    return jsonify({
        "results": results,
        "query": query,
        "search_type": "keyword"
    })

@app.route('/api/status')
def status_api():
    """API endpoint for checking application status"""
    # Update status
    app_status["vector_store_available"] = vector_store_exists()
    app_status["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Count transcript files
    transcript_count = 0
    if os.path.exists(PROCESSED_DIR):
        transcript_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
        transcript_count = len(transcript_files)
    app_status["transcript_count"] = transcript_count
    
    return jsonify(app_status)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 7860))) 