# Weekly Transcript Processing Report

**Processing Date:** $(date '+%Y-%m-%d %H:%M:%S UTC')
**Pipeline Version:** GitHub Actions (Steps 1-3 only)

## Processing Summary

- **Videos Discovered:** $(python3 -c "import json; print(len(json.load(open('outlier_trading_videos.json'))))" 2>/dev/null || echo "0")
- **Transcripts Generated:** $(find transcripts -name "*.txt" 2>/dev/null | wc -l)
- **Processed Chunks:** $(find processed_transcripts -name "*.json" 2>/dev/null | wc -l)
- **Vector Store:** Created by Hugging Face during Docker build

## Processing Configuration

- **Chunk Size:** 250 words
- **Overlap:** 50 words
- **Processing Mode:** Non-interactive (CI/CD)
- **Architecture:** GitHub Actions handles transcripts, Hugging Face handles vector store

## Files Updated

- `outlier_trading_videos.json` - Video metadata
- `transcripts/` - Raw transcript files
- `processed_transcripts/` - Chunked transcript data

## Next Steps

- Vector store creation happens automatically on Hugging Face during Docker build
- Hugging Face deployment will be triggered after this workflow completes

---
*This report was generated automatically by GitHub Actions*
