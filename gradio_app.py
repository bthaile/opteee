import sys
import os
from datetime import datetime

print(f"===== Gradio Wrapper Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")

# Install gradio if not already installed
try:
    import gradio as gr
    print("✅ Gradio is already installed")
except ImportError:
    print("⚠️ Gradio not found, attempting to install")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio==3.50.2"])
    import gradio as gr
    print("✅ Successfully installed gradio")

# Start Flask app in background
def start_flask_app():
    try:
        import threading
        from app import app
        
        def run_flask():
            app.run(host="0.0.0.0", port=7860)
        
        # Start Flask in a thread
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        print("✅ Flask app started in background thread")
        return True
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")
        import traceback
        traceback.print_exc()
        return False

# Create a simple Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Options Trading Knowledge Search")
    gr.Markdown("## Loading Flask application...")
    
    # Use HTML to embed the Flask application
    html_content = """
    <div style="text-align: center; margin: 20px 0;">
        <p>The Flask application is running at port 7860.</p>
        <p>Loading the application in an iframe below:</p>
    </div>
    
    <iframe 
        id="flask-app-frame" 
        style="width:100%; height:600px; border:1px solid #ddd; border-radius: 8px;" 
        src="">
    </iframe>
    
    <script>
        // Set the iframe source to the current hostname with port 7860
        function updateIframeSource() {
            var iframe = document.getElementById('flask-app-frame');
            var host = window.location.hostname;
            iframe.src = window.location.protocol + '//' + host + ':7860';
            console.log('Set iframe source to: ' + iframe.src);
        }
        
        // Try to update immediately and also after a delay
        updateIframeSource();
        setTimeout(updateIframeSource, 2000);
    </script>
    """
    
    # Display the HTML
    gr.HTML(html_content)

# Start Flask app when Gradio loads
start_flask_app()

# Launch Gradio interface on port 7861
try:
    demo.launch(server_name="0.0.0.0", server_port=7861)
except Exception as e:
    print(f"❌ Error launching Gradio interface: {e}")
    # If Gradio fails, try to start Flask directly as a fallback
    try:
        from app import app
        print("Falling back to direct Flask execution")
        app.run(host="0.0.0.0", port=7860)
    except Exception as e2:
        print(f"❌ Also failed to run Flask directly: {e2}")

# Simple redirector to app.py
print("gradio_app.py redirecting to app.py...")
import app 