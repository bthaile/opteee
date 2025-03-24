FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the new entry point file
COPY main.py .
COPY static/ ./static/
COPY templates/ ./templates/

# Create necessary directories
RUN mkdir -p processed_transcripts vector_store

# Show what files we have
RUN ls -la

EXPOSE 7860

# Use our new entry point
CMD ["python", "main.py"] 