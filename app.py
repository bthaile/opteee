"""
Entry point for Hugging Face Spaces.
This file checks and rebuilds the vector store if needed, then runs the Gradio app.
"""
import os
import sys
import subprocess

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