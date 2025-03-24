FROM python:3.9-slim

WORKDIR /app

# Copy requirements files
COPY requirements.txt .
COPY runtime_requirements.txt ./runtime_requirements.txt

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gradio==3.50.2  # Explicitly install Gradio

# Show installed packages for debugging
RUN pip list

# Explicitly copy Python modules
COPY *.py ./
COPY static/ ./static/
COPY templates/ ./templates/

# Create writable directories with proper permissions
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store
RUN chmod -R 777 /tmp

# Print debug information
RUN echo "Files in /app:"
RUN ls -la
RUN echo "Python path:"
RUN python -c "import sys; print(sys.path)"

EXPOSE 7860
EXPOSE 7861  # For Gradio

# Use Gradio as entry point
CMD ["python", "gradio_app.py"] 