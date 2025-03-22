#!/usr/bin/env python
"""
Script to verify if all processed transcripts are correctly loaded in the vector store.
This helps ensure that the RAG system has access to all the processed transcript data.
"""

import os
import json
import pickle
import faiss
import numpy as np
from collections import Counter, defaultdict
from tqdm import tqdm

# Configuration
VECTOR_STORE_DIR = "vector_store"
PROCESSED_DIR = "processed_transcripts"

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

def get_processed_transcripts():
    """Get list of processed transcript files and count total chunks"""
    print("\n🔍 Checking processed transcripts...")
    if not os.path.exists(PROCESSED_DIR):
        print(f"❌ Error: {PROCESSED_DIR} directory not found!")
        return [], {}
        
    files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
    print(f"📊 Found {len(files)} processed transcript files")
    
    # Load each file and count chunks
    transcript_chunks = {}
    print("📊 Loading transcript files to count chunks...")
    for file in tqdm(files):
        try:
            with open(os.path.join(PROCESSED_DIR, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Extract video ID from filename (remove _processed.json)
                video_id = file.replace('_processed.json', '')
                
                # Store chunk count
                transcript_chunks[video_id] = len(data)
        except Exception as e:
            print(f"❌ Error loading {file}: {e}")
    
    print(f"📊 Total transcripts: {len(transcript_chunks)}")
    return files, transcript_chunks

def extract_video_ids_from_metadata(metadata):
    """Extract video IDs from metadata and count chunks per video"""
    video_ids = []
    chunk_counts = defaultdict(int)
    
    for meta in metadata:
        video_id = meta.get('video_id', '')
        if video_id:
            video_ids.append(video_id)
            chunk_counts[video_id] += 1
    
    return video_ids, chunk_counts

def compare_transcript_coverage(transcript_chunks, vector_store_chunks):
    """Compare transcript chunks between processed files and vector store"""
    print("\n🔍 Comparing transcript coverage...")
    
    all_video_ids = set(transcript_chunks.keys()) | set(vector_store_chunks.keys())
    
    # Count stats
    in_both = 0
    only_in_processed = 0
    only_in_vector_store = 0
    chunk_mismatches = 0
    
    missing_in_vector = []
    missing_in_processed = []
    mismatched_chunks = []
    
    for video_id in all_video_ids:
        processed_count = transcript_chunks.get(video_id, 0)
        vector_count = vector_store_chunks.get(video_id, 0)
        
        if processed_count > 0 and vector_count > 0:
            in_both += 1
            if processed_count != vector_count:
                chunk_mismatches += 1
                mismatched_chunks.append((video_id, processed_count, vector_count))
        elif processed_count > 0:
            only_in_processed += 1
            missing_in_vector.append(video_id)
        else:
            only_in_vector_store += 1
            missing_in_processed.append(video_id)
    
    print(f"✅ Transcripts in both: {in_both}")
    print(f"⚠️ Transcripts only in processed files: {only_in_processed}")
    print(f"⚠️ Transcripts only in vector store: {only_in_vector_store}")
    print(f"⚠️ Transcripts with chunk count mismatches: {chunk_mismatches}")
    
    # Show details of mismatches if there are any issues
    if only_in_processed > 0:
        print("\n⚠️ Transcripts missing from vector store (top 5):")
        for video_id in missing_in_vector[:5]:
            print(f"  - {video_id} ({transcript_chunks[video_id]} chunks)")
    
    if only_in_vector_store > 0:
        print("\n⚠️ Transcripts in vector store but not in processed files (top 5):")
        for video_id in missing_in_processed[:5]:
            print(f"  - {video_id} ({vector_store_chunks[video_id]} chunks)")
    
    if chunk_mismatches > 0:
        print("\n⚠️ Transcripts with chunk count mismatches (top 5):")
        for video_id, processed_count, vector_count in mismatched_chunks[:5]:
            print(f"  - {video_id}: {processed_count} chunks in processed file, {vector_count} chunks in vector store")
    
    # Calculate coverage percentage
    coverage_percent = (in_both / len(all_video_ids)) * 100 if all_video_ids else 0
    print(f"\n📊 Overall transcript coverage: {coverage_percent:.2f}% ({in_both}/{len(all_video_ids)})")
    
    return in_both, only_in_processed, only_in_vector_store, chunk_mismatches

def check_metadata_quality(metadata):
    """Check the quality of metadata in the vector store"""
    print("\n🔍 Checking metadata quality...")
    
    total_items = len(metadata)
    if total_items == 0:
        print("❌ No metadata found!")
        return
    
    # Check for required fields
    fields_to_check = ['video_id', 'title', 'chunk_index', 'total_chunks', 'start_timestamp']
    missing_fields = {field: 0 for field in fields_to_check}
    
    for meta in metadata:
        for field in fields_to_check:
            if field not in meta or meta[field] == "":
                missing_fields[field] += 1
    
    # Report quality metrics
    print("📊 Metadata quality check:")
    for field, missing_count in missing_fields.items():
        percent = (missing_count / total_items) * 100
        if missing_count > 0:
            print(f"⚠️ {field}: Missing in {missing_count}/{total_items} entries ({percent:.2f}%)")
        else:
            print(f"✅ {field}: Present in all entries")

def main():
    """Main function to verify vector store completeness"""
    print("="*80)
    print("VECTOR STORE VERIFICATION")
    print("="*80)
    
    # Check if vector store directory exists
    if not os.path.exists(VECTOR_STORE_DIR):
        print(f"❌ Error: Vector store directory '{VECTOR_STORE_DIR}' not found!")
        return
    
    # Check if processed transcripts directory exists
    if not os.path.exists(PROCESSED_DIR):
        print(f"❌ Error: Processed transcripts directory '{PROCESSED_DIR}' not found!")
        return
    
    # Load vector store
    index, texts, metadata = load_vector_store()
    if index is None or texts is None or metadata is None:
        return
    
    # Extract video IDs from vector store metadata
    vector_store_video_ids, vector_store_chunks = extract_video_ids_from_metadata(metadata)
    print(f"📊 Found {len(set(vector_store_video_ids))} unique video IDs in vector store metadata")
    
    # Get processed transcript files
    processed_files, transcript_chunks = get_processed_transcripts()
    
    # Compare coverage
    in_both, only_in_processed, only_in_vector_store, chunk_mismatches = compare_transcript_coverage(
        transcript_chunks, vector_store_chunks
    )
    
    # Check metadata quality
    check_metadata_quality(metadata)
    
    # Report overall status
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    
    if only_in_processed == 0 and chunk_mismatches == 0:
        print("\n✅ All processed transcripts are correctly included in the vector store!")
        print(f"✅ Total of {len(transcript_chunks)} transcripts with {len(metadata)} chunks are ready for RAG.")
    else:
        print("\n⚠️ There are some issues with the vector store:")
        if only_in_processed > 0:
            print(f"  - {only_in_processed} transcripts are missing from the vector store")
        if chunk_mismatches > 0:
            print(f"  - {chunk_mismatches} transcripts have chunk count mismatches")
        print("\n⚠️ Recommendation: Re-run the vector store creation script to ensure all transcripts are included.")

if __name__ == "__main__":
    main() 