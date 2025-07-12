FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# First, copy only requirements to leverage cache for pip install
COPY minimal_requirements.txt /app/requirements.txt

# Install Python dependencies (this layer will be cached)
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/vector_store /app/static /app/templates

# Copy all Python files first (this layer will be cached)
COPY *.py /app/

# Copy static assets
COPY static /app/static

# Copy processed transcripts (this layer will be cached)
COPY processed_transcripts /app/processed_transcripts

# Build vector store (this layer will be cached)
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store && \
    cp -r /app/processed_transcripts/* /tmp/processed_transcripts/ && \
    python create_vector_store.py --output-dir /tmp/vector_store && \
    cp -r /tmp/vector_store/* /app/vector_store/ && \
    rm -rf /tmp/processed_transcripts /tmp/vector_store

# Copy the remaining files that change most frequently
COPY startup.sh /app/

# Make startup script executable
RUN chmod +x /app/startup.sh

# Create cache and flagged directories
RUN mkdir -p /app/cache/matplotlib /app/cache/huggingface /app/flagged

# Set permissions on the entire /app directory
RUN chmod -R 777 /app

# Set environment variables
ENV VECTOR_STORE_PREBUILT=true
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV MPLCONFIGDIR=/app/cache/matplotlib
ENV TRANSFORMERS_CACHE=/app/cache/huggingface
ENV XDG_CACHE_HOME=/app/cache
ENV XDG_CONFIG_HOME=/app/cache

# Run the app
CMD ["/app/startup.sh"] 