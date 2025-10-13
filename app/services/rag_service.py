"""
RAG Service - Extracted from original app.py
Contains all the core RAG processing logic
"""

import os
import markdown
from datetime import datetime
from typing import List, Dict, Any, Optional
from vector_search import search_vector_store, build_vector_store
from rag_pipeline import (
    CustomFAISSRetriever,
    create_rag_chain,
    run_rag_query,
    get_available_providers,
    DEFAULT_TOP_K
)
from app.services.formatters import ResponseFormatter
from app.models.chat_models import ConversationMessage
from config import VECTOR_DIR

class RAGService:
    """Service class to handle all RAG-related operations"""
    
    def __init__(self):
        self.retriever = None
        self.provider_chains = {}
        self.formatter = ResponseFormatter()
        self.initialized = False
    
    async def initialize(self):
        """Initialize the RAG service with vector store and chains"""
        if self.initialized:
            return
        
        print(" Initializing RAG Service...")
        
        # Check if we need to build the vector store
        index_path = os.path.join(VECTOR_DIR, "faiss.index")
        vector_store_exists = os.path.exists(os.path.dirname(index_path))
        if not vector_store_exists:
            print(f"⚠️ WARNING: Vector store not found at {index_path}")
            print(f"📍 Using vector directory: {VECTOR_DIR}")
        
        # Initialize the retriever
        self.retriever = CustomFAISSRetriever(top_k=DEFAULT_TOP_K)
        
        # Initialize chains for all available providers
        await self._initialize_chains()
        
        self.initialized = True
        print(" RAG service initialization complete")
    
    async def _initialize_chains(self):
        """Initialize chains for all available providers"""
        available_providers = get_available_providers()
        for provider in available_providers:
            try:
                _, chain = create_rag_chain(self.retriever, provider=provider)
                self.provider_chains[provider] = chain
                print(f" Initialized chain for {provider}")
            except Exception as e:
                print(f"❌ Failed to initialize {provider} chain: {e}")
    
    async def process_query(self, query: str, provider: str = "claude", num_results: int = 10, format: str = "html", conversation_history: Optional[List[ConversationMessage]] = None) -> Dict[str, Any]:
        """
        Process a user query and return formatted response
        Now supports conversation history for context
        """
        if not self.initialized:
            raise RuntimeError("RAG service not initialized")
        
        if not query.strip():
            # Return empty content - let frontend handle placeholder messaging
            return {
                "answer": "",
                "sources": "",
                "raw_sources": []
            }
        
        try:
            # Update retriever settings
            self.retriever.top_k = num_results
            
            # Get the appropriate chain
            if provider not in self.provider_chains:
                error_msg = f"❌ Provider '{provider}' not available"
                return {
                    "answer": error_msg,
                    "sources": "",
                    "raw_sources": []
                }
            
            chain = self.provider_chains[provider]
            
            # Run the RAG query with conversation context if provided
            if conversation_history and len(conversation_history) > 0:
                result = self._run_rag_query_with_context(self.retriever, chain, query, conversation_history)
            else:
                # Use existing run_rag_query for backward compatibility
                result = run_rag_query(self.retriever, chain, query)
            
            # Format the response using the new formatter
            formatted_result = self.formatter.format_response(
                result.get('answer', ''),
                result.get('sources', []),
                format_type=format
            )
            
            formatted_response = formatted_result["formatted_content"]
            
            return {
                "answer": formatted_response["answer"],
                "sources": formatted_response["sources"],
                "raw_sources": formatted_response["raw_sources"]
            }
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            return {
                "answer": error_msg,  # Return raw error message - frontend will wrap it
                "sources": "",
                "raw_sources": []
            }
    
    def _run_rag_query_with_context(self, retriever, chain, query: str, conversation_history: List[ConversationMessage]) -> Dict[str, Any]:
        """
        Run a RAG query with conversation history context
        This creates a modified prompt that includes conversation history
        """
        from langchain.prompts import ChatPromptTemplate
        from langchain.schema.output_parser import StrOutputParser
        from langchain.schema.runnable import RunnablePassthrough
        from rag_pipeline import format_documents
        from config import SYSTEM_PROMPT
        
        # Get relevant documents (same as standard flow)
        docs = retriever.get_relevant_documents(query)
        
        if not docs:
            return {
                "answer": "",  # Return empty - let frontend handle no results messaging
                "sources": []
            }
        
        # Format conversation history for the prompt
        conversation_context = self._format_conversation_history(conversation_history)
        
        # Create a modified prompt template that includes conversation history
        template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", """Conversation History:
{conversation_context}

Context for answering the current question:
{context}

Current User Question: {question}

Please answer the current question considering the conversation history above. Refer back to previous parts of the conversation when relevant, but focus primarily on answering the current question using the provided context.""")
        ])
        
        # Simplified approach: modify the query to include conversation context
        # and use the existing chain which already handles documents properly
        enhanced_query = f"""Previous conversation:
{conversation_context}

Current question: {query}"""
        
        # Use the existing chain but with enhanced query that includes context
        answer = chain.invoke(enhanced_query)
        
        # Extract sources (maintaining order) - same as run_rag_query
        sources = []
        for doc in docs:
            meta = doc.metadata
            
            # Get video ID and ensure it's valid
            video_id = meta.get("video_id", "")
            
            # Fix any URL issues by reconstructing with the proper video_id
            timestamp_seconds = meta.get("start_timestamp_seconds", 0)
            if isinstance(timestamp_seconds, float) or isinstance(timestamp_seconds, int):
                timestamp_seconds = int(timestamp_seconds)
            else:
                timestamp_seconds = 0
                
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_url_with_timestamp = f"{video_url}&t={timestamp_seconds}" if video_id and timestamp_seconds > 0 else video_url
            
            # Convert duration to seconds - use existing logic from run_rag_query
            from rag_pipeline import iso_duration_to_seconds
            duration = meta.get("duration", "")
            duration_seconds = iso_duration_to_seconds(duration)

            source = {
                "title": meta.get("title", "Unknown"),
                "video_id": video_id,
                "url": video_url,
                "video_url_with_timestamp": video_url_with_timestamp,
                "start_timestamp_seconds": timestamp_seconds,
                "timestamp": meta.get("start_timestamp", ""),
                "channel": meta.get("channel_name", meta.get("channel", "Unknown")),
                "upload_date": meta.get("upload_date") or meta.get("published_at") or "Unknown",
                "score": meta.get("score", 0.0),
                "content": doc.page_content,  # Include the actual transcript content
                "duration_seconds": duration_seconds,  # Pass raw seconds
            }
            sources.append(source)
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    def _format_conversation_history(self, conversation_history: List[ConversationMessage]) -> str:
        """
        Format conversation history for inclusion in the prompt
        """
        if not conversation_history:
            return "No previous conversation."
        
        formatted_messages = []
        for msg in conversation_history:
            role = msg.role
            content = msg.content
            timestamp = msg.timestamp
            
            # Truncate very long messages to avoid prompt bloat
            if len(content) > 500:
                content = content[:497] + "..."
            
            if role == "user":
                formatted_messages.append(f"User: {content}")
            elif role == "assistant":
                formatted_messages.append(f"Assistant: {content}")
        
        # Limit to last 10 messages to keep prompt manageable
        if len(formatted_messages) > 10:
            formatted_messages = formatted_messages[-10:]
            formatted_messages.insert(0, "[Earlier conversation truncated...]")
        
        return "\n".join(formatted_messages)
    
    def _format_chat_response(self, answer: str, sources: List[Dict]) -> Dict[str, Any]:
        """
        Format the chat response with enhanced video reference cards
        Extracted from original format_chat_response function
        """
        # Process markdown but keep structure simple for frontend compatibility
        formatted_answer = self._process_markdown_simple(answer)
        
        # Clean the HTML to remove any wrapper divs that would conflict with frontend
        formatted_answer = self._clean_html_structure(formatted_answer)
        
        # Create enhanced video reference cards
        if not sources:
            return {
                "answer": formatted_answer,
                "sources": "",
                "raw_sources": []
            }
        
        # Don't add outer wrapper - frontend will handle main container
        sources_content = '<div class="video-references">'
        
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
            
            # Get transcript content
            content = source.get('content', source.get('text', ''))
            truncated_content = content[:200] + "..." if len(content) > 200 else content

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
            "answer": formatted_answer,
            "sources": sources_content,
            "raw_sources": sources
        }
    
    def _process_markdown_simple(self, text: str) -> str:
        """
        Process markdown text into simple HTML without nested structures
        This avoids the nested div issues while still formatting content properly
        """
        import re
        
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
        import re
        
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