#!/bin/zsh
set -euo pipefail

# OPTEEE weekly refresh for the native macOS deployment.
# Launchd owns the app lifecycle through com.opteee.native, so "redeploy" here
# means: pull code, refresh deps, and restart the daemon's Python process.
#
# Restart mechanism (no sudo): the daemon has KeepAlive=true and runs python as
# bradfordhaile. We kill that python; launchd respawns it with the fresh code/deps.
# (sudo launchctl kickstart would need root; kill + KeepAlive does not.)

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

REPO_DIR="/Users/bradfordhaile/clawd/opteee"
VENV="${REPO_DIR}/.venv-native"
PIPELINE_SCRIPT="${REPO_DIR}/run_transcripts.sh"
HEALTH_URL="http://127.0.0.1:7860/api/health"
LOCK_DIR="/tmp/opteee-weekly-refresh.lock"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting OPTEEE weekly refresh (native)"

if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
  echo "Another refresh is already running. Exiting."
  exit 0
fi
trap 'rmdir "${LOCK_DIR}" 2>/dev/null || true' EXIT

cd "${REPO_DIR}"

command -v git >/dev/null 2>&1 || { echo "git not found in PATH"; exit 1; }
[[ -x "${VENV}/bin/python" ]] || { echo "native venv missing at ${VENV}"; exit 1; }

# NOTE: this guard skips the pull whenever ANY tracked file is modified. The repo
# tracks generated data (transcripts/, processed_transcripts/, *.json) that the
# pipeline rewrites, so the worktree is often dirty and the pull gets skipped.
# To make weekly CODE updates land reliably, untrack that generated data
# (git rm --cached + .gitignore) or relax this check. See DEPLOYMENT.md.
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Git worktree is dirty; skipping git pull to avoid clobbering local edits."
else
  current_branch="$(git rev-parse --abbrev-ref HEAD)"
  echo "Pulling latest from origin/${current_branch}"
  git pull --ff-only origin "${current_branch}"
fi

# Refresh transcript-backed content before restarting the native service.
[[ -x "${PIPELINE_SCRIPT}" ]] || chmod +x "${PIPELINE_SCRIPT}"
echo "Running transcript/content refresh pipeline"
"${PIPELINE_SCRIPT}"

# Refresh Python deps in case requirements-serve.txt changed (idempotent; fast when satisfied)
echo "Refreshing native venv dependencies"
"${VENV}/bin/pip" install -q -r requirements-serve.txt || echo "pip refresh reported an issue (continuing)"

# Restart the native service: kill the running python; launchd KeepAlive respawns it.
echo "Restarting com.opteee.native (kill -> KeepAlive respawn)"
pkill -f "${VENV}/bin/python" || echo "no running opteee python matched (launchd will start it fresh)"

echo "Waiting for health endpoint"
for _ in {1..60}; do
  if curl -fsS "${HEALTH_URL}" >/dev/null 2>&1; then
    echo "Health check passed"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly refresh complete"
    exit 0
  fi
  sleep 2
done

echo "Health check FAILED after 120s — check logs/native.err.log"
exit 1
