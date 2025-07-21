FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (curl for health checks)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Discord bot files
COPY discord_bot.py /app/
COPY health_server.py /app/
COPY start.sh /app/

# Make startup script executable
RUN chmod +x /app/start.sh

# Create logs directory with write permissions
RUN mkdir -p /app/logs && chmod 777 /app/logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Health check for HuggingFace Spaces
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run both Discord bot and health server
CMD ["/app/start.sh"] 