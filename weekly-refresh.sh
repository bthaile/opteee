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
REFRESH_ARTIFACTS=(
  "outlier_trading_videos.json"
  "outlier_trading_videos_metadata.json"
  "transcripts"
  "processed_transcripts"
  "vector_store"
  "wiki"
)

# --dry-run: run the full pipeline ordering (ingest → normalize → annotate → lint →
# vectors → graph) and offline acceptance checks, but DO NOT restart production, commit,
# or push. (Hardening §15 #7.)
DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then DRY_RUN=1; echo "*** DRY RUN — no restart / commit / push ***"; fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting OPTEEE weekly refresh (native)"

if ! mkdir "${LOCK_DIR}" 2>/dev/null; then
  echo "Another refresh is already running. Exiting."
  exit 0
fi
trap 'rmdir "${LOCK_DIR}" 2>/dev/null || true' EXIT

cd "${REPO_DIR}"

command -v git >/dev/null 2>&1 || { echo "git not found in PATH"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "curl not found in PATH"; exit 1; }
[[ -x "${VENV}/bin/python" ]] || { echo "native venv missing at ${VENV}"; exit 1; }

commit_refresh_artifacts() {
  local current_branch refresh_commit_message

  current_branch="$(git rev-parse --abbrev-ref HEAD)"

  # Atomic publish (Hardening §15 #6): content + wiki/ commit TOGETHER. We only reach
  # here if run_transcripts.sh's lint gate already passed (it aborts the run otherwise),
  # so the three artifacts are guaranteed consistent — no partial/withheld wiki publish.
  echo "Staging refresh artifacts for commit"
  git add -A -- "${REFRESH_ARTIFACTS[@]}"

  if git diff --cached --quiet; then
    echo "No refresh artifact changes to commit"
    return 0
  fi

  refresh_commit_message="chore: refresh OPTEEE content $(date '+%Y-%m-%d %H:%M:%S')"
  echo "Committing refresh artifacts"
  git commit -m "${refresh_commit_message}"
  echo "Pushing refresh commit to origin/${current_branch}"
  git push origin "${current_branch}"
}

# Generated data (transcripts/, processed_transcripts/, vector_store/, wiki/) stays TRACKED
# — it is versioned + pushed each refresh. To keep CODE pulls reliable despite that dirty
# generated data, pull with --autostash instead of skipping the pull. (Hardening §15 #8.)
if [[ $DRY_RUN -eq 1 ]]; then
  echo "DRY RUN: skipping git pull"
else
  current_branch="$(git rev-parse --abbrev-ref HEAD)"
  echo "Pulling latest from origin/${current_branch} (autostash to survive dirty generated data)"
  git pull --ff-only --autostash origin "${current_branch}" || echo "⚠️ git pull failed (continuing with local code)"
fi

# Refresh transcript-backed content before restarting the native service.
[[ -x "${PIPELINE_SCRIPT}" ]] || chmod +x "${PIPELINE_SCRIPT}"
echo "Running transcript/content refresh pipeline"
"${PIPELINE_SCRIPT}"

# Refresh Python deps in case requirements-serve.txt changed (idempotent; fast when satisfied)
echo "Refreshing native venv dependencies"
"${VENV}/bin/pip" install -q -r requirements-serve.txt || echo "pip refresh reported an issue (continuing)"

# Dry-run stops here: validate the freshly-built artifacts offline, no restart/commit/push.
if [[ $DRY_RUN -eq 1 ]]; then
  echo "DRY RUN: skipping app restart, commit, and push"
  echo "DRY RUN: running offline acceptance checks (smoke_test.sh --no-api)"
  "${REPO_DIR}/smoke_test.sh" --no-api || echo "⚠️ dry-run acceptance checks reported failures"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] DRY RUN complete — nothing restarted/committed/pushed"
  exit 0
fi

# Restart the native service: kill the running python; launchd KeepAlive respawns it.
echo "Restarting com.opteee.native (kill -> KeepAlive respawn)"
pkill -f "${VENV}/bin/python" || echo "no running opteee python matched (launchd will start it fresh)"

echo "Waiting for health endpoint"
for _ in {1..60}; do
  if curl -fsS "${HEALTH_URL}" >/dev/null 2>&1; then
    echo "Health check passed"
    # Post-refresh acceptance checks (Hardening §15 #10) — informational, logged.
    echo "Running post-refresh smoke test (acceptance checks)"
    "${REPO_DIR}/smoke_test.sh" > "${REPO_DIR}/logs/smoke-test.log" 2>&1 \
      && echo "Smoke test: PASS (see logs/smoke-test.log)" \
      || echo "⚠️ Smoke test reported failures — see logs/smoke-test.log"
    commit_refresh_artifacts
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Weekly refresh complete"
    exit 0
  fi
  sleep 2
done

echo "Health check FAILED after 120s — check logs/native.err.log"
exit 1
