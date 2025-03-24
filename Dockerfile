FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files - most important is app.py
COPY app.py .
COPY static/ ./static/
COPY templates/ ./templates/

# Create necessary directories
RUN mkdir -p processed_transcripts vector_store

# List files for debugging
RUN ls -la

EXPOSE 7860

# Run the Flask app directly
CMD ["python", "app.py"] 