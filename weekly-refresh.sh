#!/bin/zsh
set -euo pipefail

# launchd runs with a minimal environment; set PATH explicitly.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

REPO_DIR="/Users/bradfordhaile/clawd/opteee"
HEALTH_URL="http://127.0.0.1:7860/api/health"
LOCK_DIR="/tmp/opteee-weekly-refresh.lock"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting OPTEEE weekly refresh"

if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
  echo "Another refresh is already running. Exiting."
  exit 0
fi
trap 'rmdir "${LOCK_DIR}" 2>/dev/null || true' EXIT

cd "${REPO_DIR}"

if ! command -v git >/dev/null 2>&1; then
  echo "git not found in PATH"
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "docker not found in PATH"
  exit 1
fi

# Keep automation safe: only pull if worktree is clean.
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Git worktree is dirty; skipping git pull to avoid clobbering local edits."
else
  current_branch="$(git rev-parse --abbrev-ref HEAD)"
  echo "Pulling latest changes from origin/${current_branch}"
  git pull --ff-only origin "${current_branch}"
fi

echo "Rebuilding and restarting OPTEEE container"
docker compose up -d --build --remove-orphans

echo "Waiting for health endpoint"
for _ in {1..60}; do
  if curl -fsS "${HEALTH_URL}" >/dev/null 2>&1; then
    echo "Health check passed"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly refresh complete"
    exit 0
  fi
  sleep 2
done

echo "Health check failed after waiting 120 seconds"
exit 1
