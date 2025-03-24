FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
COPY runtime_requirements.txt .

# Install requirements (separately to maintain flexibility)
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r runtime_requirements.txt
# Add Gradio
RUN pip install gradio==3.50.2

# Copy application files
COPY *.py ./
COPY static/ ./static/
COPY templates/ ./templates/

# Create directories
RUN mkdir -p processed_transcripts vector_store

# Debug: Show all files
RUN ls -la

EXPOSE 7860
EXPOSE 7861

# Use the gradio wrapper script
CMD ["python", "gradio_app.py"] 