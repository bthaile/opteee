import os
import argparse
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Configuration
VECTOR_DIR = "vector_store"
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 10  # Number of results to return

def load_vector_store():
    """Load the FAISS index and metadata"""
    print(f"Loading vector store from {VECTOR_DIR}...")
    
    # Check if directory exists
    if not os.path.exists(VECTOR_DIR):
        raise FileNotFoundError(f"Directory {VECTOR_DIR} not found. Run create_vector_store.py first.")
    
    # Load FAISS index
    index_path = os.path.join(VECTOR_DIR, "transcript_index.faiss")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Index file not found at {index_path}. Run create_vector_store.py first.")
    
    index = faiss.read_index(index_path)
    print(f"✅ Loaded FAISS index with {index.ntotal} vectors")
    
    # Load metadata
    metadata_path = os.path.join(VECTOR_DIR, "transcript_metadata.pkl")
    with open(metadata_path, 'rb') as f:
        metadatas = pickle.load(f)
    print(f"✅ Loaded metadata for {len(metadatas)} chunks")
    
    return index, metadatas

def search(query, index, metadatas, model_name=MODEL_NAME, top_k=TOP_K, show_text=False):
    """Search the vector store for relevant transcript chunks"""
    print(f"\nQuery: '{query}'")
    
    # Load model and create query embedding
    print("Loading model and creating query embedding...")
    model = SentenceTransformer(model_name)
    query_embedding = model.encode([query])[0].reshape(1, -1).astype('float32')
    
    # Search the index
    print(f"Searching index with {index.ntotal} vectors...")
    distances, indices = index.search(query_embedding, top_k)
    
    print(f"\nTop {top_k} relevant results:")
    print("="*80)
    
    for i, (idx, distance) in enumerate(zip(indices[0], distances[0])):
        metadata = metadatas[idx]
        title = metadata['title']
        timestamp = metadata['start_timestamp']
        video_url = metadata['video_url_with_timestamp']
        
        # Print result with separator line
        print(f"\n{i+1}. {title}")
        print(f"   🕒 Timestamp: {timestamp}")
        print(f"   🔗 {video_url}")
        print(f"   📊 Relevance score: {1 - distance/10:.2f}")
        
        if show_text:
            # Get the text content if we want to display it
            # This would require loading the original file, we skip for simplicity
            # In a real app, you might want to store the texts separately for fast access
            print(f"   Content: <load from processed_transcripts/{metadata['video_id']}_processed.json>")
        
        print("-"*40)

def main():
    parser = argparse.ArgumentParser(description='Search transcript vector store')
    parser.add_argument('query', type=str, nargs='+', help='Search query')
    parser.add_argument('--model', type=str, default=MODEL_NAME, 
                        help=f'Sentence transformer model to use (default: {MODEL_NAME})')
    parser.add_argument('--top-k', type=int, default=TOP_K,
                        help=f'Number of results to return (default: {TOP_K})')
    parser.add_argument('--show-text', action='store_true',
                        help='Show text content of results')
    
    args = parser.parse_args()
    print(f"DEBUG: Command line arguments: {args}")
    
    print("="*80)
    print("TRANSCRIPT SEARCH")
    print("="*80)
    
    # Load the vector store
    index, metadatas = load_vector_store()
    
    # Combine query words into a single string
    query = ' '.join(args.query)
    
    # Search
    search(query, index, metadatas, model_name=args.model, top_k=args.top_k, show_text=args.show_text)
    
    print("\n"+"="*80)
    print("Search complete!")
    print("="*80)

if __name__ == "__main__":
    main() 