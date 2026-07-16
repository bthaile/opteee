#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two OPTEEE eval run.json files")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output-md", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    baseline = load(args.baseline)
    candidate = load(args.candidate)

    b_by_id = {r["id"]: r for r in baseline["results"]}
    c_by_id = {r["id"]: r for r in candidate["results"]}
    rows = []
    for prompt_id in sorted(b_by_id):
        b = b_by_id[prompt_id]
        c = c_by_id[prompt_id]
        rows.append({
            "id": prompt_id,
            "category": b["category"],
            "latency_delta_seconds": round(c["latency_seconds"] - b["latency_seconds"], 3),
            "answer_word_delta": c["answer_words"] - b["answer_words"],
            "source_delta": c["raw_source_count"] - b["raw_source_count"],
            "wiki_delta": c["wiki_reference_count"] - b["wiki_reference_count"],
            "token_delta": c["total_tokens"] - b["total_tokens"],
            "baseline_preview": b["answer_preview"],
            "candidate_preview": c["answer_preview"],
        })

    b_sum = baseline["summary"]
    c_sum = candidate["summary"]
    aggregate = {
        "baseline_label": baseline["metadata"]["label"],
        "candidate_label": candidate["metadata"]["label"],
        "avg_latency_delta_seconds": None if b_sum["avg_latency_seconds"] is None or c_sum["avg_latency_seconds"] is None else round(c_sum["avg_latency_seconds"] - b_sum["avg_latency_seconds"], 3),
        "avg_total_tokens_delta": None if b_sum["avg_total_tokens"] is None or c_sum["avg_total_tokens"] is None else round(c_sum["avg_total_tokens"] - b_sum["avg_total_tokens"], 1),
        "avg_answer_words_delta": None if b_sum["avg_answer_words"] is None or c_sum["avg_answer_words"] is None else round(c_sum["avg_answer_words"] - b_sum["avg_answer_words"], 1),
        "avg_raw_sources_delta": None if b_sum["avg_raw_sources"] is None or c_sum["avg_raw_sources"] is None else round(c_sum["avg_raw_sources"] - b_sum["avg_raw_sources"], 2),
        "avg_wiki_references_delta": None if b_sum["avg_wiki_references"] is None or c_sum["avg_wiki_references"] is None else round(c_sum["avg_wiki_references"] - b_sum["avg_wiki_references"], 2),
        "video_source_hits_delta": c_sum["video_source_hits"] - b_sum["video_source_hits"],
        "pdf_source_hits_delta": c_sum["pdf_source_hits"] - b_sum["pdf_source_hits"],
    }

    payload = {"aggregate": aggregate, "rows": rows}
    Path(args.output_json).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# OPTEEE eval comparison",
        "",
        f"- Baseline: `{aggregate['baseline_label']}`",
        f"- Candidate: `{aggregate['candidate_label']}`",
        "",
        "## Aggregate deltas (candidate - baseline)",
        "",
    ]
    for key, value in aggregate.items():
        if key.endswith("_label"):
            continue
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Per prompt deltas", ""])
    for row in rows:
        lines.extend([
            f"### {row['id']} — {row['category']}",
            f"- latency_delta_seconds: `{row['latency_delta_seconds']}`",
            f"- answer_word_delta: `{row['answer_word_delta']}`",
            f"- source_delta: `{row['source_delta']}`",
            f"- wiki_delta: `{row['wiki_delta']}`",
            f"- token_delta: `{row['token_delta']}`",
            f"- baseline_preview: {row['baseline_preview']}",
            f"- candidate_preview: {row['candidate_preview']}",
            "",
        ])
    Path(args.output_md).write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
