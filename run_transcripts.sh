#!/bin/bash
# Run the transcript pipeline with venv. Ensures consistent Python environment.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

if [ ! -d "venv" ]; then
    echo "Creating venv..."
    python3 -m venv venv
fi

source venv/bin/activate

# Ensure full deps (Whisper, yt-dlp, etc.)
pip install -q -r requirements.txt

echo "Running transcript pipeline (scrape → transcripts → whisper → preprocess → vectors)..."
python3 run_pipeline.py --step scrape --non-interactive
python3 run_pipeline.py --step transcripts --non-interactive
python3 retry_and_whisper.py
python3 run_pipeline.py --step preprocess --non-interactive
python3 run_pipeline.py --step vectors --non-interactive

echo ""
echo "Done. Restart Docker to use new content: docker compose up --build -d"
