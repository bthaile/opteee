#!/bin/bash

# This script fixes dependency issues on Hugging Face Spaces
echo "===== Fixing dependencies for Hugging Face Spaces ====="

# Update huggingface_hub to a compatible version
pip install --upgrade huggingface_hub>=0.19.3

# Install transformers and sentence-transformers with compatible versions
pip install --upgrade transformers>=4.35.0
pip install --upgrade sentence-transformers>=2.3.0

# Create necessary directories if they don't exist
mkdir -p vector_store transcripts processed_transcripts

# Check if vector store already exists
echo "===== Checking vector store status ====="
if [ -f "vector_store/transcript_index.faiss" ] && [ -f "vector_store/transcript_metadata.pkl" ]; then
    echo "✅ Vector store files found"
else
    echo "⚠️ Vector store doesn't exist"
    # Since we have processed transcripts, we can try to rebuild
    if [ -d "processed_transcripts" ] && [ "$(ls -A processed_transcripts)" ]; then
        echo "📄 Processed transcripts found, attempting to rebuild vector store..."
        python create_vector_store.py
    else
        echo "❌ No processed transcripts available"
    fi
fi

echo "===== Dependency fix completed ====="

# Run the application
echo "Starting the application..."
python app.py 