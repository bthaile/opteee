FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
COPY runtime_requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r runtime_requirements.txt

# Copy application files - explicitly list important files
COPY app.py ./
COPY config.py ./
COPY vector_search.py ./
COPY static/ ./static/
COPY templates/ ./templates/

# Create directories
RUN mkdir -p processed_transcripts vector_store

# Debug: Show all files
RUN ls -la

EXPOSE 7860

# Run the Flask app directly
CMD ["python", "app.py"] 