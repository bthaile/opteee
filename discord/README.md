---
title: OPTEEE Discord Bot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8080
pinned: false
---

# OPTEEE Discord Bot

A Discord bot that provides access to the OPTEEE options trading knowledge base through Discord. This bot connects to the main OPTEEE API to search through thousands of options trading video transcripts.

## Features

- Search options trading knowledge base using natural language queries
- Get detailed answers with video sources, timestamps, and transcript excerpts
- See the exact transcript content that matched your query
- User-friendly video references with timestamps (replaces "[Document N]" with clickable "[Video N @ 66:10: Title]")
- Easy-to-use commands
- Clean, professional Discord formatting

## Setup

### 1. Create a Discord Bot:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" section and click "Add Bot"
   - Copy the bot token
   - Enable the following bot intents:
     - **Message Content Intent** ✅
     - **Server Members Intent** ✅

### 2. Install Dependencies:
   ```bash
   cd discord/
   pip install -r requirements.txt
   ```

### 3. Create Environment File:
   Create a `.env` file in the `discord/` directory:
   ```bash
   # Discord Bot Configuration
   DISCORD_TOKEN=your_discord_bot_token_here
   
   # OPTEEE API Configuration
   # For local development: http://localhost:7860
   # For production: https://bthaile-opteee.hf.space
   OPTEEE_API_URL=https://bthaile-opteee.hf.space
   
   # Optional: Default settings
   DEFAULT_PROVIDER=openai
   DEFAULT_RESULTS=5
   ```

### 4. Local Development Setup:
   ```bash
   # For testing against local API
   echo "OPTEEE_API_URL=http://localhost:7860" >> .env
   
   # Make sure your main opteee app is running first:
   cd ..
   python main.py  # Start the FastAPI backend
   
   # Then in another terminal:
   cd discord/
   python discord_bot.py
   ```

4. Invite the Bot to Your Server:
   - Go to OAuth2 > URL Generator in the Discord Developer Portal
   - Select the following scopes:
     - `bot`
     - `applications.commands`
   - Select the following bot permissions:
     - Send Messages
     - Read Message History
   - Copy the generated URL and open it in a browser to invite the bot

## Usage

### 1. Start the bot:
   ```bash
   cd discord/
   python discord_bot.py
   ```

### 2. Available Commands:

#### Basic Commands:
- `!search <query>` - Search with transcript excerpts, timestamps, and clickable video links  
- `!search_advanced <num_results> <query>` - Advanced search with custom result count
- `!health` - Check API health status
- `!show_help` - Show help information

#### Examples:
```bash
# Basic search (uses default settings)
!search What is gamma in options trading?

# Advanced search with custom result count
!search_advanced 8 Explain butterfly spread strategies

# Check if the API is working
!health
```

#### Advanced Search Options:
- **Results:** 1-10 (higher = more comprehensive but longer responses)
- **AI Provider:** Uses default provider set in environment variables

## Notes

- The bot uses the opteee application hosted on Hugging Face Spaces
- Responses are formatted in Markdown for better readability
- Long responses are automatically split into multiple messages to comply with Discord's message length limits
- Logs are saved to `discord_bot.log` for debugging purposes 