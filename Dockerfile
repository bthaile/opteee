FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
COPY runtime_requirements.txt .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r runtime_requirements.txt

# Copy application files
COPY *.py ./
COPY static/ ./static/
COPY templates/ ./templates/

# IMPORTANT: Copy processed transcripts if they exist
COPY processed_transcripts/ ./processed_transcripts/ || true

# Create writable directories
RUN mkdir -p /tmp/processed_transcripts /tmp/vector_store
RUN chmod -R 777 /tmp

# Copy and make executable the startup script
COPY startup.sh ./
RUN chmod +x startup.sh

# Debug output
RUN ls -la
RUN echo "Processed transcripts:"
RUN ls -la processed_transcripts || echo "No processed_transcripts directory"

EXPOSE 7860

# Use the startup script as the entry point
CMD ["./startup.sh"]

# Add this to set default API keys if available from Hugging Face secrets
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY} 