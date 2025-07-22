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
        logging.FileHandler('/app/logs/discord_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Force refresh deployment

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
logger.info(f"Token loaded: {'Yes' if DISCORD_TOKEN else 'No'}")
logger.info(f"Token length: {len(DISCORD_TOKEN) if DISCORD_TOKEN else 0}")

# API Configuration - support both local development and production
API_BASE_URL = os.getenv('OPTEEE_API_URL', 'https://bthaile-opteee.hf.space')
CHAT_ENDPOINT = f"{API_BASE_URL}/api/chat"
HEALTH_ENDPOINT = f"{API_BASE_URL}/api/health"

# Bot Configuration
DEFAULT_PROVIDER = os.getenv('DEFAULT_PROVIDER', 'openai')
DEFAULT_RESULTS = int(os.getenv('DEFAULT_RESULTS', '5'))

# Discord Message Templates
VIDEO_REFERENCE_TEMPLATES = {
    # Full template with all details - matches user's request
    'full': {
        'header': "**Video Sources:**\n",
        'entry': "**{index}.** **[{title}](<{url}>)** | `Start: {timestamp}` | `Duration: {duration}`{date}\n{content}\n\n",
        'content': "*\"{preview}\"*",
        'no_content': "",
        'date_format': " • {formatted_date}",
        'max_title_length': 999,  # Show full titles
        'max_content_length': 200  # 200 characters as requested
    },
    
    # Compact template for space-saving
    'compact': {
        'header': "**Sources:**\n",
        'entry': "**{index}.** **[{title}](<{url}>)** `{timestamp}` `{duration}`{date}\n",
        'content': "",  # No content preview in compact mode
        'no_content': "",
        'date_format': " • {formatted_date}",
        'max_title_length': 60,  # Longer titles for compact
        'max_content_length': 0
    },
    
    # Minimal template for very long responses
    'minimal': {
        'header': "**Videos:**\n",
        'entry': "**{index}.** **[{title}](<{url}>)** `{timestamp}`\n",
        'content': "",
        'no_content': "",
        'date_format': "",
        'max_title_length': 40,
        'max_content_length': 0
    }
}

"""
VIDEO REFERENCE TEMPLATE SYSTEM DOCUMENTATION
===========================================

Template Structure:
- header: Section header text
- entry: Main entry template with placeholders
- content: Template for content preview (when content exists)
- no_content: Template when no content available
- date_format: Format for upload date
- max_title_length: Maximum title length before truncation
- max_content_length: Maximum content preview length (0 = no preview)

Available Placeholders:
- {index}: Source number (1, 2, 3...)
- {title}: Video title (truncated if needed)
- {url}: Video URL with timestamp
- {timestamp}: Start timestamp (MM:SS format)
- {duration}: Video duration (MM:SS format) 
- {date}: Formatted upload date
- {content}: Content preview (if enabled)
- {preview}: Raw content text (for use in {content} template)
- {formatted_date}: Raw formatted date (for use in {date_format})

Usage Examples:
- format_video_sources(sources, template_name='full')     # Full details
- format_video_sources(sources, template_name='compact')  # Space-saving
- format_video_sources(sources, template_name='minimal')  # Ultra-compact

Custom Templates:
To add a new template, add an entry to VIDEO_REFERENCE_TEMPLATES:

'custom_name': {
    'header': "**My Custom Header:**\n",
    'entry': "**{index}.** [{title}]({url}) at {timestamp}\n",
    'content': "Preview: {preview}",
    'no_content': "",
    'date_format': " ({formatted_date})",
    'max_title_length': 40,
    'max_content_length': 80
}

Then use: format_video_sources(sources, template_name='custom_name')
"""

# Set up Discord bot with intents and custom DNS resolver
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# DNS Resolver Configuration - Needed for HuggingFace DNS issues
ENABLE_CUSTOM_DNS = os.getenv('ENABLE_CUSTOM_DNS', 'true').lower() == 'true'

# Global variables for custom session management
custom_session = None
custom_connector = None
custom_resolver_available = False

# Save original aiohttp functions before patching for clean API calls
original_client_session_init = None
original_tcp_connector_init = None

# Import aiohttp components (but don't initialize yet)
try:
    import aiohttp
    import asyncio
    if ENABLE_CUSTOM_DNS:
        from aiohttp.resolver import AsyncResolver
    import discord
    import discord.http
    import discord.gateway
    custom_resolver_available = ENABLE_CUSTOM_DNS
    logger.info(f" Custom DNS resolver {'enabled' if ENABLE_CUSTOM_DNS else 'disabled'}")
except ImportError as e:
    logger.warning(f"⚠️ AsyncResolver not available: {e}")
    custom_resolver_available = False

# Bot will be created after setting up DNS resolver (see main function)
bot = None

async def setup_custom_dns_resolver():
    """Set up custom DNS resolver in async context"""
    global custom_session, custom_connector
    
    if not custom_resolver_available or not ENABLE_CUSTOM_DNS:
        logger.info("ℹ️ Using system DNS (custom DNS resolver disabled)")
        return False
    
    try:
        logger.info("🔧 Setting up custom DNS resolver in async context...")
        
        # Create custom DNS resolver with multiple servers
        custom_resolver = AsyncResolver(nameservers=['8.8.8.8', '8.8.4.4', '1.1.1.1'])
        
        # Create connector with custom DNS resolver
        custom_connector = aiohttp.TCPConnector(
            resolver=custom_resolver,
            ttl_dns_cache=300,
            use_dns_cache=True,
            limit=100,
            limit_per_host=30,
            enable_cleanup_closed=True
        )
        
        # Create custom aiohttp session with our DNS resolver
        # Note: Don't share this session - let discord.py create its own with our patches
        custom_session = aiohttp.ClientSession(
            connector=custom_connector,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        
        logger.info(" Custom DNS session created (for API calls, not discord.py)")
        
        logger.info(" Created custom DNS resolver with Google/Cloudflare DNS in async context")
        
        # Comprehensive monkey patching for discord.py
        await setup_discord_patches()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create custom DNS resolver: {e}")
        return False

async def setup_discord_patches():
    """Set up comprehensive aiohttp and discord.py DNS patches"""
    global custom_session, custom_connector, original_client_session_init, original_tcp_connector_init
    
    try:
        logger.info("🔧 Applying comprehensive aiohttp and discord.py DNS patches...")
        
        # Save original functions before patching
        original_client_session_init = aiohttp.ClientSession.__init__
        original_tcp_connector_init = aiohttp.TCPConnector.__init__
        
        # 1. Patch aiohttp ClientSession creation at the core level
        
        def custom_client_session_init(self, *args, **kwargs):
            """Override all aiohttp ClientSession creation to use our custom connector"""
            # If no connector specified and we have our custom one, use it
            if custom_connector and 'connector' not in kwargs:
                kwargs['connector'] = custom_connector
                logger.info("🔧 aiohttp ClientSession using custom DNS connector")
            
            # Call original init
            return original_client_session_init(self, *args, **kwargs)
        
        # Apply global aiohttp patch
        aiohttp.ClientSession.__init__ = custom_client_session_init
        logger.info(" Applied global aiohttp ClientSession DNS patch")
        
        # 2. Let discord.py create its own sessions (they'll use our custom connector via global patches)
        logger.info(" Discord will create its own sessions using global aiohttp DNS patches")
        
        # 3. Patch aiohttp connector creation as fallback
        original_tcp_connector_init = aiohttp.TCPConnector.__init__
        
        def custom_tcp_connector_init(self, *args, **kwargs):
            """Override TCPConnector init to use our custom DNS resolver"""
            # If no resolver specified and we have our custom one, use it
            if custom_connector and hasattr(custom_connector, '_resolver') and 'resolver' not in kwargs:
                kwargs['resolver'] = custom_connector._resolver
                logger.info("🔧 aiohttp TCPConnector using custom DNS resolver")
            
            # Call original init
            return original_tcp_connector_init(self, *args, **kwargs)
        
        # Apply TCPConnector patch
        aiohttp.TCPConnector.__init__ = custom_tcp_connector_init
        logger.info(" Applied aiohttp TCPConnector DNS resolver patch")
        
        # 4. Global patches are sufficient - discord.py will use our DNS resolver automatically
        logger.info(" All comprehensive DNS patches applied successfully")
        
    except Exception as patch_error:
        logger.error(f"Failed to apply comprehensive DNS patches: {patch_error}")
        raise

async def query_opteee(query: str, num_results: int = 5, provider: str = "openai", format: str = "discord") -> dict:
    """Query the opteee application using clean session isolated from Discord DNS patches"""
    global original_client_session_init, original_tcp_connector_init
    
    try:
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        
        # Use original functions if available (before patching), otherwise fallback to standard
        if original_tcp_connector_init and original_client_session_init:
            logger.info("Using original aiohttp functions for clean API call")
            
            # Create connector using original constructor
            connector = aiohttp.TCPConnector.__new__(aiohttp.TCPConnector)
            original_tcp_connector_init(
                connector,
                limit=100,
                limit_per_host=30,
                ttl_dns_cache=300,
                use_dns_cache=True,
                enable_cleanup_closed=True
            )
            
            # Create session using original constructor  
            session = aiohttp.ClientSession.__new__(aiohttp.ClientSession)
            original_client_session_init(
                session,
                connector=connector,
                timeout=timeout,
                headers={"Content-Type": "application/json"}
            )
        else:
            logger.info("Using standard aiohttp functions for API call")
            # Fallback to standard session creation
            connector = aiohttp.TCPConnector(
                limit=100,
                limit_per_host=30,
                ttl_dns_cache=300,
                use_dns_cache=True,
                enable_cleanup_closed=True
            )
            session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={"Content-Type": "application/json"}
            )
        
        try:
            payload = {
                "query": query,
                "provider": provider,
                "num_results": num_results,
                "format": format
            }
            
            logger.info(f"Making clean API request to {CHAT_ENDPOINT}")
            
            async with session.post(CHAT_ENDPOINT, json=payload) as response:
                logger.info(f"API response status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "answer": result.get("answer", ""),
                        "sources": result.get("raw_sources", []),
                        "timestamp": result.get("timestamp", "")
                    }
                else:
                    error_text = await response.text()
                    error_msg = f"API Error (Status {response.status}): {error_text[:200]}"
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg
                    }
        finally:
            # Clean up the session
            if session and not session.closed:
                await session.close()
                
    except Exception as e:
        error_msg = f"Connection error: {str(e)}"
        logger.error(f"Clean API request failed: {error_msg}")
        logger.error(f"API endpoint: {CHAT_ENDPOINT}")
        return {
            "success": False,
            "error": error_msg
        }

def format_video_sources(raw_sources: list, max_sources: int = 5, template_name: str = 'full') -> str:
    """Format raw_sources for Discord display using standardized templates
    
    Args:
        raw_sources: List of source dictionaries from API response
        max_sources: Maximum number of sources to display
        template_name: Template to use ('full', 'compact', 'minimal')
        
    Returns:
        Formatted string ready for Discord display
    """
    if not raw_sources:
        return ""
    
    # Get template configuration
    template = VIDEO_REFERENCE_TEMPLATES.get(template_name, VIDEO_REFERENCE_TEMPLATES['full'])
    
    sources_text = "\n\n" + template['header']
    
    for i, source in enumerate(raw_sources[:max_sources], 1):
        # Extract source data
        source_data = _extract_source_data(source, template)
        
        # Format the entry using template
        entry_text = template['entry'].format(
            index=i,
            title=source_data['title'],
            url=source_data['url'],
            timestamp=source_data['timestamp'],
            duration=source_data['duration'],
            date=source_data['date'],
            content=source_data['content']
        )
        
        sources_text += entry_text
    
    return sources_text

def _extract_source_data(source: dict, template: dict) -> dict:
    """Extract and format source data according to template specifications"""
    # Get raw data
    title = source.get('title', 'Untitled Video')
    url = source.get('video_url_with_timestamp', source.get('url', '#'))
    start_seconds = source.get('start_timestamp_seconds', 0)
    duration_seconds = source.get('duration_seconds', 0)
    content = source.get('content', '')
    upload_date = source.get('upload_date', '')
    
    # Format timestamp
    timestamp = _format_time(start_seconds) if start_seconds else "0:00"
    
    # Format duration  
    duration = _format_time(duration_seconds) if duration_seconds else "Unknown"
    
    # Format upload date
    date = ""
    if upload_date and upload_date != 'Unknown' and len(upload_date) == 8:
        try:
            from datetime import datetime
            date_obj = datetime.strptime(upload_date, '%Y%m%d')
            formatted_date = date_obj.strftime('%b %Y')
            date = template['date_format'].format(formatted_date=formatted_date)
        except:
            pass
    
    # Clean up title (handle video IDs)
    if len(title) == 11 and title.isalnum():  # Likely a video ID
        title = "Video " + title[:8] + "..."
    
    # Truncate title if too long
    max_title_length = template['max_title_length']
    if len(title) > max_title_length:
        title = title[:max_title_length-3] + "..."
    
    # Format content preview
    content_text = ""
    max_content_length = template['max_content_length']
    if content and max_content_length > 0:
        content_clean = content.strip()[:max_content_length]
        if len(content) > max_content_length:
            # Try to end at word boundary
            if ' ' in content_clean[-20:]:
                content_clean = content_clean[:content_clean.rfind(' ')] + "..."
            else:
                content_clean += "..."
        content_text = template['content'].format(preview=content_clean)
        logger.info(f"Content preview: {len(content_clean)} chars from {len(content)} total")
    else:
        logger.info(f"No content: content={bool(content)}, max_length={max_content_length}")
        content_text = template['no_content']
    
    return {
        'title': title,
        'url': url,
        'timestamp': timestamp,
        'duration': duration,
        'date': date,
        'content': content_text
    }

def _format_time(seconds: float) -> str:
    """Convert seconds to MM:SS format"""
    if not seconds or seconds <= 0:
        return "0:00"
    
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

async def send_discord_response(ctx, response_text: str):
    """Send response to Discord, handling message length limits"""
    # Discord has a 2000 character limit per message
    if len(response_text) <= 2000:
        await ctx.send(response_text)
    else:
        # Split into chunks at reasonable boundaries
        chunks = []
        current_chunk = ""
        
        for line in response_text.split('\n'):
            # If adding this line would exceed limit, start new chunk
            if len(current_chunk) + len(line) + 1 > 1900:  # Leave some buffer
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = line
            else:
                current_chunk += '\n' + line if current_chunk else line
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # Send all chunks
        for chunk in chunks:
            await ctx.send(chunk)

async def search_handler(ctx, query: str, template_override: str = None):
    """Search for options trading information - simplified with server-side formatting"""
    logger.info(f'Search query from {ctx.author}: {query} (template: {template_override or "auto"})')
    
    # Send initial response with template info
    template_info = f" [{template_override} format]" if template_override else ""
    await ctx.send(f"**Searching the knowledge base...**{template_info}\n> {query}\n*Analyzing thousands of transcript segments...*")
    
    try:
        # Query with Discord format - server handles all formatting
        response = await query_opteee(query, num_results=DEFAULT_RESULTS, provider=DEFAULT_PROVIDER, format="discord")
        
        if not response["success"]:
            await ctx.send(f"Error: {response['error']}")
            return
        
        # Server returns pre-formatted Discord content
        formatted_answer = response["answer"]
        raw_sources = response["sources"]
        
        # Template selection - FORCE full template for debugging
        template_name = template_override if template_override else 'full'
        logger.info(f"Template override: {template_override}, Selected: {template_name}")
        
        # Add video sources with selected template
        logger.info(f"Using template: {template_name} for {len(raw_sources)} sources")
        video_sources = format_video_sources(raw_sources, max_sources=5, template_name=template_name)
        
        # Add footer with format options
        if template_override:
            footer = f"\n\n━━━━━━━━━━━━━━━━━━━━\nTry other formats: `!search_full`, `!search_compact`, `!search_minimal`"
        else:
            footer = f"\n\n━━━━━━━━━━━━━━━━━━━━\nTip: Use `!search_advanced {min(10, DEFAULT_RESULTS + 2)} your question` for more detailed results"
        
        final_response = formatted_answer + video_sources + footer
        
        # Send the response (handles splitting automatically)
        await send_discord_response(ctx, final_response)
            
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        await ctx.send(error_msg)

async def search_advanced_handler(ctx, num_results: int, query: str):
    """Advanced search with custom result count - simplified with server-side formatting"""
    # Validate inputs
    if not 1 <= num_results <= 10:
        await ctx.send("Number of results must be between 1 and 10")
        return
    
    provider = DEFAULT_PROVIDER
    
    logger.info(f'Advanced search from {ctx.author}: {query} (provider: {provider}, results: {num_results})')
    await ctx.send(f"**Advanced Search Mode**\n> {query}\n*Using {provider.upper()} AI • Retrieving {num_results} sources • Processing...*")
    
    try:
        # Query with Discord format - server handles all formatting
        response = await query_opteee(query, num_results=num_results, provider=provider, format="discord")
        
        if not response["success"]:
            await ctx.send(f"Error: {response['error']}")
            return
        
        # Server returns pre-formatted Discord content
        formatted_answer = response["answer"]
        raw_sources = response["sources"]
        
        # Add provider info header
        provider_header = f"**{provider.upper()} Response ({num_results} sources):**\n\n"
        
        # Force full verbose format for advanced search (always show transcript content)
        template_name = 'full'  # Force most verbose format with 200-char transcript content
        video_sources = format_video_sources(raw_sources, max_sources=num_results, template_name=template_name)
        
        # Add footer
        if num_results < 8:
            footer = f"\n\n━━━━━━━━━━━━━━━━━━━━\nTry more sources for detailed analysis: `!search_advanced {min(10, num_results + 3)} your question`"
        else:
            footer = f"\n\n━━━━━━━━━━━━━━━━━━━━\nTry basic search for quicker results: `!search your question`"
        
        final_response = provider_header + formatted_answer + video_sources + footer
        
        # Send the response (handles splitting automatically)
        await send_discord_response(ctx, final_response)
            
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        logger.error(error_msg)
        await ctx.send(error_msg)

async def health_handler(ctx):
    """Check if the OPTEEE API is healthy"""
    global original_client_session_init, original_tcp_connector_init
    
    await ctx.send("**System Health Check**\n*Testing connection to OPTEEE API...*")
    
    try:
        timeout = aiohttp.ClientTimeout(total=15)
        
        # Use original functions for clean health check if available
        if original_tcp_connector_init and original_client_session_init:
            connector = aiohttp.TCPConnector.__new__(aiohttp.TCPConnector)
            original_tcp_connector_init(connector, limit=10, ttl_dns_cache=60)
            
            session = aiohttp.ClientSession.__new__(aiohttp.ClientSession)
            original_client_session_init(session, connector=connector, timeout=timeout)
        else:
            # Fallback to standard session creation
            connector = aiohttp.TCPConnector(limit=10, ttl_dns_cache=60)
            session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        
        try:
            async with session.get(HEALTH_ENDPOINT) as response:
                if response.status == 200:
                    data = await response.json()
                    status = data.get('status', 'unknown')
                    version = data.get('version', 'unknown')
                    await ctx.send(f"""**All Systems Operational**

**Status:** `{status.title()}`
**Version:** `{version}`
**Endpoint:** `{API_BASE_URL}`

*Ready to search thousands of options trading transcripts!*""")
                else:
                    await ctx.send(f"**API Unhealthy** (HTTP {response.status})\n*The OPTEEE API may be temporarily unavailable.*")
        finally:
            if session and not session.closed:
                await session.close()
                
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        await ctx.send(f"**Connection Failed**\n*Unable to reach OPTEEE API*\n```\n{str(e)[:100]}...\n```")

async def show_help_handler(ctx):
    """Show help information"""
    help_text = f"""**OPTEEE Discord Bot - Options Trading Knowledge Search**

**Basic Commands:**
• `!search <query>` - Smart search (auto-selects video format)
• `!search_advanced <count> <query>` - Advanced search (1-10 results)
• `!health` - Check API status
• `!show_help` - Show this help

**Video Format Commands:**
• `!search_full <query>` - Full details (title, time, duration, content preview)
• `!search_compact <query>` - Compact format (title, time, duration only)  
• `!search_minimal <query>` - Minimal format (title and timestamp only)

**Examples:**
```
!search What is gamma in options trading?
!search_full Explain butterfly spread strategies  
!search_compact How does theta decay work?
!search_minimal Quick gamma definition
!search_advanced 8 Complex iron condor strategies
!health
```

**Video Reference Formats:**

**Full:** `[Title](link) | 63:55 | 80:29 • Apr 2025`
         `"Content preview of first 100 characters..."`

**Compact:** `[Title](link) 63:55 80:29 • Apr 2025`

**Minimal:** `[Title](link) 63:55`

**Current Settings:**
• **Provider:** `{DEFAULT_PROVIDER.upper()}`
• **Default Results:** `{DEFAULT_RESULTS}`
• **API:** `{API_BASE_URL}`

*Choose your preferred video reference style for optimal Discord experience*
*All formats include clickable video links with exact timestamps*
*Powered by server-side Discord formatting for clean, readable results*
"""
    await ctx.send(help_text)

# Note: Event handlers are added dynamically in create_bot_with_dns()

async def cleanup_custom_session():
    """Clean up custom aiohttp session and connector"""
    global custom_session, custom_connector
    try:
        if custom_session and not custom_session.closed:
            await custom_session.close()
            logger.info(" Cleaned up custom aiohttp session")
        if custom_connector:
            await custom_connector.close()
            logger.info(" Cleaned up custom DNS connector")
    except Exception as e:
        logger.warning(f"⚠️ Error during cleanup: {e}")

async def setup_custom_dns_and_patches():
    """Set up custom DNS resolver and apply discord.py patches before bot creation"""
    global custom_session, custom_connector
    
    logger.info("🔧 Setting up custom DNS resolver and discord.py patches...")
    
    # Set up custom DNS resolver
    dns_success = await setup_custom_dns_resolver()
    
    if dns_success and custom_connector and custom_session:
        logger.info(" Custom DNS resolver setup successful")
        logger.info(" Discord.py patches applied before bot creation")
        return True
    else:
        logger.warning("⚠️ Custom DNS resolver setup failed - will use system DNS")
        return False

def create_bot():
    """Create bot instance (DNS resolver patches should already be applied)"""
    global bot
    
    logger.info("🔧 Creating bot instance...")
    
    # Create bot with intents
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    # Add event handlers to the bot
    @bot.event
    async def on_ready():
        """Called when the bot is ready and connected to Discord"""
        logger.info(f'🎉 Bot is ready! Logged in as {bot.user.name}')
        logger.info('Use !search <query> to search for options trading information')
        logger.info('Use !show_help to see all available commands')
        
        # Verify custom DNS resolver is working
        if custom_session and not custom_session.closed:
            logger.info(' Custom DNS resolver active and ready')
        if custom_connector:
            logger.info(' Discord.py using global aiohttp DNS patches with custom resolver')
        else:
            logger.warning('⚠️ Custom DNS resolver not available')
        
        # Set bot's activity status
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="!show_help for options trading info"
            )
        )

    @bot.event
    async def close():
        """Clean up resources when bot shuts down"""
        await cleanup_custom_session()
    
    @bot.event
    async def on_command_error(ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.command.name == 'search_advanced':
                await ctx.send("Please provide result count and query. Example: `!search_advanced 8 What is gamma?`")
            else:
                await ctx.send("Please provide a search query. Example: `!search What is gamma?`")
        else:
            error_msg = f"An error occurred: {str(error)}"
            logger.error(error_msg)
            await ctx.send(error_msg)
    
    # Add command handlers
    @bot.command(name='search')
    async def search_command(ctx, *, query: str):
        """Search for options trading information"""
        await search_handler(ctx, query)
    
    @bot.command(name='search_advanced')
    async def search_advanced_command(ctx, num_results: int, *, query: str):
        """Advanced search with custom result count"""
        await search_advanced_handler(ctx, num_results, query)
    
    @bot.command(name='search_full')
    async def search_full_command(ctx, *, query: str):
        """Search with full video details (title, timestamp, duration, content preview)"""
        await search_handler(ctx, query, template_override='full')
    
    @bot.command(name='search_compact')
    async def search_compact_command(ctx, *, query: str):
        """Search with compact video details (title, timestamp, duration only)"""
        await search_handler(ctx, query, template_override='compact')
    
    @bot.command(name='search_minimal')
    async def search_minimal_command(ctx, *, query: str):
        """Search with minimal video details (title and timestamp only)"""
        await search_handler(ctx, query, template_override='minimal')
    
    @bot.command(name='health')
    async def health_command(ctx):
        """Check API health status"""
        await health_handler(ctx)
    
    @bot.command(name='show_help')
    async def show_help_command(ctx):
        """Show help information"""
        await show_help_handler(ctx)
    
    return bot

def main():
    """Main function to run the bot with custom DNS resolver set up before connection"""
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found in environment variables")
        return
    
    logger.info("Starting Discord bot with pre-configured custom DNS resolver...")
    
    # Set up event loop properly (HuggingFace pattern)
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        logger.info(" Using uvloop for improved performance")
    except ImportError:
        logger.info("⚠️ uvloop not available - using default asyncio")
    
    # Basic environment setup
    import os
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'  # Prevent .pyc files
    
    # Pre-flight system DNS check (for comparison)
    logger.info("Pre-flight system DNS check...")
    try:
        import socket
        discord_ip = socket.gethostbyname('discord.com')
        logger.info(f" System DNS resolved discord.com -> {discord_ip}")
    except Exception as dns_error:
        logger.warning(f"⚠️ System DNS failed: {dns_error}")
        logger.info("🔧 Custom DNS resolver will bypass this issue")
    
    # Report resolver availability
    if custom_resolver_available:
        logger.info(" Custom DNS resolver dependencies available")
    else:
        logger.warning("⚠️ Custom DNS resolver dependencies not available - using system DNS")
    
    async def run_bot_with_custom_dns():
        """Main async function: set up DNS resolver, then create and start bot"""
        try:
            logger.info(" Phase 1: Setting up custom DNS resolver...")
            
            # Step 1: Set up custom DNS resolver and discord.py patches
            dns_success = await setup_custom_dns_and_patches()
            
            if dns_success:
                logger.info(" Custom DNS resolver and patches ready")
            else:
                logger.warning("⚠️ Using system DNS (custom resolver failed)")
            
            logger.info(" Phase 2: Creating bot instance...")
            
            # Step 2: Create bot instance (patches already applied)
            create_bot()
            logger.info(" Bot instance created")
            
            logger.info(" Phase 3: Starting bot with custom DNS resolver...")
            
            # Step 3: Start the bot (should now use our custom DNS for all connections)
            await bot.start(DISCORD_TOKEN)
            
        except Exception as e:
            logger.error(f"Bot failed to start: {str(e)}")
            logger.info("Diagnosing the issue...")
            
            # Quick connectivity diagnostics
            try:
                import socket
                socket.create_connection(("8.8.8.8", 53), timeout=3).close()
                logger.info(" Internet connectivity OK")
            except Exception:
                logger.error("❌ No internet connectivity")
            
            # Check if it's still a DNS issue
            try:
                discord_ip = socket.gethostbyname('discord.com')
                logger.info(f" System DNS works: discord.com -> {discord_ip}")
                logger.error("Issue may not be DNS-related")
            except Exception as dns_error:
                logger.error(f"System DNS still failing: {dns_error}")
                logger.error("Custom DNS resolver should have bypassed this")
                
            raise  # Re-raise the exception
        finally:
            # Clean up custom sessions and connectors
            logger.info("🧹 Cleaning up custom DNS resolver resources...")
            await cleanup_custom_session()
    
    try:
        # Run the bot with custom DNS resolver setup
        asyncio.run(run_bot_with_custom_dns())
    except Exception as e:
        logger.error(f"Bot startup failed: {str(e)}")
        logger.error("Custom DNS resolver approach was unsuccessful")

if __name__ == "__main__":
    main() 