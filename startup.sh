#!/bin/bash

# Check for required API keys
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$CLAUDE_API_KEY" ]; then
    echo "Error: No API keys found in environment variables!"
    echo "Please set at least one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, or CLAUDE_API_KEY"
    echo "You can set these in your hosting platform's environment variables"
    exit 1
fi

# Start the application
python app.py 