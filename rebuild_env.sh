#!/bin/bash

# Exit on error
set -e

echo " Rebuilding virtual environment for opteee..."

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3."
    exit 1
fi

# Remove any existing environments
echo "🧹 Cleaning up any existing environments..."
rm -rf venv .venv fresh_env new_venv 2>/dev/null || true

# Create a new virtual environment
echo "🔧 Creating a new virtual environment..."
python3 -m venv env

# Activate the virtual environment
echo "🔌 Activating virtual environment..."
source env/bin/activate

# Upgrade pip and tools
echo "🔄 Upgrading pip and tools..."
python -m pip install --upgrade pip setuptools wheel

# Install requirements 
echo "📦 Installing required packages..."
python -m pip install -r requirements.txt

echo "✅ Environment setup complete! To activate the environment, run:"
echo "   source env/bin/activate" 