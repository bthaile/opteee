#!/bin/bash

# Fast Development Environment for OPTEEE
# Runs FastAPI directly for instant UI updates (no Docker rebuilds needed)

echo " Starting OPTEEE Fast Development Environment"
echo "=============================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please create a .env file with your API keys:"
    echo "OPENAI_API_KEY=your_key_here"
    echo "ANTHROPIC_API_KEY=your_key_here"
    echo ""
    echo "💡 You can copy from .env.example if it exists"
    exit 1
fi

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if we have the required dependencies
echo " Checking dependencies..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    exit 1
fi

# Check if virtual environment exists, if not suggest creating one
if [ ! -d "venv" ] && [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  No virtual environment detected!"
    echo "💡 Recommended: Create a virtual environment first:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Load environment variables
echo "📋 Loading environment variables from .env..."
export $(grep -v '^#' .env | xargs)

# Check if vector store exists
if [ ! -d "vector_store" ] || [ ! "$(ls -A vector_store 2>/dev/null)" ]; then
    echo "⚠️  Vector store not found or empty!"
    echo "🔧 Creating vector store (this may take a few minutes)..."
    python create_vector_store.py
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to create vector store"
        echo "💡 Make sure you have processed transcripts in processed_transcripts/ directory"
        exit 1
    fi
fi

# Check if frontend build exists
if [ ! -f "frontend/build/index.html" ]; then
    echo "⚠️  Frontend build files not found!"
    echo "💡 Expected: frontend/build/index.html"
    echo "   Make sure your frontend is built and placed in frontend/build/"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ Environment checks passed!"
echo ""
echo "🔥 Starting FastAPI development server..."
echo " Edit frontend/build/index.html and refresh browser for instant updates!"
echo "🌐 Open http://localhost:7860 in your browser"
echo "🔧 API endpoints available at http://localhost:7860/docs"
echo ""
echo "⚡ FAST DEVELOPMENT MODE:"
echo "   • UI changes: Edit frontend/build/index.html → refresh browser"
echo "   • Backend changes: Auto-reload enabled! ✨"
echo "   • No Docker rebuilds needed!"
echo ""
echo "⏹️  Press Ctrl+C to stop the server"
echo "==========================================="

# Check for test mode parameter
if [[ "$1" == "--test" ]] || [[ "$1" == "test" ]]; then
    export TEST_MODE=true
    echo "🧪 Running in TEST MODE (mock responses)"
else
    echo "🎯 Running in PRODUCTION MODE (real RAG responses)"
    echo "⚠️  This requires vector store and API keys to be properly configured"
fi

# Check if uvicorn is available for auto-reload
if command -v uvicorn &> /dev/null; then
    echo "🔥 Starting with uvicorn auto-reload..."
    uvicorn main:app --host 0.0.0.0 --port 7860 --reload
else
    echo "⚠️  uvicorn not found - install with: pip install uvicorn"
    echo " Falling back to standard Python (manual restart required)"
    python main.py
fi 