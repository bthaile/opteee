#!/bin/bash

# Super simple UI development script
# Just run this and start editing!

echo "🎨 Quick UI Development Mode"
echo "=========================="

# Set development mode for hot reload
export GRADIO_RELOAD=true

# Load environment variables if .env exists
if [ -f .env ]; then
    export $(cat .env | xargs) 2>/dev/null
fi

echo " Starting UI development server..."
echo " Edit app_enhanced.py and save to see changes!"
echo "🌐 http://localhost:7860"
echo ""

# Run the enhanced app
python3 app_enhanced.py 