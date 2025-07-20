import os
import json
import numpy as np
from tqdm import tqdm
import faiss
import pickle

# Set up environment variables for model caching before importing SentenceTransformer
os.environ.setdefault('TRANSFORMERS_CACHE', '/app/cache/huggingface')
os.environ.setdefault('SENTENCE_TRANSFORMERS_HOME', '/app/cache/sentence_transformers')
os.environ.setdefault('HF_HOME', '/app/cache/huggingface')

from sentence_transformers import SentenceTransformer
import argparse
from pipeline_config import PROCESSED_DIR, VECTOR_STORE_DIR, BATCH_SIZE

# Use the correct directory paths from pipeline_config
MODEL_NAME = "all-MiniLM-L6-v2"

# Global variable to allow override of vector store directory
VECTOR_OUTPUT_DIR = VECTOR_STORE_DIR

def load_processed_transcripts():
    """Load all processed transcript chunks from JSON files"""
    print(f"Loading processed transcripts from {PROCESSED_DIR}...")
    all_chunks = []
    all_metadatas = []
    
    # Ensure directory exists
    if not os.path.exists(PROCESSED_DIR):
        raise FileNotFoundError(f"Directory {PROCESSED_DIR} not found. Run preprocess_transcripts.py first.")
    
    # Get all JSON files
    json_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
    print(f"Found {len(json_files)} processed transcript files")
    
    for filename in tqdm(json_files, desc="Loading files"):
        try:
            file_path = os.path.join(PROCESSED_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                # The file now contains a list of chunks
                video_chunks = json.load(f)
                
                for chunk in video_chunks:
                    text = chunk.get('text', '')
                    
                    if text and len(text.strip()) > 0:
                        all_chunks.append(text)
                        # The entire chunk dictionary is the metadata
                        all_metadatas.append(chunk)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    
    print(f"✅ Loaded {len(all_chunks)} transcript chunks")
    return all_chunks, all_metadatas

def create_embeddings(texts, model_name=MODEL_NAME, batch_size=BATCH_SIZE):
    """Create embeddings for all texts using the specified model"""
    print(f"\nLoading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    
    print(f"Creating embeddings for {len(texts)} chunks (batch size: {batch_size})...")
    embeddings = []
    
    # Process in batches to avoid memory issues
    for i in tqdm(range(0, len(texts), batch_size), desc="Creating embeddings"):
        batch_texts = texts[i:i+batch_size]
        batch_embeddings = model.encode(batch_texts, show_progress_bar=False)
        embeddings.extend(batch_embeddings)
    
    embeddings = np.array(embeddings).astype('float32')
    print(f"✅ Created embeddings with shape: {embeddings.shape}")
    return embeddings

def create_faiss_index(embeddings, metadatas, texts):
    """Create and save a FAISS index for fast similarity search"""
    # Create directory for vector store if it doesn't exist
    os.makedirs(VECTOR_OUTPUT_DIR, exist_ok=True)
    
    # Get dimension of embeddings
    dimension = embeddings.shape[1]
    print(f"\nCreating FAISS index with dimension {dimension}...")
    
    # Create a flat index - simple but effective for smaller datasets
    index = faiss.IndexFlatL2(dimension)
    
    # Add vectors to the index
    index.add(embeddings)
    print(f"✅ Added {index.ntotal} vectors to the index")
    
    # Save the index
    index_path = os.path.join(VECTOR_OUTPUT_DIR, "transcript_index.faiss")
    faiss.write_index(index, index_path)
    print(f"✅ Saved FAISS index to {index_path}")
    
    # Save the metadata mapping (needed for retrieval)
    metadata_path = os.path.join(VECTOR_OUTPUT_DIR, "transcript_metadata.pkl")
    with open(metadata_path, 'wb') as f:
        pickle.dump(metadatas, f)
    print(f"✅ Saved metadata mapping to {metadata_path}")
    
    # Save raw texts for retrieval
    texts_path = os.path.join(VECTOR_OUTPUT_DIR, "transcript_texts.pkl")
    with open(texts_path, 'wb') as f:
        pickle.dump(texts, f)
    print(f"✅ Saved raw texts to {texts_path}")
    
    return index

def test_search(index, embeddings, metadatas, model_name=MODEL_NAME, top_k=5):
    """Test the search functionality with a sample query"""
    print("\n=== Testing Search Functionality ===")
    model = SentenceTransformer(model_name)
    
    test_queries = [
        "options trading strategies for beginners",
        "how to manage risk in trading",
        "what is gamma in options",
        "best technical indicators for trading"
    ]
    
    for query in test_queries:
        print(f"\nTest Query: '{query}'")
        
        # Create embedding for query
        query_embedding = model.encode([query])[0].reshape(1, -1).astype('float32')
        
        # Search the index
        distances, indices = index.search(query_embedding, top_k)
        
        print(f"Top {top_k} results:")
        for i, (idx, distance) in enumerate(zip(indices[0], distances[0])):
            result_text = metadatas[idx]['title']
            timestamp = metadatas[idx]['start_timestamp']
            video_url = metadatas[idx]['video_url_with_timestamp']
            
            # Get description and content summary if available
            description = metadatas[idx].get('description', '')
            content_summary = metadatas[idx].get('content_summary', '')
            
            # Truncate description if it's too long
            if description and len(description) > 100:
                description = description[:97] + "..."
                
            print(f"{i+1}. {result_text} (at {timestamp}, distance: {distance:.4f})")
            print(f"   🔗 {video_url}")
            if content_summary:
                print(f"   📝 Summary: {content_summary}")
            if description:
                print(f"   📄 Description: {description}")
            print("")

def main(args):
    global VECTOR_OUTPUT_DIR
    
    # Set output directory if provided
    if hasattr(args, 'output_dir') and args.output_dir:
        VECTOR_OUTPUT_DIR = args.output_dir
    
    print("="*80)
    print(f"VECTOR STORE CREATION - Using model: {args.model}")
    print(f"Output directory: {VECTOR_OUTPUT_DIR}")
    print("="*80)
    
    # Load processed transcript chunks
    texts, metadatas = load_processed_transcripts()
    
    # Create embeddings
    embeddings = create_embeddings(texts, model_name=args.model, batch_size=args.batch_size)
    
    # Create and save FAISS index
    index = create_faiss_index(embeddings, metadatas, texts)
    
    # Test search if requested
    if args.test_search:
        test_search(index, embeddings, metadatas, model_name=args.model)
    
    print("\n"+"="*80)
    print("📝 Vector store creation complete!")
    print(f"✅ Model used: {args.model}")
    print(f"✅ Total chunks indexed: {len(texts)}")
    print(f"📁 Vector store saved to {VECTOR_OUTPUT_DIR}/")
    print("="*80)
    print("\nTo search your vector store, use search_transcripts.py")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a vector store from processed transcripts')
    parser.add_argument('--model', type=str, default=MODEL_NAME, 
                        help=f'Sentence transformer model to use (default: {MODEL_NAME})')
    parser.add_argument('--batch-size', type=int, default=BATCH_SIZE,
                        help=f'Batch size for embedding creation (default: {BATCH_SIZE})')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='Output directory for vector store (default: use config)')
    parser.add_argument('--test-search', action='store_true',
                        help='Run test queries after creating the index')
    
    args = parser.parse_args()
    main(args) 