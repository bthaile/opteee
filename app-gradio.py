"""
OPTEEE - Options Trading Education Expert
Modern Chat Interface with Local Storage
"""

import gradio as gr
import json
import os
import markdown
import base64
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from vector_search import search_vector_store, build_vector_store
from rag_pipeline import (
    CustomFAISSRetriever,
    create_rag_chain,
    run_rag_query,
    get_available_providers,
    DEFAULT_TOP_K
)

# Initialize vector store and chains
print(" Initializing OPTEEE Chat Interface...")

# Check if we need to build the vector store
index_path = os.path.join("/app/vector_store", "faiss.index")
vector_store_exists = os.path.exists(os.path.dirname(index_path))
if not vector_store_exists:
    print(f"⚠️ WARNING: Vector store not found at {index_path}")

# Initialize the retriever and chains
retriever = CustomFAISSRetriever(top_k=DEFAULT_TOP_K)
provider_chains = {}

def initialize_chains():
    """Initialize chains for all available providers"""
    available_providers = get_available_providers()
    for provider in available_providers:
        try:
            _, chain = create_rag_chain(retriever, provider=provider)
            provider_chains[provider] = chain
            print(f" Initialized chain for {provider}")
        except Exception as e:
            print(f"❌ Failed to initialize {provider} chain: {e}")

# Initialize chains at startup
initialize_chains()

# Load CSS and JavaScript from separate files
def load_chat_css():
    """Load the CSS for the chat interface from external file"""
    try:
        css_path = os.path.join(os.path.dirname(__file__), "static", "chat.css")
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"⚠️ WARNING: Could not load CSS file: {e}")
        # Fallback to basic CSS if file loading fails
        return """
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        """

# JavaScript functionality removed to avoid compatibility issues with Gradio
# The chat interface works perfectly without custom JavaScript

def format_chat_response(answer: str, sources: List[Dict]) -> Dict[str, Any]:
    """
    Format the chat response with enhanced video reference cards
    """
    # Format the answer text - convert markdown to HTML
    formatted_answer = markdown.markdown(answer)
    
    # Create enhanced video reference cards
    if not sources:
        return {
            "answer": formatted_answer,
            "sources": "",
            "raw_sources": []
        }
    
    sources_content = '<div class="video-references">'
    
    for i, source in enumerate(sources):
        title = source.get('title', 'Untitled Video')
        url = source.get('url', '#')
        video_url_with_timestamp = source.get('video_url_with_timestamp', url) # Use base url as fallback
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
                from datetime import datetime
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

def chat_response(message: str, history: List[Dict], provider: str = "openai", num_results: int = 5) -> List[Dict]:
    """
    Process chat message and return updated conversation history
    """
    try:
        # Add user message to history
        history.append({"role": "user", "content": message})
        
        # Update retriever settings
        retriever.top_k = num_results
        
        # Get the appropriate chain
        if provider not in provider_chains:
            error_msg = f"❌ Provider '{provider}' not available"
            history.append({"role": "assistant", "content": error_msg})
            return history
        
        chain = provider_chains[provider]
        
        # Run the RAG query
        result = run_rag_query(retriever, chain, message)
        
        # Format the response
        formatted_response = format_chat_response(result.get('answer', ''), result.get('sources', []))
        
        # Add assistant response
        history.append({
            "role": "assistant", 
            "content": formatted_response["answer"]
        })
        
        # Add sources as a separate message with metadata
        if formatted_response["sources"]:
            history.append({
                "role": "assistant",
                "content": formatted_response["sources"],
                "metadata": {"title": "Video References"}
            })
        
        return history
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        history.append({"role": "assistant", "content": error_msg})
        return history

# Create the Gradio chat interface
def create_chat_interface():
    """Create the modern sidebar + main panel interface using Gradio"""
    
    with gr.Blocks(
        css=load_chat_css(),
        title="OPTEEE - Options Trading Expert",
        theme=gr.themes.Soft()
    ) as demo:
        
        # Global state for chat history
        chat_history = gr.State(value=[])
        
        # Main container with two columns
        with gr.Row(elem_id="main-container"):
            # Sidebar
            with gr.Column(scale=1, elem_id="sidebar"):
                with gr.Row():
                    gr.HTML('<h3 class="sidebar-title">Chat History</h3>')
                    new_chat_btn = gr.Button(
                        "+ New Chat",
                        elem_classes="new-chat-btn",
                        size="sm"
                    )
                
                
                # Recent Prompts section
                gr.HTML('<h4 class="prompts-title">Recent Prompts</h4>')
                prompts_list = gr.HTML(
                    value='<div class="prompts-empty">No recent prompts</div>',
                    elem_id="prompts-list",
                    elem_classes="prompts-container"
                )
                
                # Configuration variables (no UI - hardcoded defaults)
                # These maintain the same variable names for the event handlers
                provider_dropdown = gr.State(value="openai")  # Default to OpenAI
                num_results_input = gr.State(value=10)        # Default to 10 results
            
            # Main Panel
            with gr.Column(scale=3, elem_id="main-panel"):
                # Header
                gr.HTML("""
                    <div class="main-header">
                        <p class="main-subtitle">Options Trading Education Expert</p>
                    </div>
                """)
                
                # Example Questions
                gr.HTML("""
                    <div class="example-questions">
                        <div class="example-grid">
                            <button class="example-button" onclick="selectExample(this)">Explain covered calls and when to use them</button>
                            <button class="example-button" onclick="selectExample(this)">How does implied volatility affect option pricing?</button>
                            <button class="example-button" onclick="selectExample(this)">What are the Greeks in options trading?</button>
                            <button class="example-button" onclick="selectExample(this)">How do you manage theta decay in options?</button>
                        </div>
                    </div>
                """)
                
                # User Input Section
                with gr.Column(elem_id="user-input-section", elem_classes="user-input-section"):
                    with gr.Column(elem_classes="input-container"):
                        msg_input = gr.Textbox(
                            placeholder="Ask me anything about options trading...",
                            show_label=False,
                            lines=2,
                            elem_id="user-input",
                            elem_classes="input-wrapper"
                        )
                        submit_btn = gr.Button(
                            "Send",
                            variant="primary",
                            elem_classes="submit-btn",
                            elem_id="submit-btn"
                        )
                
                # Answer Display Section
                with gr.Column(elem_id="answer-section", elem_classes="answer-section"):
                    answer_display = gr.HTML(
                        value='<div class="answer-placeholder">Ask a question to get started</div>',
                        elem_id="answer-display"
                    )
                
                # Sources Display Section
                with gr.Column(elem_id="sources-section"):
                    sources_display = gr.HTML(
                        value="",
                        elem_id="sources-display"
                    )
        
        # JavaScript with proper localStorage management
        demo.load(lambda: None, js="""
        () => {
            console.log('Initializing OPTEEE Chat Interface with localStorage');
            
            // Prompt management with localStorage
            class PromptManager {
                constructor() {
                    this.storageKey = 'opteee_prompt_history';
                    this.maxPrompts = 10;
                    this.container = null;
                    this.init();
                }
                
                init() {
                    // Find the prompts container
                    setTimeout(() => {
                        this.container = document.querySelector('#prompts-list');
                        if (this.container) {
                            this.loadAndDisplay();
                            this.setupSubmitCapture();
                        }
                    }, 1000);
                }
                
                loadAndDisplay() {
                    const prompts = this.getPrompts();
                    this.displayPrompts(prompts);
                }
                
                getPrompts() {
                    try {
                        const stored = localStorage.getItem(this.storageKey);
                        return stored ? JSON.parse(stored) : [];
                    } catch (e) {
                        console.error('Error loading prompts:', e);
                        return [];
                    }
                }
                
                savePrompts(prompts) {
                    try {
                        localStorage.setItem(this.storageKey, JSON.stringify(prompts));
                    } catch (e) {
                        console.error('Error saving prompts:', e);
                    }
                }
                
                addPrompt(prompt) {
                    let prompts = this.getPrompts();
                    
                    // Remove duplicate
                    prompts = prompts.filter(p => p !== prompt);
                    
                    // Add at beginning
                    prompts.unshift(prompt);
                    
                    // Keep only last maxPrompts
                    if (prompts.length > this.maxPrompts) {
                        prompts = prompts.slice(0, this.maxPrompts);
                    }
                    
                    this.savePrompts(prompts);
                    this.displayPrompts(prompts);
                }
                
                removePrompt(index) {
                    let prompts = this.getPrompts();
                    if (index >= 0 && index < prompts.length) {
                        prompts.splice(index, 1);
                        this.savePrompts(prompts);
                        this.displayPrompts(prompts);
                    }
                }
                
                displayPrompts(prompts) {
                    if (!this.container) return;
                    
                    if (prompts.length === 0) {
                        this.container.innerHTML = '<div class="prompts-empty">No recent prompts</div>';
                        return;
                    }
                    
                    let html = '';
                    prompts.forEach((prompt, index) => {
                        const truncated = prompt.length > 60 ? prompt.substring(0, 57) + '...' : prompt;
                        const escaped = this.escapeHtml(prompt);
                        const escapedTruncated = this.escapeHtml(truncated);
                        
                        html += `
                            <div class="prompt-item" onclick="promptManager.selectPrompt(${index})">
                                <div class="prompt-text" title="${escaped}">${escapedTruncated}</div>
                                <button class="prompt-delete-btn" onclick="promptManager.deletePrompt(${index}); event.stopPropagation();" title="Remove prompt">×</button>
                            </div>
                        `;
                    });
                    
                    this.container.innerHTML = html;
                }
                
                escapeHtml(text) {
                    const map = {
                        '&': '&amp;',
                        '<': '&lt;',
                        '>': '&gt;',
                        '"': '&quot;',
                        "'": '&#039;'
                    };
                    return text.replace(/[&<>"']/g, m => map[m]);
                }
                
                selectPrompt(index) {
                    const prompts = this.getPrompts();
                    if (index >= 0 && index < prompts.length) {
                        const prompt = prompts[index];
                        const input = document.querySelector('#user-input textarea');
                        if (input) {
                            input.value = prompt;
                            input.focus();
                            input.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    }
                }
                
                deletePrompt(index) {
                    this.removePrompt(index);
                }
                
                setupSubmitCapture() {
                    const submitBtn = document.querySelector('#submit-btn');
                    if (submitBtn) {
                        submitBtn.addEventListener('click', () => {
                            const input = document.querySelector('#user-input textarea');
                            if (input && input.value.trim()) {
                                this.addPrompt(input.value.trim());
                            }
                        });
                    }
                }
            }
            
            // Initialize prompt manager
            window.promptManager = new PromptManager();
            
            // Example question selection
            window.selectExample = function(button) {
                const input = document.querySelector('#user-input textarea');
                if (input) {
                    input.value = button.textContent;
                    input.focus();
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
            };
            
            // Copy to clipboard functionality with visual feedback
            window.copyToClipboard = function(text, button) {
                navigator.clipboard.writeText(text).then(function() {
                    // Success - show visual feedback
                    const originalIcon = button.innerHTML;
                    const originalClass = button.className;
                    
                    // Change to checkmark and add copied class
                    button.innerHTML = '✓';
                    button.classList.add('copied');
                    
                    // Reset after 2 seconds
                    setTimeout(function() {
                        button.innerHTML = originalIcon;
                        button.className = originalClass;
                    }, 2000);
                    
                }).catch(function(err) {
                    console.error('Could not copy text: ', err);
                });
            };

        }
        """)
        
        # Event Handlers
        def process_question(question, provider, num_results):
            """Process a user question and return formatted response"""
            if not question.strip():
                return {"answer": "", "sources": ""}
            
            try:
                # Update retriever settings
                retriever.top_k = num_results
                
                # Get the appropriate chain
                if provider not in provider_chains:
                    error_msg = f"❌ Provider '{provider}' not available"
                    return {"answer": error_msg, "sources": ""}
                
                chain = provider_chains[provider]
                
                # Run the RAG query
                result = run_rag_query(retriever, chain, question)
                
                # Format the response
                formatted_response = format_chat_response(result.get('answer', ''), result.get('sources', []))
                
                return {
                    "answer": formatted_response["answer"],
                    "sources": formatted_response["sources"]
                }
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                return {"answer": error_msg, "sources": ""}
        

        
        def handle_submit(message, history, provider, num_results):
            """Handle user message submission - simplified without prompt management"""
            if not message.strip():
                return "", history, '<div class="answer-placeholder">Ask a question to get started</div>', ""
            
            try:
                # Get response from RAG pipeline
                response_data = process_question(message, provider, num_results)
                
                # Update chat history (for server-side state)
                new_history = history + [{
                    "question": message,
                    "answer": response_data["answer"],
                    "sources": response_data["sources"],
                    "timestamp": datetime.now().isoformat()
                }]
                
                # Format answer display
                answer_html = f'<div class="answer-content">{response_data["answer"]}</div>'
                
                return "", new_history, answer_html, response_data["sources"]
                
            except Exception as e:
                error_msg = f"Error processing question: {str(e)}"
                error_html = f'<div class="answer-content" style="color: var(--error-color);">{error_msg}</div>'
                return "", history, error_html, ""
        
        # Wire up the interface
        submit_btn.click(
            handle_submit,
            inputs=[msg_input, chat_history, provider_dropdown, num_results_input],
            outputs=[msg_input, chat_history, answer_display, sources_display]
        )
        
        # New Chat functionality - simplified
        def start_new_chat():
            """Start a new chat session"""
            return [], '<div class="answer-placeholder">Ask a question to get started</div>', ""
        
        new_chat_btn.click(
            start_new_chat,
            inputs=[],
            outputs=[chat_history, answer_display, sources_display]
        )
    
    return demo

# Launch the chat interface
if __name__ == "__main__":
    print(" Starting OPTEEE Chat Interface...")
    demo = create_chat_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 
