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
- **Persistent Conversation History**: Full user/assistant threads stored in SQL (Postgres recommended)
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
- **Deployment**: Docker containerization with resource-limited local serving

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Docker (optional, for containerized deployment)
- Git

### Docker (Recommended)

1. **Clone the repository**:
```bash
git clone https://github.com/bthaile/opteee.git
cd opteee
```

2. **Create your `.env` file**:
```bash
cp .env.example .env
# Edit .env with your API key(s)
```

3. **Build and run**:
```bash
docker compose up --build
```

The application will be available at `http://localhost:7860`

The Docker setup uses `Dockerfile.serve` — a slim image with CPU-only PyTorch, no Whisper/Selenium overhead, and mounts the pre-built vector store as a volume. Resource limits (2GB RAM, 2 CPUs) are configured in `docker-compose.yml`.

### Local Development (Without Docker)

```bash
pip install -r requirements-serve.txt
python main.py
```

Use `requirements-serve.txt` for serving only. The full `requirements.txt` includes pipeline dependencies (Whisper, YouTube downloaders) needed for transcript processing.

## API Documentation

### Endpoints

- **GET `/api/health`** - Health check endpoint
  - Returns service status and version information

- **POST `/api/chat`** - Main chat endpoint
  - Request body:
    ```json
    {
      "query": "What is a covered call?",
      "provider": "claude",
      "num_results": 5,
      "format": "html",
      "conversation_history": [],
      "conversation_id": "optional-existing-conversation-id"
    }
    ```
  - Returns answer with sources, timestamps, and `conversation_id`

- **POST `/api/conversations`** - Create a new persisted conversation
  - Returns conversation metadata (`id`, `title`, timestamps)

- **GET `/api/conversations?limit=25`** - List recent conversations
  - Returns newest-first conversation summaries for sidebar/history UIs

- **GET `/api/conversations/{conversation_id}`** - Load one conversation with full message history
  - Returns all persisted `user` and `assistant` messages for replay/rebuild

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
│   ├── db/                      # SQLAlchemy engine, models, and DB init
│   ├── models/                  # Pydantic models
│   │   └── chat_models.py       # Chat request/response models (supports video + PDF)
│   └── services/                # Business logic services
│       ├── rag_service.py       # RAG service implementation
│       ├── conversation_service.py # Conversation/message persistence service
│       ├── history_utils.py     # History sanitization for prompt context
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
├── Dockerfile                   # Production Docker image (full pipeline)
├── Dockerfile.serve             # Slim Docker image (serving only, CPU-only PyTorch)
├── docker-compose.yml           # Local Docker serving with resource limits
├── requirements.txt             # Full dependencies (pipeline + serving)
├── requirements-serve.txt       # Slim dependencies (serving only)
└── tests/                       # Unit tests for persistence and history logic
```

## Key Technologies

- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance Python web framework
- **[React](https://reactjs.org/)** - Modern frontend JavaScript library
- **[Sentence Transformers](https://www.sbert.net/)** - State-of-the-art sentence embeddings
- **[FAISS](https://github.com/facebookresearch/faiss)** - Efficient similarity search and clustering
- **[Docker](https://www.docker.com/)** - Containerization platform
- **[LangChain](https://www.langchain.com/)** - LLM orchestration and RAG pipeline

## Development Workflow

1. **Backend Changes**: Modify FastAPI endpoints in `main.py` or services in `app/services/`
2. **Frontend Changes**: Update React components in `frontend/src/` (requires separate build)
3. **Testing**: Run locally with `python main.py`
4. **Vector Store Updates**: Rebuild with `python rebuild_vector_store.py`
5. **Deploy**: `docker compose up --build`

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

After the weekly pipeline commits new transcripts, rebuild the vector store locally to make new content searchable:

```bash
python rebuild_vector_store.py
docker compose up --build
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

### Monitoring Updates

**Check Processing Status:**
- View workflow runs in the GitHub Actions tab
- Each run generates a processing report showing:
  - Number of videos discovered
  - Transcripts generated
  - Processed chunks created

**Verify Locally:**
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

4. **Rebuild vector store**: `python rebuild_vector_store.py && docker compose up --build`

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
2. **Verify secrets** - Ensure `YOUTUBE_API_KEY` is valid
3. **Check API quotas** - YouTube API has daily limits
4. **Manual rebuild** - Trigger the workflow manually if the scheduled run missed
5. **Local testing** - Run the pipeline locally to debug issues

**Common Issues:**
- **YouTube API quota exceeded** - Wait for quota reset (midnight Pacific Time)
- **Transcripts not available** - Some videos may not have captions enabled
- **Long processing times** - Large batches may take 1-2 hours

## Docker Setup

Two Dockerfiles are provided:

- **`Dockerfile.serve`** (default in docker-compose) - Slim image for serving: CPU-only PyTorch, no Whisper/Selenium, mounts pre-built vector store
- **`Dockerfile`** - Full image for production: includes vector store build step, all pipeline dependencies

### Environment Variables

```bash
# .env file (see .env.example)
CLAUDE_API_KEY=...           # Anthropic API key (at least one LLM key required)
OPENAI_API_KEY=...           # OpenAI API key (optional)
DATABASE_URL=...             # Optional; enables persisted conversation history (Postgres recommended)
```

For Docker + host Postgres on macOS, use:

```bash
DATABASE_URL=postgresql+psycopg://postgres:postgres@host.docker.internal:5432/opteee
```

Notes:
- If `DATABASE_URL` is not set, OPTEEE falls back to local SQLite (`opteee.db`).
- Conversation tables are created automatically on app startup.

### Resource Limits

Docker Compose is configured with sensible limits for local development:
- **Memory:** 2GB
- **CPUs:** 2

## Local Auto-Refresh (macOS launchd)

Use this when running OPTEEE locally with Docker and you want an automatic weekly refresh that:
1. Pulls latest changes from GitHub
2. Rebuilds/restarts the Docker service
3. Verifies `/api/health` on port `7860`

### Files to keep in this repo

- `weekly-refresh.sh` - refresh script used by launchd
- `com.opteee.weekly-refresh.plist` - launchd job definition (template tracked in git)

### One-time setup

```bash
cd /Users/bradfordhaile/clawd/opteee
mkdir -p logs
chmod +x weekly-refresh.sh
cp com.opteee.weekly-refresh.plist ~/Library/LaunchAgents/com.opteee.weekly-refresh.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.opteee.weekly-refresh.plist
launchctl enable gui/$(id -u)/com.opteee.weekly-refresh
```

### Schedule

The tracked plist is configured to run every Sunday at 11:00 PM local time:
- `Weekday=0` (Sunday)
- `Hour=23`
- `Minute=0`

### Useful operations

```bash
# Run immediately (manual test)
launchctl kickstart -k gui/$(id -u)/com.opteee.weekly-refresh

# Check status
launchctl print gui/$(id -u)/com.opteee.weekly-refresh

# Disable/enable
launchctl disable gui/$(id -u)/com.opteee.weekly-refresh
launchctl enable gui/$(id -u)/com.opteee.weekly-refresh

# Reload after plist edits
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.opteee.weekly-refresh.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.opteee.weekly-refresh.plist
```

### Logs

Launchd output logs are written to:
- `logs/weekly-refresh.out.log`
- `logs/weekly-refresh.err.log`

### Notes

- The script skips `git pull` if your repo has uncommitted changes to avoid clobbering local edits.
- Keep Docker Desktop running so scheduled refresh jobs can rebuild/restart successfully.

## Discord Bot

The project includes a Discord bot integration in the `discord/` directory. The bot provides the same semantic search capabilities directly in Discord channels.

See `discord/README.md` for setup instructions.

## Additional Documentation

- `docs/BEGINNER_GUIDE.md` - Getting started guide
- `docs/DEPLOYMENT_STEPS.md` - Deployment instructions
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
