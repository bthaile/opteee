FROM node:18-slim as frontend-builder

# Build React frontend
WORKDIR /frontend

# Copy package files (will be created later)
# For now, create a placeholder structure
RUN mkdir -p public src
RUN echo '{"name": "opteee-frontend", "version": "1.0.0", "dependencies": {"react": "^18.0.0", "react-dom": "^18.0.0"}, "scripts": {"build": "echo No frontend build yet && mkdir -p build && echo Frontend placeholder > build/index.html"}}' > package.json
RUN npm install
RUN npm run build

# Python backend stage
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-fastapi.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/vector_store /app/static /app/app/models /app/app/services

# Copy Python files
COPY main.py /app/
COPY app/ /app/app/
COPY *.py /app/

# Copy static assets (CSS, etc.) 
COPY static /app/static

# Copy processed transcripts (this layer will be cached)
COPY processed_transcripts /app/processed_transcripts

# Build vector store (this layer will be cached)
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store && \
    cp -r /app/processed_transcripts/* /tmp/processed_transcripts/ && \
    python create_vector_store.py --output-dir /tmp/vector_store && \
    cp -r /tmp/vector_store/* /app/vector_store/ && \
    rm -rf /tmp/processed_transcripts /tmp/vector_store

# Copy React build from frontend stage
COPY --from=frontend-builder /frontend/build /app/frontend/build

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

# Expose port for HuggingFace compatibility
EXPOSE 7860

# Run the FastAPI app
CMD ["python", "main.py"] 