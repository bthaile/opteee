import os
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
    # Check if directory exists
    if not os.path.exists(VECTOR_DIR):
        raise FileNotFoundError(f"Directory {VECTOR_DIR} not found. Run create_vector_store.py first.")
    
    # Load FAISS index
    index_path = os.path.join(VECTOR_DIR, "transcript_index.faiss")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Index file not found at {index_path}. Run create_vector_store.py first.")
    
    index = faiss.read_index(index_path)
    
    # Load metadata
    metadata_path = os.path.join(VECTOR_DIR, "transcript_metadata.pkl")
    with open(metadata_path, 'rb') as f:
        metadatas = pickle.load(f)
    
    return index, metadatas

def search_transcripts(query, top_k=TOP_K, model_name=MODEL_NAME):
    """
    Search for transcripts matching the query
    
    Args:
        query (str): The search query
        top_k (int): Number of results to return
        model_name (str): Name of the sentence transformer model to use
        
    Returns:
        list: List of dictionaries with search results
    """
    # Load vector store
    index, metadatas = load_vector_store()
    
    # Load model and create query embedding
    model = SentenceTransformer(model_name)
    query_embedding = model.encode([query])[0].reshape(1, -1).astype('float32')
    
    # Search the index
    distances, indices = index.search(query_embedding, top_k)
    
    # Format results
    results = []
    for idx, distance in zip(indices[0], distances[0]):
        metadata = metadatas[idx]
        
        result = {
            'title': metadata['title'],
            'timestamp': metadata['start_timestamp'],
            'video_url': metadata['video_url_with_timestamp'],
            'relevance_score': 1 - distance/10,  # Convert distance to a more intuitive score
            'metadata': metadata
        }
        
        results.append(result)
    
    return results

def format_results(results):
    """Format search results for display"""
    output = []
    
    for i, result in enumerate(results):
        output.append(f"\n{i+1}. {result['title']}")
        output.append(f"   🕒 Timestamp: {result['timestamp']}")
        output.append(f"   🔗 {result['video_url']}")
        output.append(f"   📊 Relevance score: {result['relevance_score']:.2f}")
        output.append("-"*40)
    
    return "\n".join(output)

# Example usage
if __name__ == "__main__":
    results = search_transcripts("options trading strategies for beginners")
    print(format_results(results)) 