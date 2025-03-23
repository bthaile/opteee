import os
import gradio as gr
from dotenv import load_dotenv
from rag_pipeline import (
    CustomFAISSRetriever, 
    create_rag_chain,
    run_rag_query,
    get_available_providers,
    DEFAULT_TOP_K,
    DEFAULT_TEMPERATURE,
    DEFAULT_LLM_PROVIDER
)

# Load environment variables
load_dotenv()

# Initialize the RAG pipeline
def setup_rag_pipeline(top_k=DEFAULT_TOP_K, provider=DEFAULT_LLM_PROVIDER):
    """Set up the RAG pipeline with the specified parameters"""
    try:
        # Initialize retriever
        retriever = CustomFAISSRetriever(top_k=top_k)
        
        # Create RAG chain
        retriever, chain = create_rag_chain(
            retriever,
            temperature=DEFAULT_TEMPERATURE,
            provider=provider
        )
        
        return retriever, chain
    except Exception as e:
        print(f"Error setting up RAG pipeline: {str(e)}")
        return None, None

# Function to query the RAG pipeline
def query_rag(question, top_k=DEFAULT_TOP_K, provider="openai"):
    """Query the RAG pipeline and format results for the web interface"""
    try:
        retriever, chain = setup_rag_pipeline(top_k=top_k, provider=provider)
        if retriever is None or chain is None:
            return "Error: Could not initialize RAG pipeline. Please check logs.", "No sources available."
            
        result = run_rag_query(retriever, chain, question)
        
        # Format the answer and sources for display
        answer = result['answer']
        
        sources_text = "## Sources:\n\n"
        for i, source in enumerate(result['sources']):
            sources_text += f"{i+1}. **{source['title']}**\n"
            sources_text += f"   - Timestamp: {source['timestamp']}\n"
            sources_text += f"   - [Watch Video]({source['url']})\n\n"
        
        return answer, sources_text
    except Exception as e:
        return f"Error: {str(e)}", "No sources available due to error."

# Check available providers
try:
    available_providers = get_available_providers()
    if not available_providers:
        default_provider = "openai"  # Default to OpenAI even if not available
        print("⚠️ Warning: No API keys found. You will need to configure API keys in Hugging Face Spaces.")
    else:
        default_provider = available_providers[0]
except Exception as e:
    print(f"Error getting providers: {str(e)}")
    default_provider = "openai"
    available_providers = ["openai", "claude"]

# Create Gradio interface
def create_demo():
    with gr.Blocks(title="Options Trading Education Assistant") as demo:
        gr.Markdown("# Options Trading Education Assistant")
        gr.Markdown("Ask questions about options trading based on Outlier Trading videos!")
        
        with gr.Row():
            with gr.Column(scale=3):
                question = gr.Textbox(
                    label="Your Question", 
                    placeholder="Ask anything about options trading...",
                    lines=3
                )
            with gr.Column(scale=1):
                top_k = gr.Slider(
                    minimum=1, 
                    maximum=10, 
                    value=DEFAULT_TOP_K, 
                    step=1, 
                    label="Number of sources to retrieve"
                )
                provider = gr.Dropdown(
                    choices=available_providers,
                    value=default_provider,
                    label="LLM Provider"
                )
        
        submit_btn = gr.Button("Get Answer", variant="primary")
        
        with gr.Row():
            with gr.Column():
                answer_box = gr.Markdown(label="Answer")
            with gr.Column():
                sources_box = gr.Markdown(label="Sources")
        
        submit_btn.click(
            fn=query_rag,
            inputs=[question, top_k, provider],
            outputs=[answer_box, sources_box]
        )
        
        return demo

# This will be imported by app.py
demo = create_demo()

# Launch the app if run directly
if __name__ == "__main__":
    demo.launch() 