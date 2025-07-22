import os
import json
from collections import defaultdict

def verify_chunks():
    """Verify that all transcripts have been properly chunked"""
    print("\n Starting chunk verification...")
    
    # Directories to check
    TRANSCRIPT_DIR = "transcripts"
    PROCESSED_DIR = "processed_transcripts"
    
    # Get all transcript files
    transcript_files = [f for f in os.listdir(TRANSCRIPT_DIR) if f.endswith('.txt')]
    print(f"\nFound {len(transcript_files)} transcript files in {TRANSCRIPT_DIR}")
    
    # Get all processed chunk files
    chunk_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('_processed.json')]
    print(f"Found {len(chunk_files)} processed chunk files in {PROCESSED_DIR}")
    
    # Extract video IDs from transcript filenames
    transcript_video_ids = set()
    for filename in transcript_files:
        # Try to extract video ID from filename
        base_name = os.path.splitext(filename)[0]
        if len(base_name) == 11 and base_name.replace('-', '').isalnum():
            transcript_video_ids.add(base_name)
        else:
            # If not a direct video ID, use the filename as is
            transcript_video_ids.add(base_name)
    
    # Extract video IDs from chunk files
    chunk_video_ids = set()
    for filename in chunk_files:
        video_id = filename.replace('_processed.json', '')
        chunk_video_ids.add(video_id)
    
    # Find missing chunks
    missing_chunks = transcript_video_ids - chunk_video_ids
    extra_chunks = chunk_video_ids - transcript_video_ids
    
    # Check chunk file contents
    chunk_stats = defaultdict(lambda: {'chunks': 0, 'total_words': 0})
    for chunk_file in chunk_files:
        try:
            with open(os.path.join(PROCESSED_DIR, chunk_file), 'r') as f:
                chunks = json.load(f)
                video_id = chunk_file.replace('_processed.json', '')
                chunk_stats[video_id]['chunks'] = len(chunks)
                chunk_stats[video_id]['total_words'] = sum(len(chunk['text'].split()) for chunk in chunks)
        except Exception as e:
            print(f"❌ Error reading {chunk_file}: {e}")
    
    # Print summary
    print("\n📊 Verification Summary:")
    print(f"Total transcript files: {len(transcript_files)}")
    print(f"Total processed chunk files: {len(chunk_files)}")
    
    if missing_chunks:
        print(f"\n❌ Missing chunks for {len(missing_chunks)} videos:")
        for video_id in sorted(missing_chunks):
            print(f"- {video_id}")
    
    if extra_chunks:
        print(f"\n⚠️ Extra chunk files for {len(extra_chunks)} videos (no matching transcript):")
        for video_id in sorted(extra_chunks):
            print(f"- {video_id}")
    
    print("\n📈 Chunk Statistics:")
    for video_id, stats in chunk_stats.items():
        print(f"\n{video_id}:")
        print(f"- Number of chunks: {stats['chunks']}")
        print(f"- Total words: {stats['total_words']}")
        print(f"- Average words per chunk: {stats['total_words']/stats['chunks']:.1f}")
    
    # Overall statistics
    total_chunks = sum(stats['chunks'] for stats in chunk_stats.values())
    total_words = sum(stats['total_words'] for stats in chunk_stats.values())
    print(f"\n📊 Overall Statistics:")
    print(f"Total chunks across all videos: {total_chunks}")
    print(f"Total words across all chunks: {total_words}")
    print(f"Average chunks per video: {total_chunks/len(chunk_stats):.1f}")
    print(f"Average words per chunk: {total_words/total_chunks:.1f}")
    
    # Final status
    if not missing_chunks and not extra_chunks:
        print("\n✅ All transcripts have been properly chunked!")
    else:
        print("\n⚠️ Some transcripts need attention:")
        if missing_chunks:
            print(f"- {len(missing_chunks)} transcripts need to be chunked")
        if extra_chunks:
            print(f"- {len(extra_chunks)} chunk files have no matching transcript")

if __name__ == "__main__":
    verify_chunks() 