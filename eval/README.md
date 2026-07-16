# OPTEEE eval harness

This folder holds a fixed 20-prompt regression suite for OPTEEE chat output.

## Files

- `prompts/opteee_baseline_20.json` — fixed prompt set for repeatable runs
- `run_chat_eval.py` — hits `/api/chat`, saves raw JSON + CSV + markdown summary
- `compare_chat_eval_runs.py` — compares two `run.json` artifacts
- `runs/` — committed run artifacts for history

## Example

```bash
/Users/bradfordhaile/clawd/opteee/.venv-native/bin/python eval/run_chat_eval.py \
  --base-url http://127.0.0.1:7860 \
  --prompts eval/prompts/opteee_baseline_20.json \
  --output-dir eval/runs/2026-07-16-baseline-live \
  --label baseline-live
```

Then compare:

```bash
/Users/bradfordhaile/clawd/opteee/.venv-native/bin/python eval/compare_chat_eval_runs.py \
  --baseline eval/runs/2026-07-16-baseline-live/run.json \
  --candidate eval/runs/2026-07-16-chonkie/run.json \
  --output-md eval/runs/2026-07-16-comparison/SUMMARY.md \
  --output-json eval/runs/2026-07-16-comparison/comparison.json
```
