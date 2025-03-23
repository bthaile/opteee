# Automatic Vector Store Rebuilding

This project uses an automatic vector store rebuilding approach that checks for new or updated transcripts and rebuilds the vector store automatically when the app starts.

## How It Works

1. **Transcript Files**: Raw transcript files are stored in the `processed_transcripts/` directory and are included in the Git repository.

2. **Vector Store Files**: Vector store files (`vector_store/*.faiss`, `vector_store/*.pkl`) are NOT stored in the Git repository because they're too large. Instead, they are built on-demand.

3. **Auto-Rebuild Process**:
   - When the app starts, it runs `rebuild_vector_store.py`
   - This script checks if any transcript files have been modified since the last vector store rebuild
   - If new/modified transcripts are found, it automatically rebuilds the vector store

## Adding New Content

To add new videos/transcripts:

1. Process new videos locally using your existing pipeline:
   ```bash
   python save_youtube_transcript.py <YouTube URL>
   python preprocess_transcripts.py
   ```

2. Commit the new transcript files to Git:
   ```bash
   git add processed_transcripts/*.json
   git commit -m "Add new video transcripts"
   git push
   ```

3. Deploy to Hugging Face Spaces:
   - The GitHub Actions workflow will push changes to Hugging Face
   - When your app restarts on Hugging Face, it will detect the new transcripts
   - The vector store will be automatically rebuilt with the new content

## Benefits

- **Simple Process**: You only need to add new transcripts; everything else is automatic
- **Consistent Rebuilding**: Vector store is always in sync with transcript files
- **No Manual Steps**: No need to manually rebuild and upload the vector store
- **Traceable History**: All transcript content is version-controlled in Git

## Important Notes

- The first startup after adding new transcripts will be slower because it needs to rebuild the vector store
- If the vector store build fails for any reason, the app will still start, but queries may fail
- To debug rebuild issues, check the logs in your Hugging Face Space 