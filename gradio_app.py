# This is the module that Hugging Face is looking for
import gradio as gr
import os
import sys
import threading
from datetime import datetime

print(f"===== gradio_app.py Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")

# Create a minimal Flask app for our search functionality
from flask import Flask, request, render_template, jsonify

# Set up writable directories
PROCESSED_DIR = "/tmp/processed_transcripts"
VECTOR_DIR = "/tmp/vector_store"
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)

# Create a simple Flask app
app = Flask(__name__)

# Sample data
SAMPLE_TRANSCRIPTS = [
    {
        "title": "Options Trading Basics",
        "timestamp": "05:23",
        "video_url": "https://example.com/video1?t=323",
        "content": "Options give you the right, but not the obligation, to buy or sell an underlying asset."
    }
]

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

@app.route('/api/search')
def search_api():
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'semantic').strip()
    
    if not query:
        return jsonify({"results": [], "message": "Please provide a search query"})
    
    # Return sample results
    results = [
        {
            "title": "Options Trading Basics",
            "timestamp": "05:23",
            "video_url": "https://example.com/video",
            "content": f"This is a sample text result for query: {query}. Options give you the right, but not the obligation, to buy or sell an underlying asset.",
            "score": 0.95,
            "duration": "15:30"
        },
        {
            "title": "Call Options Explained",
            "timestamp": "10:15",
            "video_url": "https://example.com/video2",
            "content": "A call option gives the holder the right to buy an asset at a specified price within a specific time period.",
            "score": 0.88,
            "duration": "12:45"
        },
        {
            "title": "Put Options Strategies",
            "timestamp": "07:45",
            "video_url": "https://example.com/video3",
            "content": "Put options are financial contracts that give the buyer the right to sell an asset at a specified price within a specific time period.",
            "score": 0.82,
            "duration": "18:20"
        }
    ]
    
    return jsonify({
        "results": results,
        "query": query,
        "search_type": search_type
    })

# Function to run Flask in background
def run_flask():
    app.run(host="0.0.0.0", port=7860)

# Start Flask app in background thread
threading.Thread(target=run_flask, daemon=True).start()
print("✅ Flask app started in background thread")

# Create a Gradio interface that wraps the Flask app
def empty_fn():
    return "Options Trading Knowledge Search is running at port 7860!"

# Create the gradio interface
demo = gr.Interface(
    fn=empty_fn,
    inputs=None,
    outputs=gr.Textbox(),
    title="Options Trading Knowledge Search",
    description="The application is running on port 7860. This Gradio interface is just a wrapper."
)

# This is what Hugging Face specifically looks for
gradio_app = demo 