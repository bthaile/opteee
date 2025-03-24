#!/bin/bash

echo "===== Starting application setup ====="
echo "Current directory: $(pwd)"
echo "Listing files:"
ls -la

# Check if processed transcripts exist
echo "Checking for processed transcripts..."
if [ -d "processed_transcripts" ]; then
  echo "✅ Found local processed_transcripts directory"
  # Copy to tmp directory for write access
  echo "Copying transcripts to /tmp/processed_transcripts..."
  mkdir -p /tmp/processed_transcripts
  cp -r processed_transcripts/* /tmp/processed_transcripts/
  echo "✅ Copied $(ls -1 /tmp/processed_transcripts | wc -l) transcript files"
else
  echo "❌ No local processed_transcripts directory found"
  # Look for transcripts in other locations
  if [ -d "/tmp/processed_transcripts" ] && [ "$(ls -A /tmp/processed_transcripts)" ]; then
    echo "✅ Found transcripts in /tmp/processed_transcripts"
  else
    echo "❌ No transcripts found! Vector store cannot be built."
    echo "Please make sure processed transcript files are included in your deployment."
  fi
fi

# Make sure all directories are writable
echo "Setting permissions..."
chmod -R 777 /tmp

# Build the vector store
echo "===== Building vector store ====="
python create_vector_store.py

# Check if vector store was built
if [ -f "/tmp/vector_store/transcript_index.faiss" ]; then
  echo "✅ Vector store built successfully!"
else
  echo "❌ Vector store build failed!"
fi

# Start the Flask app
echo "===== Starting Flask application ====="
python app.py 