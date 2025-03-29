# Opteee Discord Bot

A Discord bot that provides access to the opteee options trading knowledge base through Discord.

## Features

- Search options trading knowledge base using natural language queries
- Get detailed answers with video sources and timestamps
- Easy-to-use commands
- Markdown-formatted responses

## Setup

1. Create a Discord Bot:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" section and click "Add Bot"
   - Copy the bot token
   - Enable the following bot intents:
     - Message Content Intent
     - Server Members Intent

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your actual Discord bot token.

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

1. Start the bot:
   ```bash
   python discord_bot.py
   ```

2. Available Commands:
   - `!search <query>` - Search for options trading information
   - `!show_help` - Show help information

Example:
```
!search What is gamma in options trading?
```

## Notes

- The bot uses the opteee application hosted on Hugging Face Spaces
- Responses are formatted in Markdown for better readability
- Long responses are automatically split into multiple messages to comply with Discord's message length limits
- Logs are saved to `discord_bot.log` for debugging purposes 