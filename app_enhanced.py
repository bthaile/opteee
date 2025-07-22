"""
Enhanced version of app.py with custom theming and development features.
This version supports both development and production modes.
"""
import gradio as gr
import os
import markdown
from vector_search import search_vector_store, build_vector_store
from rag_pipeline import (
    CustomFAISSRetriever,
    create_rag_chain,
    run_rag_query,
    get_available_providers,
    DEFAULT_TOP_K
)
from datetime import datetime

# Development mode detection
DEV_MODE = os.getenv('GRADIO_RELOAD', 'false').lower() == 'true'

# Custom CSS for enhanced theming
CUSTOM_CSS = """
/* Custom theme for OPTEEE */
.gradio-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    max-width: 1200px;
    margin: 0 auto;
}

.gr-button {
    background: linear-gradient(45deg, #4285f4, #34a853);
    border: none;
    color: white;
    font-weight: 500;
    transition: all 0.3s ease;
}

.gr-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.gr-textbox {
    border-radius: 8px;
    border: 2px solid #e0e0e0;
    transition: border-color 0.3s ease;
}

.gr-textbox:focus {
    border-color: #4285f4;
    box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
}

.result-container {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
    border-left: 4px solid #4285f4;
}

.source-link {
    color: #1a73e8;
    text-decoration: none;
    font-weight: 500;
}

.source-link:hover {
    text-decoration: underline;
}

.timestamp {
    background: #e8f0fe;
    color: #1a73e8;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.9em;
    font-weight: 500;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    .result-container {
        background: #1f1f1f;
        color: #e0e0e0;
    }
    
    .gr-textbox {
        background: #2d2d2d;
        color: #e0e0e0;
        border-color: #555;
    }
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .gradio-container {
        padding: 8px;
    }
    
    .gr-button {
        width: 100%;
        margin: 4px 0;
    }
}
"""

# Custom JavaScript for enhanced interactivity
CUSTOM_JS = """
function initializeEnhancements() {
    // Add click-to-copy functionality for timestamps
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('timestamp')) {
            navigator.clipboard.writeText(e.target.textContent);
            e.target.style.background = '#34a853';
            e.target.textContent = 'Copied!';
            setTimeout(() => {
                e.target.style.background = '#e8f0fe';
                e.target.textContent = e.target.dataset.original;
            }, 1000);
        }
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            document.querySelector('button[type="submit"]')?.click();
        }
    });
    
    // Add loading animation
    const submitButton = document.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.addEventListener('click', function() {
            this.innerHTML = '🔄 Searching...';
            setTimeout(() => {
                this.innerHTML = 'Search';
            }, 3000);
        });
    }
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeEnhancements);
} else {
    initializeEnhancements();
}
"""

# Load custom CSS from file if it exists (for development)
def load_custom_css():
    css_path = "static/styles.css"
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            return f.read()
    return CUSTOM_CSS

# Initialize vector store and chains
print(" Initializing OPTEEE Enhanced Interface...")
if DEV_MODE:
    print("🔥 Development mode enabled - hot reload active!")

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

def format_response_enhanced(response, sources):
    """Enhanced response formatting with better styling"""
    formatted_response = f"""
    <div class="result-container">
        <div style="margin-bottom: 16px;">
            <h3 style="color: #1a73e8; margin: 0 0 12px 0;">🤖 AI Response</h3>
            <div style="line-height: 1.6; color: #333;">
                {markdown.markdown(response)}
            </div>
        </div>
        
        <div style="border-top: 1px solid #e0e0e0; padding-top: 16px;">
            <h4 style="color: #1a73e8; margin: 0 0 12px 0;">📚 Sources</h4>
            <div>
    """
    
    for i, source in enumerate(sources, 1):
        formatted_response += f"""
            <div style="margin-bottom: 12px; padding: 8px; background: #f5f5f5; border-radius: 4px;">
                <div style="font-weight: 500; color: #1a73e8; margin-bottom: 4px;">
                    {i}. {source.get('title', 'Unknown Title')}
                </div>
                <div style="font-size: 0.9em; color: #666;">
                    <span class="timestamp" data-original="{source.get('timestamp', 'N/A')}">{source.get('timestamp', 'N/A')}</span>
                    <a href="{source.get('url', '#')}" target="_blank" class="source-link" style="margin-left: 12px;">
                        🎬 Watch Video
                    </a>
                </div>
            </div>
        """
    
    formatted_response += """
            </div>
        </div>
    </div>
    """
    
    return formatted_response

def search_transcripts(query, num_results_str, provider, sort_by):
    """Enhanced search function with better error handling"""
    try:
        if not query.strip():
            return "<div class='result-container'>❌ Please enter a search query.</div>"
        
        # Parse number of results
        try:
            num_results = int(num_results_str)
            if num_results < 1 or num_results > 10:
                num_results = DEFAULT_TOP_K
        except ValueError:
            num_results = DEFAULT_TOP_K
        
        # Perform RAG query
        if provider not in provider_chains:
            return f"<div class='result-container'>❌ Provider '{provider}' not available.</div>"
        
        result = run_rag_query(
            query=query,
            retriever=retriever,
            chain=provider_chains[provider],
            top_k=num_results
        )
        
        # Format the response
        return format_response_enhanced(result['answer'], result['sources'])
        
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        if DEV_MODE:
            error_msg += f"\n\nDebug info: {repr(e)}"
        return f"<div class='result-container'>{error_msg}</div>"

# Initialize chains
initialize_chains()

# Create enhanced Gradio interface
with gr.Blocks(
    css=load_custom_css(),
    js=CUSTOM_JS,
    title="OPTEEE - Options Trading Education Assistant",
    theme=gr.themes.Soft()
) as demo:
    
    gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #1a73e8; margin: 0;">🔥 OPTEEE</h1>
            <h2 style="color: #666; margin: 8px 0;">Options Trading Education Assistant</h2>
            <p style="color: #666; margin: 0;">AI-powered search through 14,721+ educational transcript chunks</p>
        </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            query_input = gr.Textbox(
                label="Ask a Question",
                placeholder="What is gamma in options trading?",
                lines=2,
                max_lines=5
            )
        
        with gr.Column(scale=1):
            submit_btn = gr.Button(
                " Search",
                variant="primary",
                scale=1
            )
    
    with gr.Row():
        num_results = gr.Textbox(
            label="Number of Results",
            value=str(DEFAULT_TOP_K),
            placeholder="1-10",
            scale=1
        )
        
        provider = gr.Dropdown(
            choices=get_available_providers(),
            value=get_available_providers()[0] if get_available_providers() else "openai",
            label="AI Provider",
            scale=1
        )
        
        sort_by = gr.Dropdown(
            choices=["relevance", "date", "combined"],
            value="relevance",
            label="Sort By",
            scale=1
        )
    
    results_output = gr.HTML(label="Results")
    
    # Enhanced examples
    gr.Examples(
        examples=[
            ["What is gamma in options trading?", "5", "openai", "relevance"],
            ["Explain covered call strategies", "3", "claude", "date"],
            ["What is implied volatility?", "4", "openai", "combined"],
            ["How do you manage risk in options trading?", "6", "claude", "relevance"],
            ["What is a butterfly spread?", "5", "openai", "combined"],
        ],
        inputs=[query_input, num_results, provider, sort_by],
        outputs=results_output,
        fn=search_transcripts,
        cache_examples=False
    )
    
    # Event handlers
    submit_btn.click(
        fn=search_transcripts,
        inputs=[query_input, num_results, provider, sort_by],
        outputs=results_output
    )
    
    query_input.submit(
        fn=search_transcripts,
        inputs=[query_input, num_results, provider, sort_by],
        outputs=results_output
    )
    
    if DEV_MODE:
        gr.HTML("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 12px; border-radius: 4px; margin: 16px 0;">
                <strong>🔥 Development Mode Active</strong><br>
                Edit <code>app_enhanced.py</code> or <code>static/styles.css</code> and refresh to see changes!
            </div>
        """)

# Launch the app
if __name__ == "__main__":
    print(" Launching OPTEEE Enhanced Interface...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        reload=DEV_MODE,
        show_error=DEV_MODE
    ) 