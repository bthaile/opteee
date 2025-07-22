#!/bin/bash

echo "🎨 UI Development Mode - No Docker Rebuilds!"
echo "=============================================="
echo "✅ Dependencies fixed and ready"
echo " Starting local Gradio app..."
echo "🌐 Access at: http://localhost:7860"
echo ""
echo "💡 Tips for UI iteration:"
echo "   - Edit app.py, static/styles.css, templates/index.html"
echo "   - Save changes and refresh browser"
echo "   - Ctrl+C to stop, then restart for Python changes"
echo ""

# Export environment variables from .env file
export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d'=' -f2)
export ANTHROPIC_API_KEY=$(grep ANTHROPIC_API_KEY .env | cut -d'=' -f2)

# Start the app
python3 app.py 