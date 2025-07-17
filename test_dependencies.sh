#!/bin/bash

# Test Dependencies Script
# This script creates a fresh virtual environment and tests your requirements.txt

echo "🧪 Testing dependencies in fresh virtual environment..."

# Clean up any existing test environment
rm -rf test_env/

# Create fresh virtual environment
python3 -m venv test_env
source test_env/bin/activate

# Upgrade pip to latest version
pip install --upgrade pip

echo "📦 Installing dependencies from requirements.txt..."

# Test dependency installation
if pip install -r requirements.txt; then
    echo "✅ All dependencies installed successfully!"
    
    # Test basic imports
    echo "🔍 Testing basic imports..."
    python3 -c "
import sys
try:
    import langchain
    import gradio
    import openai
    import transformers
    import sentence_transformers
    import numpy
    import pandas
    print('✅ All critical imports successful!')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"
    
    # Show installed versions
    echo "📋 Installed package versions:"
    pip freeze | grep -E "(langchain|gradio|openai|transformers|numpy|pandas)" | head -10
    
else
    echo "❌ Dependency installation failed!"
    deactivate
    exit 1
fi

# Clean up
deactivate
echo "🧹 Cleaning up test environment..."
rm -rf test_env/

echo "🎉 Dependency test completed successfully!" 