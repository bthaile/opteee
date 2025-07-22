#!/bin/bash

# OPTEEE Discord Bot Deployment Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Get current user and paths
CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)
PROJECT_ROOT=$(cd .. && pwd)

print_step "OPTEEE Discord Bot Deployment"
echo "User: $CURRENT_USER"
echo "Discord Bot Directory: $CURRENT_DIR"
echo "Project Root: $PROJECT_ROOT"
echo ""

# Check if we're in the right directory
if [[ ! -f "discord_bot.py" ]]; then
    print_error "This script must be run from the discord/ directory"
    print_error "Current directory: $CURRENT_DIR"
    exit 1
fi

# Check if .env file exists
if [[ ! -f ".env" ]]; then
    print_warning ".env file not found"
    print_step "Creating .env template..."
    cat > .env << EOF
# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here

# OPTEEE API Configuration
OPTEEE_API_URL=https://bthaile-opteee.hf.space

# Optional: Default settings
DEFAULT_PROVIDER=openai
DEFAULT_RESULTS=5
EOF
    print_success "Created .env template - please edit with your Discord bot token"
    echo ""
fi

# Check dependencies
print_step "Checking dependencies..."
if ! python3 -c "import discord, aiohttp, dotenv" 2>/dev/null; then
    print_warning "Dependencies not installed"
    read -p "Install dependencies? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install -r requirements.txt
        print_success "Dependencies installed"
    else
        print_error "Dependencies required to run the bot"
        exit 1
    fi
else
    print_success "Dependencies installed"
fi

# Test bot configuration
print_step "Testing bot configuration..."
if python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
if not token or token == 'your_discord_bot_token_here':
    exit(1)
print('Token configured')
" 2>/dev/null; then
    print_success "Bot token configured"
else
    print_error "Discord bot token not configured in .env file"
    print_error "Please edit .env and set DISCORD_TOKEN"
    exit 1
fi

# Ask about systemd service
echo ""
read -p "Install as systemd service? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_step "Installing systemd service..."
    
    # Create service file with correct paths
    SERVICE_FILE="/tmp/opteee-discord-bot.service"
    cat > $SERVICE_FILE << EOF
[Unit]
Description=OPTEEE Discord Bot
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
Environment=PYTHONPATH=$CURRENT_DIR
ExecStart=$PROJECT_ROOT/venv/bin/python discord_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    # Install service
    sudo cp $SERVICE_FILE /etc/systemd/system/opteee-discord-bot.service
    sudo systemctl daemon-reload
    sudo systemctl enable opteee-discord-bot.service
    
    print_success "Systemd service installed"
    
    # Ask if user wants to start it now
    read -p "Start the bot service now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo systemctl start opteee-discord-bot.service
        sleep 2
        
        if systemctl is-active --quiet opteee-discord-bot.service; then
            print_success "Bot service started successfully"
            print_step "Service management commands:"
            echo "  Status: sudo systemctl status opteee-discord-bot.service"
            echo "  Logs:   sudo journalctl -f -u opteee-discord-bot.service"
            echo "  Stop:   sudo systemctl stop opteee-discord-bot.service"
            echo "  Start:  sudo systemctl start opteee-discord-bot.service"
        else
            print_error "Bot service failed to start"
            print_step "Check logs: sudo journalctl -u opteee-discord-bot.service"
        fi
    fi
else
    print_step "Manual deployment selected"
    print_success "To run the bot manually: python3 discord_bot.py"
fi

echo ""
print_success "Deployment complete!"
print_step "Next steps:"
echo "1. Make sure your Discord bot is invited to your server"
echo "2. Test with: !health command in Discord"
echo "3. Try: !search What is gamma in options trading?"
echo "4. Try: !search_advanced 8 What are butterfly spreads?" 