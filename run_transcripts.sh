#!/usr/bin/env bash
# Run the transcript pipeline with a durable local venv. Ensures consistent Python
# environment even if the old interpreter path inside venv/ went stale.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

VENV_DIR="$SCRIPT_DIR/venv"

find_python() {
    local candidate
    for candidate in \
        /opt/homebrew/bin/python3.14 \
        /opt/homebrew/bin/python3.13 \
        /opt/homebrew/bin/python3.12 \
        /Users/bradfordhaile/.local/bin/python3.11 \
        /usr/bin/python3; do
        if [ -x "$candidate" ]; then
            echo "$candidate"
            return 0
        fi
    done
    return 1
}

if [ ! -x "$VENV_DIR/bin/python" ] || [ ! -x "$VENV_DIR/bin/pip" ]; then
    echo "Bootstrapping pipeline venv..."
    PYTHON_BIN="$(find_python)" || { echo "No usable Python interpreter found for pipeline venv"; exit 1; }
    rm -rf "$VENV_DIR"
    if command -v uv >/dev/null 2>&1; then
        uv venv --seed --python "$PYTHON_BIN" "$VENV_DIR"
    else
        "$PYTHON_BIN" -m venv "$VENV_DIR"
        "$VENV_DIR/bin/python" -m ensurepip --upgrade
    fi
fi

source "$VENV_DIR/bin/activate"

# Ensure full deps (Whisper, yt-dlp, etc.)
python -m pip install -q -r requirements.txt

echo "Running transcript pipeline (scrape → transcripts → whisper → preprocess → wiki → vectors)..."
python3 run_pipeline.py --step scrape --non-interactive
python3 run_pipeline.py --step transcripts --non-interactive
python3 retry_and_whisper.py
python3 run_pipeline.py --step preprocess --non-interactive

# --- LLM Wiki (see schema/WIKI_SCHEMA.md + docs/plans/2026-07-03-llm-wiki-design.md) ---
# ATOMIC PUBLISH CONTRACT (Hardening §15 #1, #6): annotate + lint are HARD GATES that
# run BEFORE vectors. If the wiki is inconsistent we abort the whole run *before*
# reindexing — so processed_transcripts/, vector_store/, and wiki/ are never published
# out of sync. On abort, weekly-refresh.sh also aborts and the previous known-good
# state is kept. ingest + normalize are soft (a transient Haiku failure retries next week).
echo "Wiki: incremental source-pass (new videos only, Haiku)..."
python3 scripts/ingest_wiki.py --new-only || echo "⚠️ wiki ingest reported issues (continuing without new source pages)"
echo "Wiki: normalizing frontmatter (self-heal LLM title-quoting quirk before the lint gate)..."
python3 scripts/normalize_frontmatter.py || echo "⚠️ frontmatter normalize reported issues (continuing)"
echo "Wiki: generating topic layer from the corpus (concepts/strategies/securities/interviews)..."
python3 scripts/build_topics.py || echo "⚠️ topic generation reported issues (continuing)"
echo "Wiki: syncing slug registry with corpus usage (keeps lint from blocking on new topics)..."
python3 scripts/sync_slugs.py || echo "⚠️ slug sync reported issues (continuing)"
echo "Wiki: extracting grounded topic relationships (incremental, Haiku; uses last graph.json)..."
python3 scripts/extract_relationships.py --new-only || echo "⚠️ relationship extraction reported issues (continuing)"
echo "Wiki: annotating chunks with related_wiki_pages (RAG bridge)..."
python3 scripts/annotate_chunks.py || { echo "❌ chunk annotation FAILED — aborting before vectors to avoid a stale bridge"; exit 1; }
echo "Wiki: lint gate (must pass before reindex — keeps the three artifacts consistent)..."
python3 scripts/lint_wiki.py || { echo "❌ wiki lint FAILED — aborting before vectors; previous known-good state is kept"; exit 1; }
# --------------------------------------------------------------------------------------

python3 run_pipeline.py --step vectors --non-interactive

echo "Wiki: rebuilding graph.json..."
python3 scripts/build_graph.py || { echo "❌ graph build FAILED — aborting to avoid stale wiki graph"; exit 1; }
echo "Wiki: rebuilding index.md from graph.json..."
python3 scripts/build_wiki_index.py || { echo "❌ graph index build FAILED — aborting to avoid stale wiki index"; exit 1; }

echo ""
echo "Done. Refresh the native app to pick up new content: ./weekly-refresh.sh"
