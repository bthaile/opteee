import os

# Directories
PROCESSED_DIR = "processed_transcripts"
VECTOR_DIR = "vector_store"
  
# Model configuration
MODEL_NAME = "all-MiniLM-L6-v2"  # Small, fast model good for semantic search
  
# Search configuration
DEFAULT_TOP_K = 5
  
# Processing configuration
BATCH_SIZE = 32  # For embedding creation
  
# Ensure directories exist
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True) 