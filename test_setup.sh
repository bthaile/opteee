#!/bin/bash

echo " Testing OPTEEE Docker Setup"
echo "================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo " Docker is running"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Creating example..."
    cat > .env << 'EOF'
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
EOF
    echo " Created .env file. Please add your API keys and try again."
    exit 1
fi

echo " .env file found"

# Check if API keys are set
if grep -q "your_.*_api_key_here" .env; then
    echo "⚠️  Warning: Default API keys detected in .env file"
    echo "   Please replace with your actual API keys"
fi

echo " Ready to build and run!"
echo ""
echo "Run the following command to start the application:"
echo "  ./run_local.sh"
echo ""
echo "The application will be available at: http://localhost:7860" 