FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly copy config.py and other Python modules
COPY app.py .
COPY config.py .
COPY vector_search.py .
COPY static/ ./static/
COPY templates/ ./templates/

# Create writable directories with proper permissions
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store
RUN chmod -R 777 /tmp/processed_transcripts /tmp/vector_store

# Also create a local data directory with write permissions
RUN mkdir -p ./data/transcripts ./data/vectors
RUN chmod -R 777 ./data

# List all files to verify and debug permissions
RUN ls -la
RUN ls -la /tmp

# Add these debugging commands
RUN echo "Python path: $PYTHONPATH"
RUN python -c "import sys; print('Python module paths:', sys.path)"
RUN find / -name config.py 2>/dev/null || echo "config.py not found"

EXPOSE 7860

# Run the Flask app
CMD ["python", "app.py"] 