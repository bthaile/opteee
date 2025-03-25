import os
from pathlib import Path

# Use /app paths since vector store is built during image creation
PROCESSED_DIR = "/app/processed_transcripts"
VECTOR_DIR = "/app/vector_store"
VECTOR_STORE_PATH = VECTOR_DIR
PROCESSED_TRANSCRIPTS_PATH = PROCESSED_DIR

# Model configuration
MODEL_NAME = "all-MiniLM-L6-v2"
DEVICE = "cpu"  # Use "cuda" if GPU is available

# Search configuration
TOP_K = 5
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Vector store configuration
BATCH_SIZE = 32

# Create necessary directories
Path(PROCESSED_DIR).mkdir(exist_ok=True, parents=True)
Path(VECTOR_DIR).mkdir(exist_ok=True, parents=True)

# Create directories if they don't exist
for directory in [PROCESSED_DIR, VECTOR_DIR]:
    os.makedirs(directory, exist_ok=True) 