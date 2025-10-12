"""
This script patches SentenceTransformer to work with modern huggingface_hub
"""
import os
import sys
import re

def patch_sentence_transformers():
    """Find and patch sentence_transformers code to replace cached_download with hf_hub_download"""
    try:
        import sentence_transformers
        st_path = os.path.dirname(sentence_transformers.__file__)
        
        # Files likely using cached_download
        files_to_patch = [
            os.path.join(st_path, "models", "Transformer.py"),
            os.path.join(st_path, "SentenceTransformer.py")
        ]
        
        for file_path in files_to_patch:
            if os.path.exists(file_path):
                print(f"Patching {file_path}")
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Replace imports
                content = re.sub(
                    r'from huggingface_hub import cached_download', 
                    'from huggingface_hub import hf_hub_download', 
                    content
                )
                
                # Replace function calls (may need adjustment based on actual code)
                content = re.sub(
                    r'cached_download\(([^)]*)\)', 
                    r'hf_hub_download(repo_id="sentence-transformers/all-MiniLM-L6-v2", filename=\1)', 
                    content
                )
                
                with open(file_path, 'w') as f:
                    f.write(content)
                
                print(f" Successfully patched {file_path}")
        
        print("Patching complete!")
        return True
    except Exception as e:
        print(f"❌ Error patching sentence_transformers: {e}")
        return False

if __name__ == "__main__":
    patch_sentence_transformers() 