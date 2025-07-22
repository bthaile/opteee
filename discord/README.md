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

## DNS Resolution & HuggingFace Deployment

### The DNS Challenge
HuggingFace Spaces environments frequently experience DNS resolution failures that prevent Discord bots from connecting. Common errors include:
- `[Errno -5] No address associated with hostname`
- `Session is closed` 
- Connection timeouts to Discord gateway

### Complex DNS Solution
This bot implements a sophisticated DNS resolution strategy to handle HuggingFace's network limitations:

#### Architecture Overview
```
Discord Gateway Connection
    ↓ (Custom DNS Resolver)
Discord.py ← [Google DNS 8.8.8.8, Cloudflare 1.1.1.1]
    ↓
Bot Commands ← (Clean Sessions)  
    ↓
OPTEEE API ← [Isolated from DNS patches]
```

#### Technical Implementation
1. **Custom DNS Resolver**: Uses Google DNS (8.8.8.8) and Cloudflare DNS (1.1.1.1) as alternative resolvers
2. **Selective Patching**: Applies custom DNS only to Discord.py connections via monkey patching
3. **Session Isolation**: API calls use clean aiohttp sessions that bypass DNS patches
4. **Dual-Mode Operation**: 
   - Discord connections: Custom DNS resolver (works around HF DNS)
   - API calls: Original aiohttp functions (prevents session conflicts)

#### Key Components
- **`setup_custom_dns_resolver()`**: Creates alternative DNS resolver with Google/Cloudflare DNS
- **`setup_discord_patches()`**: Monkey patches aiohttp for Discord connections only  
- **`query_opteee()`**: Uses saved original functions for clean API calls
- **Fallback Logic**: Gracefully handles DNS resolver failures

#### Environment Configuration
```bash
# Enable/disable custom DNS resolver (default: enabled)
ENABLE_CUSTOM_DNS=true

# Discord bot configuration
DISCORD_TOKEN=your_token_here
OPTEEE_API_URL=https://bthaile-opteee.hf.space
```

#### Log Messages to Expect
```
✅ Custom DNS resolver dependencies available
🔧 Setting up custom DNS resolver in async context...
✅ Applied comprehensive aiohttp and discord.py DNS patches
Using original aiohttp functions for clean API call
Making clean API request to https://...
API response status: 200
```

### Troubleshooting DNS Issues

#### Common Problems & Solutions

**Problem: "Session is closed" errors**
- **Cause**: DNS patches interfering with API session creation
- **Solution**: Bot automatically uses clean sessions with original aiohttp functions
- **Check**: Look for "Using original aiohttp functions for clean API call" in logs

**Problem: Discord connection failures**  
- **Cause**: HuggingFace DNS can't resolve discord.com
- **Solution**: Custom DNS resolver with Google/Cloudflare DNS
- **Check**: Look for "Custom DNS resolver active and ready" in logs

**Problem: Bot startup hanging**
- **Cause**: DNS resolver initialization failure
- **Solution**: Set `ENABLE_CUSTOM_DNS=false` to disable custom DNS
- **Fallback**: Bot will use system DNS (may have connection issues)

#### Debug Steps
1. **Check logs** for DNS resolver status messages
2. **Verify API endpoint** is reachable from your environment
3. **Test with custom DNS disabled**: Set `ENABLE_CUSTOM_DNS=false`
4. **Monitor health**: Use `!health` command to check API connectivity
5. **Wait for HF recovery**: DNS issues often resolve automatically after 1-5 minutes

#### Advanced Debugging
```bash
# Test DNS resolution manually
nslookup discord.com 8.8.8.8

# Check if API is reachable  
curl -s https://bthaile-opteee.hf.space/api/health

# Monitor bot logs in real-time
tail -f discord_bot.log
```

### Why This Complexity is Necessary
- **HuggingFace Limitation**: Spaces environments have unreliable DNS resolution
- **Discord Requirement**: Discord.py needs reliable DNS for gateway connections  
- **API Isolation**: Prevents DNS patches from breaking HTTP API calls
- **Production Stability**: Ensures bot works reliably in HF deployment environment

This implementation prioritizes stability and reliability over simplicity, ensuring the bot works consistently despite HuggingFace's DNS challenges.