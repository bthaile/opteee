FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (minimal for Discord bot)
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Discord bot files
COPY discord_bot.py /app/
COPY health_server.py /app/

# Copy test files for validation
COPY test_docker_formatting.py /app/

# Create logs directory
RUN mkdir -p /app/logs

# Test that all libraries work correctly (this will fail the build if imports fail)
RUN python3 /app/test_docker_formatting.py

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Health check for HuggingFace Spaces
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create startup script that runs both Discord bot and health server
COPY start.sh /app/
RUN chmod +x /app/start.sh

# Run both Discord bot and health server
CMD ["/app/start.sh"] 