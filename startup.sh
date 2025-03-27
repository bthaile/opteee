#!/bin/bash
set -e

echo "===== Setting up environment ====="

# Function to try creating directories and return success/failure
try_dir() {
    local base_dir=$1
    local mpl_dir="$base_dir/matplotlib"
    local hf_dir="$base_dir/huggingface"
    
    echo "Trying to create cache directories in $base_dir..."
    if mkdir -p "$mpl_dir" "$hf_dir" 2>/dev/null; then
        echo "SUCCESS: Created cache directories in $base_dir"
        export MPLCONFIGDIR="$mpl_dir"
        export TRANSFORMERS_CACHE="$hf_dir"
        export XDG_CACHE_HOME="$base_dir"
        export XDG_CONFIG_HOME="$base_dir"
        return 0
    else
        echo "FAILED: Could not create directories in $base_dir"
        return 1
    fi
}

# Export HOME as current directory
export HOME=$(pwd)
echo "HOME set to: $HOME"

# Try several locations in order of preference
if try_dir "$HOME/.cache"; then
    echo "Using home directory for cache"
elif try_dir "/tmp"; then
    echo "Using /tmp for cache"
elif try_dir "/var/tmp"; then
    echo "Using /var/tmp for cache"
else
    echo "WARNING: Could not create cache directories in any location!"
    echo "Python libraries may fail to load models or create visualizations."
fi

# Print current environment settings
echo "MPLCONFIGDIR: $MPLCONFIGDIR"
echo "TRANSFORMERS_CACHE: $TRANSFORMERS_CACHE"
echo "XDG_CACHE_HOME: $XDG_CACHE_HOME"
echo "XDG_CONFIG_HOME: $XDG_CONFIG_HOME"
echo "HOME: $HOME"
echo "Current directory: $(pwd)"
echo "Current user: $(whoami)"

# Set Python path
export PYTHONPATH=/app

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