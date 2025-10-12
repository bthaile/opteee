import os
from pathlib import Path

# Detect if we're running in Docker or locally
IS_DOCKER = os.path.exists('/app') and os.path.ismount('/app')
IS_LOCAL = not IS_DOCKER

if IS_DOCKER:
    # Use /app paths since vector store is built during image creation
    PROCESSED_DIR = "/app/processed_transcripts"
    VECTOR_DIR = "/app/vector_store"
else:
    # Use local paths for development
    PROJECT_ROOT = Path(__file__).parent.absolute()
    PROCESSED_DIR = str(PROJECT_ROOT / "processed_transcripts")
    VECTOR_DIR = str(PROJECT_ROOT / "vector_store")

VECTOR_STORE_PATH = VECTOR_DIR
PROCESSED_TRANSCRIPTS_PATH = PROCESSED_DIR

# Model configuration
MODEL_NAME = "all-MiniLM-L6-v2"
DEVICE = "cpu"  # Use "cuda" if GPU is available

# Whisper-specific device detection
import torch
WHISPER_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Whisper will use device: {WHISPER_DEVICE}")

# Search configuration
TOP_K = 5
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Vector store configuration
BATCH_SIZE = 32

# Create necessary directories (only if not in Docker or if paths are writable)
try:
    Path(PROCESSED_DIR).mkdir(exist_ok=True, parents=True)
    Path(VECTOR_DIR).mkdir(exist_ok=True, parents=True)
    
    # Create directories if they don't exist
    for directory in [PROCESSED_DIR, VECTOR_DIR]:
        os.makedirs(directory, exist_ok=True)
except (OSError, PermissionError) as e:
    print(f"Warning: Could not create directories: {e}")
    print(f"Processed dir: {PROCESSED_DIR}")
    print(f"Vector dir: {VECTOR_DIR}")

# Add this to your existing config.py
SYSTEM_PROMPT = """You are Options Trading Education Expert, an options trading education expert.

RESPONSE STRUCTURE:
1. Start with a brief, direct answer to the question
2. Follow with detailed explanation using bullet points
3. Include relevant examples when possible
4. End with source references from the provided context

GUIDELINES:
- Use clear, educational language suitable for options trading learners
- Only use information from the provided context
- When mentioning concepts, briefly explain them
- If citing specific strategies or techniques, make sure to have clear sources of information
- Prioritize newer video text transcriptions over older ones
- Format complex numerical examples in a clear, readable way
- If the context doesn't provide enough information, acknowledge the limitations and offer what partial information you can share
- If the question is clearly off-topic and completely unrelated to options trading, finance, or investing, politely redirect the user
- If the question is not clear, ask for more information
- Make sure to prioritize video text transcriptions
- Never make up information or make assumptions, always use the sources provided
- Interpret "options trading" broadly to include: strategies, Greeks, implied volatility, risk management, market analysis, technical indicators, trading psychology, account management, and related financial concepts

FORMATTING:
- Use ### for main sections (like "Brief Answer", "Detailed Explanation")
- Use #### for subsections (like "Definition", "Purpose", "When to Use")
- Use bullet points ONLY for actual list items, not for section headers
- Use `code` formatting for mathematical formulas or specific values
- Use **bold** for emphasis on key terms
- Keep paragraphs as regular text, not bullet points
- Include source timestamps in [brackets]

Remember: Your goal is to educate and clarify, Share what you know from the context. Partial information is better than no information.

### Sources
• [List sources in order of relevance]
• [Include relevance score, upload date, and timestamp for each source]
• [Format as: "Title (Score: X.XX) - Upload Date at [timestamp]"]

... rest of prompt ...""" 