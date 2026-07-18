# OPTEEE - Options Trading Education Expert

OPTEEE is a semantic search and chat app for options-trading education. It serves a FastAPI backend plus a browser chat UI over a curated knowledge base of transcripts and research documents.

## Current runtime model

**OPTEEE runs natively on macOS via launchd.**

Production ownership is:
- App service: `com.opteee.native`
- Weekly refresh job: `com.opteee.weekly-refresh`
- Service port: `7860`
- App root: `/Users/bradfordhaile/clawd/opteee`

See [`DEPLOYMENT.md`](DEPLOYMENT.md) for the canonical operations guide.

## Features

- Semantic search over transcripts and PDFs
- FastAPI API with persisted conversation history
- Browser chat UI served from the same app
- Timestamped video citations and page-aware document citations
- Local vector search with FAISS + sentence transformers
- Native macOS service ownership via launchd

## Architecture

- Backend: FastAPI
- Frontend: static browser UI served by FastAPI
- Search: sentence-transformers + FAISS
- Storage: Postgres recommended; SQLite fallback for local-only use
- Native runtime: `.venv-native` + launchd
- Pipeline runtime: `venv` for transcript + vector-store work
- Dedicated Marker runtime: `.venv-marker` for reliable PDF OCR/extraction

## Key paths

- App entrypoint: `main.py`
- Native launcher: `start_native.sh`
- Weekly refresh script: `weekly-refresh.sh`
- Launchd template: `com.opteee.weekly-refresh.plist`
- Native service logs:
  - `logs/native.out.log`
  - `logs/native.err.log`
- Weekly refresh logs:
  - `logs/weekly-refresh.out.log`
  - `logs/weekly-refresh.err.log`

## Python environments

OPTEEE intentionally uses three environments:

### 1. Native serving environment
Used by the live macOS service.

- Path: `.venv-native/`
- Purpose: run `main.py` as the production app
- Dependency file: `requirements-serve.txt`

### 2. Pipeline/development environment
Used for transcript ingestion, Whisper, preprocessing, and vector rebuilds.

- Path: `venv/`
- Purpose: local development and content pipeline work
- Dependency file: `requirements.txt`

### 3. Dedicated Marker environment
Used only for Marker OCR/extraction so the PDF stack can stay on a proven Python 3.11 dependency set.

- Path: `.venv-marker/`
- Purpose: direct Marker extraction invoked by the routed PDF processor
- Dependency file: `requirements-marker.txt`
- Verification command: `./.venv-marker/bin/python scripts/check_marker_env.py --smoke-pdf tests/fixtures/marker_smoke.pdf`

## Quick start

### Local app run (non-launchd)

```bash
cd /Users/bradfordhaile/clawd/opteee
python3.13 -m venv .venv-native
source .venv-native/bin/activate
pip install -r requirements-serve.txt
python main.py
```

App will be available at:
- `http://127.0.0.1:7860`
- health: `http://127.0.0.1:7860/api/health`

### Local pipeline environment

```bash
cd /Users/bradfordhaile/clawd/opteee
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## API overview

### `GET /api/health`
Returns service health and version.

### `POST /api/chat`
Main chat endpoint.

Example:

```json
{
  "query": "What is a covered call?",
  "provider": "claude",
  "num_results": 5,
  "format": "json"
}
```

For agents/bots, use `format: "json"` or `format: "bot"`. Responses include `wiki_references` when retrieved sources map to synthesized wiki pages.

### LLM Wiki endpoints

The wiki API exposes the compiled education layer as REST data for other web apps and AI agents.

- `GET /api/wiki/index/document` - generated wiki index as `{path, frontmatter, markdown, wikilinks}`. Agent entrypoint.
- `GET /api/wiki/pages/{path}?format=json` - one wiki page as `{path, frontmatter, markdown, html, wikilinks}`.
- `GET /api/wiki/graph.json` - graph data with `nodes[]` and labeled `edges[]`.
- `GET /api/wiki/index` - lightweight page/source catalog for browse/search.

Typical agent flow: call `/api/chat` with `format: "json"`, inspect `wiki_references`, fetch referenced pages via `/api/wiki/pages/{path}?format=json`, and use `/api/wiki/index/document` plus `/api/wiki/graph.json` for broader analysis.

### Web App Integration

Web apps use the same wiki REST endpoints, but usually consume the browser-oriented forms:

- `GET /api/wiki/graph.json` to render an interactive graph or relationship map.
- `GET /api/wiki/index` to build search, catalog drawers, filters, and page lists.
- `GET /api/wiki/pages/{path}` to fetch one rendered page as JSON with `frontmatter`, `html`, and structured `wikilinks`.
- `GET /api/wiki/pages/{path}?format=json` if the app also needs raw Markdown.
- `GET /wiki/page/{path}` for direct links, new tabs, or iframe-style standalone page views.

Typical web-app flow:

1. Fetch `graph.json` and `index` on startup.
2. Render graph nodes from `nodes[]`; render relationships from `edges[]`.
3. When a user selects a node, call `/api/wiki/pages/{node.id}`.
4. Insert the returned `html` into your page detail panel.
5. Intercept links in that HTML with `a[data-page]` and fetch the next page through the same endpoint.

Minimal browser example:

```js
const API = "http://127.0.0.1:7860";

async function loadWikiShell() {
  const [graph, catalog] = await Promise.all([
    fetch(`${API}/api/wiki/graph.json`).then(r => r.json()),
    fetch(`${API}/api/wiki/index`).then(r => r.json()),
  ]);
  return { graph, catalog };
}

async function loadWikiPage(path) {
  const page = await fetch(`${API}/api/wiki/pages/${encodeURI(path)}`).then(r => r.json());
  document.querySelector("#wiki-title").textContent =
    page.frontmatter?.title || page.path;
  document.querySelector("#wiki-body").innerHTML = page.html;
}

function wireWikiLinks() {
  document.querySelector("#wiki-body").addEventListener("click", event => {
    const link = event.target.closest("a[data-page]");
    if (!link) return;
    event.preventDefault();
    loadWikiPage(link.dataset.page);
  });
}
```

The local API currently allows cross-origin browser requests for development. If this is exposed beyond your LAN, restrict CORS origins in `main.py`.

### `GET /api/conversations?limit=25`
Lists recent conversations.

### `GET /api/conversations/{conversation_id}`
Loads a persisted conversation.

## Weekly refresh ownership

There is exactly **one** supported weekly refresh path:

- scheduler: system LaunchDaemon `com.opteee.weekly-refresh`
- plist: `/Library/LaunchDaemons/com.opteee.weekly-refresh.plist`
- tracked template: `./com.opteee.weekly-refresh.plist`
- script: `./weekly-refresh.sh`

The weekly refresh script:
1. pulls latest Git changes with `--autostash` so tracked generated artifacts do not block code updates,
2. bootstraps/refreshes the dedicated `.venv-marker` from `requirements-marker.txt`,
3. verifies Marker with `scripts/check_marker_env.py --smoke-pdf tests/fixtures/marker_smoke.pdf`,
4. runs the transcript/content pipeline via `run_transcripts.sh`,
5. refreshes `requirements-serve.txt` into `.venv-native`,
6. restarts `com.opteee.native` indirectly by killing the running Python process,
7. waits for `http://127.0.0.1:7860/api/health` to pass,
8. stages refresh artifacts (`outlier_trading_videos*.json`, `transcripts/`, `processed_transcripts/`, `vector_store/`, `wiki/`), commits them when changed, and pushes the refresh commit to `origin/<current-branch>`.

## Transcript and vector-store workflow

The content pipeline is separate from the native service runtime.

### Run the full local pipeline

```bash
cd /Users/bradfordhaile/clawd/opteee
source venv/bin/activate
./run_transcripts.sh
```

That runs:
1. scrape new videos
2. fetch transcripts
3. Whisper fallback
4. preprocess transcript chunks
5. rebuild vectors

### Run individual steps

```bash
source venv/bin/activate
python3 run_pipeline.py --step scrape --non-interactive
python3 run_pipeline.py --step transcripts --non-interactive
python3 run_pipeline.py --step whisper --non-interactive
python3 run_pipeline.py --step preprocess --non-interactive
python3 run_pipeline.py --step vectors --non-interactive
```

### Rebuild vectors directly

```bash
source venv/bin/activate
python3 rebuild_vector_store.py
```

After pipeline or vector-store changes, refresh the running native app with:

```bash
/Users/bradfordhaile/clawd/opteee/weekly-refresh.sh
```

or wait for the scheduled `com.opteee.weekly-refresh` run.

## One-time launchd setup

```bash
cd /Users/bradfordhaile/clawd/opteee
chmod +x weekly-refresh.sh start_native.sh
sudo cp com.opteee.weekly-refresh.plist /Library/LaunchDaemons/com.opteee.weekly-refresh.plist
sudo launchctl bootstrap system /Library/LaunchDaemons/com.opteee.weekly-refresh.plist
sudo launchctl enable system/com.opteee.weekly-refresh
```

## Useful operations

```bash
# Check app health
curl -fsS http://127.0.0.1:7860/api/health

# Run weekly refresh now
sudo launchctl kickstart -k system/com.opteee.weekly-refresh

# Check refresh job status
launchctl print system/com.opteee.weekly-refresh

# Restart native app directly
sudo launchctl kickstart -k system/com.opteee.native
```

## Project structure

```text
opteee/
├── main.py
├── config.py
├── rag_pipeline.py
├── rebuild_vector_store.py
├── run_transcripts.sh
├── start_native.sh
├── weekly-refresh.sh
├── com.opteee.weekly-refresh.plist
├── app/
├── frontend/
├── static/
├── templates/
├── docs/
├── bots/
├── vector_store/
├── processed_transcripts/
├── processed_pdfs/
├── transcripts/
├── requirements.txt
├── requirements-serve.txt
└── tests/
```

## Relevant docs

- [`DEPLOYMENT.md`](DEPLOYMENT.md) — canonical runtime and operations guide
- `docs/BEGINNER_GUIDE.md` — getting started
- `bots/README.md` — bot integration guide
- `docs/BOT_INTEGRATION.md` — compatibility/redirect bot notes
- `docs/CHAT_CONVERSION_SOW.md` — historical UI chat conversion notes
- `docs/HIGHLIGHTING_FIX_SUMMARY.md` — highlighting feature notes

## Notes

- The native service expects `com.opteee.native` to be installed with `KeepAlive=true`.
- `weekly-refresh.sh` now uses `git pull --ff-only --autostash` and also owns the dedicated Marker stack bootstrap/verification path.
- `DATABASE_URL` for the native app should point at `127.0.0.1`, not a container hostname.
- Raw PDFs and downloaded audio are not meant to be committed; processed JSON artifacts are the durable searchable assets.

## License

MIT.
