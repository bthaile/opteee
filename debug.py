#!/usr/bin/env python
import os
import sys
import subprocess
from datetime import datetime

print(f"===== DEBUG SCRIPT at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

print("\nFILES IN CURRENT DIRECTORY:")
for root, dirs, files in os.walk('.', topdown=True):
    for file in files:
        full_path = os.path.join(root, file)
        size = os.path.getsize(full_path)
        print(f"  - {full_path} ({size} bytes)")

print("\nENVIRONMENT VARIABLES:")
for key, value in sorted(os.environ.items()):
    print(f"  {key}={value}")

print("\nINSTALLED PYTHON PACKAGES:")
subprocess.call([sys.executable, "-m", "pip", "list"])

print("\nPYTHON PATH:")
for path in sys.path:
    print(f"  - {path}")

# Try to create the gradio_app module directly
with open('gradio_app.py', 'w') as f:
    f.write("""
# Direct creation of gradio_app module
import gradio as gr
import os
import threading
from datetime import datetime

print(f"===== CREATED gradio_app.py Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")

# Create a minimal Flask app
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Options Trading Knowledge Search is running!"

# Function to run Flask
def run_flask():
    app.run(host="0.0.0.0", port=7860)

# Start Flask app in background
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
print(" Flask app started in background thread")

# Create Gradio interface
def empty_fn():
    return "Application is running!"

# Create and export the interface
demo = gr.Interface(
    fn=empty_fn,
    inputs=None,
    outputs=gr.Textbox(),
    title="Options Trading Knowledge Search",
    description="This is a minimal version created directly by debug.py"
)

# Export what Hugging Face is looking for
gradio_app = demo
""")

print("\n Created gradio_app.py directly")

# Try running the main command that would normally be run
print("\nTrying to run gradio_app module:")
try:
    from gradio_app import gradio_app
    print(" Successfully imported gradio_app")
except Exception as e:
    print(f"❌ Error importing gradio_app: {e}")
    import traceback
    traceback.print_exc() 