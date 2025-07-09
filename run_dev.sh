#!/bin/bash

# Development script for hot reload UI development
# This allows you to edit UI code without rebuilding the Docker image

echo "🚀 Starting OPTEEE Development Environment with Hot Reload"
echo "==========================================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo "OPENAI_API_KEY=your_key_here"
    echo "ANTHROPIC_API_KEY=your_key_here"
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker compose -f docker-compose.dev.yml down 2>/dev/null || true

# Build the base image (only needed once or when dependencies change)
echo "🏗️ Building base image (if needed)..."
docker compose -f docker-compose.dev.yml build

# Start the development environment
echo "🔥 Starting development server with hot reload..."
echo "📝 Edit app_enhanced.py, static/*, templates/* and changes will reflect immediately!"
echo "🌐 Open http://localhost:7860 in your browser"
echo "⏹️ Press Ctrl+C to stop"

# Run with volume mounts for hot reload
docker compose -f docker-compose.dev.yml up

echo "✅ Development environment stopped" 