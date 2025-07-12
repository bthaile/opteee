"""
OPTEEE - Options Trading Education Expert
Modern Chat Interface with Local Storage
"""

import gradio as gr
import json
import os
import markdown
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
print("🚀 Initializing OPTEEE Chat Interface...")

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
            print(f"✅ Initialized chain for {provider}")
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
    
    for source in sources:
        # Extract video information
        video_id = source.get('video_id', 'unknown')
        title = source.get('title', 'Unknown Video')
        relevance_score = source.get('relevance_score', 0.0)
        
        # Format timestamp
        start_time = source.get('start_timestamp_seconds', 0)
        timestamp_formatted = f"{int(start_time // 60)}:{int(start_time % 60):02d}"
        
        # Create video URL with timestamp
        url = source.get('video_url_with_timestamp', f'https://youtube.com/watch?v={video_id}&t={int(start_time)}')
        
        # Get additional metadata with better defaults
        upload_date = source.get('upload_date', source.get('uploaded', 'Unknown'))
        duration_seconds = source.get('duration_seconds', source.get('duration', 0))
        channel = source.get('channel', source.get('uploader', 'Outlier Trading'))
        
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
            f'<div class="metadata-item" title="Jump to timestamp in video"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0f766e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polygon points="10 8 16 12 10 16 10 8"></polygon></svg><span>{timestamp_formatted}</span></div>',
            f'<div class="metadata-item" title="Total video duration"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0f766e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg><span>{duration_formatted}</span></div>',
            f'<div class="metadata-item" title="Video upload date"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0f766e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg><span>{upload_date_formatted}</span></div>'
        ]

        metadata_html = ''.join(meta_items)

        # Create compact and professional video card HTML
        sources_content += f'''
            <div class="video-card">
                <div class="video-card-header">
                    <a href="{url}" target="_blank" class="video-title-link">
                        <h4 class="video-title">{title}</h4>
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
                        <a href="{url}" target="_blank" class="video-action-btn" title="Watch on YouTube">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0f766e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2A29 29 0 0 0 23 11.75a29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg>
                        </a>
                        <button class="video-action-btn" onclick="copyToClipboard('{url}', this)" title="Copy link">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0f766e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
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
        current_question = gr.State(value="")
        current_answer = gr.State(value="")
        current_sources = gr.State(value="")
        
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
                        # Processing bar
                        processing_bar = gr.HTML(
                            value='<div class="processing-bar" id="processing-bar"></div>',
                            elem_id="processing-bar-container",
                            visible=True
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
                
                # Hidden component for JavaScript triggers
                js_trigger = gr.HTML(
                    value="",
                    elem_id="js-trigger",
                    visible=False
                )
        
        # JavaScript for localStorage chat history and UI interactions
        demo.load(lambda: None, js="""
        () => {
            // Chat History Management
            class ChatHistoryManager {
                constructor() {
                    this.storageKey = 'opteee_chat_history';
                    this.currentSessionId = null;
                    this.init();
                }
                
                init() {
                    console.log('Initializing Chat History Manager');
                    this.setupEventListeners();
                    this.loadAndDisplayHistory();
                }
                
                setupEventListeners() {
                    // Monitor for save triggers
                    const observer = new MutationObserver(() => {
                        this.checkForSaveTrigger();
                    });
                    
                    // Find and observe the trigger element
                    const findTrigger = () => {
                        const trigger = document.querySelector('#js-trigger');
                        if (trigger) {
                            observer.observe(trigger, { childList: true, subtree: true });
                            console.log('Trigger observer set up');
                        } else {
                            setTimeout(findTrigger, 500);
                        }
                    };
                    
                    findTrigger();
                    
                    // Also check periodically
                    setInterval(() => this.checkForSaveTrigger(), 1000);
                }
                
                checkForSaveTrigger() {
                    const trigger = document.querySelector('#js-trigger');
                    if (trigger && trigger.innerHTML) {
                        const content = trigger.innerHTML;
                        
                        // Handle processing bar triggers
                        if (content.includes('SHOW_PROCESSING')) {
                            if (window.processingBar) {
                                window.processingBar.show();
                            }
                        }
                        if (content.includes('HIDE_PROCESSING')) {
                            if (window.processingBar) {
                                window.processingBar.hide();
                            }
                        }
                        
                        // Handle chat save triggers
                        if (content.includes('SAVE_CHAT:')) {
                            try {
                                const chatData = content.split('SAVE_CHAT:')[1].split('|')[0];
                                const data = JSON.parse(chatData);
                                this.addChatSession(data.question, data.answer, data.sources);
                            } catch (e) {
                                console.error('Error parsing chat data:', e);
                            }
                        }
                        
                        trigger.innerHTML = '';
                    }
                }
                
                generateSessionId() {
                    return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                }
                
                loadHistoryFromStorage() {
                    try {
                        const stored = localStorage.getItem(this.storageKey);
                        return stored ? JSON.parse(stored) : [];
                    } catch (e) {
                        console.error('Error loading chat history:', e);
                        return [];
                    }
                }
                
                saveHistoryToStorage(history) {
                    try {
                        localStorage.setItem(this.storageKey, JSON.stringify(history));
                    } catch (e) {
                        console.error('Error saving chat history:', e);
                    }
                }
                
                addChatSession(question, answer, sources) {
                    console.log('Adding chat session:', question);
                    
                    const history = this.loadHistoryFromStorage();
                    const sessionId = this.generateSessionId();
                    
                    const newSession = {
                        id: sessionId,
                        question: question,
                        answer: answer,
                        sources: sources,
                        timestamp: new Date().toISOString(),
                        title: this.generateChatTitle(question)
                    };
                    
                    history.unshift(newSession);
                    
                    // Keep only last 50 conversations
                    if (history.length > 50) {
                        history.splice(50);
                    }
                    
                    this.saveHistoryToStorage(history);
                    this.currentSessionId = sessionId;
                    this.displayHistory();
                }
                
                generateChatTitle(question) {
                    if (question.length <= 50) return question;
                    return question.substring(0, 47) + '...';
                }
                
                displayHistory() {
                    const history = this.loadHistoryFromStorage();
                    const container = this.findHistoryContainer();
                    
                    if (!container) {
                        console.error('Chat history container not found');
                        return;
                    }
                    
                    console.log('Updating chat history container:', container.id || container.className);
                    
                    if (history.length === 0) {
                        container.innerHTML = '<div class="history-empty">No previous chats</div>';
                        return;
                    }
                    
                    let html = '';
                    history.forEach(session => {
                        const date = new Date(session.timestamp).toLocaleDateString();
                        const isActive = session.id === this.currentSessionId ? 'active' : '';
                        
                        html += `
                            <div class="history-item ${isActive}" onclick="chatHistory.loadSession('${session.id}')">
                                <div class="history-question">${session.title}</div>
                                <div class="history-date">${date}</div>
                            </div>
                        `;
                    });
                    
                    container.innerHTML = html;
                }
                
                findHistoryContainer() {
                    // Try specific selectors only - no fallback to avoid conflicts
                    const selectors = [
                        '#history-list', 
                        '[data-testid="history-list"]', 
                        '.chat-history-container'
                    ];
                    
                    for (let selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element) return element;
                    }
                    
                    console.warn('Chat history container not found');
                    return null;
                }
                
                loadSession(sessionId) {
                    console.log('Loading session:', sessionId);
                    
                    const history = this.loadHistoryFromStorage();
                    const session = history.find(s => s.id === sessionId);
                    
                    if (!session) {
                        console.error('Session not found:', sessionId);
                        return;
                    }
                    
                    this.currentSessionId = sessionId;
                    
                    // Update UI
                    this.updateAnswer(session.answer);
                    this.updateSources(session.sources);
                    this.clearInput();
                    this.displayHistory();
                }
                
                updateAnswer(answer) {
                    const answerDisplay = document.querySelector('#answer-display');
                    if (answerDisplay) {
                        answerDisplay.innerHTML = `<div class="answer-content">${answer}</div>`;
                    }
                }
                
                updateSources(sources) {
                    const sourcesDisplay = document.querySelector('#sources-display');
                    if (sourcesDisplay) {
                        sourcesDisplay.innerHTML = sources || '';
                    }
                }
                
                clearInput() {
                    const input = document.querySelector('#user-input textarea');
                    if (input) {
                        input.value = '';
                    }
                }
                
                startNewChat() {
                    console.log('Starting new chat');
                    this.currentSessionId = null;
                    this.clearInput();
                    this.updateAnswer('<div class="answer-placeholder">Ask a question to get started</div>');
                    this.updateSources('');
                    this.displayHistory();
                }
                
                loadAndDisplayHistory() {
                    setTimeout(() => {
                        this.displayHistory();
                    }, 500);
                }
            }
            
            // Initialize chat history manager
            window.chatHistory = new ChatHistoryManager();
            
            // Prompt History Management
            class PromptHistoryManager {
                constructor() {
                    this.storageKey = 'opteee_prompt_history';
                    this.maxPrompts = 10; // Keep last 10 prompts
                    this.init();
                }
                
                init() {
                    console.log('Initializing Prompt History Manager');
                    this.displayPrompts();
                    this.setupPromptCapture();
                }
                
                setupPromptCapture() {
                    // Monitor for submit button clicks and Enter key presses
                    setTimeout(() => {
                        const submitBtn = document.querySelector('#submit-btn');
                        const userInput = document.querySelector('#user-input textarea');
                        
                        if (submitBtn) {
                            submitBtn.addEventListener('click', () => {
                                this.capturePrompt();
                            });
                        }
                        
                        if (userInput) {
                            userInput.addEventListener('keydown', (e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    this.capturePrompt();
                                }
                            });
                        }
                    }, 1000);
                }
                
                capturePrompt() {
                    const input = document.querySelector('#user-input textarea');
                    if (input && input.value.trim()) {
                        const prompt = input.value.trim();
                        this.savePrompt(prompt);
                    }
                }
                
                loadPromptsFromStorage() {
                    try {
                        const stored = localStorage.getItem(this.storageKey);
                        return stored ? JSON.parse(stored) : [];
                    } catch (e) {
                        console.error('Error loading prompt history:', e);
                        return [];
                    }
                }
                
                savePromptsToStorage(prompts) {
                    try {
                        localStorage.setItem(this.storageKey, JSON.stringify(prompts));
                    } catch (e) {
                        console.error('Error saving prompt history:', e);
                    }
                }
                
                savePrompt(prompt) {
                    let prompts = this.loadPromptsFromStorage();
                    
                    // Remove duplicate if exists
                    prompts = prompts.filter(p => p.text !== prompt);
                    
                    // Add new prompt at the beginning
                    prompts.unshift({
                        text: prompt,
                        timestamp: new Date().toISOString()
                    });
                    
                    // Keep only the last maxPrompts
                    if (prompts.length > this.maxPrompts) {
                        prompts = prompts.slice(0, this.maxPrompts);
                    }
                    
                    this.savePromptsToStorage(prompts);
                    this.displayPrompts();
                }
                
                displayPrompts() {
                    const container = this.findPromptsContainer();
                    if (!container) {
                        console.error('Prompts container not found');
                        return;
                    }
                    
                    console.log('Updating prompts container:', container.id || container.className);
                    
                    const prompts = this.loadPromptsFromStorage();
                    
                    if (prompts.length === 0) {
                        container.innerHTML = '<div class="prompts-empty">No recent prompts</div>';
                        return;
                    }
                    
                    let html = '';
                    prompts.forEach((prompt, index) => {
                        const truncatedText = prompt.text.length > 60 
                            ? prompt.text.substring(0, 57) + '...' 
                            : prompt.text;
                        
                        html += `
                            <div class="prompt-item" title="${this.escapeHtml(prompt.text)}">
                                <div class="prompt-text" onclick="promptHistory.selectPrompt('${this.escapeHtml(prompt.text)}')">${this.escapeHtml(truncatedText)}</div>
                                <button class="prompt-delete-btn" onclick="event.stopPropagation(); promptHistory.deletePrompt(${index})" title="Remove prompt">×</button>
                            </div>
                        `;
                    });
                    
                    container.innerHTML = html;
                }
                
                findPromptsContainer() {
                    const selectors = [
                        '#prompts-list',
                        '.prompts-container'
                    ];
                    
                    for (let selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element) {
                            console.log('Found prompts container with selector:', selector);
                            return element;
                        }
                    }
                    
                    console.warn('Prompts container not found');
                    return null;
                }
                
                selectPrompt(promptText) {
                    const input = document.querySelector('#user-input textarea');
                    if (input) {
                        input.value = promptText;
                        input.focus();
                        // Trigger input event to ensure Gradio recognizes the change
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                }
                
                escapeHtml(text) {
                    const div = document.createElement('div');
                    div.textContent = text;
                    return div.innerHTML;
                }
                
                deletePrompt(index) {
                    let prompts = this.loadPromptsFromStorage();
                    
                    if (index >= 0 && index < prompts.length) {
                        prompts.splice(index, 1);
                        this.savePromptsToStorage(prompts);
                        this.displayPrompts();
                    }
                }
                
                clearPrompts() {
                    this.savePromptsToStorage([]);
                    this.displayPrompts();
                }
            }
            
            // Initialize prompt history manager
            window.promptHistory = new PromptHistoryManager();
            
            // Processing bar management
            window.processingBar = {
                show: function() {
                    const bar = document.querySelector('#processing-bar');
                    if (bar) {
                        bar.classList.add('active');
                    }
                },
                hide: function() {
                    const bar = document.querySelector('#processing-bar');
                    if (bar) {
                        bar.classList.remove('active');
                    }
                    // Also remove loading state from submit button
                    const submitBtn = document.querySelector('#submit-btn');
                    if (submitBtn) {
                        submitBtn.classList.remove('loading');
                        submitBtn.disabled = false;
                    }
                }
            };
            
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
                    // Fallback for older browsers
                    console.error('Could not copy text: ', err);
                    
                    // Try fallback method
                    const textArea = document.createElement('textarea');
                    textArea.value = text;
                    document.body.appendChild(textArea);
                    textArea.focus();
                    textArea.select();
                    
                    try {
                        document.execCommand('copy');
                        // Show success feedback
                        const originalIcon = button.innerHTML;
                        const originalClass = button.className;
                        
                        button.innerHTML = '✓';
                        button.classList.add('copied');
                        
                        setTimeout(function() {
                            button.innerHTML = originalIcon;
                            button.className = originalClass;
                        }, 2000);
                        
                    } catch (err) {
                        console.error('Fallback copy failed: ', err);
                        // Show error feedback
                        const originalIcon = button.innerHTML;
                        button.innerHTML = '✗';
                        button.style.color = '#dc3545';
                        
                        setTimeout(function() {
                            button.innerHTML = originalIcon;
                            button.style.color = '';
                        }, 2000);
                    }
                    
                    document.body.removeChild(textArea);
                });
            };
            
            // Add event listeners for submit events
            setTimeout(() => {
                const submitBtn = document.querySelector('#submit-btn');
                const userInput = document.querySelector('#user-input textarea');
                
                // Show processing bar and loading state on submit button click
                if (submitBtn) {
                    submitBtn.addEventListener('click', function() {
                        const input = document.querySelector('#user-input textarea');
                        if (input && input.value.trim()) {
                            window.processingBar.show();
                            this.classList.add('loading');
                            this.disabled = true;
                        }
                    });
                }
                
                                        // Show processing bar and loading state on Enter key press
                        if (userInput) {
                            userInput.addEventListener('keydown', function(e) {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    if (this.value.trim()) {
                                        window.processingBar.show();
                                        const submitButton = document.querySelector('#submit-btn');
                                        if (submitButton) {
                                            submitButton.classList.add('loading');
                                            submitButton.disabled = true;
                                        }
                                    }
                                }
                            });
                        }
            }, 1000);
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
            """Handle user message submission"""
            if not message.strip():
                return "", history, gr.update(value='<div class="answer-placeholder">Ask a question to get started</div>'), "", "HIDE_PROCESSING"
            
            try:
                # Get response from RAG pipeline
                response_data = process_question(message, provider, num_results)
                
                # Update history (for server-side state)
                new_history = history + [{
                    "question": message,
                    "answer": response_data["answer"],
                    "sources": response_data["sources"],
                    "timestamp": datetime.now().isoformat()
                }]
                
                # Format answer display - the answer is already HTML from format_chat_response
                answer_html_content = response_data["answer"]
                answer_html = f'<div class="answer-content">{answer_html_content}</div>'
                
                # Trigger localStorage save and hide processing bar
                import json
                save_trigger = "SAVE_CHAT:" + json.dumps({
                    "question": message,
                    "answer": answer_html_content,  # Save the HTML version
                    "sources": response_data["sources"]
                }) + "|HIDE_PROCESSING"
                
                return message, new_history, gr.update(value=answer_html), response_data["sources"], save_trigger
                
            except Exception as e:
                error_msg = f"Error processing question: {str(e)}"
                error_html = f'<div class="answer-content" style="color: var(--error-color);">{error_msg}</div>'
                return message, history, gr.update(value=error_html), "", "HIDE_PROCESSING"
        
        # Wire up the interface
        msg_input.submit(
            handle_submit,
            inputs=[msg_input, chat_history, provider_dropdown, num_results_input],
            outputs=[msg_input, chat_history, answer_display, sources_display, js_trigger]
        )
        
        submit_btn.click(
            handle_submit,
            inputs=[msg_input, chat_history, provider_dropdown, num_results_input],
            outputs=[msg_input, chat_history, answer_display, sources_display, js_trigger]
        )
        
        # New Chat functionality
        def start_new_chat():
            """Start a new chat session"""
            return [], '<div class="answer-placeholder">Ask a question to get started</div>', "", "NEW_CHAT"
        
        new_chat_btn.click(
            start_new_chat,
            outputs=[chat_history, answer_display, sources_display, js_trigger],
            js="() => { if (window.chatHistory) window.chatHistory.startNewChat(); }"
        )
    
    return demo

# Launch the chat interface
if __name__ == "__main__":
    print("🚀 Starting OPTEEE Chat Interface...")
    demo = create_chat_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True
    ) 