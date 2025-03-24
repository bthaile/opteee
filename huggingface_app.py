# Explicit entry point for Hugging Face - Flask app only
print("===== Starting Flask Application =====")
print("Note: This is a Flask app, not a Gradio app")

# Import Flask application
try:
    from app import app
    
    # Run the app
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=7860)
        
except ImportError as e:
    print(f"Error importing app: {e}")
    print("Available modules:", sys.modules.keys())
    raise 