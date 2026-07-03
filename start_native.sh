#!/usr/bin/env bash
set -euo pipefail

# Native launcher for the OPTEEE Gradio/FastAPI service.
# Run by the com.opteee.native LaunchDaemon. Binds 0.0.0.0:7860 for LAN access.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV="$SCRIPT_DIR/.venv-native"
CACHE="$SCRIPT_DIR/.cache-native"

# App reads CLAUDE/OPENAI keys + LLM config from .env via python-dotenv (non-override).
# We export DATABASE_URL here so the native runtime always uses local Postgres on
# 127.0.0.1 regardless of any stale environment setting.
export PORT=7860
export DATABASE_URL='postgresql+psycopg://postgres:postgres@127.0.0.1:5432/opteee'
export PYTHONPATH="$SCRIPT_DIR"
export VECTOR_STORE_PREBUILT=true
export HF_HOME="$CACHE/hf"
export TRANSFORMERS_CACHE="$CACHE/hf"
export SENTENCE_TRANSFORMERS_HOME="$CACHE/st"

# Refuse to start if the port is already held by another process.
if lsof -nP -iTCP:7860 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port 7860 already in use by another process. Exiting." >&2
  exit 1
fi

exec "$VENV/bin/python" main.py
