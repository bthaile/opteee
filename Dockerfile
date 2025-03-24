FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make sure Gradio is installed
RUN pip install gradio==3.50.2

# Copy application files
COPY app.py .
COPY static/ ./static/
COPY templates/ ./templates/

# Create writable directories
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store
RUN chmod -R 777 /tmp

# Print directory listing for debugging
RUN ls -la

EXPOSE 7860

# Run the app.py which now has both the Flask app and Gradio
CMD ["python", "app.py"] 