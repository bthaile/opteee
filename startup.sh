#!/bin/bash
set -e

echo "===== Setting up environment ====="

# Create app directory (should always be writable)
echo "Creating cache directories in /app..."
mkdir -p /app/cache/matplotlib /app/cache/huggingface

# Set environment variables (before Python is imported)
echo "Setting environment variables..."
export MPLCONFIGDIR=/app/cache/matplotlib
export TRANSFORMERS_CACHE=/app/cache/huggingface
export XDG_CACHE_HOME=/app/cache
export XDG_CONFIG_HOME=/app/cache
export PYTHONPATH=/app

# Make sure Python knows not to try to use the root directory
export HOME=/app

# Print current environment settings
echo "MPLCONFIGDIR: $MPLCONFIGDIR"
echo "TRANSFORMERS_CACHE: $TRANSFORMERS_CACHE"
echo "XDG_CACHE_HOME: $XDG_CACHE_HOME"
echo "XDG_CONFIG_HOME: $XDG_CONFIG_HOME"
echo "HOME: $HOME"

# Check for required API keys
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$CLAUDE_API_KEY" ]; then
    echo "Error: No API keys found in environment variables!"
    echo "Please set at least one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, or CLAUDE_API_KEY"
    echo "You can set these in your hosting platform's environment variables"
    exit 1
fi

echo "===== Starting application ====="
date

# Start the application
python app.py 