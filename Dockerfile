FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
COPY runtime_requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r runtime_requirements.txt

# Copy application files
COPY *.py ./
COPY static/ ./static/
COPY templates/ ./templates/

# Create writable directories with proper permissions
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store
RUN chmod -R 777 /tmp

# Copy processed transcripts to the writable directory
COPY processed_transcripts/ /tmp/processed_transcripts/ || true

# Print directory contents for debugging
RUN echo "Files in directory:" && ls -la
RUN echo "Transcript files:" && ls -la /tmp/processed_transcripts/ || true

# IMPORTANT: Create the vector store during container initialization
# This is run when the container starts but before the app is accessed
ENTRYPOINT ["sh", "-c", "python create_vector_store.py && python app.py"]

# Add this to set default API keys if available from Hugging Face secrets
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY} 