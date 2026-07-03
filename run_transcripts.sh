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

echo "Running transcript pipeline (scrape → transcripts → whisper → preprocess → vectors)..."
python3 run_pipeline.py --step scrape --non-interactive
python3 run_pipeline.py --step transcripts --non-interactive
python3 retry_and_whisper.py
python3 run_pipeline.py --step preprocess --non-interactive
python3 run_pipeline.py --step vectors --non-interactive

echo ""
echo "Done. Refresh the native app to pick up new content: ./weekly-refresh.sh"
