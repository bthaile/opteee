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
MARKER_VENV="${REPO_DIR}/.venv-marker"
MARKER_REQUIREMENTS="${REPO_DIR}/requirements-marker.txt"
MARKER_CHECK_SCRIPT="${REPO_DIR}/scripts/check_marker_env.py"
MARKER_SMOKE_PDF="${REPO_DIR}/tests/fixtures/marker_smoke.pdf"
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
[[ -f "${MARKER_REQUIREMENTS}" ]] || { echo "marker requirements missing at ${MARKER_REQUIREMENTS}"; exit 1; }
[[ -f "${MARKER_CHECK_SCRIPT}" ]] || { echo "marker checker missing at ${MARKER_CHECK_SCRIPT}"; exit 1; }
[[ -f "${MARKER_SMOKE_PDF}" ]] || { echo "marker smoke PDF missing at ${MARKER_SMOKE_PDF}"; exit 1; }

find_marker_python() {
  local candidate
  for candidate in \
    /Users/bradfordhaile/.local/bin/python3.11 \
    /opt/homebrew/bin/python3.11 \
    /opt/homebrew/bin/python3.12 \
    /opt/homebrew/bin/python3.13 \
    /opt/homebrew/bin/python3.14 \
    /usr/bin/python3; do
    [[ -x "$candidate" ]] && { echo "$candidate"; return 0; }
  done
  return 1
}

ensure_marker_env() {
  local marker_python

  if [[ ! -x "${MARKER_VENV}/bin/python" ]]; then
    echo "Bootstrapping dedicated Marker venv at ${MARKER_VENV}"
    marker_python="$(find_marker_python)" || { echo "No usable Python interpreter found for Marker venv"; exit 1; }
    rm -rf "${MARKER_VENV}"
    if command -v uv >/dev/null 2>&1; then
      uv venv --seed --python "$marker_python" "${MARKER_VENV}"
    else
      "$marker_python" -m venv "${MARKER_VENV}"
      "${MARKER_VENV}/bin/python" -m ensurepip --upgrade
    fi
  fi

  echo "Refreshing dedicated Marker venv dependencies"
  "${MARKER_VENV}/bin/python" -m pip install -q -r "${MARKER_REQUIREMENTS}"
  echo "Verifying dedicated Marker venv"
  "${MARKER_VENV}/bin/python" "${MARKER_CHECK_SCRIPT}" --smoke-pdf "${MARKER_SMOKE_PDF}"
}

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

ensure_marker_env

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
    # Give the native service a little extra time to settle after the first healthy response.
    echo "Waiting 3 minutes before post-refresh smoke test"
    sleep 180
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
