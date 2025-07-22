#!/bin/bash

# Local development script for fastest UI iteration
# No Docker needed - runs directly on your machine

echo " Starting OPTEEE Local Development (No Docker)"
echo "================================================="

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo " Virtual environment active: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected"
    echo "🔧 Activating virtual environment..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        echo " Virtual environment activated"
    else
        echo "❌ Virtual environment not found at venv/bin/activate"
        echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo "OPENAI_API_KEY=your_key_here"
    echo "ANTHROPIC_API_KEY=your_key_here"
    exit 1
fi

# Load environment variables
export $(cat .env | xargs)

# Check for required files
if [ ! -f "app_enhanced.py" ]; then
    echo "❌ Error: app_enhanced.py not found!"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Set development mode
export GRADIO_RELOAD=true

echo "🔥 Starting enhanced development server..."
echo " Edit app_enhanced.py, static/*, templates/* and save to see changes!"
echo "🌐 Open http://localhost:7860 in your browser"
echo "⏹️ Press Ctrl+C to stop"
echo "🔄 Server will auto-reload when you save files"
echo ""

# Run the enhanced app with hot reload
python3 app_enhanced.py 