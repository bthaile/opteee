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

- Python 3.13 (recommended; 3.14+ not yet supported by scipy/numba)
- Docker (optional, for containerized deployment)
- Git

### Python Environment (venv)

Use a virtual environment for all local Python work (serving, transcript pipeline, vector store rebuild):

```bash
cd opteee

# Create venv (once)
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-serve.txt   # Serving only
# OR
pip install -r requirements.txt         # Full (includes Whisper, pipeline)
```

**Always activate venv before running Python scripts:**
```bash
source venv/bin/activate
python3 main.py
python3 run_pipeline.py --step scrape
```

The `venv/` directory is in `.gitignore` and should not be committed.

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
source venv/bin/activate
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
  - `format` supports `html`, `json`, and `bot` (prefer `json` for chat bots)
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
├── run_transcripts.sh           # Transcript pipeline (venv + scrape→whisper→vectors)
├── process_pdfs.py              # PDF semantic chunking utility
├── app/
│   ├── db/                      # SQLAlchemy engine, models, and DB init
│   ├── models/                  # Pydantic models
│   │   └── chat_models.py       # Chat request/response models (supports video + PDF)
│   └── services/                # Business logic services
│       ├── rag_service.py       # RAG service implementation
│       ├── conversation_service.py # Conversation/message persistence service
│       ├── history_utils.py     # History sanitization for prompt context
│       └── formatters.py        # Response formatting (HTML + JSON/bot-friendly)
├── frontend/
│   └── build/                   # React production build
├── vector_store/                # FAISS vector database files
├── processed_transcripts/       # Processed video transcript chunks (JSON)
├── processed_pdfs/              # Processed PDF document chunks (JSON)
├── transcripts/                 # Raw transcript data
├── static/                      # Static assets (CSS, JS)
├── templates/                   # HTML templates
├── bots/                        # Platform-agnostic bot integration docs/examples
│   ├── README.md                # Canonical bot integration guide
│   └── examples/                # Minimal client examples
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
3. **Testing**: Run locally with `source venv/bin/activate && python main.py`
4. **Vector Store Updates**: Rebuild with `source venv/bin/activate && python rebuild_vector_store.py`
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
source venv/bin/activate
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

### Local Transcript Pipeline (with Whisper)

To run the full transcript pipeline locally—including Whisper for videos without YouTube captions:

**Prerequisites:**
- Python 3.13 (`brew install python@3.13` on macOS — Python 3.14 is not yet supported by scipy/numba)
- `ffmpeg` installed (`brew install ffmpeg` on macOS)
- venv created with Python 3.13: `python3.13 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- `YOUTUBE_API_KEY` in `.env` (for video discovery)

**Activate venv before running any pipeline step:**
```bash
source venv/bin/activate
```

**One-liner** (runs all steps in sequence):
```bash
./run_transcripts.sh
```

---

#### Step 1 — Discover new videos

Scans the configured YouTube channels (see `pipeline_config.py` → `CHANNEL_URLS`) and writes a list of all video IDs, titles, and metadata to `outlier_trading_videos.json`. Already-known videos are skipped on subsequent runs.

```bash
source venv/bin/activate
python3 run_pipeline.py --step scrape --non-interactive
```

What it does:
- Uses `yt-dlp` to enumerate every video across all channel URLs (videos, shorts, streams, podcasts, live)
- De-duplicates by video ID
- Saves results to `outlier_trading_videos.json`

---

#### Step 2 — Fetch transcripts via YouTube API

Attempts to pull captions directly from YouTube for every video in `outlier_trading_videos.json`. Videos where captions are unavailable are marked for Whisper processing.

```bash
source venv/bin/activate
python3 run_pipeline.py --step transcripts --non-interactive
```

What it does:
- Reads `outlier_trading_videos.json`
- Calls the `youtube-transcript-api` for each video
- Saves successful transcripts to `transcripts/<video_id>.txt` (one line per segment: `123.45s: text`)
- Records successes/failures in `transcript_progress.json`
- Skips videos already in `transcripts/` — only processes new ones

To force re-fetching everything:

```bash
python3 run_pipeline.py --step transcripts --non-interactive --force-reprocess
```

---

#### Step 3 — Whisper (second pass for failed videos)

For any video that YouTube couldn't provide captions for, this step downloads the audio track and runs OpenAI Whisper to generate a transcript locally. The pipeline captures failures in Step 2 and processes them here.

```bash
source venv/bin/activate
# Run as pipeline step (recommended — runs automatically after transcripts)
python3 run_pipeline.py --step whisper --non-interactive

# Or run retry_and_whisper directly for more control:
python3 retry_and_whisper.py --whisper-only   # Skip YouTube retry, go straight to Whisper
python3 retry_and_whisper.py                  # Retry YouTube first, then Whisper for rest
python3 retry_and_whisper.py --retry-only     # Only retry YouTube (no Whisper)
python3 retry_and_whisper.py --max-whisper 10 # Limit to N videos (for testing)
```

What it does under the hood:
1. **Audio download** — Uses `yt-dlp` + `ffmpeg` to pull the best available audio stream and convert it to a 128 kbps MP3, saved to `audio_files/<video_id>.mp3`
2. **Whisper transcription** — Loads the Whisper model (`WHISPER_MODEL` in `pipeline_config.py`, default `tiny`) and transcribes the audio, producing timestamped segments
3. Writes the result to `transcripts/<video_id>.txt` in the same `123.45s: text` format as YouTube transcripts
4. Updates `transcript_progress.json` (`whisper_processed` list)

**Whisper model options** (set `WHISPER_MODEL` in `pipeline_config.py`):

| Model | Speed | Accuracy | Notes |
|-------|-------|----------|-------|
| `tiny` | ~32× faster than base | ~90% | Default — good for large batches |
| `base` | baseline | ~95% | Good balance |
| `small` | ~2× slower than base | ~97% | Better for tricky audio |
| `medium` | ~5× slower | ~99% | High accuracy, slower |
| `large` | ~10× slower | Best | Use only when quality matters most |

**Note:** Audio files in `audio_files/` are not committed to the repository and can be deleted after transcription to save disk space.

---

#### Step 4 — Chunk transcripts for search

Converts raw transcript files into overlapping word-window chunks with full metadata (video URL, timestamp, title). This is what gets indexed into the vector store.

```bash
source venv/bin/activate
python3 run_pipeline.py --step preprocess --non-interactive

# Or run the preprocessor directly for more control:
python3 preprocess_transcripts.py                    # Process all new transcripts
python3 preprocess_transcripts.py --force            # Force reprocess everything
python3 preprocess_transcripts.py --video-id ABC123  # Process one specific video
```

What it does:
- Reads all `.txt` files from `transcripts/`
- Splits each into overlapping chunks (default: **250 words** per chunk, **50-word overlap** — configured in `pipeline_config.py`)
- Attaches metadata: `video_id`, `title`, `url`, `timestamp`, `upload_date`
- Outputs one JSON file per video to `processed_transcripts/<video_id>.json`
- Skips already-processed videos unless `--force` is passed

---

#### Step 5 — Build the vector store

Embeds all processed chunks using the sentence-transformer model and writes the FAISS index to `vector_store/`.

```bash
source venv/bin/activate
python3 run_pipeline.py --step vectors --non-interactive

# Or rebuild directly (also picks up processed PDFs):
python3 rebuild_vector_store.py
```

---

#### Step 6 — Restart the app

```bash
docker compose up --build -d
```

The vector store is mounted as a volume, so the container picks up the updated index without a full image rebuild. The `--build` flag ensures any code changes are included.

---

#### Full pipeline in one command

Run all five steps sequentially (scrape → transcripts → whisper → preprocess → vectors):

```bash
python3 run_pipeline.py --non-interactive
```

The Whisper step runs automatically after transcripts and processes any videos that couldn't get captions from YouTube.

---

**Note:** The GitHub Actions workflow uses YouTube transcripts only (no Whisper). Whisper is for local processing of videos without captions.

### Local Knowledge Base Rebuild

To rebuild the vector store locally (for development or testing):

```bash
source venv/bin/activate
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

4. **Rebuild vector store**: `source venv/bin/activate && python rebuild_vector_store.py && docker compose up --build`

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

### Restart and Rebuild

| Action | Command |
|--------|---------|
| **Stop containers** | `docker compose down` |
| **Stop and remove volumes** | `docker compose down -v` |
| **Build and start** | `docker compose up --build` |
| **Build and start (detached)** | `docker compose up --build -d` |
| **Clean rebuild** (no cache) | `docker compose build --no-cache && docker compose up -d` |
| **View logs** | `docker compose logs -f` |
| **View last 50 lines** | `docker compose logs --tail 50` |

**Typical workflow after code or config changes:**

```bash
# Stop current containers
docker compose down

# Rebuild and restart
docker compose up --build -d
```

**After vector store rebuild** (e.g. after `python rebuild_vector_store.py`):

```bash
docker compose up --build -d
```

The `--build` flag ensures the image is rebuilt with any code changes; the vector store is mounted as a volume, so a rebuild picks up updated `vector_store/` files without rebuilding the image.

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
- **macOS compatibility**: These `launchctl` commands use the modern `bootstrap`/`bootout` syntax (not legacy `load`/`unload`) and work on macOS Tahoe 26 and earlier.

## Bots

OPTEEE supports simple bot clients across platforms (Telegram, Slack, webhooks, custom chat apps).

Use `bots/README.md` as the canonical integration guide (includes conversation state support).

`bots/` is the only supported bot integration path.

## Additional Documentation

- `docs/BEGINNER_GUIDE.md` - Getting started guide
- `docs/DEPLOYMENT_STEPS.md` - Deployment instructions
- `bots/README.md` - Canonical bot integration guide (includes conversation support)
- `bots/examples/python_client.py` - Minimal Python bot client example
- `docs/BOT_INTEGRATION.md` - Redirect/compatibility bot guide

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
