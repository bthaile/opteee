"""
Script to download and setup vector store on Hugging Face Spaces
"""
import os
import sys
import requests
import tarfile
from io import BytesIO
import subprocess

# URL to your vector store (upload to Dropbox/Google Drive/etc)
VECTOR_STORE_URL = "YOUR_VECTOR_STORE_DOWNLOAD_URL"  # Replace with your actual URL

def download_vector_store():
    """Download vector store from external source"""
    print("Downloading vector store from external source...")
    try:
        response = requests.get(VECTOR_STORE_URL, stream=True)
        response.raise_for_status()
        
        # Create a file-like object from the response content
        fileobj = BytesIO(response.content)
        
        # Extract the tar file
        with tarfile.open(fileobj=fileobj, mode="r:gz") as tar:
            tar.extractall(path=".")
        
        print(" Vector store downloaded and extracted successfully")
        return True
    except Exception as e:
        print(f"❌ Error downloading vector store: {str(e)}")
        return False

def check_vector_store():
    """Check if vector store exists and is valid"""
    required_files = [
        "vector_store/transcript_index.faiss",
        "vector_store/transcript_metadata.pkl"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            return False
    return True

def main():
    """Main function to download and setup the vector store"""
    print("=" * 50)
    print("VECTOR STORE SETUP")
    print("=" * 50)
    
    # Check if vector store already exists
    if check_vector_store():
        print(" Vector store already exists")
        return True
    
    # Download vector store
    if download_vector_store():
        print(" Setup completed successfully")
        return True
    
    print("❌ Setup failed")
    return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 