FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure gradio is installed
RUN pip install gradio==3.50.2

# Copy debug script and other files
COPY debug.py .
COPY app.py .
COPY gradio_app.py .
COPY static/ ./static/
COPY templates/ ./templates/

# Make debug script executable
RUN chmod +x debug.py

# Create directories
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store
RUN chmod -R 777 /tmp

EXPOSE 7860
EXPOSE 7861

# Run the debug script first, then try to run gradio_app
CMD ["python", "debug.py"] 