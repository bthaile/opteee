# OPTEEE Deployment (Native macOS)

This file is the **canonical source of truth** for how OPTEEE runs in production.

## Production ownership

OPTEEE runs natively on macOS through **system launchd**.

### Live services
- App service: `com.opteee.native`
- Weekly refresh scheduler: `com.opteee.weekly-refresh`
- App port: `7860`
- App root: `/Users/bradfordhaile/clawd/opteee`

## Runtime model

### App service
- launchd label: `com.opteee.native`
- plist path: `/Library/LaunchDaemons/com.opteee.native.plist`
- launcher: `start_native.sh`
- runtime env: `.venv-native/`
- logs:
  - `logs/native.out.log`
  - `logs/native.err.log`

### Weekly refresh job
- launchd label: `com.opteee.weekly-refresh`
- plist path: `/Library/LaunchDaemons/com.opteee.weekly-refresh.plist`
- tracked repo template: `./com.opteee.weekly-refresh.plist`
- script: `./weekly-refresh.sh`
- logs:
  - `logs/weekly-refresh.out.log`
  - `logs/weekly-refresh.err.log`

## What the weekly refresh does

`weekly-refresh.sh` is the only supported weekly refresh path. It:
1. pulls latest Git changes with `git pull --ff-only --autostash`,
2. bootstraps or refreshes the dedicated `.venv-marker` from `requirements-marker.txt`,
3. verifies Marker with `scripts/check_marker_env.py --smoke-pdf tests/fixtures/marker_smoke.pdf`,
4. runs the transcript/content pipeline via `run_transcripts.sh`,
5. refreshes `.venv-native` dependencies from `requirements-serve.txt`,
6. restarts the app by killing the live Python process,
7. relies on `com.opteee.native` `KeepAlive=true` to respawn,
8. waits for `http://127.0.0.1:7860/api/health` to pass,
9. waits an additional 3 minutes before the post-refresh smoke test so the native service can settle,
10. runs the post-refresh smoke test and logs it to `logs/smoke-test.log`,
11. stages refresh artifacts (`outlier_trading_videos*.json`, `transcripts/`, `processed_transcripts/`, `vector_store/`, `wiki/`), commits them when changed, and pushes the refresh commit to `origin/<current-branch>`.

## Schedule

The tracked plist runs:
- Sunday
- 11:00 PM local time

In plist terms:
- `Weekday=0`
- `Hour=23`
- `Minute=0`

## Manual operations

### Verify app health
```bash
curl -fsS http://127.0.0.1:7860/api/health
```

### Verify Marker runtime
```bash
cd /Users/bradfordhaile/clawd/opteee
./.venv-marker/bin/python scripts/check_marker_env.py --smoke-pdf tests/fixtures/marker_smoke.pdf
```

### Dry-run the weekly refresh without restart/commit/push
```bash
cd /Users/bradfordhaile/clawd/opteee
./weekly-refresh.sh --dry-run
```

### Run the weekly refresh immediately
```bash
sudo launchctl kickstart -k system/com.opteee.weekly-refresh
```

### Restart the native app directly
```bash
sudo launchctl kickstart -k system/com.opteee.native
```

### Check launchd state
```bash
launchctl print system/com.opteee.native
launchctl print system/com.opteee.weekly-refresh
```

## One-time install / reload

```bash
cd /Users/bradfordhaile/clawd/opteee
chmod +x weekly-refresh.sh start_native.sh
sudo cp com.opteee.weekly-refresh.plist /Library/LaunchDaemons/com.opteee.weekly-refresh.plist
sudo launchctl bootout system /Library/LaunchDaemons/com.opteee.weekly-refresh.plist 2>/dev/null || true
sudo launchctl bootstrap system /Library/LaunchDaemons/com.opteee.weekly-refresh.plist
sudo launchctl enable system/com.opteee.weekly-refresh
```

## Important constraints

- The native app uses `DATABASE_URL` pointed at `127.0.0.1`.
- `weekly-refresh.sh` owns the dedicated Marker stack as well as the native app refresh; if Marker starts failing, inspect `requirements-marker.txt`, `scripts/check_marker_env.py`, and `tests/fixtures/marker_smoke.pdf` together.
- The content pipeline (`run_pipeline.py`, `run_transcripts.sh`, `rebuild_vector_store.py`) is separate from launchd ownership.
- If launchd ownership changes in the future, update **this file first**, then `README.md`, then the tracked plist/script comments.
