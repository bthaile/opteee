#!/usr/bin/env python
"""
Script to fix the vector store by regenerating it with the correct text data format.
This ensures that the texts file contains actual text strings instead of embeddings.
"""

import os
import json
import pickle
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Configuration
PROCESSED_DIR = "processed_transcripts"
VECTOR_DIR = "vector_store"
MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 32

def load_processed_transcripts():
    """Load all processed transcript chunks from JSON files"""
    print(f"Loading processed transcripts from {PROCESSED_DIR}...")
    chunks = []
    metadatas = []
    
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
                chunk_data = json.load(f)
                
                for chunk in chunk_data:
                    text = chunk.get('text', '')
                    metadata = chunk.get('metadata', {})
                    
                    if text and len(text.strip()) > 0:
                        chunks.append(text)
                        metadatas.append(metadata)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
    
    print(f"✅ Loaded {len(chunks)} transcript chunks")
    return chunks, metadatas

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

def create_and_save_index(embeddings, texts, metadatas):
    """Create and save a FAISS index and related data for fast similarity search"""
    # Create directory for vector store if it doesn't exist
    os.makedirs(VECTOR_DIR, exist_ok=True)
    
    # Get dimension of embeddings
    dimension = embeddings.shape[1]
    print(f"\nCreating FAISS index with dimension {dimension}...")
    
    # Create a flat index - simple but effective for smaller datasets
    index = faiss.IndexFlatL2(dimension)
    
    # Add vectors to the index
    index.add(embeddings)
    print(f"✅ Added {index.ntotal} vectors to the index")
    
    # Save the index
    index_path = os.path.join(VECTOR_DIR, "transcript_index.faiss")
    faiss.write_index(index, index_path)
    print(f"✅ Saved FAISS index to {index_path}")
    
    # Save the metadata
    metadata_path = os.path.join(VECTOR_DIR, "transcript_metadata.pkl")
    with open(metadata_path, 'wb') as f:
        pickle.dump(metadatas, f)
    print(f"✅ Saved metadata to {metadata_path}")
    
    # Save raw texts (important: save texts, not embeddings)
    texts_path = os.path.join(VECTOR_DIR, "transcript_texts.pkl")
    with open(texts_path, 'wb') as f:
        pickle.dump(texts, f)
    print(f"✅ Saved raw texts to {texts_path}")
    
    return index

def verify_saved_data():
    """Verify that the saved data is correct"""
    print("\nVerifying saved data...")
    
    try:
        # Check index
        index_path = os.path.join(VECTOR_DIR, "transcript_index.faiss")
        index = faiss.read_index(index_path)
        print(f"✅ FAISS index verified: {index.ntotal} vectors with dimension {index.d}")
        
        # Check texts
        texts_path = os.path.join(VECTOR_DIR, "transcript_texts.pkl")
        with open(texts_path, 'rb') as f:
            texts = pickle.load(f)
        
        # Ensure texts is a list of strings
        if isinstance(texts, list) and (not texts or isinstance(texts[0], str)):
            print(f"✅ Texts verified: {len(texts)} text chunks")
            print(f"   Sample text: {texts[0][:100]}..." if texts else "No texts")
        else:
            print(f"❌ Texts file has incorrect format")
            print(f"   Type: {type(texts)}")
            print(f"   First item type: {type(texts[0]) if texts else 'No items'}")
            return False
        
        # Check metadata
        metadata_path = os.path.join(VECTOR_DIR, "transcript_metadata.pkl")
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        print(f"✅ Metadata verified: {len(metadata)} metadata entries")
        
        # Check consistency
        if len(texts) == len(metadata) == index.ntotal:
            print(f"✅ Data consistency verified: all components have {len(texts)} items")
            return True
        else:
            print(f"❌ Data inconsistency detected:")
            print(f"   Texts: {len(texts)}, Metadata: {len(metadata)}, Index: {index.ntotal}")
            return False
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def test_search(index, texts, metadatas, model_name=MODEL_NAME, top_k=5):
    """Test the search functionality with sample queries"""
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
            if idx < 0 or idx >= len(texts):
                print(f"{i+1}. Invalid index {idx}")
                continue
                
            # Get text snippet
            text_snippet = texts[idx][:100] + "..." if len(texts[idx]) > 100 else texts[idx]
            
            # Get metadata info
            title = metadatas[idx].get('title', 'Unknown')
            timestamp = metadatas[idx].get('start_timestamp', 'Unknown')
            video_url = metadatas[idx].get('video_url_with_timestamp', 'Unknown')
            
            print(f"{i+1}. {title} (at {timestamp}, distance: {distance:.4f})")
            print(f"   🔗 {video_url}")
            print(f"    {text_snippet}")

def main():
    print("="*80)
    print("VECTOR STORE FIX UTILITY")
    print("="*80)
    
    # Backup existing vector store if it exists
    if os.path.exists(VECTOR_DIR):
        backup_dir = f"{VECTOR_DIR}_backup"
        print(f"Creating backup of existing vector store to {backup_dir}")
        os.system(f"rm -rf {backup_dir}")
        os.system(f"cp -r {VECTOR_DIR} {backup_dir}")
        print(f"✅ Backup created")
        
        # Remove existing vector store
        print(f"Removing existing vector store")
        os.system(f"rm -rf {VECTOR_DIR}")
    
    # Load processed transcript chunks
    texts, metadatas = load_processed_transcripts()
    
    # Create embeddings
    embeddings = create_embeddings(texts)
    
    # Create and save FAISS index
    index = create_and_save_index(embeddings, texts, metadatas)
    
    # Verify data
    if verify_saved_data():
        print("\n✅ Vector store has been successfully fixed!")
    else:
        print("\n❌ Issues detected with the fixed vector store. Please check the logs.")
        return
    
    # Test search
    test_search(index, texts, metadatas)
    
    print("\n" + "="*80)
    print(" Vector store fix complete!")
    print(f"✅ Total chunks indexed: {len(texts)}")
    print(f"📁 Fixed vector store saved to {VECTOR_DIR}/")
    print("="*80)

if __name__ == "__main__":
    main() 