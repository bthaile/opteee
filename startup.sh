#!/bin/bash
set -e

echo "===== Setting up environment ====="

# Try app directory first (should always be writable)
echo "Creating cache directories in /app..."
if mkdir -p /app/cache/matplotlib /app/cache/huggingface; then
    echo "Successfully created cache directories in /app"
    export MPLCONFIGDIR=/app/cache/matplotlib
    export TRANSFORMERS_CACHE=/app/cache/huggingface
    export XDG_CACHE_HOME=/app/cache
    export XDG_CONFIG_HOME=/app/cache
# If app directory fails, try workspace
elif [ -d "/workspace" ] && mkdir -p /workspace/cache/matplotlib /workspace/cache/huggingface 2>/dev/null; then
    echo "Using /workspace for cache directories..."
    export MPLCONFIGDIR=/workspace/cache/matplotlib
    export TRANSFORMERS_CACHE=/workspace/cache/huggingface
    export XDG_CACHE_HOME=/workspace/cache
    export XDG_CONFIG_HOME=/workspace/cache
# Last resort - try tmp
else
    echo "WARNING: Could not create cache directories in /app or /workspace. Using /tmp as last resort."
    mkdir -p /tmp/matplotlib /tmp/huggingface
    export MPLCONFIGDIR=/tmp/matplotlib
    export TRANSFORMERS_CACHE=/tmp/huggingface
    export XDG_CACHE_HOME=/tmp
    export XDG_CONFIG_HOME=/tmp
fi

# Print current environment settings
echo "MPLCONFIGDIR: $MPLCONFIGDIR"
echo "TRANSFORMERS_CACHE: $TRANSFORMERS_CACHE"
echo "XDG_CACHE_HOME: $XDG_CACHE_HOME"
echo "XDG_CONFIG_HOME: $XDG_CONFIG_HOME"

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