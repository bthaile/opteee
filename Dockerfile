FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY *.py ./
COPY static/ ./static/
COPY templates/ ./templates/

# Create necessary directories
RUN mkdir -p processed_transcripts vector_store

# Print files for debugging
RUN ls -la

EXPOSE 7860

# Use the explicit entry point
CMD ["python", "huggingface_app.py"] 