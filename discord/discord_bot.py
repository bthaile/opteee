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

# Set up Discord bot with intents and custom DNS resolver
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Global variables for custom session management
custom_session = None
custom_connector = None
custom_resolver_available = False

# Import aiohttp components (but don't initialize yet)
try:
    import aiohttp
    import asyncio
    from aiohttp.resolver import AsyncResolver
    import discord
    import discord.http
    import discord.gateway
    custom_resolver_available = True
    logger.info("✅ Custom DNS resolver dependencies available")
except ImportError as e:
    logger.warning(f"⚠️ AsyncResolver not available: {e}")
    custom_resolver_available = False

# Bot will be created after setting up DNS resolver (see main function)
bot = None

async def setup_custom_dns_resolver():
    """Set up custom DNS resolver in async context"""
    global custom_session, custom_connector
    
    if not custom_resolver_available:
        logger.warning("⚠️ Custom DNS resolver dependencies not available")
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
        custom_session = aiohttp.ClientSession(
            connector=custom_connector,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        
        logger.info("✅ Created custom DNS resolver with Google/Cloudflare DNS in async context")
        
        # Comprehensive monkey patching for discord.py
        await setup_discord_patches()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create custom DNS resolver: {e}")
        return False

async def setup_discord_patches():
    """Set up comprehensive discord.py patches to use custom DNS resolver"""
    global custom_session, custom_connector
    
    try:
        logger.info("🔧 Applying comprehensive discord.py DNS patches...")
        
        # 1. Patch session creation after HTTPClient initialization
        original_http_init = discord.http.HTTPClient.__init__
        
        def custom_http_init(self, *args, **kwargs):
            """Override HTTPClient init to replace session after normal initialization"""
            # Call original init normally - let it handle all arguments properly
            result = original_http_init(self, *args, **kwargs)
            
            # After initialization, replace the session with our custom DNS session
            if custom_session:
                # Close the default session if it exists
                if hasattr(self, '_HTTPClient__session') and self._HTTPClient__session and not self._HTTPClient__session.closed:
                    # Schedule closure for later (can't await in sync function)
                    pass
                
                # Replace with our custom DNS session
                self._HTTPClient__session = custom_session
                self._custom_session_patched = True
                logger.info("🔧 HTTPClient session replaced with custom DNS session")
            
            return result
        
        # Apply HTTPClient init patch  
        discord.http.HTTPClient.__init__ = custom_http_init
        logger.info("✅ Applied HTTPClient session replacement patch")
        
        # 2. Patch HTTP requests (backup/fallback)
        original_request = discord.http.HTTPClient.request
        
        async def custom_request(self, route, **kwargs):
            """Override discord.py HTTP requests to use our custom session"""
            # Ensure we're using our custom session
            if not hasattr(self, '_custom_session_patched') and custom_session:
                if hasattr(self, '_HTTPClient__session') and not self._HTTPClient__session.closed:
                    await self._HTTPClient__session.close()
                self._HTTPClient__session = custom_session
                self._custom_session_patched = True
                logger.info("🔧 Late-patched HTTP client to use custom DNS resolver")
            
            return await original_request(self, route, **kwargs)
        
        # Apply the HTTP request patch
        discord.http.HTTPClient.request = custom_request
        logger.info("✅ Applied HTTP request patch")
        
        # 3. Patch WebSocket connections for gateway
        try:
            original_websocket_from_client = discord.gateway.DiscordWebSocket.from_client
            
            @classmethod
            async def custom_websocket_from_client(cls, client, **kwargs):
                """Override discord.py WebSocket to use custom DNS resolver"""
                # Ensure the client's HTTP session uses our custom session
                if hasattr(client.http, '_HTTPClient__session') and custom_session:
                    if not client.http._HTTPClient__session.closed:
                        await client.http._HTTPClient__session.close()
                    client.http._HTTPClient__session = custom_session
                    logger.info("🔧 WebSocket client session replaced with custom DNS session")
                
                return await original_websocket_from_client(client, **kwargs)
            
            # Apply WebSocket patch
            discord.gateway.DiscordWebSocket.from_client = custom_websocket_from_client
            logger.info("✅ Applied WebSocket gateway patch")
            
        except (ImportError, AttributeError) as ws_error:
            logger.warning(f"⚠️ Could not patch WebSocket DNS resolver: {ws_error}")
        
        logger.info("✅ All discord.py DNS patches applied successfully")
        
    except Exception as patch_error:
        logger.error(f"❌ Failed to apply discord.py DNS patches: {patch_error}")
        raise

def format_answer_for_discord(html_content: str) -> str:
    """Convert HTML content to Discord-native markdown format using html_to_markdown library"""
    try:
        from html_to_markdown import convert_to_markdown
        from bs4 import BeautifulSoup
        import re
        
        # Use html_to_markdown for robust HTML to markdown conversion
        markdown_content = convert_to_markdown(
            html_content,
            heading_style='atx',  # Use # headers initially, we'll convert to bold for Discord
            bullets='*',
            strong_em_symbol='*',
            escape_asterisks=False,  # We'll handle escaping ourselves
            escape_underscores=False,
            extract_metadata=False,  # Don't add metadata comments
            strip_newlines=True,
            wrap=False
        )
        
        content = markdown_content
        
    except ImportError:
        # Fallback to old method if html_to_markdown is not available
        from bs4 import BeautifulSoup
        from markdownify import markdownify
        import re
        
        # Parse HTML properly with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Clean up source references before converting
        for elem in soup.find_all(['div', 'section', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'], string=re.compile(r'Source References?', re.I)):
            elem.decompose()
        
        for elem in soup.find_all(string=re.compile(r'Source References?', re.I)):
            parent = elem.parent
            if parent:
                parent.decompose()
        
        # Convert HTML to markdown using markdownify
        markdown_content = markdownify(str(soup), 
                                      heading_style="ATX",  # Use # for headers
                                      bullets="-",          # Use - for bullets
                                      strip=['img', 'script', 'style'])  # Remove unwanted elements
        
        content = markdown_content
    
    # Convert ATX headers (# ## ###) to Discord bold format since Discord doesn't render them well
    content = re.sub(r'^#+\s*(.*?)$', r'**\1**', content, flags=re.MULTILINE)
    
    # Convert bullet points to Discord format (• instead of -)
    content = re.sub(r'^[\-\*]\s+', '• ', content, flags=re.MULTILINE)
    
    # Essential Discord-specific formatting
    
    # Handle LaTeX formulas - simplified approach for better Discord compatibility
    def convert_latex_formulas(text_content):
        
        def clean_latex_formula(formula):
            """Clean and convert a LaTeX formula to readable text"""
            # Start with the raw formula
            cleaned = formula.strip()
            
            # Clean up \text{} commands first - handle both single and double backslashes
            cleaned = re.sub(r'\\\\text\s*\{([^}]*)\}', r'\1', cleaned)
            cleaned = re.sub(r'\\text\s*\{([^}]*)\}', r'\1', cleaned)
            
            # Handle LaTeX symbol replacements - account for double backslashes from HTML
            replacements = {
                # Double backslash versions (from HTML)
                r'\\\\sum\b': '∑', r'\\\\prod\b': '∏', r'\\\\times\b': '×',
                r'\\\\cdot\b': '·', r'\\\\div\b': '÷', r'\\\\pm\b': '±',
                r'\\\\alpha\b': 'α', r'\\\\beta\b': 'β', r'\\\\gamma\b': 'γ',
                r'\\\\delta\b': 'δ', r'\\\\epsilon\b': 'ε', r'\\\\zeta\b': 'ζ',
                r'\\\\eta\b': 'η', r'\\\\theta\b': 'θ', r'\\\\lambda\b': 'λ',
                r'\\\\mu\b': 'μ', r'\\\\pi\b': 'π', r'\\\\rho\b': 'ρ',
                r'\\\\sigma\b': 'σ', r'\\\\tau\b': 'τ', r'\\\\phi\b': 'φ',
                r'\\\\chi\b': 'χ', r'\\\\psi\b': 'ψ', r'\\\\omega\b': 'ω',
                # Single backslash versions (fallback)
                r'\\sum\b': '∑', r'\\prod\b': '∏', r'\\times\b': '×',
                r'\\cdot\b': '·', r'\\div\b': '÷', r'\\pm\b': '±',
                r'\\alpha\b': 'α', r'\\beta\b': 'β', r'\\gamma\b': 'γ',
                r'\\delta\b': 'δ', r'\\epsilon\b': 'ε', r'\\zeta\b': 'ζ',
                r'\\eta\b': 'η', r'\\theta\b': 'θ', r'\\lambda\b': 'λ',
                r'\\mu\b': 'μ', r'\\pi\b': 'π', r'\\rho\b': 'ρ',
                r'\\sigma\b': 'σ', r'\\tau\b': 'τ', r'\\phi\b': 'φ',
                r'\\chi\b': 'χ', r'\\psi\b': 'ψ', r'\\omega\b': 'ω',
                # Math operators
                r'\\sqrt\b': '√', r'\\infty\b': '∞', r'\\approx\b': '≈',
                r'\\leq\b': '≤', r'\\geq\b': '≥', r'\\neq\b': '≠'
            }
            
            for latex_cmd, unicode_symbol in replacements.items():
                cleaned = re.sub(latex_cmd, unicode_symbol, cleaned)
            
            # Remove remaining LaTeX commands (both single and double backslashes)
            cleaned = re.sub(r'\\\\[a-zA-Z]+\*?', '', cleaned)
            cleaned = re.sub(r'\\[a-zA-Z]+\*?', '', cleaned)
            
            # Remove leftover braces and backslashes
            cleaned = re.sub(r'[{}]+', '', cleaned)
            cleaned = re.sub(r'\\+', '', cleaned)
            
            # Handle superscripts and subscripts
            superscript_map = {
                '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
                '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
                '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾'
            }
            
            subscript_map = {
                '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
                '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
                '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎'
            }
            
            # Convert simple superscripts (like ^2, ^3)
            def convert_superscript(match):
                char = match.group(1)
                return superscript_map.get(char, f'^{char}')
            
            def convert_subscript(match):
                char = match.group(1)
                return subscript_map.get(char, f'_{char}')
            
            # Apply superscript/subscript conversions
            cleaned = re.sub(r'\^([0-9+\-=()])', convert_superscript, cleaned)
            cleaned = re.sub(r'_([0-9+\-=()])', convert_subscript, cleaned)
            
            # Fix spacing around operators
            cleaned = re.sub(r'\s*([+\-×÷=])\s*', r' \1 ', cleaned)
            cleaned = re.sub(r'\s*([()])\s*', r'\1', cleaned)
            
            # Clean up excessive whitespace
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            
            return cleaned
        
        # Process different LaTeX formula patterns with better detection
        patterns = [
            # Display math patterns
            (r'\\\[(.*?)\\\]', lambda m: f'\n```\n{clean_latex_formula(m.group(1))}\n```\n'),
            (r'\$\$(.*?)\$\$', lambda m: f'\n```\n{clean_latex_formula(m.group(1))}\n```\n'),
            # Inline math patterns  
            (r'\\\((.*?)\\\)', lambda m: f' `{clean_latex_formula(m.group(1))}` '),
            (r'\$([^$\n]{1,50})\$', lambda m: f' `{clean_latex_formula(m.group(1))}` '),
        ]
        
        for pattern, replacement in patterns:
            text_content = re.sub(pattern, replacement, text_content, flags=re.DOTALL)
        
        return text_content
    
    # Apply LaTeX formula conversion
    content = convert_latex_formulas(content)
    
    # Remove source references sections
    source_patterns = [
        r'\*\*Source References?\*\*.*$',
        r'Source References?.*$', 
        r'^.*Source References?.*$'
    ]
    
    for pattern in source_patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE)
    
    # Remove citation patterns
    citation_patterns = [
        r'\n\d+\.\s+".*?"\s*\(Score:.*?\).*?\n',  # Numbered citations with scores
        r'\n\d+\.\s+".*?"\s*-\s*Upload Date:.*?\n',  # Numbered citations with dates
        r'^•\s*".*?"\s*\(Score:.*?\).*$',  # Bullet citations with scores
        r'^•\s*".*?"\s*-\s*Upload Date:.*$'  # Bullet citations with dates
    ]
    
    for pattern in citation_patterns:
        content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Enhanced bullet point labels
    bullet_enhancements = {
        '• Definition:': '• **Definition:**',
        '• Formula:': '• **Formula:**', 
        '• Example:': '• **Example:**',
        '• Purpose:': '• **Purpose:**',
        '• Note:': '• **Note:**',
        '• Key Point:': '• **Key Point:**'
    }
    
    for old, new in bullet_enhancements.items():
        content = content.replace(old, new)
    
    # Format financial values and percentages
    content = re.sub(r'(?<!\*)\$(\d+(?:\.\d{2})?)\b', r'**$\1**', content)  # Dollar amounts
    content = re.sub(r'\b(\d+(?:\.\d+)?)%\b(?!\*)', r'**\1%**', content)   # Percentages
    
    # Format technical terms
    technical_terms = ['Theta', 'Delta', 'Gamma', 'Vega', 'Rho', 'Greeks', 'IV', 'ATM', 'ITM', 'OTM']
    for term in technical_terms:
        content = re.sub(rf'(?<![`*\[\]])\b{re.escape(term)}\b(?![`*\]\)])', f'`{term}`', content)
    
    # Clean up excessive whitespace and backslashes
    content = re.sub(r'\s\\+\s', ' ', content)  # Multiple backslashes between spaces
    content = re.sub(r'^\s*\\+\s*$', '', content, flags=re.MULTILINE)  # Lines with only backslashes
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)  # Multiple newlines to double newlines
    content = re.sub(r'^\s+|\s+$', '', content)  # Leading/trailing whitespace
    
    # Add block quote for Quick Answer (if present)
    content = re.sub(r'^(\*\*Quick Answer\*\*)', r'> \1', content, flags=re.MULTILINE)
    
    return content.strip()

def improve_document_references(answer: str, sources: list) -> str:
    """Replace [Document N] references with more user-friendly video link references"""
    import re
    
    if not sources:
        return answer
    
    # Create a mapping of document numbers to video info
    doc_mapping = {}
    for i, source in enumerate(sources, 1):
        timestamp_seconds = source.get('start_timestamp_seconds', 0)
        
        # Format timestamp for inline display
        timestamp_str = ""
        if timestamp_seconds and timestamp_seconds > 0:
            minutes = int(timestamp_seconds // 60)
            seconds = int(timestamp_seconds % 60)
            timestamp_str = f" @ {minutes}:{seconds:02d}"
        
        # Get the best available title
        title = source.get('title', 'Untitled Video')
        
        # If title looks like a video ID, try to get a better title
        if len(title) == 11 and title.isalnum():  # YouTube video ID format
            # Try to use filename or other fields
            title = source.get('filename', source.get('file_name', title))
            # Clean up filename extensions
            title = title.replace('.mp3', '').replace('.wav', '').replace('.mp4', '')
        
        # Ensure we have a reasonable URL
        url = source.get('video_url_with_timestamp') or source.get('url', '#')
        if url == '#' or not url:
            # Try to construct from video ID if available
            video_id = source.get('video_id') or source.get('id')
            if video_id and timestamp_seconds:
                url = f"https://www.youtube.com/watch?v={video_id}&t={int(timestamp_seconds)}s"
            elif video_id:
                url = f"https://www.youtube.com/watch?v={video_id}"
        
        doc_mapping[i] = {
            'title': title,
            'url': url,
            'timestamp_str': timestamp_str
        }
    
    def replace_doc_ref(match):
        doc_num = int(match.group(1))
        if doc_num in doc_mapping:
            title = doc_mapping[doc_num]['title']
            url = doc_mapping[doc_num]['url']
            timestamp_str = doc_mapping[doc_num]['timestamp_str']
            
            # Clean up title and truncate if too long for inline display
            title = title.replace('|', '-').replace('[', '(').replace(']', ')')
            # Reduce title length more to accommodate timestamp
            if len(title) > 25:
                title = title[:22] + "..."
            
            # Create clickable link with timestamp info in Discord format (suppress preview with < >)
            return f"**[Video {doc_num}{timestamp_str}: {title}](<{url}>)**"
        else:
            return f"**[Video {doc_num}]**"
    
    # Replace [Document N] with enhanced video references (case insensitive)
    answer = re.sub(r'\[Document (\d+)\]', replace_doc_ref, answer, flags=re.IGNORECASE)
    
    return answer

async def query_opteee(query: str, num_results: int = 5, provider: str = "openai") -> dict:
    """Query the opteee application using the new FastAPI backend"""
    try:
        async with aiohttp.ClientSession() as session:
            # Use the new FastAPI ChatRequest format
            payload = {
                "query": query,
                "provider": provider,
                "num_results": num_results
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            async with session.post(CHAT_ENDPOINT, json=payload, headers=headers) as response:
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
    except Exception as e:
        error_msg = f"Connection error: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

# Command handler functions (will be added to bot dynamically)

async def search_handler(ctx, query: str):
    """Search for options trading information"""
    logger.info(f'Search query from {ctx.author}: {query}')
    
    # Send initial response with more engaging format
    await ctx.send(f"**Searching the knowledge base...**\n> {query}\n*Analyzing thousands of transcript segments...*")
    
    try:
        # Query opteee with default settings
        response = await query_opteee(query, num_results=DEFAULT_RESULTS, provider=DEFAULT_PROVIDER)
        
        if not response["success"]:
            await ctx.send(f"{response['error']}")
            return
        
        answer = response["answer"]
        sources = response["sources"]
        
        # First convert HTML to Discord markdown
        formatted_answer = format_answer_for_discord(answer)
        
        # Then improve document references (after HTML processing to avoid corruption)
        formatted_answer = improve_document_references(formatted_answer, sources)
        
        # Format the response for Discord (Discord doesn't support ## headers)
        formatted_response = f"{formatted_answer}"
        
        # Add source information if available
        if sources:
            source_text = f"\n\n**Video Sources**\n"
            for i, source in enumerate(sources[:5], 1):  # Show up to 5 sources
                title = source.get('title', 'Untitled Video')
                url = source.get('video_url_with_timestamp', source.get('url', '#'))
                timestamp = source.get('start_timestamp_seconds', 0)
                upload_date = source.get('upload_date', '')
                
                # Format timestamp (specific location in video)
                if timestamp > 0:
                    minutes = int(timestamp // 60)
                    seconds = int(timestamp % 60)
                    time_str = f"▶️ {minutes}:{seconds:02d}"
                else:
                    time_str = "▶️ 0:00"
                
                # Format total duration for context
                total_duration = source.get('duration_seconds', 0)
                duration_context = ""
                if total_duration and total_duration > 0:
                    dur_minutes = int(total_duration // 60)
                    dur_seconds = int(total_duration % 60)
                    duration_context = f" / {dur_minutes}:{dur_seconds:02d} total"
                
                # Format upload date
                date_str = ""
                if upload_date and upload_date != 'Unknown':
                    try:
                        if len(upload_date) == 8:  # YYYYMMDD format
                            from datetime import datetime
                            date_obj = datetime.strptime(upload_date, '%Y%m%d')
                            date_str = f" • {date_obj.strftime('%b %Y')}"
                    except:
                        pass
                
                # Get transcript content
                content = source.get('content', source.get('text', ''))
                if content:
                    # Truncate if too long and clean up
                    max_content_length = 200
                    if len(content) > max_content_length:
                        truncated_content = content[:max_content_length].strip()
                        # Try to end at a sentence or word boundary
                        if '.' in truncated_content[-50:]:
                            truncated_content = truncated_content[:truncated_content.rfind('.') + 1]
                        elif ' ' in truncated_content[-20:]:
                            truncated_content = truncated_content[:truncated_content.rfind(' ')]
                        truncated_content += "..."
                    else:
                        truncated_content = content.strip()
                    
                    # Create professional source entry with transcript and duration context (suppress preview)
                    source_text += f"**{i}.** **[{title}](<{url}>)** `{time_str}{duration_context}`{date_str}\n"
                    source_text += f"*\"{truncated_content}\"*\n\n"
                else:
                    # Fallback without transcript content (suppress preview)
                    source_text += f"**{i}.** **[{title}](<{url}>)** `{time_str}{duration_context}`{date_str}\n"
            
            formatted_response += source_text
        
        # Add footer with helpful context  
        footer = f"\n\n━━━━━━━━━━━━━━━━━━━━\n*Refine your search to get better results!*"
        formatted_response += footer
        
        # Split response into chunks if it's too long (Discord has 2000 char limit)
        if len(formatted_response) > 1900:
            chunks = [formatted_response[i:i+1900] for i in range(0, len(formatted_response), 1900)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(formatted_response)
            
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        await ctx.send(error_msg)

async def search_advanced_handler(ctx, num_results: int, query: str):
    """Advanced search with custom result count"""
    # Validate inputs
    if not 1 <= num_results <= 10:
        await ctx.send("Number of results must be between 1 and 10")
        return
    
    # Use default provider
    provider = DEFAULT_PROVIDER
    
    logger.info(f'Advanced search from {ctx.author}: {query} (provider: {provider}, results: {num_results})')
    await ctx.send(f"**Advanced Search Mode**\n> {query}\n*Using {provider.upper()} AI • Retrieving {num_results} sources • Processing...*")
    
    try:
        response = await query_opteee(query, num_results=num_results, provider=provider)
        
        if not response["success"]:
            await ctx.send(f"{response['error']}")
            return
        
        answer = response["answer"]
        sources = response["sources"]
        
        # First convert HTML to Discord markdown
        formatted_answer = format_answer_for_discord(answer)
        
        # Then improve document references (after HTML processing to avoid corruption)
        formatted_answer = improve_document_references(formatted_answer, sources)
        
        # Format response with provider info (Discord doesn't support ## headers)
        formatted_response = f"**{provider.upper()} Response:**\n{formatted_answer}"
        
        if sources:
            source_text = f"\n\n**Video Sources**\n"
            for i, source in enumerate(sources[:5], 1):  # Show up to 5 sources
                title = source.get('title', 'Untitled Video')
                url = source.get('video_url_with_timestamp', source.get('url', '#'))
                timestamp = source.get('start_timestamp_seconds', 0)
                upload_date = source.get('upload_date', '')
                
                # Format timestamp (specific location in video)
                if timestamp > 0:
                    minutes = int(timestamp // 60)
                    seconds = int(timestamp % 60)
                    time_str = f"▶️ {minutes}:{seconds:02d}"
                else:
                    time_str = "▶️ 0:00"
                
                # Format total duration for context
                total_duration = source.get('duration_seconds', 0)
                duration_context = ""
                if total_duration and total_duration > 0:
                    dur_minutes = int(total_duration // 60)
                    dur_seconds = int(total_duration % 60)
                    duration_context = f" / {dur_minutes}:{dur_seconds:02d} total"
                
                # Format upload date
                date_str = ""
                if upload_date and upload_date != 'Unknown':
                    try:
                        if len(upload_date) == 8:  # YYYYMMDD format
                            from datetime import datetime
                            date_obj = datetime.strptime(upload_date, '%Y%m%d')
                            date_str = f" • {date_obj.strftime('%b %Y')}"
                    except:
                        pass
                
                # Get transcript content
                content = source.get('content', source.get('text', ''))
                if content:
                    # Truncate if too long and clean up
                    max_content_length = 200
                    if len(content) > max_content_length:
                        truncated_content = content[:max_content_length].strip()
                        # Try to end at a sentence or word boundary
                        if '.' in truncated_content[-50:]:
                            truncated_content = truncated_content[:truncated_content.rfind('.') + 1]
                        elif ' ' in truncated_content[-20:]:
                            truncated_content = truncated_content[:truncated_content.rfind(' ')]
                        truncated_content += "..."
                    else:
                        truncated_content = content.strip()
                    
                    # Create professional source entry with transcript and duration context (suppress preview)
                    source_text += f"**{i}.** **[{title}](<{url}>)** `{time_str}{duration_context}`{date_str}\n"
                    source_text += f"*\"{truncated_content}\"*\n\n"
                else:
                    # Fallback without transcript content (suppress preview)
                    source_text += f"**{i}.** **[{title}](<{url}>)** `{time_str}{duration_context}`{date_str}\n"
            
            formatted_response += source_text
        
        # Add footer with helpful suggestions
        if num_results < 8:
            footer = f"\n\n━━━━━━━━━━━━━━━━━━━━\n*Try more sources for detailed analysis:*\n`!search_advanced {min(10, num_results + 3)} your question`"
        else:
            footer = f"\n\n━━━━━━━━━━━━━━━━━━━━\n*Try basic search for quicker results:*\n`!search your question`"
        formatted_response += footer
        
        # Split if too long
        if len(formatted_response) > 1900:
            chunks = [formatted_response[i:i+1900] for i in range(0, len(formatted_response), 1900)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(formatted_response)
            
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        logger.error(error_msg)
        await ctx.send(error_msg)

async def health_handler(ctx):
    """Check if the OPTEEE API is healthy"""
    await ctx.send("**System Health Check**\n*Testing connection to OPTEEE API...*")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(HEALTH_ENDPOINT) as response:
                if response.status == 200:
                    data = await response.json()
                    status = data.get('status', 'unknown')
                    version = data.get('version', 'unknown')
                    await ctx.send(f"""**All Systems Operational**
                    
**API Status:** `{status.title()}`
**Version:** `{version}`
**Endpoint:** `{API_BASE_URL}`

*Ready to search thousands of options trading transcripts!*""")
                else:
                    await ctx.send(f"**API Status:** `Unhealthy` (HTTP {response.status})\n*The main OPTEEE API may be temporarily unavailable.*")
    except Exception as e:
        await ctx.send(f"**Connection Failed**\n*Unable to reach OPTEEE API*\n```\n{str(e)[:100]}...\n```")

async def show_help_handler(ctx):
    """Show help information"""
    help_text = f"""
**OPTEEE Discord Bot - Options Trading Knowledge Search**

**Basic Commands:**
`!search <query>` - Search with transcript excerpts, timestamps, and clickable video links
`!search_advanced <num_results> <query>` - Advanced search with custom result count
`!health` - Check API status
`!show_help` - Show this help message

**Examples:**
`!search What is gamma in options trading?`
`!search_advanced 8 Explain butterfly spread strategies`
`!health`

**Advanced Search Options:**
• **Results:** 1-10 (more results = more comprehensive but longer response)

**Current Settings:**
• Default Provider: `{DEFAULT_PROVIDER}`
• Default Results: `{DEFAULT_RESULTS}`
• API Endpoint: `{API_BASE_URL}`

*This bot searches through thousands of options trading video transcripts to provide accurate, sourced answers with user-friendly video references.*

**Note:** Technical references like "[Document 4]" are automatically converted to **clickable video links with timestamps** like "**[Video 4 @ 66:10: Options Greeks Explained](url)**" that take you directly to the relevant moment in the video!

*Current AI Provider: {DEFAULT_PROVIDER.upper()}*
"""
    await ctx.send(help_text)

# Note: Event handlers are added dynamically in create_bot_with_dns()

async def cleanup_custom_session():
    """Clean up custom aiohttp session and connector"""
    global custom_session, custom_connector
    try:
        if custom_session and not custom_session.closed:
            await custom_session.close()
            logger.info("✅ Cleaned up custom aiohttp session")
        if custom_connector:
            await custom_connector.close()
            logger.info("✅ Cleaned up custom DNS connector")
    except Exception as e:
        logger.warning(f"⚠️ Error during cleanup: {e}")

async def setup_custom_dns_and_patches():
    """Set up custom DNS resolver and apply discord.py patches before bot creation"""
    global custom_session, custom_connector
    
    logger.info("🔧 Setting up custom DNS resolver and discord.py patches...")
    
    # Set up custom DNS resolver
    dns_success = await setup_custom_dns_resolver()
    
    if dns_success and custom_connector and custom_session:
        logger.info("✅ Custom DNS resolver setup successful")
        logger.info("✅ Discord.py patches applied before bot creation")
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
            logger.info('✅ Custom DNS resolver active and ready')
        if hasattr(bot.http, '_custom_session_patched'):
            logger.info('✅ Discord.py is using custom DNS resolver for HTTP requests')
        else:
            logger.warning('⚠️ Custom DNS resolver patch not detected (may be OK if using fallback)')
        
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
        logger.info("✅ Using uvloop for improved performance")
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
        logger.info(f"✅ System DNS resolved discord.com -> {discord_ip}")
    except Exception as dns_error:
        logger.warning(f"⚠️ System DNS failed: {dns_error}")
        logger.info("🔧 Custom DNS resolver will bypass this issue")
    
    # Report resolver availability
    if custom_resolver_available:
        logger.info("✅ Custom DNS resolver dependencies available")
    else:
        logger.warning("⚠️ Custom DNS resolver dependencies not available - using system DNS")
    
    async def run_bot_with_custom_dns():
        """Main async function: set up DNS resolver, then create and start bot"""
        try:
            logger.info("🚀 Phase 1: Setting up custom DNS resolver...")
            
            # Step 1: Set up custom DNS resolver and discord.py patches
            dns_success = await setup_custom_dns_and_patches()
            
            if dns_success:
                logger.info("✅ Custom DNS resolver and patches ready")
            else:
                logger.warning("⚠️ Using system DNS (custom resolver failed)")
            
            logger.info("🚀 Phase 2: Creating bot instance...")
            
            # Step 2: Create bot instance (patches already applied)
            create_bot()
            logger.info("✅ Bot instance created")
            
            logger.info("🚀 Phase 3: Starting bot with custom DNS resolver...")
            
            # Step 3: Start the bot (should now use our custom DNS for all connections)
            await bot.start(DISCORD_TOKEN)
            
        except Exception as e:
            logger.error(f"Bot failed to start: {str(e)}")
            logger.info("Diagnosing the issue...")
            
            # Quick connectivity diagnostics
            try:
                import socket
                socket.create_connection(("8.8.8.8", 53), timeout=3).close()
                logger.info("✅ Internet connectivity OK")
            except Exception:
                logger.error("❌ No internet connectivity")
            
            # Check if it's still a DNS issue
            try:
                discord_ip = socket.gethostbyname('discord.com')
                logger.info(f"✅ System DNS works: discord.com -> {discord_ip}")
                logger.error("💡 Issue may not be DNS-related")
            except Exception as dns_error:
                logger.error(f"❌ System DNS still failing: {dns_error}")
                logger.error("💡 Custom DNS resolver should have bypassed this")
                
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