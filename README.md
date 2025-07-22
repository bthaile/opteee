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

# Options Trading Knowledge Search

A modern web application providing semantic search across a collection of options trading transcripts and videos. Built with FastAPI backend and React frontend for optimal performance and user experience.

## Architecture

- **Backend**: FastAPI with RESTful API endpoints
- **Frontend**: React with modern UI components
- **Search Engine**: Sentence-transformers with FAISS vector database
- **Deployment**: Docker containerization for HuggingFace Spaces

## Features

- **Semantic Search**: Advanced natural language search using sentence-transformers
- **Fast Retrieval**: FAISS vector database for millisecond search responses
- **Video Integration**: Direct links to specific timestamps in relevant YouTube videos
- **Chat Interface**: Modern chat UI with conversation history
- **Prompt History**: Sidebar with recent queries for easy re-use
- **Source Citations**: Clickable video references with timestamps
- **Responsive Design**: Works on desktop and mobile devices

## API Endpoints

- `GET /api/health` - Health check endpoint
- `POST /api/chat` - Main chat endpoint accepting queries and returning answers with sources
- `GET /` - Serves the React frontend application

## Local Development

### Prerequisites

- Python 3.9+
- Docker (for containerized deployment)
- Git

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd opteee
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file with necessary API keys and configuration
cp .env.example .env
```

4. Run the development server:
```bash
python main.py
```

The application will be available at `http://localhost:7860`

### Docker Development

For local Docker testing that matches the production environment:

```bash
# Build and run with Docker
./run_local.sh
```

This script:
- Stops any existing containers
- Builds a fresh Docker image
- Runs the container with environment variables

## Production Deployment

### HuggingFace Spaces

The application is configured for automatic deployment to HuggingFace Spaces via GitHub Actions:

1. **Automatic Deployment**: Pushes to `main` branch trigger deployment
2. **Manual Deployment**: Use GitHub Actions "Deploy to Hugging Face Space" workflow
3. **Docker Build**: Production builds include both backend and frontend assets

### Local Production Testing

To test the full production build locally:

```bash
# Prepare production files
python prepare_production_files.py

# Build and test with Docker
./run_local.sh
```

## Project Structure

```
opteee/
├── main.py                 # FastAPI application entry point
├── api/                    # API route handlers
├── services/              # Business logic (RAG pipeline, vector search)
├── models/                # Pydantic models for API
├── frontend/              # React frontend source
│   ├── build/            # Production build files
│   └── src/              # React components and styles
├── vector_store/          # FAISS vector database
├── transcripts/           # Processed video transcripts
├── audio_files_processed/ # Audio processing cache
└── docker-compose.yml     # Container orchestration
```

## Key Technologies

- **FastAPI**: High-performance Python web framework
- **React**: Modern frontend JavaScript library
- **Sentence Transformers**: Semantic embedding models
- **FAISS**: Efficient similarity search library
- **Docker**: Containerization platform
- **GitHub Actions**: CI/CD pipeline
- **HuggingFace Spaces**: Deployment platform

## Development Workflow

1. **Backend Changes**: Modify API endpoints in `api/` or services in `services/`
2. **Frontend Changes**: Update React components in `frontend/src/`
3. **Testing**: Run locally with `python main.py` or `./run_local.sh`
4. **Production Prep**: Run `python prepare_production_files.py` before deployment
5. **Deploy**: Push to `main` branch for automatic HuggingFace deployment

## HuggingFace Deployment Notes

### DNS Resolution Issues
HuggingFace Spaces environments often experience DNS resolution problems that can affect network connections. This project includes several strategies to handle these issues:

#### Main Application
- **Robust Error Handling**: API endpoints include comprehensive error handling for network failures
- **Timeout Configuration**: Proper timeouts configured for all external requests
- **Health Checks**: `/api/health` endpoint for monitoring service availability

#### Discord Bot (Special Considerations)
The Discord bot requires more complex DNS handling due to HuggingFace DNS limitations:

- **Custom DNS Resolver**: Uses Google DNS (8.8.8.8) and Cloudflare DNS (1.1.1.1) as fallbacks
- **Selective Patching**: Custom DNS resolver applied only to Discord.py connections
- **Isolated API Sessions**: API calls use clean sessions isolated from DNS patches
- **Dual-Mode Operation**: 
  - Discord connections: Custom DNS resolver (bypasses HF DNS issues)
  - API calls: Standard sessions (avoids "Session is closed" errors)

#### Environment Variables
```bash
# Discord bot DNS configuration
ENABLE_CUSTOM_DNS=true  # Enable custom DNS resolver (default: true)
```

#### Troubleshooting DNS Issues
If you encounter DNS-related errors:

1. **Check logs** for DNS resolution failures
2. **Monitor health endpoint** at `/api/health` 
3. **For Discord bot**: Set `ENABLE_CUSTOM_DNS=false` to disable custom DNS if causing issues
4. **Network issues**: HuggingFace DNS problems typically resolve automatically after 1-5 minutes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with Docker
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
