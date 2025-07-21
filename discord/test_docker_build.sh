#!/bin/bash

# Test script to verify Docker build works with new libraries
# This helps catch dependency issues before deployment

set -e  # Exit on any error

echo "🔧 Testing Discord Bot Docker Build"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "discord_bot.py" ]; then
    echo "❌ Error: Must be run from the discord directory"
    exit 1
fi

# Check if requirements.txt exists and contains our new libraries
echo "📋 Checking requirements.txt..."
if ! grep -q "html-to-markdown" requirements.txt; then
    echo "❌ Error: html-to-markdown not found in requirements.txt"
    exit 1
fi

echo "✅ Requirements file looks good"

# Build the Docker image
echo ""
echo "🏗️  Building Docker image..."
docker build -t opteee-discord-bot-test .

if [ $? -eq 0 ]; then
    echo "✅ Docker build successful!"
    
    # Run a quick test inside the container
    echo ""
    echo "🧪 Running library tests inside container..."
    docker run --rm --name discord-bot-test opteee-discord-bot-test python3 /app/test_docker_formatting.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎉 All tests passed! Docker image is ready for deployment."
        echo ""
        echo "To run the container:"
        echo "docker run -d --name opteee-discord-bot --env-file .env opteee-discord-bot-test"
        echo ""
        echo "To clean up test image:"
        echo "docker rmi opteee-discord-bot-test"
    else
        echo "❌ Tests failed inside container"
        exit 1
    fi
else
    echo "❌ Docker build failed"
    exit 1
fi 