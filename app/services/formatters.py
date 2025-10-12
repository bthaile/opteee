"""
Response formatters for different output formats (HTML, Discord, etc.)
"""

import re
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class ResponseFormatter:
    """Base class for response formatting"""
    
    def __init__(self):
        self.formatters = {
            "html": HtmlFormatter(),
            "discord": DiscordFormatter()
        }
    
    def format_response(self, answer: str, sources: List[Dict], format_type: str = "html") -> Dict[str, Any]:
        """
        Format the response based on the requested format type
        
        Args:
            answer: The RAG-generated answer
            sources: List of source documents
            format_type: Format type ("html" or "discord")
            
        Returns:
            Dictionary with formatted_content and format
        """
        formatter = self.formatters.get(format_type.lower(), self.formatters["html"])
        return formatter.format(answer, sources)


class HtmlFormatter:
    """HTML formatter - maintains existing web UI formatting"""
    
    def format(self, answer: str, sources: List[Dict]) -> Dict[str, Any]:
        """Format response for web UI (HTML)"""
        # Process markdown but keep structure simple for frontend compatibility
        formatted_answer = self._process_markdown_simple(answer)
        
        # Clean the HTML to remove any wrapper divs that would conflict with frontend
        formatted_answer = self._clean_html_structure(formatted_answer)
        
        # Extract quotes from the answer for highlighting
        quotes = self._extract_quotes_from_answer(answer)
        
        # Create enhanced video reference cards
        if not sources:
            return {
                "formatted_content": {
                    "answer": formatted_answer,
                    "sources": "",
                    "raw_sources": []
                },
                "format": "html"
            }
        
        # Don't add outer wrapper - frontend will handle main container
        sources_content = '<div class="video-references">'
        
        # Add informative header if we have highlights
        if quotes and len(quotes) > 0:
            sources_content += '''
                <div class="sources-header">
                    <h4>📚 Source Videos with Highlighted Quotes</h4>
                    <p>Key phrases from the AI's answer are <span class="highlight-legend">highlighted</span> in the transcript snippets below for easy reference.</p>
                </div>
            '''
        
        for i, source in enumerate(sources):
            title = source.get('title', 'Untitled Video')
            url = source.get('url', '#')
            video_url_with_timestamp = source.get('video_url_with_timestamp', url)
            upload_date = source.get('upload_date', 'Unknown')
            duration_seconds = source.get('duration_seconds', 0)
            start_timestamp_seconds = source.get('start_timestamp_seconds', 0.0)

            # Format start timestamp
            if isinstance(start_timestamp_seconds, (int, float)) and start_timestamp_seconds > 0:
                minutes = int(start_timestamp_seconds // 60)
                seconds = int(start_timestamp_seconds % 60)
                timestamp_formatted = f"{minutes}:{seconds:02d}"
            else:
                timestamp_formatted = "0:00"

            # Format duration
            if isinstance(duration_seconds, (int, float)) and duration_seconds > 0:
                duration_minutes = int(duration_seconds // 60)
                duration_secs = int(duration_seconds % 60)
                duration_formatted = f"{duration_minutes}:{duration_secs:02d}"
            else:
                duration_formatted = "Unknown"
            
            # Format upload date
            if upload_date != 'Unknown':
                try:
                    if isinstance(upload_date, str) and len(upload_date) == 8:  # YYYYMMDD format
                        date_obj = datetime.strptime(upload_date, '%Y%m%d')
                        upload_date_formatted = date_obj.strftime('%B %d, %Y')
                    elif isinstance(upload_date, str) and '-' in upload_date:  # YYYY-MM-DD format
                        date_obj = datetime.strptime(upload_date.split('T')[0], '%Y-%m-%d')
                        upload_date_formatted = date_obj.strftime('%B %d, %Y')
                    else:
                        upload_date_formatted = str(upload_date)
                except:
                    upload_date_formatted = str(upload_date)
            else:
                upload_date_formatted = 'Unknown'
            
            # Get transcript content and apply highlighting
            content = source.get('content', source.get('text', ''))
            highlighted_content = self._highlight_text_in_content(content, quotes)
            
            # Show more context if quotes were found - expand to 400 chars
            display_length = 400 if any(q.lower() in content.lower() for q in quotes) else 200
            
            # Truncate after highlighting (preserve HTML tags)
            if len(content) > display_length:
                truncated_content = highlighted_content[:display_length + 50] + '...'
            else:
                truncated_content = highlighted_content

            meta_items = [
                f'''<div class="metadata-item" title="Jump to timestamp in video"><svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#0f766e' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'></circle><polygon points='10 8 16 12 10 16 10 8'></polygon></svg><span>{timestamp_formatted}</span></div>''',
                f'''<div class="metadata-item" title="Total video duration"><svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#0f766e' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='12' cy='12' r='10'></circle><polyline points='12 6 12 12 16 14'></polyline></svg><span>{duration_formatted}</span></div>''',
                f'''<div class="metadata-item" title="Video upload date"><svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#0f766e' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='4' width='18' height='18' rx='2' ry='2'></rect><line x1='16' y1='2' x2='16' y2='6'></line><line x1='8' y1='2' x2='8' y2='6'></line><line x1='3' y1='10' x2='21' y2='10'></line></svg><span>{upload_date_formatted}</span></div>'''
            ]

            metadata_html = ''.join(meta_items)

            # Create compact and professional video card HTML
            sources_content += f'''
                <div class="video-card">
                    <div class="video-card-header">
                        <a href='{video_url_with_timestamp}' target='_blank' class='video-title-link'>
                            <h4 class='video-title'>{title}</h4>
                        </a>
                    </div>

                    <div class="transcript-snippet">
                        <p>"{truncated_content}"</p>
                    </div>

                    <div class="video-footer">
                        <div class="video-metadata">
                            {metadata_html}
                        </div>
                        <div class="video-actions">
                            <a href='{video_url_with_timestamp}' target='_blank' class='video-action-btn' title='Watch on YouTube'>
                                <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='#0f766e' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2A29 29 0 0 0 23 11.75a29 29 0 0 0-.46-5.33z'></path><polygon points='9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02'></polygon></svg>
                            </a>
                            <button class='video-action-btn' onclick="copyToClipboard('{video_url_with_timestamp}', this)" title='Copy link'>
                                <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='#0f766e' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='9' y='9' width='13' height='13' rx='2' ry='2'></rect><path d='M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1'></path></svg>
                            </button>
                        </div>
                    </div>
                </div>
            '''
        
        sources_content += '</div>'
        
        return {
            "formatted_content": {
                "answer": formatted_answer,
                "sources": sources_content,
                "raw_sources": sources
            },
            "format": "html"
        }
    
    def _process_markdown_simple(self, text: str) -> str:
        """
        Process markdown text into simple HTML without nested structures
        This avoids the nested div issues while still formatting content properly
        """
        # Process headers - convert ### to h3, #### to h4, etc.
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
        
        # Process bold text
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        
        # Process code blocks
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        
        # Process simple bullet points (but not nested ones to avoid complexity)
        lines = text.split('\n')
        processed_lines = []
        in_list = False
        
        for line in lines:
            stripped = line.strip()
            
            # Check if this is a bullet point
            if stripped.startswith('- '):
                if not in_list:
                    processed_lines.append('<ul>')
                    in_list = True
                # Simple list item without nested paragraphs
                processed_lines.append(f'<li>{stripped[2:].strip()}</li>')
            else:
                # If we were in a list and this isn't a list item, close the list
                if in_list:
                    processed_lines.append('</ul>')
                    in_list = False
                
                # Add regular content
                if stripped:
                    processed_lines.append(stripped)
                elif processed_lines:  # Only add empty lines if we have content
                    processed_lines.append('')
        
        # Close list if still open
        if in_list:
            processed_lines.append('</ul>')
        
        # Join lines and create paragraphs
        content = '\n'.join(processed_lines)
        
        # Split into paragraphs and wrap non-HTML content
        paragraphs = content.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                # If it's already HTML (starts with <), don't wrap
                if para.startswith('<'):
                    formatted_paragraphs.append(para)
                else:
                    # Convert single newlines to <br> within paragraph
                    para = para.replace('\n', '<br>')
                    formatted_paragraphs.append(f'<p>{para}</p>')
        
        return '\n'.join(formatted_paragraphs)

    def _clean_html_structure(self, html_content: str) -> str:
        """
        Clean up HTML structure to remove any wrapper divs that would conflict with frontend
        The frontend will add its own .answer-content wrapper, so we return clean content only
        """
        # Remove ANY outer div wrappers (markdown might add these)
        while re.match(r'^\s*<div[^>]*>.*</div>\s*$', html_content, flags=re.DOTALL):
            html_content = re.sub(r'^\s*<div[^>]*>\s*(.*?)\s*</div>\s*$', r'\1', html_content, flags=re.DOTALL)
        
        # Remove empty paragraphs
        html_content = re.sub(r'<p>\s*</p>', '', html_content)
        
        # Remove empty divs
        html_content = re.sub(r'<div[^>]*>\s*</div>', '', html_content)
        
        # Clean up excessive whitespace
        html_content = re.sub(r'\s+', ' ', html_content)
        html_content = re.sub(r'>\s+<', '><', html_content)
        
        # Ensure proper spacing after block elements for readability
        html_content = re.sub(r'</h([1-6])>', r'</h\1>\n', html_content)
        html_content = re.sub(r'</p>', r'</p>\n', html_content)
        html_content = re.sub(r'</ul>', r'</ul>\n', html_content)
        html_content = re.sub(r'</ol>', r'</ol>\n', html_content)
        
        return html_content.strip()
    
    def _extract_quotes_from_answer(self, answer: str) -> List[str]:
        """
        Extract quoted text from the LLM's answer.
        Looks for text in "quotes" or other citation patterns.
        """
        quotes = []
        
        # Pattern 1: Text in "regular quotes" (most common)
        # Match quotes with at least 10 characters (lowered threshold)
        regular_quotes = re.findall(r'"([^"]{10,}?)"', answer)
        quotes.extend([q.strip() for q in regular_quotes])
        
        # Pattern 2: Text in 'single quotes' (alternative quoting style)
        single_quotes = re.findall(r"'([^']{15,}?)'", answer)
        quotes.extend([q.strip() for q in single_quotes])
        
        # Pattern 3: Look for contextual phrases followed by quoted text
        contextual_phrases = [
            r'(?:as stated|according to|mentions that|explains that|states that|notes that)',
            r'(?:the expert says|the video explains|the speaker mentions)',
            r'(?:as mentioned|as explained|as described)'
        ]
        
        for phrase_pattern in contextual_phrases:
            contextual_quotes = re.findall(
                f'{phrase_pattern}[:\s]+"([^"]+)"', 
                answer, 
                re.IGNORECASE
            )
            quotes.extend([q.strip() for q in contextual_quotes if len(q.strip()) > 10])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_quotes = []
        for q in quotes:
            q_lower = q.lower()
            if q_lower not in seen:
                seen.add(q_lower)
                unique_quotes.append(q)
        
        # Debug logging
        if unique_quotes:
            print(f"✅ Extracted {len(unique_quotes)} quotes for highlighting:")
            for i, q in enumerate(unique_quotes[:5], 1):
                print(f"   {i}. \"{q[:60]}...\"" if len(q) > 60 else f"   {i}. \"{q}\"")
        else:
            print("⚠️ No quotes extracted from AI answer - highlighting will not work")
            print("   Tip: The AI needs to use \"direct quotes\" from the source material")
        
        return unique_quotes[:5]  # Limit to top 5 quotes to avoid over-highlighting
    
    def _highlight_text_in_content(self, content: str, quotes: List[str]) -> str:
        """
        Highlight quoted passages in the transcript content.
        Uses fuzzy matching to handle minor variations.
        """
        if not quotes or not content:
            return content
        
        highlighted_content = content
        highlights_found = 0
        
        for quote in quotes:
            # Clean quote for matching (remove extra spaces, normalize)
            quote_clean = ' '.join(quote.split()).lower()
            
            # Try direct substring match first (case-insensitive)
            content_lower = content.lower()
            if quote_clean in content_lower:
                # Find the exact position in the original content
                start_idx = content_lower.find(quote_clean)
                end_idx = start_idx + len(quote_clean)
                
                # Get the original text with proper capitalization
                original_text = content[start_idx:end_idx]
                
                # Replace with highlighted version (only if not already highlighted)
                if '<mark' not in highlighted_content[max(0, start_idx-10):min(len(highlighted_content), end_idx+10)]:
                    highlighted_content = highlighted_content.replace(
                        original_text,
                        f'<mark class="quote-highlight">{original_text}</mark>',
                        1  # Only replace first occurrence
                    )
                    highlights_found += 1
                    print(f"   ✓ Highlighted: \"{original_text[:50]}...\"" if len(original_text) > 50 else f"   ✓ Highlighted: \"{original_text}\"")
                continue
            
            # Fallback: Try fuzzy matching with sliding window
            content_words = content.split()
            quote_words = quote_clean.split()
            
            # Simple sliding window to find matches
            for i in range(len(content_words) - len(quote_words) + 1):
                window = ' '.join(content_words[i:i+len(quote_words)]).lower()
                window_normalized = ' '.join(window.split())
                
                # Check for close match (handles minor variations)
                if quote_clean in window_normalized or window_normalized in quote_clean:
                    # Get the original text (with proper capitalization)
                    original_text = ' '.join(content_words[i:i+len(quote_words)])
                    
                    # Replace with highlighted version (only if not already highlighted)
                    if '<mark' not in highlighted_content:
                        highlighted_content = highlighted_content.replace(
                            original_text,
                            f'<mark class="quote-highlight">{original_text}</mark>',
                            1  # Only replace first occurrence
                        )
                        highlights_found += 1
                        print(f"   ✓ Highlighted (fuzzy): \"{original_text[:50]}...\"" if len(original_text) > 50 else f"   ✓ Highlighted (fuzzy): \"{original_text}\"")
                    break
        
        if highlights_found == 0:
            print("   ⚠️ No highlights applied - quotes not found in source content")
        else:
            print(f"   ✅ Applied {highlights_found} highlight(s) to source content")
        
        return highlighted_content


class DiscordFormatter:
    """Discord formatter - converts HTML to Discord-friendly markdown"""
    
    def format(self, answer: str, sources: List[Dict]) -> Dict[str, Any]:
        """Format response for Discord (plain text with markdown)"""
        # Convert HTML answer to Discord markdown
        formatted_answer = self._format_answer_for_discord(answer)
        
        # Replace document references with video links using raw source data
        formatted_answer = self._improve_document_references(formatted_answer, sources)
        
        return {
            "formatted_content": {
                "answer": formatted_answer,
                "sources": "",  # Discord doesn't use HTML sources
                "raw_sources": sources
            },
            "format": "discord"
        }
    
    def _format_answer_for_discord(self, mixed_content: str) -> str:
        """Convert mixed HTML/text content from RAG system to Discord-compatible format
        
        Uses BeautifulSoup to reliably handle mixed HTML and text content.
        """
        try:
            from bs4 import BeautifulSoup, NavigableString
            soup_available = True
        except ImportError:
            soup_available = False
        
        if not mixed_content or not mixed_content.strip():
            return "No answer available."
        
        # PRE-PROCESS: Convert markdown headers to HTML before BeautifulSoup processing
        mixed_content = self._preprocess_markdown_headers(mixed_content)
        
        if soup_available:
            try:
                # Step 1: Parse mixed HTML/text content with BeautifulSoup
                soup = BeautifulSoup(mixed_content, 'html.parser')
                
                # Step 2: Convert HTML elements to Discord markdown
                # Handle headers (h1-h6) -> **bold**
                for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                    tag_text = tag.get_text().strip()
                    if tag_text:
                        # Replace the tag with bold text
                        tag.replace_with(f"\n\n**{tag_text}**\n")
                
                # Handle strong/b tags -> **bold**
                for tag in soup.find_all(['strong', 'b']):
                    tag_text = tag.get_text().strip()
                    if tag_text:
                        tag.replace_with(f"**{tag_text}**")
                
                # Handle em/i tags -> *italic*
                for tag in soup.find_all(['em', 'i']):
                    tag_text = tag.get_text().strip()
                    if tag_text:
                        tag.replace_with(f"*{tag_text}*")
                
                # Handle unordered lists
                for ul in soup.find_all('ul'):
                    list_items = []
                    for li in ul.find_all('li'):
                        li_text = li.get_text().strip()
                        if li_text:
                            list_items.append(f"• {li_text}")
                    
                    if list_items:
                        ul.replace_with('\n' + '\n'.join(list_items) + '\n')
                    else:
                        ul.decompose()
                
                # Handle ordered lists
                for ol in soup.find_all('ol'):
                    list_items = []
                    for i, li in enumerate(ol.find_all('li'), 1):
                        li_text = li.get_text().strip()
                        if li_text:
                            list_items.append(f"{i}. {li_text}")
                    
                    if list_items:
                        ol.replace_with('\n' + '\n'.join(list_items) + '\n')
                    else:
                        ol.decompose()
                
                # Handle remaining list items that weren't in ul/ol
                for li in soup.find_all('li'):
                    li_text = li.get_text().strip()
                    if li_text:
                        li.replace_with(f"• {li_text}")
                
                # Remove any remaining HTML tags
                for tag in soup.find_all():
                    tag.unwrap()
                
                # Step 3: Get the clean text
                content = soup.get_text()
                
                # Step 4: Handle LaTeX formulas - convert to readable text
                def convert_latex_to_text(match):
                    latex = match.group(1).strip()
                    # Simple LaTeX to text conversion for Discord
                    latex = latex.replace('\\text{Expected Return}', 'Expected Return')
                    latex = latex.replace('\\text{Probability of Outcome}', 'Probability of Outcome')
                    latex = latex.replace('\\text{Return of Outcome}', 'Return of Outcome')
                    latex = latex.replace('\\sum', 'Σ')
                    latex = latex.replace('\\times', '×')
                    latex = latex.replace('\\cdot', '·')
                    latex = latex.replace('\\text{', '').replace('}', '')
                    latex = latex.replace('\\\\', ' ')
                    latex = latex.replace('\\', '')
                    # Clean up extra spaces and format as code
                    latex = re.sub(r'\s+', ' ', latex).strip()
                    return f"\n`{latex}`\n"
                
                # Convert LaTeX formulas
                content = re.sub(r'\\\[([^\]]+)\\\]', convert_latex_to_text, content)
                content = re.sub(r'\$\$([^$]+)\$\$', convert_latex_to_text, content)
                
                # Step 5: Apply Discord-specific formatting
                # Clean up [Document N] references for later processing
                content = re.sub(r'\[Document\s+(\d+)\]', r'[Document \1]', content, flags=re.IGNORECASE)
                
                # Remove "Source References" section (we handle sources separately)
                content = re.sub(r'\*\*Source References\*\*.*$', '', content, flags=re.DOTALL | re.IGNORECASE)
                content = re.sub(r'^.*Source References.*$', '', content, flags=re.MULTILINE | re.IGNORECASE)
                
                # Fix bold text spacing issues (Discord is sensitive to spaces around **)
                content = re.sub(r'\*\*\s+(.+?)\s+\*\*', r'**\1**', content)
                content = re.sub(r'\*\*(.+?)\*\*', lambda m: f'**{m.group(1).strip()}**', content)
                
                # Enhance key terms with code formatting (Discord renders `code` well)
                key_terms = [
                    r'\b(Delta|Gamma|Theta|Vega|Rho)\b',  # Options Greeks
                    r'\b(ITM|OTM|ATM|IV|Greeks)\b',       # Options terminology  
                    r'\b(Call|Put|Strike|Expiration|Premium)\b'  # Common terms
                ]
                
                for term_pattern in key_terms:
                    # Only apply if not already formatted with `, *, [, or ]
                    content = re.sub(
                        rf'(?<![`*\[\]]){term_pattern}(?![`*\]\)])', 
                        lambda m: f'`{m.group(1)}`', 
                        content
                    )
                
                # Emphasize financial values 
                content = re.sub(r'(?<!\*)\$(\d+(?:\.\d{2})?)\b', r'**$\1**', content)
                content = re.sub(r'\b(\d+(?:\.\d+)?)%\b(?!\*)', r'**\1%**', content)
                
                # Clean up excessive whitespace
                content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)  # Max 2 consecutive newlines
                content = re.sub(r'^\s+|\s+$', '', content)  # Trim edges
                
                # Add block quotes for special sections
                content = re.sub(r'^(\*\*Quick Answer\*\*.*?)$', r'> \1', content, flags=re.MULTILINE)
                
                return content
                
            except Exception as e:
                # Fallback: if BeautifulSoup processing fails, use basic processing
                print(f"BeautifulSoup processing failed: {e}, using fallback")
        
        # Fallback processing (either BeautifulSoup not available or processing failed)
        # Basic HTML to text conversion using regex
        content = mixed_content.strip()
        
        # First, process any remaining markdown headers that weren't caught earlier
        content = self._preprocess_markdown_headers(content)
        
        # Remove HTML tags (basic cleanup for fallback)
        content = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'\n**\1**\n', content)  # Headers to bold
        content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content)  # Strong to bold
        content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content)  # Em to italic
        content = re.sub(r'<li[^>]*>(.*?)</li>', r'• \1\n', content)  # List items
        content = re.sub(r'<[^>]+>', '', content)  # Remove remaining HTML tags
        
        # Basic LaTeX cleanup
        content = re.sub(r'\\\[([^\]]+)\\\]', r'`\1`', content)
        content = re.sub(r'\\text\{([^}]+)\}', r'\1', content)
        
        # Clean up excessive whitespace
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = re.sub(r'^\s+|\s+$', '', content)
        
        return content

    def _preprocess_markdown_headers(self, text: str) -> str:
        """Convert markdown headers to HTML before processing
        
        This ensures Discord gets proper **bold** formatting instead of raw #### syntax
        """
        import re
        
        # Convert markdown headers to HTML (same pattern as HtmlFormatter)
        # ## Header -> <h2>Header</h2>
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        # ### Header -> <h3>Header</h3>  
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        # #### Header -> <h4>Header</h4>
        text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
        # ##### Header -> <h5>Header</h5>
        text = re.sub(r'^##### (.+)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
        # ###### Header -> <h6>Header</h6>
        text = re.sub(r'^###### (.+)$', r'<h6>\1</h6>', text, flags=re.MULTILINE)
        
        return text

    def _improve_document_references(self, answer: str, sources: list) -> str:
        """Replace [Document N] references with Discord-friendly video links"""
        if not sources:
            # Remove any remaining document references if no sources available
            answer = re.sub(r'\[Document \d+\]', '', answer, flags=re.IGNORECASE)
            return answer
        
        # Create a mapping of document numbers to video info
        doc_mapping = {}
        for i, source in enumerate(sources, 1):
            timestamp_seconds = source.get('start_timestamp_seconds', 0)
            
            # Format timestamp for display
            timestamp_str = ""
            if timestamp_seconds and timestamp_seconds > 0:
                minutes = int(timestamp_seconds // 60)
                seconds = int(timestamp_seconds % 60)
                timestamp_str = f" @ {minutes}:{seconds:02d}"
            
            # Get the best available title
            title = source.get('title', 'Untitled Video')
            
            # Clean up video ID titles
            if len(title) == 11 and title.isalnum():  # Likely a video ID
                title = source.get('filename', source.get('file_name', title))
                title = title.replace('.mp3', '').replace('.wav', '').replace('.mp4', '')
            
            # Get URL with timestamp
            url = source.get('video_url_with_timestamp') or source.get('url', '#')
            if url == '#' or not url:
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
                
                # Clean up title for Discord display
                title = title.replace('|', '-').replace('[', '(').replace(']', ')')
                if len(title) > 30:  # Shorter for Discord
                    title = title[:27] + "..."
                
                # Create Discord link with timestamp (suppress preview with < >)
                return f"**[Video {doc_num}{timestamp_str}: {title}](<{url}>)**"
            else:
                return f"**[Video {doc_num}]**"
        
        # Replace [Document N] with video references
        answer = re.sub(r'\[Document (\d+)\]', replace_doc_ref, answer, flags=re.IGNORECASE)
        
        return answer 