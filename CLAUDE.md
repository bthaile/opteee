# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What OPTEEE is

OPTEEE (Options Trading Education Expert) is a RAG chat app over a curated knowledge base of options-trading YouTube transcripts (from the Outlier Trading channel) and research PDFs. A FastAPI backend serves a browser chat UI, does semantic retrieval over a local FAISS index, and answers via a pluggable LLM (Claude / OpenAI / Ollama), returning answers with timestamped video and page-aware document citations. It runs natively on macOS under launchd on port `7860`.

## Three Python environments (important)

This repo deliberately keeps three venvs with different dependency sets. Activate the right one or imports/commands will fail:

- **`.venv-native/`** — serving the live app. Deps: `requirements-serve.txt` (no Whisper/yt-dlp/PDF tooling). Used by launchd `com.opteee.native` via `start_native.sh`.
- **`venv/`** — the content pipeline (scrape, Whisper, preprocess, vector rebuild). Deps: `requirements.txt`. Bootstrapped/managed by `run_transcripts.sh`.
- **`.venv-marker/`** — dedicated Marker OCR/extraction runtime. Deps: `requirements-marker.txt`, pinned to the known-good Python 3.11 Marker stack. Bootstrapped/managed by `weekly-refresh.sh` and verified by `scripts/check_marker_env.py`.

## Common commands

```bash
# Run the app locally (serving env)
source .venv-native/bin/activate && python main.py   # http://127.0.0.1:7860

# Run API without RAG/vector store (fast, no model load) — for endpoint/DB tests
TEST_MODE=true python main.py

# Tests (unittest-based, runnable via pytest; from repo root)
python -m pytest tests/
python -m pytest tests/test_query_routing.py                       # one file
python -m pytest tests/test_query_routing.py -k test_chat_request_defaults_effort_to_low   # one test
python -m unittest tests.test_query_routing                        # unittest equivalent

# Content pipeline (pipeline env) — full run, or one step
source venv/bin/activate && ./run_transcripts.sh
python3 run_pipeline.py --step {scrape|transcripts|whisper|preprocess|vectors} --non-interactive
python3 rebuild_vector_store.py                                    # rebuild serving index only

# After a pipeline/vector change, refresh the running native app
./weekly-refresh.sh

# Verify the dedicated Marker runtime
./.venv-marker/bin/python scripts/check_marker_env.py --smoke-pdf tests/fixtures/marker_smoke.pdf
```

See `DEPLOYMENT.md` (canonical) for launchd operations; do not add alternate deploy paths.

## Architecture (request flow)

A `POST /api/chat` request flows: `main.py` (endpoint, CORS, conversation persistence) → `app/services/rag_service.py` `RAGService.process_query` → `rag_pipeline.py` (retrieval + LLM chains) → `app/services/formatters.py` (output shaping).

- **`RAGService`** (`app/services/rag_service.py`) is the orchestrator. It owns a single `CustomFAISSRetriever` and a cache of per-`(provider, model)` LangChain chains, and implements the **provider fallback loop**: it tries the resolved primary provider, then falls back to other available providers on timeout/error, with a special Ollama model-not-found (404) fallback path. Conversation history is injected by rewriting the query (`_run_rag_query_with_context`), not via a separate chain.
- **`rag_pipeline.py`** is the retrieval + LLM engine: `CustomFAISSRetriever` (embeds queries with `all-MiniLM-L6-v2`, searches FAISS, enriches hits from `outlier_trading_videos_metadata.json`), `create_rag_chain`, `run_rag_query`, `resolve_llm_selection` (provider/model/effort resolution), `get_available_providers`, and timeout wrapping (`invoke_chain_with_timeout` runs the chain in a thread with a hard timeout). This module is imported by the app but is also a standalone CLI.
- **Persistence**: `app/db/` (SQLAlchemy). `DATABASE_URL` defaults to `sqlite:///./opteee.db`; Postgres is preferred in production (`postgres://`/`postgresql://` URLs are auto-normalized to `postgresql+psycopg://`). `ConversationService` persists every user+assistant turn; when a `conversation_id` is supplied, server-side history is the source of truth (client-sent history is ignored).
- **Frontend**: served by FastAPI from `frontend/build/` if present; otherwise `main.py` serves an inline fallback page. `bots/` contains external bot-integration clients that hit the same API.

## The LLM Wiki (knowledge layer + RAG bridge)

A compounding, LLM-maintained knowledge layer over the corpus, alongside the RAG. Full design + hardening status: `docs/plans/2026-07-03-llm-wiki-design.md`; constitution: `schema/WIKI_SCHEMA.md`; slug registry: `schema/slugs.md`.

- **Layout.** `wiki/sources/{video_id}.md` = one auto-generated page per video (coverage, ~1139). `wiki/{concepts,strategies,securities,people,macro,syntheses}/` = curated synthesis pages (the *knowledge layer*). `wiki/graph.json` (knowledge nodes only) + `wiki/related_videos.json` (reverse map) are generated. Folders = knowledge; series/format/experts are frontmatter facets.
- **Build pipeline** (wired into `run_transcripts.sh`, **atomic + gated**): `ingest_wiki.py --new-only` (Haiku source-pass, incremental; bad pages → `wiki/_quarantine/`) → `normalize_frontmatter.py` (self-heals unquoted-colon titles) → `annotate_chunks.py` (**hard gate**) → `lint_wiki.py` (**hard gate** — aborts before reindex if the wiki is broken) → `vectors` (reindex) → `build_graph.py`. `weekly-refresh.sh` commits content + `wiki/` together; a lint failure keeps the previous known-good state. `--shard i/N` on ingest is for manual bulk backfill only.
- **RAG bridge (how wiki links reach chat).** `annotate_chunks.py` stamps `related_wiki_pages` onto each chunk in `processed_transcripts/*.json` (from each knowledge page's `related_videos`). `create_vector_store.py` bakes the **whole chunk dict** into FAISS metadata, so the retriever returns `related_wiki_pages` on `doc.metadata` → it surfaces in `/api/chat` as per-source `raw_sources[].related_wiki_pages` **and** a top-level **`wiki_references`** array (`{path,category,label,url}`). Both `format=html` and `format=json` include it. Only videos backing a knowledge page are "bridged" — refs grow as you add synthesis pages.
- **⚠️ Chat-UI render path (easy to get confused).** The browser chat UI is `frontend/build/index.html` — a **self-contained HTML with inline JS, no build step**. It builds its own source cards from `raw_sources` and **ignores the response's `sources` HTML string**. Chat-visible "Wiki References" therefore render from `data.wiki_references` via `generateWikiReferencesHTML()` in that file. To change the chat UI, **edit `frontend/build/index.html` directly** (served fresh via `FileResponse` — no rebuild, just hard-refresh the browser). The formatter (`formatters.py`) also embeds a Wiki References section in the `sources` HTML string for API consumers that render it, but the frontend does not use that string.
- **Browse/graph routes.** `GET /wiki` (interactive Cytoscape graph, vendored at `static/vendor/`, served `/assets/`; double-click a node to drill into its videos, search/filter by topic), `GET /wiki/page/<path>` (standalone page — target of chat ref links, opens new tab), `GET /api/wiki/{graph.json,index,pages/<path>}` (JSON).
- **Verify after any refresh:** `./smoke_test.sh` (add `--with-chat` for a live query). It checks coverage, the lint gate, **bridge freshness** (FAISS metadata matches the reverse map — catches a stale reindex), and all APIs. `weekly-refresh.sh` runs it automatically and logs to `logs/smoke-test.log`; `weekly-refresh.sh --dry-run` runs the whole ordering with no restart/commit/push.

## Non-obvious things to know

- **Two vector-store formats live in `vector_store/`.** The **serving path** (`CustomFAISSRetriever`) requires `transcript_index.faiss` + `transcript_texts.pkl` + `transcript_metadata.pkl`, produced by `create_vector_store.py` / `rebuild_vector_store.py`. The separate `vector_search.py` module uses a *different* format (`faiss.index` + `metadata.json`). Don't assume one implies the other; rebuild the serving format when changing retrieval. Missing serving files cause `CustomFAISSRetriever.__init__` to `sys.exit(1)`.
- **The system prompt is a hard contract** (`config.py` `SYSTEM_PROMPT`): the LLM is required to emit 3–5 *exact, character-for-character* quotes from sources. These quotes are string-matched and highlighted in the source cards — paraphrasing silently breaks highlighting. Preserve this behavior when editing prompt or formatting.
- **Provider/model selection** is env-driven and resolved in `resolve_llm_selection`. Effort is restricted to `low`/`medium`, mapped per-provider via `{OPENAI,CLAUDE,OLLAMA}_MODEL_{LOW,MEDIUM}` env vars. A provider is only "available" if its key is set (`OPENAI_API_KEY`, `CLAUDE_API_KEY`/`ANTHROPIC_API_KEY`) or `OLLAMA_BASE_URL` is set. Some models omit the `temperature` param (`MODELS_NO_TEMPERATURE`); extend that list rather than passing temperature blindly. See `.env.example` for the full knob set.
- **Two chunking configs exist and are not shared:** `config.py` (serving/retrieval: `CHUNK_SIZE=500`) vs `pipeline_config.py` (ingestion: `CHUNK_SIZE=250`). Edit the one for the layer you mean.
- **`config.py` path switching**: paths resolve to `/app/...` when running from the packaged/mounted `/app` layout, else local repo paths. Keep both branches working.
- **Weekly refresh** (`weekly-refresh.sh`, launchd `com.opteee.weekly-refresh`, Sun 23:00) runs the pipeline, refreshes `.venv-native`, bootstraps/refreshes the dedicated `.venv-marker` from `requirements-marker.txt`, verifies Marker with `scripts/check_marker_env.py --smoke-pdf tests/fixtures/marker_smoke.pdf`, restarts the app by killing its Python process (relies on `KeepAlive=true`), waits for health, then waits an additional 3 minutes before running the post-refresh smoke test (`logs/smoke-test.log`), and commits/pushes refreshed artifacts. It pulls with `--autostash` so tracked generated artifacts do not block code updates. `DATABASE_URL` for the native app must point at `127.0.0.1`.
- Committed durable assets are the processed JSON + vector store; raw PDFs and downloaded audio are not meant to be committed.
