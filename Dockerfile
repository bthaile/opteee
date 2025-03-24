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

# Create necessary directories
RUN mkdir -p processed_transcripts vector_store

# List all files to verify
RUN ls -la

# Add these debugging commands
RUN echo "Python path: $PYTHONPATH"
RUN python -c "import sys; print('Python module paths:', sys.path)"
RUN find / -name config.py 2>/dev/null || echo "config.py not found"

EXPOSE 7860

# Run the Flask app
CMD ["python", "app.py"] 