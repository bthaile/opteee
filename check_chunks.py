#!/usr/bin/env python
"""
This script verifies that transcript chunks are being processed correctly and can be retrieved 
from the vector store for RAG queries. It provides diagnostics about the index and performs test searches.
"""

import os
import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Configuration
VECTOR_STORE_DIR = "vector_store"
PROCESSED_DIR = "processed_transcripts"
MODEL_NAME = "all-MiniLM-L6-v2"
TEST_QUERIES = [
    "What is delta in options trading?",
    "How to manage risk in options trading?",
    "What are the greeks in options?",
    "How to roll options positions?"
]

def load_vector_store():
    """Load the vector store index and metadata"""
    print("\n🔍 Loading vector store...")
    
    # Check if all required files exist
    index_path = os.path.join(VECTOR_STORE_DIR, "transcript_index.faiss") 
    texts_path = os.path.join(VECTOR_STORE_DIR, "transcript_texts.pkl")
    metadata_path = os.path.join(VECTOR_STORE_DIR, "transcript_metadata.pkl")
    
    for path in [index_path, texts_path, metadata_path]:
        if not os.path.exists(path):
            print(f"❌ Error: {path} not found!")
            return None, None, None
    
    # Load the index
    try:
        index = faiss.read_index(index_path)
        print(f"✅ FAISS index loaded: {index.ntotal} vectors with dimension {index.d}")
        
        # Load texts and metadata
        with open(texts_path, 'rb') as f:
            texts = pickle.load(f)
        
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        
        print(f"✅ Loaded {len(texts)} text chunks")
        print(f"✅ Loaded {len(metadata)} metadata entries")
        
        if len(texts) != index.ntotal or len(metadata) != index.ntotal:
            print(f"⚠️ Warning: Mismatch in counts - FAISS: {index.ntotal}, Texts: {len(texts)}, Metadata: {len(metadata)}")
        
        return index, texts, metadata
    except Exception as e:
        print(f"❌ Error loading vector store: {e}")
        return None, None, None

def count_processed_transcripts():
    """Count the number of processed transcript files and their chunks"""
    if not os.path.exists(PROCESSED_DIR):
        print(f"❌ Error: {PROCESSED_DIR} directory not found!")
        return 0, 0
    
    files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
    total_chunks = 0
    
    print(f"\n📊 Found {len(files)} processed transcript files")
    
    # Sample a few files to count chunks
    sample_size = min(10, len(files))
    sample_files = np.random.choice(files, sample_size, replace=False) if len(files) > 0 else []
    
    for file in sample_files:
        try:
            with open(os.path.join(PROCESSED_DIR, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                total_chunks += len(data)
        except Exception as e:
            print(f"❌ Error loading {file}: {e}")
    
    # Estimate total chunks based on sample
    if sample_size > 0:
        estimated_chunks = int(total_chunks / sample_size * len(files))
        print(f"📊 Estimated total chunks across all transcripts: ~{estimated_chunks}")
    
    return len(files), total_chunks

def check_sample_chunks():
    """Display sample chunks from processed transcripts"""
    if not os.path.exists(PROCESSED_DIR):
        print(f"❌ Error: {PROCESSED_DIR} directory not found!")
        return
    
    files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
    if not files:
        print("❌ No processed transcript files found!")
        return
    
    # Choose a random file
    sample_file = np.random.choice(files)
    print(f"\n📝 Sample chunks from: {sample_file}")
    
    try:
        with open(os.path.join(PROCESSED_DIR, sample_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Display two random chunks
            if data:
                sample_indices = np.random.choice(len(data), min(2, len(data)), replace=False)
                for i, idx in enumerate(sample_indices):
                    chunk = data[idx]
                    print(f"\n------- SAMPLE CHUNK {i+1} -------")
                    print(f"Text: {chunk['text'][:200]}...")
                    print(f"Video: {chunk['metadata'].get('title', 'Unknown')}")
                    print(f"Timestamp: {chunk['metadata'].get('start_timestamp', 'Unknown')}")
                    print(f"URL: {chunk['metadata'].get('video_url_with_timestamp', 'Unknown')}")
                    print(f"Chunk index: {chunk['metadata'].get('chunk_index', 'Unknown')}/{chunk['metadata'].get('total_chunks', 'Unknown')}")
    except Exception as e:
        print(f"❌ Error reading sample chunks: {e}")

def test_search_queries():
    """Test search queries against the vector store"""
    print("\n🔍 Loading embedding model...")
    try:
        model = SentenceTransformer(MODEL_NAME)
        print(f"✅ Model loaded: {MODEL_NAME}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Load vector store
    index, texts, metadata = load_vector_store()
    if not index or not texts or not metadata:
        return
    
    print("\n🔎 Testing search queries...")
    for query in TEST_QUERIES:
        print(f"\n📌 Query: {query}")
        
        # Encode the query
        query_embedding = model.encode([query])[0]
        query_embedding = np.array([query_embedding]).astype('float32')
        
        # Search the index
        k = 3  # Number of results to retrieve
        distances, indices = index.search(query_embedding, k)
        
        # Display results
        print(f"Top {k} results:")
        for i, idx in enumerate(indices[0]):
            if idx == -1 or idx >= len(texts):
                continue
                
            text = texts[idx]
            meta = metadata[idx]
            score = float(distances[0][i])
            
            print(f"\n--- Result {i+1} (score: {score:.4f}) ---")
            print(f"Text: {text[:150]}...")
            print(f"Video: {meta.get('title', 'Unknown')}")
            print(f"Timestamp: {meta.get('start_timestamp', 'Unknown')}")
            print(f"URL: {meta.get('video_url_with_timestamp', meta.get('url', 'Unknown'))}")

def main():
    """Main function to run all checks"""
    print("="*80)
    print("CHUNK PROCESSING VERIFICATION")
    print("="*80)
    
    # Check if vector store directory exists
    if not os.path.exists(VECTOR_STORE_DIR):
        print(f"❌ Error: Vector store directory '{VECTOR_STORE_DIR}' not found!")
        print("   You need to run create_vector_store.py first.")
        return
    
    # Count processed transcripts
    files_count, chunks_count = count_processed_transcripts()
    
    # Check sample chunks
    if files_count > 0:
        check_sample_chunks()
    
    # Test search queries
    test_search_queries()
    
    print("\n" + "="*80)
    print("VERIFICATION COMPLETE")
    print("="*80)
    
    if files_count > 0 and load_vector_store()[0] is not None:
        print("\n✅ The system appears to be set up correctly!")
        print("   You can now use the RAG pipeline with:")
        print("   python rag_pipeline.py \"Your question about options trading?\"")
    else:
        print("\n❌ There are issues with the chunk processing setup.")
        print("   Please check the errors above and fix them before using the RAG pipeline.")

if __name__ == "__main__":
    main() 