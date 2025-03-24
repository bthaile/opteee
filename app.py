"""
Entry point for Hugging Face Spaces.
This file runs the Gradio interface for searching options trading knowledge.
"""
import gradio as gr
import os
from vector_search import search_vector_store, build_vector_store

# Check if we need to build the vector store
index_path = os.path.join("/tmp/vector_store", "faiss.index")
if not os.path.exists(index_path):
    print("Vector store not found. Will be built during startup.")

def search_transcripts(query: str, top_k: int = 5) -> str:
    """Search for relevant transcript chunks"""
    print(f"Searching for: {query} with top_k={top_k}")  # Debug log
    
    if not isinstance(query, str) or not query.strip():
        return "Please enter a valid search query."
    
    try:
        results = search_vector_store(query, top_k=int(top_k))
        
        if not results:
            return "No results found. Try a different query."
        
        markdown_results = []
        for i, result in enumerate(results, 1):
            title = result.get('title', 'Untitled')
            video_url = result.get('video_url', '#')
            timestamp = result.get('timestamp', 0)
            text = result.get('text', '').strip()
            
            minutes = int(timestamp // 60)
            seconds = int(timestamp % 60)
            time_str = f"{minutes}:{seconds:02d}"
            
            result_text = f"### {i}. {title}\n"
            result_text += f"**Timestamp:** {time_str}\n\n"
            result_text += f"{text}\n\n"
            result_text += f"[Watch Video at Timestamp]({video_url}&t={int(timestamp)})\n\n"
            result_text += "---\n\n"
            markdown_results.append(result_text)
        
        return "".join(markdown_results)
    except Exception as e:
        print(f"Search error: {str(e)}")  # Debug log
        return f"An error occurred: {str(e)}"

# Create the Gradio interface
demo = gr.Interface(
    fn=search_transcripts,
    inputs=[
        gr.Textbox(label="Search Query", placeholder="Enter your search query here..."),
        gr.Slider(minimum=1, maximum=20, value=5, step=1, label="Number of Results")
    ],
    outputs=gr.Markdown(label="Search Results"),
    title="Options Trading Knowledge Search",
    description="Search for information across options trading videos",
    allow_flagging="never"
)

# Launch the app
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
