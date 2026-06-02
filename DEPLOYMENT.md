# OPTEEE Deployment (Native — no Docker)

**As of 2026-06-02, opteee runs natively on macOS, NOT in Docker.**
It was migrated off Docker Desktop because Docker Desktop is a GUI app that requires
a logged-in desktop session — incompatible with running this Mac headless (no login).

## How it runs

- **Service:** LaunchDaemon `com.opteee.native` → `/Library/LaunchDaemons/com.opteee.native.plist`
  - Runs as user `bradfordhaile`, starts at boot, `KeepAlive=true` (auto-restarts on crash).
  - Survives headless (no GUI login required).
- **Launcher:** `start_native.sh` (in this repo) sets env and execs the venv python.
  - `PORT=7860`, binds `0.0.0.0` → reachable on LAN at **192.168.1.219:7860**.
  - `DATABASE_URL` → `postgresql+psycopg://postgres:postgres@127.0.0.1:5432/opteee`
    (native uses `127.0.0.1`, NOT the old Docker `host.docker.internal`).
  - Caches embedding model under `.cache-native/` (gitignored).
- **Runtime:** Python 3.11 venv `.venv-native/` (gitignored), deps from `requirements-serve.txt`
  + CPU-only torch (`pip install torch --index-url https://download.pytorch.org/whl/cpu`).
- **Data:** `vector_store/`, `processed_transcripts/`, `processed_pdfs/`, metadata JSON are read
  directly from this repo dir (in Docker they were read-only volume mounts).
- **LLM:** `LLM_PROVIDER=claude` (key in `.env`); fallback `openai`; `ollama` fallback points at
  a DIFFERENT host (`m1pro.home:11434`), NOT this machine. Local Ollama was removed — no impact.

## Weekly rebuild / redeploy

Scheduled by LaunchDaemon `com.opteee.weekly-refresh` (Sunday 23:00) → runs `weekly-refresh.sh`,
which: pulls code (if worktree clean) → `pip install -r requirements-serve.txt` → restarts the
service → health-checks `http://127.0.0.1:7860/api/health`.

**Restart works without sudo:** the script `pkill`s the running python; launchd's `KeepAlive`
respawns it with fresh code/deps.

### Manual redeploy
```bash
cd ~/clawd/opteee
git pull --ff-only           # if you have committed local changes
./.venv-native/bin/pip install -q -r requirements-serve.txt   # if deps changed
pkill -f "$HOME/clawd/opteee/.venv-native/bin/python"          # KeepAlive restarts it
curl -fsS http://127.0.0.1:7860/api/health                    # verify
```
Or force a clean restart via launchd (needs sudo): `sudo launchctl kickstart -k system/com.opteee.native`

### ⚠️ Weekly `git pull` gotcha
`weekly-refresh.sh` only pulls when `git status` is clean. This repo intentionally **tracks
generated transcript/data files** (see `.gitignore` lines ~49-53), so after the pipeline runs
the worktree is dirty and the pull is **skipped**. For weekly CODE updates to land, either:
- commit/push your data before the refresh runs (this machine is the repo's source of truth), or
- untrack the generated data (`git rm --cached` + add to `.gitignore`) so the worktree stays clean.

## If you ever rebuild the venv from scratch
```bash
cd ~/clawd/opteee
python3.11 -m venv .venv-native
./.venv-native/bin/pip install --upgrade pip setuptools wheel
./.venv-native/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
./.venv-native/bin/pip install -r requirements-serve.txt
```

## Rollback to Docker (if ever needed)
The `Dockerfile`, `Dockerfile.serve`, and `docker-compose.yml` are unchanged. To revert:
`sudo launchctl bootout system/com.opteee.native` then `docker compose up -d --build`.
(Docker Desktop must be running, which requires a GUI login.)
