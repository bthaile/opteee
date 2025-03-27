#!/bin/bash
set -e

echo "===== Setting up environment ====="

# Try to use /workspace for persistence if available and writable
if [ -d "/workspace" ] && [ -w "/workspace" ]; then
    echo "Using /workspace for cache directories (persistent)..."
    
    # Try to create directories in /workspace
    if mkdir -p /workspace/cache/matplotlib /workspace/cache/huggingface 2>/dev/null; then
        echo "Successfully created directories in /workspace"
        export MPLCONFIGDIR=/workspace/cache/matplotlib
        export TRANSFORMERS_CACHE=/workspace/cache/huggingface
        export XDG_CACHE_HOME=/workspace/cache
        export XDG_CONFIG_HOME=/workspace/cache
    else
        echo "Warning: Could not create directories in /workspace, falling back to /tmp"
        mkdir -p /tmp/matplotlib /tmp/huggingface
        export MPLCONFIGDIR=/tmp/matplotlib
        export TRANSFORMERS_CACHE=/tmp/huggingface
        export XDG_CACHE_HOME=/tmp
        export XDG_CONFIG_HOME=/tmp
    fi
else
    echo "Warning: /workspace is not available or writable, using /tmp (non-persistent)..."
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