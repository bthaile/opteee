#!/usr/bin/env python
"""
Script to check the vector store files and diagnose any issues.
"""

import os
import sys
import pickle
import faiss
import numpy as np

# Constants
VECTOR_STORE_DIR = "vector_store"
TEXTS_PATH = os.path.join(VECTOR_STORE_DIR, "transcript_texts.pkl")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "transcript_metadata.pkl")
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "transcript_index.faiss")

def check_directory():
    """Check if vector store directory exists"""
    print(f"Checking for vector store directory: {VECTOR_STORE_DIR}")
    if os.path.exists(VECTOR_STORE_DIR):
        print(f"✅ Directory exists")
        print(f"Contents: {os.listdir(VECTOR_STORE_DIR)}")
    else:
        print(f"❌ Directory does not exist")
        return False
    return True

def check_file(path):
    """Check if a file exists and get its size"""
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"✅ File exists: {path}")
        print(f"   Size: {size / 1024 / 1024:.2f} MB")
        return True
    else:
        print(f"❌ File does not exist: {path}")
        return False

def load_texts():
    """Load and check texts file"""
    print("\nChecking texts file...")
    if not check_file(TEXTS_PATH):
        return None
    
    try:
        with open(TEXTS_PATH, 'rb') as f:
            texts = pickle.load(f)
            
        print(f"✅ Successfully loaded texts")
        print(f"   Type: {type(texts)}")
        
        if isinstance(texts, list):
            print(f"   Number of items: {len(texts)}")
            print(f"   First few items type: {type(texts[0])}")
            print(f"   Sample item: {texts[0][:100]}..." if texts else "No items")
        elif isinstance(texts, np.ndarray):
            print(f"   Shape: {texts.shape}")
            print(f"   Data type: {texts.dtype}")
            print(f"⚠️ Warning: Texts file contains numpy array instead of text strings")
        else:
            print(f"   Unknown format, expected list or numpy array")
            
        return texts
    except Exception as e:
        print(f"❌ Error loading texts: {e}")
        return None

def load_metadata():
    """Load and check metadata file"""
    print("\nChecking metadata file...")
    if not check_file(METADATA_PATH):
        return None
    
    try:
        with open(METADATA_PATH, 'rb') as f:
            metadata = pickle.load(f)
            
        print(f"✅ Successfully loaded metadata")
        print(f"   Type: {type(metadata)}")
        
        if isinstance(metadata, list):
            print(f"   Number of items: {len(metadata)}")
            print(f"   First item type: {type(metadata[0])}")
            print(f"   First item keys: {list(metadata[0].keys()) if metadata else 'No items'}")
            
        return metadata
    except Exception as e:
        print(f"❌ Error loading metadata: {e}")
        return None

def load_index():
    """Load and check FAISS index"""
    print("\nChecking FAISS index...")
    if not check_file(INDEX_PATH):
        return None
    
    try:
        index = faiss.read_index(INDEX_PATH)
        print(f"✅ Successfully loaded FAISS index")
        print(f"   Number of vectors: {index.ntotal}")
        print(f"   Dimension: {index.d}")
        return index
    except Exception as e:
        print(f"❌ Error loading FAISS index: {e}")
        return None

def check_consistency(texts, metadata, index):
    """Check consistency between texts, metadata, and index"""
    print("\nChecking consistency...")
    
    if texts is None or metadata is None or index is None:
        print("❌ Cannot check consistency because one or more components failed to load")
        return False
    
    # Check if texts is numpy array or list
    texts_count = len(texts) if isinstance(texts, list) else (texts.shape[0] if isinstance(texts, np.ndarray) else 0)
    metadata_count = len(metadata) if metadata else 0
    index_count = index.ntotal if index else 0
    
    print(f"Texts count: {texts_count}")
    print(f"Metadata count: {metadata_count}")
    print(f"Index vectors: {index_count}")
    
    if texts_count == metadata_count == index_count:
        print("✅ All components have the same number of items")
        return True
    else:
        print("❌ Inconsistent item counts between components")
        return False

def main():
    """Main function"""
    print("="*80)
    print("VECTOR STORE DIAGNOSTIC TOOL")
    print("="*80)
    
    # Check directory
    if not check_directory():
        return
    
    # Load components
    texts = load_texts()
    metadata = load_metadata()
    index = load_index()
    
    # Check consistency
    is_consistent = check_consistency(texts, metadata, index)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    if is_consistent and texts is not None and metadata is not None and index is not None:
        print("✅ Vector store appears to be in good condition")
        
        # Check format of texts
        if isinstance(texts, np.ndarray):
            print("\n⚠️ Warning: The texts file contains numpy arrays instead of text strings")
            print("   This may cause errors when retrieving documents")
            print("   You should recreate the vector store correctly")
    else:
        print("❌ Issues detected with the vector store")
        print("   Please recreate the vector store using create_vector_store.py")

if __name__ == "__main__":
    main() 