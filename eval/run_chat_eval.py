#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


@dataclass
class PromptResult:
    id: str
    category: str
    query: str
    status_code: int
    latency_seconds: float
    answer_chars: int
    answer_words: int
    raw_source_count: int
    video_source_count: int
    pdf_source_count: int
    wiki_reference_count: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    provider: str | None
    model: str | None
    effort: str | None
    answer_preview: str
    conversation_id: str | None
    error: str | None
    response: dict[str, Any] | None


def git_info(repo: Path) -> dict[str, str | None]:
    def run(*args: str) -> str | None:
        try:
            return subprocess.check_output(args, cwd=repo, text=True).strip()
        except Exception:
            return None
    return {
        "commit": run("git", "rev-parse", "HEAD"),
        "short_commit": run("git", "rev-parse", "--short", "HEAD"),
        "branch": run("git", "rev-parse", "--abbrev-ref", "HEAD"),
    }


def summarize(results: list[PromptResult]) -> dict[str, Any]:
    ok = [r for r in results if r.status_code == 200 and not r.error]
    latencies = [r.latency_seconds for r in ok]
    totals = [r.total_tokens for r in ok if r.total_tokens]
    return {
        "prompt_count": len(results),
        "success_count": len(ok),
        "failure_count": len(results) - len(ok),
        "avg_latency_seconds": round(statistics.mean(latencies), 3) if latencies else None,
        "p95_latency_seconds": round(sorted(latencies)[max(0, int(len(latencies) * 0.95) - 1)], 3) if latencies else None,
        "avg_total_tokens": round(statistics.mean(totals), 1) if totals else None,
        "avg_answer_words": round(statistics.mean([r.answer_words for r in ok]), 1) if ok else None,
        "avg_raw_sources": round(statistics.mean([r.raw_source_count for r in ok]), 2) if ok else None,
        "avg_wiki_references": round(statistics.mean([r.wiki_reference_count for r in ok]), 2) if ok else None,
        "video_source_hits": sum(r.video_source_count for r in ok),
        "pdf_source_hits": sum(r.pdf_source_count for r in ok),
    }


def write_summary_md(path: Path, metadata: dict[str, Any], summary: dict[str, Any], results: list[PromptResult]) -> None:
    lines = [
        "# OPTEEE chat eval summary",
        "",
        f"- Label: `{metadata['label']}`",
        f"- Base URL: `{metadata['base_url']}`",
        f"- Generated at: `{metadata['generated_at']}`",
        f"- Git branch: `{metadata['git'].get('branch')}`",
        f"- Git commit: `{metadata['git'].get('short_commit')}`",
        f"- Provider override: `{metadata.get('provider')}`",
        f"- Model override: `{metadata.get('model')}`",
        f"- Effort: `{metadata.get('effort')}`",
        f"- Num results: `{metadata.get('num_results')}`",
        "",
        "## Aggregate",
        "",
    ]
    for key, value in summary.items():
        lines.append(f"- {key}: `{value}`")
    lines.extend([
        "",
        "## Per prompt",
        "",
    ])
    for r in results:
        lines.extend([
            f"### {r.id} — {r.category}",
            f"- Query: {r.query}",
            f"- Status: `{r.status_code}`",
            f"- Latency: `{r.latency_seconds:.2f}s`",
            f"- Sources: raw `{r.raw_source_count}`, video `{r.video_source_count}`, pdf `{r.pdf_source_count}`, wiki `{r.wiki_reference_count}`",
            f"- Tokens: prompt `{r.prompt_tokens}`, completion `{r.completion_tokens}`, total `{r.total_tokens}`",
            f"- Model: `{r.provider}` / `{r.model}` / effort `{r.effort}`",
            f"- Preview: {r.answer_preview.replace(chr(10), ' ')}",
            f"- Error: `{r.error}`" if r.error else "- Error: `None`",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a fixed prompt suite against OPTEEE /api/chat")
    parser.add_argument("--base-url", default="http://127.0.0.1:7860")
    parser.add_argument("--prompts", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--provider", default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--effort", default="low")
    parser.add_argument("--num-results", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--pause-seconds", type=float, default=0.0)
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    prompts = json.loads(Path(args.prompts).read_text(encoding="utf-8"))

    metadata = {
        "label": args.label,
        "base_url": args.base_url.rstrip("/"),
        "provider": args.provider,
        "model": args.model,
        "effort": args.effort,
        "num_results": args.num_results,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git": git_info(repo),
        "prompts_file": str(Path(args.prompts).resolve()),
    }

    session = requests.Session()
    results: list[PromptResult] = []

    for prompt in prompts:
        payload = {
            "query": prompt["query"],
            "format": "json",
            "num_results": args.num_results,
            "effort": args.effort,
        }
        if args.provider:
            payload["provider"] = args.provider
        if args.model:
            payload["model"] = args.model
        t0 = time.perf_counter()
        status_code = 0
        error = None
        body = None
        try:
            resp = session.post(f"{metadata['base_url']}/api/chat", json=payload, timeout=args.timeout)
            status_code = resp.status_code
            body = resp.json()
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        latency = time.perf_counter() - t0

        answer = (body or {}).get("answer", "") if isinstance(body, dict) else ""
        raw_sources = (body or {}).get("raw_sources", []) if isinstance(body, dict) else []
        wiki_refs = (body or {}).get("wiki_references", []) if isinstance(body, dict) else []
        token_usage = (body or {}).get("token_usage", {}) if isinstance(body, dict) else {}
        result = PromptResult(
            id=prompt["id"],
            category=prompt["category"],
            query=prompt["query"],
            status_code=status_code,
            latency_seconds=round(latency, 3),
            answer_chars=len(answer),
            answer_words=len(answer.split()),
            raw_source_count=len(raw_sources),
            video_source_count=sum(1 for s in raw_sources if s.get("source_type", "video") == "video"),
            pdf_source_count=sum(1 for s in raw_sources if s.get("source_type") == "pdf"),
            wiki_reference_count=len(wiki_refs),
            prompt_tokens=int(token_usage.get("prompt_tokens") or 0),
            completion_tokens=int(token_usage.get("completion_tokens") or 0),
            total_tokens=int(token_usage.get("total_tokens") or 0),
            provider=token_usage.get("provider"),
            model=token_usage.get("model"),
            effort=token_usage.get("effort"),
            answer_preview=answer[:300],
            conversation_id=(body or {}).get("conversation_id") if isinstance(body, dict) else None,
            error=error,
            response=body if isinstance(body, dict) else None,
        )
        results.append(result)
        print(f"[{result.id}] status={result.status_code} latency={result.latency_seconds:.2f}s sources={result.raw_source_count} wiki={result.wiki_reference_count} tokens={result.total_tokens} error={result.error}")
        if args.pause_seconds:
            time.sleep(args.pause_seconds)

    summary = summarize(results)
    run_payload = {
        "metadata": metadata,
        "summary": summary,
        "results": [asdict(r) for r in results],
    }
    (outdir / "run.json").write_text(json.dumps(run_payload, indent=2), encoding="utf-8")

    with (outdir / "results.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=[k for k in asdict(results[0]).keys() if k != "response"])
        writer.writeheader()
        for r in results:
            row = asdict(r)
            row.pop("response", None)
            writer.writerow(row)

    write_summary_md(outdir / "SUMMARY.md", metadata, summary, results)
    print(json.dumps(summary, indent=2))
    return 0 if summary["failure_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
