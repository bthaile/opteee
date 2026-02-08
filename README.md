---
title: opteee
emoji: 🔥
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
pinned: false
env:
  - PYTHONPATH=/app
---

# OPTEEE - Options Trading Education Expert

A powerful semantic search application providing intelligent Q&A across a curated collection of options trading educational content. Built with modern technologies for fast, accurate, and context-aware responses.

## Overview

OPTEEE uses advanced natural language processing and vector similarity search to help traders learn from a comprehensive knowledge base of options trading transcripts and educational videos. Ask questions in plain English and get detailed answers with direct links to relevant source material.

## Features

- **Semantic Search**: Advanced NLP-powered search that understands meaning, not just keywords
- **Fast Retrieval**: FAISS vector database delivers millisecond search responses
- **Multi-Source Knowledge Base**: Combines video transcripts and academic research papers
- **Video Integration**: Direct links to specific timestamps in source YouTube videos
- **Research Paper Support**: Academic papers with page references and section context
- **Chat Interface**: Modern, responsive chat UI with conversation history
- **Source Citations**: Every answer includes clickable references with timestamps or page numbers
- **Context-Aware**: Maintains conversation history for follow-up questions
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Knowledge Base

OPTEEE draws from two primary sources:

| Source Type | Content | Count |
|-------------|---------|-------|
| **Video Transcripts** | Options trading tutorials, strategy explanations, market analysis | 17,200+ chunks |
| **Research Papers** | Academic papers on PEAD, volatility, retail trading behavior | 8,900+ chunks |

**Total:** 26,100+ searchable knowledge chunks

## Architecture

- **Backend**: FastAPI with RESTful API endpoints
- **Frontend**: React with modern UI components
- **Search Engine**: Sentence-transformers with FAISS vector database
- **NLP Model**: all-MiniLM-L6-v2 for semantic embeddings
- **Deployment**: Docker containerization for easy deployment

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerized deployment)
- Git

### Local Development Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/opteee.git
cd opteee
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the development server**:
```bash
python main.py
```

The application will be available at `http://localhost:7860`

### Docker Deployment

Build and run with Docker:

```bash
# Build the Docker image
docker build -t opteee .

# Run the container
docker run -p 7860:7860 opteee
```

Or use Docker Compose:

```bash
docker-compose up
```

## API Documentation

### Endpoints

- **GET `/api/health`** - Health check endpoint
  - Returns service status and version information

- **POST `/api/chat`** - Main chat endpoint
  - Request body:
    ```json
    {
      "query": "What is a covered call?",
      "provider": "huggingface",
      "num_results": 5,
      "format": "detailed",
      "conversation_history": []
    }
    ```
  - Returns answer with sources and timestamps

- **GET `/`** - Serves the React frontend application

## Project Structure

```
opteee/
├── main.py                      # FastAPI application entry point
├── config.py                    # Configuration and settings
├── rag_pipeline.py              # RAG implementation
├── vector_search.py             # Vector similarity search
├── create_vector_store.py       # Vector store creation (transcripts + PDFs)
├── rebuild_vector_store.py      # Vector store rebuilding
├── process_pdfs.py              # PDF semantic chunking utility
├── app/
│   ├── models/                  # Pydantic models
│   │   └── chat_models.py       # Chat request/response models (supports video + PDF)
│   └── services/                # Business logic services
│       ├── rag_service.py       # RAG service implementation
│       └── formatters.py        # Response formatting (HTML + Discord)
├── frontend/
│   └── build/                   # React production build
├── vector_store/                # FAISS vector database files
├── processed_transcripts/       # Processed video transcript chunks (JSON)
├── processed_pdfs/              # Processed PDF document chunks (JSON)
├── transcripts/                 # Raw transcript data
├── static/                      # Static assets (CSS, JS)
├── templates/                   # HTML templates
├── discord/                     # Discord bot integration
│   ├── discord_bot.py           # Discord bot implementation
│   └── ...                      # Bot configuration files
├── docs/                        # Documentation
├── archive/                     # Archived utilities and scripts
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
└── requirements.txt             # Python dependencies
```

## Key Technologies

- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance Python web framework
- **[React](https://reactjs.org/)** - Modern frontend JavaScript library
- **[Sentence Transformers](https://www.sbert.net/)** - State-of-the-art sentence embeddings
- **[FAISS](https://github.com/facebookresearch/faiss)** - Efficient similarity search and clustering
- **[Docker](https://www.docker.com/)** - Containerization platform
- **[HuggingFace](https://huggingface.co/)** - Model hosting and deployment

## Development Workflow

1. **Backend Changes**: Modify FastAPI endpoints in `main.py` or services in `app/services/`
2. **Frontend Changes**: Update React components in `frontend/src/` (requires separate build)
3. **Testing**: Run locally with `python main.py`
4. **Vector Store Updates**: Rebuild with `python rebuild_vector_store.py`
5. **Deploy**: Build and push Docker image

## Configuration

Key configuration options in `config.py`:

- `MODEL_NAME`: Sentence transformer model (default: "all-MiniLM-L6-v2")
- `TOP_K`: Number of top results to retrieve (default: 5)
- `CHUNK_SIZE`: Size of text chunks for processing (default: 500)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)

## Updating Knowledgebase

OPTEEE uses an automated GitHub Actions workflow to keep the knowledge base up-to-date with the latest educational content. The system automatically discovers new videos, generates transcripts, and deploys updates.

### Automated Weekly Updates

The knowledge base is automatically updated every Sunday at 8:00 PM UTC (3:00 PM CT) through the **Process Video Transcripts Weekly** workflow:

**What happens automatically:**

1. **Video Discovery** - Scans YouTube channels for new educational content
2. **Transcript Generation** - Creates text transcripts from videos using YouTube API and Whisper
3. **Text Processing** - Chunks transcripts into searchable segments (250 words with 50-word overlap)
4. **Repository Update** - Commits new transcripts and processed data to the repository
5. **Deployment Trigger** - Automatically triggers HuggingFace Space deployment
6. **Vector Store Rebuild** - HuggingFace rebuilds the FAISS vector database during Docker build

**Processing Pipeline:**
```
GitHub Actions:                           HuggingFace Spaces:
┌─────────────────────┐                  ┌──────────────────────┐
│ 1. Video Discovery  │                  │ 5. Docker Build      │
│ 2. Transcripts      │  ───(push)───>   │ 6. Vector Store      │
│ 3. Text Processing  │                  │ 7. Deploy App        │
│ 4. Commit & Push    │                  └──────────────────────┘
└─────────────────────┘
```

### Manual Workflow Triggering

You can manually trigger the knowledge base update at any time:

**Via GitHub Web Interface:**
1. Navigate to the **Actions** tab in the GitHub repository
2. Select **"Process Video Transcripts Weekly"** workflow
3. Click **"Run workflow"** button
4. Choose the branch (usually `main`)
5. Click **"Run workflow"** to start

**Via GitHub CLI:**
```bash
gh workflow run "Process Video Transcripts Weekly"
```

### Local Knowledge Base Rebuild

To rebuild the vector store locally (for development or testing):

```bash
# Rebuild the entire vector store from processed transcripts
python rebuild_vector_store.py

# Or use the create script directly
python create_vector_store.py
```

**Note:** The vector store files (`vector_store/`) are large and should not be committed to the repository. They are rebuilt automatically during deployment.

### Workflow Configuration

The automated pipeline is configured in `.github/workflows/process-transcripts.yml`:

**Key Settings:**
- **Schedule:** Weekly on Sunday at 20:00 UTC
- **Timeout:** 180 minutes (3 hours) for large processing jobs
- **Python Version:** 3.10
- **Dependencies:** FFmpeg (for audio processing), PyTorch, Sentence-Transformers

**Required Secrets:**
- `YOUTUBE_API_KEY` - For accessing YouTube API to fetch video metadata and transcripts
- `HF_TOKEN` - For deploying to HuggingFace Spaces

### Deployment Pipeline

After transcripts are processed, the **Deploy to Hugging Face Space** workflow automatically:

1. **Triggers On:**
   - Push to `main` branch
   - Manual trigger via workflow dispatch
   - Automatic trigger after transcript updates

2. **Deployment Steps:**
   - Checks out the latest code
   - Creates Docker startup script
   - Pushes to HuggingFace Space repository
   - HuggingFace rebuilds Docker image
   - Vector store is created during image build
   - Application is automatically redeployed

3. **Result:**
   - New transcripts are searchable within minutes
   - Zero-downtime deployment
   - Automatic rollback on failure

### Monitoring Updates

**Check Processing Status:**
- View workflow runs in the GitHub Actions tab
- Each run generates a processing report showing:
  - Number of videos discovered
  - Transcripts generated
  - Processed chunks created
  - Deployment status

**Verify Deployment:**
- Check HuggingFace Space build logs
- Test the `/api/health` endpoint
- Run a sample query to verify new content is searchable

### Adding New Video Sources

To add new YouTube channels or playlists to the discovery process:

1. Update the scraper configuration in the pipeline scripts
2. The next automated run will discover videos from the new sources
3. Or manually trigger the workflow to process immediately

### Adding Research Papers (PDFs)

To add academic papers or PDF documents to the knowledge base:

1. **Prepare PDFs**: Place PDF files in a local directory (e.g., `~/research-papers/`)

2. **Process PDFs locally**:
   ```bash
   # Process PDFs with semantic chunking
   python process_pdfs.py ~/research-papers/
   
   # Analyze first without processing (preview)
   python process_pdfs.py ~/research-papers/ --analyze-only
   ```

3. **Commit processed chunks**:
   ```bash
   git add processed_pdfs/
   git commit -m "Add research papers: [description]"
   git push
   ```

4. **Automatic deployment**: The push triggers HuggingFace rebuild with new papers

**PDF Processing Features:**
- **Semantic chunking**: Preserves paragraph boundaries and section context
- **Section detection**: Identifies headers and includes section names in metadata
- **Page tracking**: Each chunk includes page number and range
- **Author extraction**: Extracts author metadata when available
- **Lightweight storage**: Raw PDFs stay local, only JSON chunks are committed (~95% smaller)

**Note:** Raw PDF files are not committed to the repository (see `.gitignore`). Only the processed JSON chunks in `processed_pdfs/` are stored in Git.

### Troubleshooting

**If automated updates fail:**

1. **Check GitHub Actions logs** - View detailed error messages in the workflow run
2. **Verify secrets** - Ensure `YOUTUBE_API_KEY` and `HF_TOKEN` are valid
3. **Check API quotas** - YouTube API has daily limits
4. **Manual rebuild** - Trigger the workflow manually if the scheduled run missed
5. **Local testing** - Run the pipeline locally to debug issues

**Common Issues:**
- **YouTube API quota exceeded** - Wait for quota reset (midnight Pacific Time)
- **Transcripts not available** - Some videos may not have captions enabled
- **Long processing times** - Large batches may take 1-2 hours

## Docker Integration

The project includes comprehensive Docker support:

- **Dockerfile**: Production-ready Docker image
- **docker-compose.yml**: Multi-service orchestration
- **docker-compose.dev.yml**: Development configuration

### Environment Variables

```bash
PORT=7860                    # Application port
PYTHONPATH=/app              # Python module path
TEST_MODE=false              # Enable test mode (no RAG initialization)
```

## Discord Bot

The project includes a Discord bot integration in the `discord/` directory. The bot provides the same semantic search capabilities directly in Discord channels.

See `discord/README.md` for setup instructions.

## Additional Documentation

- `docs/BEGINNER_GUIDE.md` - Getting started guide
- `docs/DEPLOYMENT_STEPS.md` - Deployment instructions
- `docs/HUGGINGFACE_SETUP.md` - HuggingFace Spaces setup
- `discord/README.md` - Discord bot setup

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure everything works
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped build this project
- Built with open-source technologies and libraries
- Educational content from various options trading educators

## Contact & Support

- **Issues**: Please use [GitHub Issues](https://github.com/bthaile/opteee/issues) for bug reports and feature requests
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/bthaile/opteee/discussions)

---

**Note**: This is an educational tool. Always do your own research and consult with financial professionals before making trading decisions.
