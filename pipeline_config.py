"""
Centralized configuration for the video processing pipeline.
This ensures consistency across all scripts.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# File Paths
VIDEOS_JSON = 'outlier_trading_videos.json'  # Output from outlier_scraper.py
METADATA_JSON = 'outlier_trading_videos_metadata.json'  # Output from collect_video_metadata.py
MISSING_TRANSCRIPTS_JSON = 'missing_transcripts.json'
TRANSCRIPT_PROGRESS_JSON = 'transcript_progress.json'
MANUAL_PROCESSING_JSON = 'manual_processing_needed.json'

# Directories
TRANSCRIPT_DIR = 'transcripts'
AUDIO_DIR = 'audio_files'
PROCESSED_DIR = 'processed_transcripts'
VECTOR_STORE_DIR = 'vector_store'

# Chunking Configuration
CHUNK_SIZE = 250  # Target words per chunk
OVERLAP = 50      # Words of overlap between chunks
MIN_CHUNK_WORDS = 10  # Minimum words required for a valid chunk

# YouTube Channel URLs
CHANNEL_URLS = [
    'https://www.youtube.com/@OutlierTrading/videos',
    'https://www.youtube.com/@OutlierTrading/shorts',
    'https://www.youtube.com/@OutlierTrading/streams',
    'https://www.youtube.com/@OutlierTrading/podcasts',
    'https://www.youtube.com/@OutlierTrading/live',  # Live streams
    'https://www.youtube.com/@OutlierTrading',       # Main channel (catches all content)
    'https://www.youtube.com/channel/UCBv-ZXHocgw97AfDG5yz9xw',  # Channel ID format
    'https://www.youtube.com/channel/UCBv-ZXHocgw97AfDG5yz9xw/videos',  # Channel ID videos
    'https://www.youtube.com/channel/UCBv-ZXHocgw97AfDG5yz9xw/live',    # Channel ID live
]

# API Configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Processing Configuration
WHISPER_MODEL = "tiny"  # Whisper model size (tiny, base, small, medium, large) - optimized for speed
# Speed vs Accuracy trade-offs:
# - "tiny": ~32x faster than base, ~10% less accurate
# - "base": Current default, good balance
# - "small": ~2x slower than base, ~5% more accurate
WHISPER_MODEL_FAST = "tiny"  # For speed-optimized processing
WHISPER_MODEL_PARALLEL = "base"  # For parallel processing (better CPU utilization)

# Parallel processing settings
PARALLEL_WORKERS = 8  # Number of parallel workers (adjust based on your CPU cores)
PARALLEL_ENABLE = True  # Enable parallel processing by default
BATCH_SIZE = 64  # Batch size for embedding generation (optimized from 32)
MAX_RETRIES = 3  # Maximum retries for failed operations

# File Validation
def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [TRANSCRIPT_DIR, AUDIO_DIR, PROCESSED_DIR, VECTOR_STORE_DIR]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def get_metadata_file():
    """Return the appropriate metadata file based on what exists"""
    if os.path.exists(METADATA_JSON):
        return METADATA_JSON
    elif os.path.exists(VIDEOS_JSON):
        return VIDEOS_JSON
    else:
        raise FileNotFoundError("No video metadata file found. Please run outlier_scraper.py first.")

# Validation
def validate_config(step=None):
    """Validate configuration and environment
    
    Args:
        step: Optional step name to validate context-specific requirements
              ('scrape', 'transcripts', 'preprocess', 'vectors')
    """
    issues = []
    
    # Only validate YouTube API key for steps that actually need it
    if step in ['scrape', 'transcripts'] and not YOUTUBE_API_KEY:
        issues.append("YouTube API key not found in environment variables")
    elif step is None and not YOUTUBE_API_KEY:
        # If no step specified (full pipeline), warn about missing API key
        issues.append("YouTube API key not found in environment variables (optional for some steps)")
    
    if CHUNK_SIZE <= OVERLAP:
        issues.append(f"Chunk size ({CHUNK_SIZE}) must be larger than overlap ({OVERLAP})")
    
    if MIN_CHUNK_WORDS <= 0:
        issues.append(f"Minimum chunk words ({MIN_CHUNK_WORDS}) must be positive")
    
    return issues

if __name__ == "__main__":
    print("=== Pipeline Configuration ===")
    print(f"Chunk Size: {CHUNK_SIZE} words")
    print(f"Overlap: {OVERLAP} words")
    print(f"Min Chunk Words: {MIN_CHUNK_WORDS}")
    print(f"Whisper Model: {WHISPER_MODEL}")
    print(f"YouTube API Key: {' Found' if YOUTUBE_API_KEY else '❌ Missing'}")
    
    issues = validate_config()
    if issues:
        print("\n⚠️ Configuration Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n Configuration looks good!") 