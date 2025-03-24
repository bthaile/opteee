FROM python:3.9-slim

WORKDIR /app

# Copy requirements files
COPY minimal_requirements.txt .

# First install huggingface-hub specifically
RUN pip install huggingface-hub==0.12.1

# Then install other requirements
RUN pip install --no-cache-dir -r minimal_requirements.txt

# Create necessary directories
RUN mkdir -p /tmp/vector_store /tmp/processed_transcripts
RUN chmod -R 777 /tmp

# Copy application files
COPY app.py config.py vector_search.py startup.sh /app/
RUN chmod +x /app/startup.sh

# Copy static files and templates
COPY static/ /app/static/
COPY templates/ /app/templates/

# Run the application
CMD ["/app/startup.sh"]

# Add this to set default API keys if available from Hugging Face secrets
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY} 