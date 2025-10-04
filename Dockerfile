FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# First, copy only requirements to leverage cache for pip install
COPY requirements.txt /app/requirements.txt

# Install Python dependencies (this layer will be cached)
RUN pip install --no-cache-dir -r requirements.txt

# Create cache and necessary directories first
RUN mkdir -p /app/cache/matplotlib /app/cache/huggingface /app/cache/sentence_transformers /app/flagged
RUN mkdir -p /app/vector_store /app/static /app/templates

# Set environment variables for model caching
ENV MPLCONFIGDIR=/app/cache/matplotlib
ENV TRANSFORMERS_CACHE=/app/cache/huggingface
ENV SENTENCE_TRANSFORMERS_HOME=/app/cache/sentence_transformers
ENV XDG_CACHE_HOME=/app/cache
ENV XDG_CONFIG_HOME=/app/cache

# Pre-download the sentence transformer model during build with proper cache settings
# If download fails, continue anyway (model will be downloaded at runtime)
RUN python -c "try:
    from sentence_transformers import SentenceTransformer
    SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', cache_folder='/app/cache/sentence_transformers')
    print('✓ Model pre-downloaded successfully')
except Exception as e:
    print(f'⚠️ Model pre-download failed: {e}')
    print('Model will be downloaded at runtime instead')" || echo "Model download failed, continuing..."

# Copy all Python files first (this layer will be cached)
COPY *.py /app/

# Copy app directory
COPY app /app/app

# Copy static assets
COPY static /app/static

# Copy frontend build
COPY frontend/build /app/frontend/build

# Copy processed transcripts (this layer will be cached)
COPY processed_transcripts /app/processed_transcripts

# Build vector store (this layer will be cached)
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store && \
    cp -r /app/processed_transcripts/* /tmp/processed_transcripts/ && \
    python create_vector_store.py --output-dir /tmp/vector_store && \
    cp -r /tmp/vector_store/* /app/vector_store/ && \
    rm -rf /tmp/processed_transcripts /tmp/vector_store

# Copy the startup script
COPY startup.sh /app/

# Make startup script executable
RUN chmod +x /app/startup.sh

# Set permissions on the entire /app directory
RUN chmod -R 777 /app

# Set additional environment variables
ENV VECTOR_STORE_PREBUILT=true
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Run the app using startup script
CMD ["/app/startup.sh"]
