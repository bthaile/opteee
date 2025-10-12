#!/bin/bash
set -e

echo "===== Starting application ====="
date

# Print environment for debugging
echo "Current directory: $(pwd)"
echo "Current user: $(whoami)"

# Run the FastAPI application
python main.py
