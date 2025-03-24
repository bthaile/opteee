import os
from pathlib import Path

# Paths
PROCESSED_TRANSCRIPTS_PATH = "/tmp/processed_transcripts"
VECTOR_STORE_PATH = "/tmp/vector_store"

# Model configuration
MODEL_NAME = "all-MiniLM-L6-v2"
DEVICE = "cpu"  # Use "cuda" if GPU is available

# Search configuration
TOP_K = 5
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Create necessary directories
Path(PROCESSED_TRANSCRIPTS_PATH).mkdir(exist_ok=True, parents=True)
Path(VECTOR_STORE_PATH).mkdir(exist_ok=True, parents=True) 