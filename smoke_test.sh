#!/usr/bin/env bash
# OPTEEE wiki + RAG-bridge smoke test — run after every weekly refresh.
# Uses the serve venv (.venv-native) so it can import the retriever and hit the live app.
#
#   ./smoke_test.sh                # full run (needs the app running on :7860)
#   ./smoke_test.sh --with-chat    # also do one live /api/chat query
#   ./smoke_test.sh --no-api       # offline checks only
set -uo pipefail
cd "$(dirname "$0")"
PY=".venv-native/bin/python"
[ -x "$PY" ] || PY="venv/bin/python"
exec "$PY" scripts/smoke_test.py "$@"
