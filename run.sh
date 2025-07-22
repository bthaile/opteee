#!/bin/bash

# Function to display usage
show_usage() {
    echo "Usage: ./run.sh [command]"
    echo ""
    echo "Commands:"
    echo "  setup     - Create virtual environment and install dependencies"
    echo "  activate  - Activate the virtual environment"
    echo "  run       - Run the scraper script"
    echo "  deactivate - Deactivate the virtual environment"
    echo "  help      - Show this help message"
}

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        echo "❌ Virtual environment not found. Run './run.sh setup' first."
        exit 1
    fi
}

# Main script
case "$1" in
    "setup")
        echo " Setting up project..."
        python3 -m venv venv
        source venv/bin/activate
        pip3 install -r requirements.txt
        echo " Setup complete!"
        ;;
    "activate")
        check_venv
        echo "🔌 Activating virtual environment..."
        source venv/bin/activate
        ;;
    "run")
        check_venv
        echo "🎥 Running scraper..."
        python3 outlier_scraper.py
        ;;
    "deactivate")
        echo "🔌 Deactivating virtual environment..."
        deactivate
        ;;
    "help"|"")
        show_usage
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_usage
        exit 1
        ;;
esac 