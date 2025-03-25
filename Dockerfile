FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy all necessary files
COPY *.py /app/
COPY minimal_requirements.txt /app/requirements.txt
COPY processed_transcripts /app/processed_transcripts
COPY startup.sh /app/

# Make startup script executable
RUN chmod +x /app/startup.sh

# Create necessary directories
RUN mkdir -p /app/vector_store /app/static /app/templates

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Build vector store during image build
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store && \
    cp -r /app/processed_transcripts/* /tmp/processed_transcripts/ && \
    python create_vector_store.py && \
    cp -r /tmp/vector_store/* /app/vector_store/ && \
    rm -rf /tmp/processed_transcripts /tmp/vector_store

# Set environment variable to indicate pre-built vector store
ENV VECTOR_STORE_PREBUILT=true

# Set Python path
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Simplified startup script will just run the app
CMD ["/app/startup.sh"]

# Add this to set default API keys if available from Hugging Face secrets
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

# Add environment variables for API keys
ENV CLAUDE_API_KEY=${CLAUDE_API_KEY} 