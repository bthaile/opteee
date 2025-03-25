"""
Entry point for Hugging Face Spaces.
This file runs the Gradio interface for searching options trading knowledge.
"""
import gradio as gr
import os
from vector_search import search_vector_store, build_vector_store
from rag_pipeline import (
    CustomFAISSRetriever,
    create_rag_chain,
    run_rag_query,
    get_available_providers,
    DEFAULT_TOP_K
)

# Check if we need to build the vector store
index_path = os.path.join("/tmp/vector_store", "faiss.index")
if not os.path.exists(index_path):
    print("Vector store not found. Will be built during startup.")

# Initialize the retriever once at startup
retriever = CustomFAISSRetriever(top_k=DEFAULT_TOP_K)

# Get available providers
available_providers = get_available_providers()
if not available_providers:
    raise RuntimeError("No API keys found. Please set OPENAI_API_KEY or CLAUDE_API_KEY in environment variables.")

# Store chains for each provider
provider_chains = {}

def initialize_chains():
    """Initialize chains for all available providers"""
    for provider in available_providers:
        try:
            _, chain = create_rag_chain(retriever, provider=provider)
            provider_chains[provider] = chain
        except Exception as e:
            print(f"Warning: Failed to initialize {provider} chain: {e}")

def search_transcripts(query: str, num_results: int, provider: str) -> str:
    """Search transcripts using the RAG pipeline"""
    try:
        # Get the appropriate chain
        if provider not in provider_chains:
            return f"Error: Provider {provider} not initialized"
        
        chain = provider_chains[provider]
        
        # Update retriever top_k
        retriever.top_k = num_results
        
        # Run the query
        result = run_rag_query(retriever, chain, query)
        
        # Format the response in Markdown
        markdown_response = f"### Answer\n{result['answer']}\n\n### Sources\n"
        
        for i, source in enumerate(result['sources'], 1):
            title = source.get('title', 'Unknown')
            timestamp = source.get('timestamp', 'Unknown')
            url = source.get('url', '#')
            score = source.get('score', 0.0)
            
            markdown_response += f"{i}. **{title}**\n"
            markdown_response += f"   - Timestamp: {timestamp}\n"
            markdown_response += f"   - [Watch Video]({url})\n"
            markdown_response += f"   - Relevance: {score:.4f}\n\n"
        
        return markdown_response
        
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize the chains at startup
initialize_chains()

# Create the Gradio interface
iface = gr.Interface(
    fn=search_transcripts,
    inputs=[
        gr.Textbox(
            label="Search Query",
            placeholder="Enter your options trading question here..."
        ),
        gr.Slider(
            minimum=1,
            maximum=10,
            value=DEFAULT_TOP_K,
            step=1,
            label="Number of Results"
        ),
        gr.Dropdown(
            choices=available_providers,
            value=available_providers[0],
            label="AI Provider"
        )
    ],
    outputs=gr.Markdown(label="Results"),
    title="Options Trading Search",
    description="Search through options trading educational content using AI-powered search.",
    examples=[
        ["What is gamma in options trading?", 5, "openai"],
        ["Explain covered calls", 3, "claude"],
        ["How does implied volatility affect option prices?", 4, "openai"],
    ]
)

# Launch the app
if __name__ == "__main__":
    iface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
