"""
Entry point for Hugging Face Spaces.
This file runs the Gradio interface for searching options trading knowledge.
"""
import gradio as gr
import os
import markdown # Add import for markdown library
from vector_search import search_vector_store, build_vector_store
from rag_pipeline import (
    CustomFAISSRetriever,
    create_rag_chain,
    run_rag_query,
    get_available_providers,
    DEFAULT_TOP_K
)
from datetime import datetime

# Check if we need to build the vector store using config paths
from config import VECTOR_DIR
index_path = os.path.join(VECTOR_DIR, "faiss.index")
vector_store_exists = os.path.exists(os.path.dirname(index_path))
if not vector_store_exists:
     print(f"WARNING: Vector store index directory {os.path.dirname(index_path)} not found. RAG search might fail.")
     # Consider adding logic here to *attempt* building if missing
     # build_vector_store() # Example: If you wanted to build on startup if missing

# Initialize the retriever and chains at startup
retriever = CustomFAISSRetriever(top_k=DEFAULT_TOP_K)
provider_chains = {}

def initialize_chains():
    """Initialize chains for all available providers"""
    # First, validate system configuration
    from rag_pipeline import validate_system_configuration
    print("🔧 Validating system before initializing chains...")
    validate_system_configuration(verbose=True)
    
    available_providers = get_available_providers()
    for provider in available_providers:
        try:
            _, chain = create_rag_chain(retriever, provider=provider)
            provider_chains[provider] = chain
            print(f"✅ Initialized chain for {provider}")
        except Exception as e:
            print(f"❌ Failed to initialize {provider} chain: {e}")
            print(f"   This provider will not be available in the interface.")

def format_date(date_str):
    """Convert YYYYMMDD to readable format."""
    try:
        # Parse the date string
        if len(date_str) == 8:  # Format: YYYYMMDD
            date_obj = datetime.strptime(date_str, '%Y%m%d')
        elif 'T' in date_str:  # Format: YYYY-MM-DDT...
            date_obj = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
        elif '-' in date_str:  # Format: YYYY-MM-DD
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        else:
            return date_str  # Return original if format unknown
        
        # Format as: "Monday, January 1, 2024"
        return date_obj.strftime("%A, %B %d, %Y")
    except Exception:
        return date_str  # Return original if parsing fails

def search_transcripts(query: str, num_results: str, provider: str, sort_by: str = "relevance") -> str:
    """Search transcripts using the RAG pipeline"""
    try:
        # Convert num_results to integer and validate
        try:
            num_results = int(num_results)
            if num_results < 1 or num_results > 10:
                return "Error: Number of results must be between 1 and 10"
        except ValueError:
            return "Error: Please enter a valid number for results"
        
        # Update retriever settings
        retriever.top_k = num_results
        retriever.sort_by = sort_by
        
        # Get the appropriate chain
        if provider not in provider_chains:
            return f"Error: Provider {provider} not initialized"
        
        chain = provider_chains[provider]
        
        # Run the query
        result = run_rag_query(retriever, chain, query)
        
        # Format the response as HTML
        # Convert the Markdown answer to HTML
        answer_html = markdown.markdown(result.get('answer', 'No answer generated.'))
        html_response = f"<div>{answer_html}</div>" # Use a div instead of p for potentially multi-paragraph answers
        html_response += "<h3>Video Links</h3>"

        if not result.get('sources'):
             html_response += "<p>No relevant video sources found.</p>"
        else:
            for source in result['sources']:
                # Format the date nicely
                formatted_date = 'Unknown Date'
                try:
                    date_str = source.get('upload_date', '')
                    if date_str:
                        if 'T' in date_str:  # ISO format like 2023-10-26T...
                            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        else:  # YYYYMMDD format
                            date = datetime.strptime(date_str, '%Y%m%d')
                        formatted_date = date.strftime("%A, %b %d, %Y") # e.g., Thursday, Oct 26, 2023
                except Exception as date_e:
                    print(f"Warning: Could not parse date '{source.get('upload_date', '')}': {date_e}")
                    formatted_date = source.get('upload_date', 'Unknown Date') # Fallback to original string or unknown

                # Start the div for this result
                # Added basic inline style for margin, padding, border for visual separation
                html_response += '<div class="video-result" style="margin-bottom: 15px; border: 1px solid #eee; padding: 10px; border-radius: 5px;">'

                # Title
                title = source.get('title', 'Untitled Video')
                html_response += f'<b>{title}</b><br/>'

                # Video Link, Timestamp, Duration line
                details_parts = []
                video_link = source.get('url', '')
                if video_link:
                    details_parts.append(f'<a href="{video_link}" target="_blank">Watch Video</a>')

                timestamp = source.get('start_timestamp', '')
                if timestamp:
                     # Attempt to format timestamp if it's numeric seconds
                    try:
                        ts_seconds = float(timestamp)
                        minutes = int(ts_seconds // 60)
                        seconds = int(ts_seconds % 60)
                        timestamp_formatted = f"{minutes:02d}:{seconds:02d}"
                        details_parts.append(f'Start: {timestamp_formatted}')
                    except (ValueError, TypeError):
                         details_parts.append(f'Start: {timestamp}') # Fallback to original string
                
                duration = source.get('duration', '')
                if duration:
                     # Attempt to format duration if it's numeric seconds
                    try:
                        dur_seconds = float(duration)
                        minutes = int(dur_seconds // 60)
                        seconds = int(dur_seconds % 60)
                        duration_formatted = f"{minutes}m {seconds}s"
                        details_parts.append(f'Duration: {duration_formatted}')
                    except (ValueError, TypeError):
                         details_parts.append(f'Duration: {duration}') # Fallback to original string

                if details_parts: # Only add the line if there are details
                    html_response += ' | '.join(details_parts) + '<br/>'

                # Transcript Context Snippet
                content = source.get('content', '')
                if content:
                    # Basic escaping for HTML
                    import html
                    content_escaped = html.escape(content)
                    context_snippet = content_escaped[:300].strip() + ("..." if len(content_escaped) > 300 else "")
                    html_response += f'<i>"{context_snippet}"</i>'
                else:
                    # Fallback description
                    html_response += f'<i>Relevant content about "{query}".</i>'

                # Score and Date (on a new line for clarity)
                score = source.get('score', 0.0) # Default score to 0.0 if missing
                html_response += f'<br/><small><i>(Score: {score:.2f} | Date: {formatted_date})</i></small>' # Show score with 2 decimals

                # Close the div
                html_response += '</div>'

        return html_response

    except Exception as e:
        # Also return errors as HTML
        import traceback
        error_trace = traceback.format_exc()
        return f"<p style='color: red;'><b>Error:</b> {str(e)}</p><pre>{error_trace}</pre>"

# Initialize the chains at startup
initialize_chains()

print("==== Chains Initialized ====") # Added log

# Create the Gradio interface
print("==== Defining Gradio Interface ====") # Added log
iface = gr.Interface(
    fn=search_transcripts,
    inputs=[
        gr.Textbox(
            label="Search Query",
            placeholder="Enter your options trading question here..."
        ),
        gr.Textbox(
            label="Number of Results",
            value=str(DEFAULT_TOP_K),
            placeholder="Enter number of results (1-10)",
            info="Enter a number between 1 and 10"
        ),
        gr.Dropdown(
            choices=get_available_providers(),
            value=get_available_providers()[0],
            label="AI Provider"
        ),
        gr.Dropdown(
            choices=["relevance", "date", "combined"],
            value="relevance",
            label="Sort Results By",
            info="relevance: Best matches first | date: Newest first | combined: Balance both"
        )
    ],
    outputs=gr.HTML(label="Results"),
    title="Options Trading Search",
    description="Search through Outlier Trading Video content using AI-powered search.",
    allow_flagging="never",  # This removes the Flag button!
    examples=[
        ["What is gamma in options trading?", "5", "openai", "relevance"],
        ["Explain ratio call diagonals", "3", "claude", "date"],
        ["What is a covered strangle and when to use it?", "4", "openai", "combined"],
    ]
)

print("==== Gradio Interface Defined ====") # Added log

# Launch the app
if __name__ == "__main__":
    print("==== Entering main block ====") # Added log
    iface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
    print("==== Gradio launch command executed ====") # Added log
