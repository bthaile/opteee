import os
import logging
import discord
from discord.ext import commands
import aiohttp
import json
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
logger.info(f"Token loaded: {'Yes' if DISCORD_TOKEN else 'No'}")
logger.info(f"Token length: {len(DISCORD_TOKEN) if DISCORD_TOKEN else 0}")
HUGGINGFACE_URL = "https://bthaile-opteee.hf.space/api/predict"

# Set up Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def query_opteee(query: str, num_results: str = "5", provider: str = "openai") -> str:
    """Query the opteee application on Hugging Face"""
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "data": [
                    query,
                    num_results,
                    provider,
                    "relevance"
                ],
                "api_name": "search_transcripts"
            }
            
            async with session.post(HUGGINGFACE_URL, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result['data'][0]  # The markdown response
                else:
                    error_msg = f"Error: Failed to get response from opteee (Status: {response.status})"
                    logger.error(error_msg)
                    return error_msg
    except Exception as e:
        error_msg = f"Error querying opteee: {str(e)}"
        logger.error(error_msg)
        return error_msg

@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord"""
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')
    logger.info('Use !search <query> to search for options trading information')
    logger.info('Use !show_help to see all available commands')
    
    # Set bot's activity status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="!show_help for options trading info"
        )
    )

@bot.command(name='search')
async def search(ctx, *, query: str):
    """Search for options trading information"""
    logger.info(f'Search query from {ctx.author}: {query}')
    
    # Send initial response
    await ctx.send(f"🔍 Searching for: {query}")
    
    try:
        # Query opteee
        response = await query_opteee(query)
        
        # Split response into chunks if it's too long (Discord has 2000 char limit)
        if len(response) > 1900:  # Leave some room for formatting
            chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(response)
            
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        logger.error(error_msg)
        await ctx.send(error_msg)

@bot.command(name='show_help')
async def show_help(ctx):
    """Show help information"""
    help_text = """
**Options Trading Knowledge Bot**

Available commands:
`!search <query>` - Search for options trading information
`!show_help` - Show this help message

Example:
`!search What is gamma in options trading?`

The bot will search through a collection of options trading transcripts and videos to find relevant information.
"""
    await ctx.send(help_text)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Please provide a search query. Example: `!search What is gamma?`")
    else:
        error_msg = f"❌ An error occurred: {str(error)}"
        logger.error(error_msg)
        await ctx.send(error_msg)

def main():
    """Main function to run the bot"""
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables")
        return
    
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")

if __name__ == "__main__":
    main() 