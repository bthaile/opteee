import sys
import os
from datetime import datetime

print(f"===== Gradio Wrapper Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")

try:
    import gradio as gr
    print("✅ Successfully imported gradio")
    
    # Create Flask app (we'll directly import and run it)
    from app import app as flask_app
    print("✅ Successfully imported Flask app")
    
    # Create a simple Gradio interface that acts as a proxy to the Flask app
    with gr.Blocks() as demo:
        gr.Markdown("# Options Trading Knowledge Search")
        gr.Markdown("Loading Flask application...")
        
        # Use an iframe to display the Flask app
        iframe = """
        <iframe 
            id="flask-app-frame" 
            style="width:100%; height:600px; border:none;" 
            src="http://localhost:7860">
        </iframe>
        
        <script>
            // After 1 second, reload the iframe to make sure it loads after Flask starts
            setTimeout(function() {
                document.getElementById('flask-app-frame').src = window.location.href.replace(':7861', ':7860');
            }, 1000);
        </script>
        """
        gr.HTML(iframe)
    
    # Start Flask in a separate thread
    import threading
    
    def run_flask():
        flask_app.run(host='0.0.0.0', port=7860)
    
    # Start Flask thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("✅ Flask app started in background thread")
    
    # Start Gradio on a different port
    demo.launch(server_name="0.0.0.0", server_port=7861, share=False)
    
except Exception as e:
    print(f"❌ Error in Gradio wrapper: {e}")
    import traceback
    traceback.print_exc()
    
    # Try to run the Flask app directly as a fallback
    try:
        print("Attempting to run Flask app directly...")
        from app import app as flask_app
        flask_app.run(host='0.0.0.0', port=7860)
    except Exception as e2:
        print(f"❌ Also failed to run Flask directly: {e2}")
        traceback.print_exc() 