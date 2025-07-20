import os
import faiss
import numpy as np
import json

# Set up environment variables for model caching before importing SentenceTransformer
os.environ.setdefault('TRANSFORMERS_CACHE', '/app/cache/huggingface')
os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', '/app/cache/sentence_transformers')
os.environ.setdefault('HF_HOME', '/app/cache/huggingface')

from sentence_transformers import SentenceTransformer
from config import VECTOR_STORE_PATH, PROCESSED_TRANSCRIPTS_PATH, MODEL_NAME, TOP_K

model = None

def get_model():
    global model
    if model is None:
        print(f"Loading model: {MODEL_NAME}")
        model = SentenceTransformer(MODEL_NAME)
    return model

def build_vector_store():
    """Build vector store from processed transcripts"""
    print(f"BUILDING VECTOR STORE - Using model: {MODEL_NAME}")
    transcript_files = os.listdir(PROCESSED_TRANSCRIPTS_PATH)
    
    if not transcript_files:
        print("No transcript files found!")
        return False
    
    # Load and process chunks
    all_chunks = []
    chunk_metadata = []
    
    for filename in transcript_files:
        if not filename.endswith('.json'):
            continue
            
        file_path = os.path.join(PROCESSED_TRANSCRIPTS_PATH, filename)
        try:
            with open(file_path, 'r') as f:
                transcript_data = json.load(f)
                
            for chunk in transcript_data:
                if isinstance(chunk, dict) and 'text' in chunk and 'metadata' in chunk:
                    all_chunks.append(chunk['text'])
                    # Extract metadata in the format our search expects
                    metadata = {
                        'title': chunk['metadata'].get('title', 'Untitled'),
                        'video_url': chunk['metadata'].get('video_url_with_timestamp', '#'),
                        'timestamp': chunk['metadata'].get('start_timestamp_seconds', 0),
                        'text': chunk['text']
                    }
                    chunk_metadata.append(metadata)
                    
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    print(f"\n✅ Loaded {len(all_chunks)} transcript chunks")
    
    if len(all_chunks) == 0:
        print("No valid chunks found!")
        return False
    
    # Generate embeddings
    model = get_model()
    embeddings = model.encode(all_chunks, batch_size=32, show_progress_bar=True)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Save index and metadata
    os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
    faiss.write_index(index, os.path.join(VECTOR_STORE_PATH, "faiss.index"))
    
    with open(os.path.join(VECTOR_STORE_PATH, "metadata.json"), 'w') as f:
        json.dump(chunk_metadata, f)
    
    print(f"✅ Vector store built successfully with {len(all_chunks)} chunks")
    return True

def search_vector_store(query, top_k=TOP_K):
    # Check if vector store exists
    index_path = os.path.join(VECTOR_STORE_PATH, "faiss.index")
    metadata_path = os.path.join(VECTOR_STORE_PATH, "metadata.json")
    
    if not os.path.exists(index_path) or not os.path.exists(metadata_path):
        print("Vector store not found. Building...")
        build_vector_store()
    
    # Load index and metadata
    index = faiss.read_index(index_path)
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Encode query
    model = get_model()
    query_embedding = model.encode([query])
    
    # Search
    distances, indices = index.search(np.array(query_embedding).astype('float32'), top_k)
    
    # Format results
    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):
            result = metadata[idx].copy()
            result['score'] = float(1.0 - distances[0][i])
            results.append(result)
    
    return results 