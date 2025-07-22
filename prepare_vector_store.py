"""
Prepare vector store for external hosting
This script creates a compressed tarball of the vector store files
"""
import os
import tarfile
import shutil

# Directory containing vector store
VECTOR_STORE_DIR = "vector_store"
OUTPUT_FILE = "vector_store.tar.gz"

def main():
    """Create a compressed tarball of the vector store"""
    # Check if vector store exists
    if not os.path.exists(VECTOR_STORE_DIR):
        print(f"❌ Vector store directory {VECTOR_STORE_DIR} not found")
        return False
    
    # Create a temp directory with just the necessary files
    temp_dir = "vector_store_temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Copy the necessary files to the temp directory
    try:
        shutil.copytree(VECTOR_STORE_DIR, os.path.join(temp_dir, "vector_store"))
        print(f" Copied vector store files to {temp_dir}")
    except Exception as e:
        print(f"❌ Error copying files: {str(e)}")
        return False
    
    # Create the tarball
    try:
        with tarfile.open(OUTPUT_FILE, "w:gz") as tar:
            tar.add(temp_dir, arcname=".")
        print(f" Created compressed archive: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error creating archive: {str(e)}")
        return False
    finally:
        # Clean up the temp directory
        shutil.rmtree(temp_dir)
    
    print(f"""
=================================================
Vector store archive created: {OUTPUT_FILE}
=================================================

Next steps:
1. Upload this file to a file sharing service (Dropbox, Google Drive, etc.)
2. Get a direct download link
3. Update the VECTOR_STORE_URL in download_and_setup.py with this link
4. Commit and push your changes to GitHub

The vector store will be downloaded automatically when your app starts on Hugging Face Spaces.
""")
    return True

if __name__ == "__main__":
    main() 