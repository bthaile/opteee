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

# Try to import from config, but fall back to default values if not found
try:
    from config import PROCESSED_DIR, VECTOR_DIR, MODEL_NAME, BATCH_SIZE, DEFAULT_TOP_K
    print("✅ Successfully imported config module")
except ImportError:
    print("⚠️ Could not import config module, using defaults")
    # Use /tmp directory which should be writable
    PROCESSED_DIR = "/tmp/processed_transcripts"
    VECTOR_DIR = "/tmp/vector_store"
    MODEL_NAME = "all-MiniLM-L6-v2"
    BATCH_SIZE = 32
    DEFAULT_TOP_K = 5
    
    # Create these directories if they don't exist
    try:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        os.makedirs(VECTOR_DIR, exist_ok=True)
        print(f"✅ Created directories: {PROCESSED_DIR} and {VECTOR_DIR}")
    except Exception as e:
        print(f"⚠️ Directory creation error: {e}")

# ===== Inline vector_search functions =====
# Try to import from vector_search module, but define functions inline if not found
try:
    from vector_search import semantic_search, vector_store_exists, build_vector_store
    print("✅ Successfully imported vector_search module")
except ImportError:
    print("⚠️ Could not import vector_search module, using inline functions")
    
    def vector_store_exists():
        """Check if vector store files exist (simplified)"""
        print("Using simplified vector_store_exists function")
        return False
    
    def build_vector_store():
        """Build vector store (simplified)"""
        print("Using simplified build_vector_store function")
        return True
    
    def semantic_search(query, top_k=5):
        """Perform semantic search (simplified)"""
        print(f"Using simplified semantic_search function with query: {query}")
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
    # Add more sample data as needed
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

# All-in-one Flask application with no external dependencies
from flask import Flask, request, render_template, jsonify
import os
import sys
import json
from datetime import datetime
import random
import threading

# Print diagnostic information
print(f"===== Application Startup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Directory contents: {os.listdir()}")

# ===== Configuration (directly in app.py) =====
MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 5
BATCH_SIZE = 32

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

# All-in-one application with Flask and Gradio
import os
import sys
import json
from datetime import datetime
import random
import threading

print(f"===== Application Startup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")

# Configure fallbacks for missing modules
# Try to import from config, but fall back to default values if not found
try:
    from config import PROCESSED_DIR, VECTOR_DIR, MODEL_NAME, BATCH_SIZE, DEFAULT_TOP_K
    print("✅ Successfully imported config module")
except ImportError:
    print("⚠️ Could not import config module, using defaults")
    # Use /tmp directory which should be writable
    PROCESSED_DIR = "/tmp/processed_transcripts"
    VECTOR_DIR = "/tmp/vector_store"
    MODEL_NAME = "all-MiniLM-L6-v2"
    BATCH_SIZE = 32
    DEFAULT_TOP_K = 5
    
    # Create these directories if they don't exist
    import os
    try:
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        os.makedirs(VECTOR_DIR, exist_ok=True)
        print(f"✅ Created directories: {PROCESSED_DIR} and {VECTOR_DIR}")
    except Exception as e:
        print(f"⚠️ Directory creation error: {e}")

# Try to import from vector_search module, but define functions inline if not found
try:
    from vector_search import semantic_search, vector_store_exists, build_vector_store
    print("✅ Successfully imported vector_search module")
except ImportError:
    print("⚠️ Could not import vector_search module, using inline functions")
    
    def vector_store_exists():
        """Check if vector store files exist (simplified)"""
        print("Using simplified vector_store_exists function")
        return False
    
    def build_vector_store():
        """Build vector store (simplified)"""
        print("Using simplified build_vector_store function")
        return True
    
    def semantic_search(query, top_k=5):
        """Perform semantic search (simplified)"""
        print(f"Using simplified semantic_search function with query: {query}")
        return []

# Try to import gradio, install if needed
try:
    import gradio as gr
    print("✅ Successfully imported gradio")
    HAS_GRADIO = True
except ImportError:
    print("⚠️ Gradio not available, will try to install")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio==3.50.2"])
        import gradio as gr
        print("✅ Successfully installed and imported gradio")
        HAS_GRADIO = True
    except Exception as e:
        print(f"❌ Could not install gradio: {e}")
        HAS_GRADIO = False

# Import Flask
from flask import Flask, request, render_template, jsonify

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

# Function to create and start Gradio interface
def create_gradio_interface():
    """Create a Gradio interface that embeds the Flask app"""
    if not HAS_GRADIO:
        print("❌ Cannot create Gradio interface - gradio not available")
        return None
    
    try:
        # Start Flask in a thread
        def run_flask():
            app.run(host="0.0.0.0", port=7860)
        
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        print("✅ Started Flask server in background thread")
        
        # Create Gradio interface
        with gr.Blocks() as demo:
            gr.Markdown("# Options Trading Knowledge Search")
            gr.Markdown("## Using Flask Application")
            
            # Use HTML to embed the Flask app
            html = """
            <iframe 
                id="flask-app-frame" 
                style="width:100%; height:600px; border:1px solid #ddd;" 
                src="">
            </iframe>
            
            <script>
                // Update iframe src after a delay
                setTimeout(function() {
                    var iframe = document.getElementById('flask-app-frame');
                    iframe.src = window.location.protocol + '//' + window.location.hostname + ':7860';
                }, 1000);
            </script>
            """
            gr.HTML(html)
        
        return demo
    
    except Exception as e:
        print(f"❌ Error creating Gradio interface: {e}")
        import traceback
        traceback.print_exc()
        return None

# Main entry point
if __name__ == '__main__':
    print("Starting application...")
    
    try:
        # First try to create and start Gradio (which will also start Flask in a thread)
        demo = create_gradio_interface()
        if demo:
            print("✅ Launching Gradio interface (with embedded Flask app)")
            demo.launch(server_name="0.0.0.0", server_port=7861)
        else:
            # Fall back to just Flask if Gradio fails
            print("⚠️ Gradio not available, starting Flask directly")
            app.run(host="0.0.0.0", port=7860)
            
    except Exception as e:
        print(f"❌ Error in main: {e}")
        import traceback
        traceback.print_exc()
        
        # Last resort - try to start Flask directly
        try:
            print("Attempting to start Flask directly as last resort")
            app.run(host="0.0.0.0", port=7860)
        except Exception as e2:
            print(f"❌ Fatal error: {e2}")

# Combined Flask and Gradio application for Hugging Face Spaces
import os
import sys
import json
from datetime import datetime
import random
import threading

print(f"===== Application Startup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")

# Set up configuration variables directly
PROCESSED_DIR = "/tmp/processed_transcripts"
VECTOR_DIR = "/tmp/vector_store"

# Create directories
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)
print(f"✅ Created directories: {PROCESSED_DIR} and {VECTOR_DIR}")

# Import Flask
from flask import Flask, request, render_template, jsonify

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

# Define simplified vector search functions
def vector_store_exists():
    """Check if vector store files exist (simplified)"""
    return False

def build_vector_store():
    """Build vector store (simplified)"""
    return True

def semantic_search(query, top_k=5):
    """Perform semantic search (simplified)"""
    return []

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
    vector_status = "✅ Available" if vector_store_exists() else "❌ Not Available"
    
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
    """Search endpoint"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            "results": [],
            "message": "Please provide a search query"
        })
    
    # Use simple search
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

# Flask app runner
def run_flask():
    app.run(host="0.0.0.0", port=7860)

# IMPORTANT: Create a Gradio app to wrap the Flask app
import gradio as gr

def launch_flask_app():
    """Function that launches the Flask app in a separate thread"""
    import threading
    threading.Thread(target=run_flask, daemon=True).start()
    return "Flask app is running on port 7860!"

# Create a Gradio interface that wraps the Flask app
gradio_app = gr.Interface(
    fn=launch_flask_app,
    inputs=None,
    outputs=gr.Textbox(),
    title="Options Trading Knowledge Search",
    description="This Gradio app launches a Flask application for searching options trading knowledge."
)

# This is what Hugging Face Spaces looks for
if __name__ == "__main__":
    # Start the Flask app in a background thread
    threading.Thread(target=run_flask, daemon=True).start()
    print("✅ Flask app started in background thread")
    
    # Launch the Gradio app
    gradio_app.launch() 