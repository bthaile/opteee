#!/bin/bash

echo "===== Starting application setup ====="

# Check for transcript files
if [ -d "processed_transcripts" ]; then
  echo "✅ Found processed_transcripts directory"
  mkdir -p /tmp/processed_transcripts
  cp -r processed_transcripts/* /tmp/processed_transcripts/ || echo "Error copying files"
  echo "Copied transcripts to /tmp/processed_transcripts"
else
  echo "❌ No processed_transcripts directory found"
  exit 1
fi

# Set permissions
chmod -R 777 /tmp

# Build the vector store
echo "===== Building vector store ====="
python -c "from vector_search import build_vector_store; build_vector_store()"

# Start the Gradio app
echo "===== Starting Gradio app ====="
python app.py 