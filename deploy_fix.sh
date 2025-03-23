#!/bin/bash

echo "===== Starting Happy Face deployment fix - $(date) ====="

# Fix package versions
echo "Installing specific package versions..."
pip uninstall -y huggingface-hub transformers sentence-transformers
pip install huggingface-hub==0.17.3
pip install transformers==4.30.2
pip install sentence-transformers==2.2.2

# Make sure we have the vector store directory
echo "Checking vector store..."
if [ ! -d "vector_store" ]; then
    echo "Creating vector store directory..."
    mkdir -p vector_store
fi

# If there's a backup, restore it
if [ -d "vector_store_backup" ] && [ "$(ls -A vector_store_backup)" ]; then
    echo "Restoring vector store from backup..."
    cp -r vector_store_backup/* vector_store/
    echo "Vector store restored from backup."
    
    # Create a timestamp file to avoid rebuild
    echo "$(date +%s)" > vector_store/last_updated.txt
fi

echo "===== Happy Face deployment fix completed - $(date) ====="

# Run the application
echo "Starting the application..."
python app.py 