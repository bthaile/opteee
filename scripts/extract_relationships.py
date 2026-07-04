#!/usr/bin/env python3
"""
extract_relationships.py — grounded, typed relationships between wiki topics.

Co-occurrence tells us two topics are DISCUSSED TOGETHER; this extracts HOW they relate.
For each co-occurring pair (from wiki/graph.json), it finds a transcript passage where both
concepts are discussed and asks the LLM (Haiku) to extract the actual relationship — a
controlled relation type + a short phrase — grounded in that passage, citing the video.

Output: wiki/relationships.json, consumed by build_graph.py for real edge labels
(e.g. `vega —measures sensitivity to→ implied-volatility` instead of "shared source videos").

Incremental (--new-only default): only pairs not already in relationships.json. Sharded
(--shard i/N) for parallel workers, like ingest_wiki.py.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))  # so `import ingest_wiki` works
WIKI = ROOT / "wiki"
GRAPH = WIKI / "graph.json"
OUT = WIKI / "relationships.json"
PROCESSED = ROOT / "processed_transcripts"
KNOWLEDGE_FOLDERS = ("concepts", "strategies", "securities", "people", "macro", "syntheses")

RELATION_TYPES = ["is-a", "part-of", "measures", "drives", "hedges", "harvests",
                  "requires", "contrasts-with", "related-to"]

SYSTEM = (
    "You extract the relationship between two options-trading concepts, grounded in a "
    "transcript passage. Reply with ONLY a JSON object: "
    '{"relation":"<one of: ' + ", ".join(RELATION_TYPES) + '>", '
    '"label":"<3-6 word phrase describing how the source concept relates to the target>", '
    '"direction":"<a-to-b|b-to-a>"}. '
    "The label must be specific to options trading (e.g. 'measures sensitivity to', "
    "'harvests the premium of', 'is a leg of', 'drives dealer hedging of', 'is a type of'), "
    "never generic like 'related to' unless the relationship is genuinely unclear."
)


def load_pages() -> dict:
    pages: dict = {}
    for folder in KNOWLEDGE_FOLDERS:
        d = WIKI / folder
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            t = f.read_text(encoding="utf-8")
            m = re.search(r"^---\n(.*?)\n---", t, re.S)
            fm = m.group(1) if m else ""
            tm = re.search(r"(?m)^title:\s*(.+)$", fm)
            title = tm.group(1).strip().strip('"').strip("'") if tm else f.stem
            rv = re.search(r"(?m)^related_videos:\s*\[(.*?)\]", fm)
            vids = [x.strip().strip("\"'") for x in rv.group(1).split(",")] if rv else []
            pages[f"{folder}/{f.stem}"] = {
                "id": f"{folder}/{f.stem}", "slug": f.stem, "title": title,
                "videos": set(v for v in vids if v),
            }
    return pages


def keywords(slug: str) -> list:
    ws = [w for w in slug.split("-") if len(w) >= 4]
    return ws or [slug]


def find_snippet(a: str, b: str, pages: dict, denoise) -> tuple:
    """Return (snippet, video_id, timestamp) from a shared video mentioning BOTH concepts."""
    shared = sorted(pages[a]["videos"] & pages[b]["videos"])
    ka, kb = keywords(pages[a]["slug"]), keywords(pages[b]["slug"])
    for vid in shared[:6]:
        pf = PROCESSED / f"{vid}_processed.json"
        if not pf.is_file():
            continue
        try:
            chunks = json.loads(pf.read_text(encoding="utf-8"))
        except Exception:
            continue
        for c in chunks:
            txt = (c.get("text") or "").lower()
            if any(k in txt for k in ka) and any(k in txt for k in kb):
                raw = c.get("text") or ""
                snip = denoise(raw) if denoise else raw
                return snip[:900], vid, c.get("start_timestamp", "")
    return None, (shared[0] if shared else None), ""


def parse_json(text: str):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def candidate_pairs() -> list:
    graph = json.loads(GRAPH.read_text(encoding="utf-8")) if GRAPH.is_file() else {"edges": []}
    seen, pairs = set(), []
    for e in graph.get("edges", []):
        if e.get("type") != "cooccurrence":
            continue
        pair = sorted([e["source"], e["target"]])
        key = "||".join(pair)
        if key in seen:
            continue
        seen.add(key)
        pairs.append((pair[0], pair[1], int(e.get("weight", 1)), key))
    pairs.sort(key=lambda p: -p[2])  # strongest first
    return pairs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Extract grounded, typed topic relationships.")
    ap.add_argument("--new-only", action="store_true", help="only pairs not already extracted (default)")
    ap.add_argument("--force", action="store_true", help="re-extract all pairs")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--shard", metavar="i/N", help="process only shard i of N (parallel workers)")
    ap.add_argument("--provider", default="claude")
    ap.add_argument("--model", default="claude-haiku-4-5")
    ap.add_argument("--out", help="write results here (default wiki/relationships.json); "
                                  "use a per-shard path when running parallel workers, then merge")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    out_path = Path(args.out) if args.out else OUT

    shard = None
    if args.shard:
        i_s, n_s = args.shard.split("/")
        shard = (int(i_s), int(n_s))

    pages = load_pages()
    pairs = [p for p in candidate_pairs() if p[0] in pages and p[1] in pages]

    existing = {}
    if OUT.is_file() and not args.force:
        try:
            existing = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    todo = [p for p in pairs if args.force or p[3] not in existing]
    if shard:
        i, n = shard
        todo = [p for idx, p in enumerate(todo) if idx % n == i]
    if args.limit is not None:
        todo = todo[: args.limit]

    print(f"relationships: pairs={len(pairs)} existing={len(existing)} todo={len(todo)}")
    if args.dry_run:
        return 0

    import ingest_wiki  # lazy: provides denoise() + call_llm(); loads .env

    result = dict(existing)
    done = err = 0
    for a, b, w, key in todo:
        try:
            snip, vid, ts = find_snippet(a, b, pages, ingest_wiki.denoise)
            at, bt = pages[a]["title"], pages[b]["title"]
            if snip:
                human = (f'Concept A: "{at}"\nConcept B: "{bt}"\n\n'
                         f'Passage from a video discussing both:\n"{snip}"\n\nHow does A relate to B?')
            else:
                human = (f'Concept A: "{at}"\nConcept B: "{bt}"\n\n'
                         f'(Discussed together in {w} videos.) Using your options-trading '
                         f'knowledge, how does A relate to B?')
            raw = ingest_wiki.call_llm(SYSTEM, human, args.provider, args.model)
            obj = parse_json(raw)
            if not obj or obj.get("relation") not in RELATION_TYPES:
                err += 1
                continue
            src, tgt = (a, b) if obj.get("direction", "a-to-b") == "a-to-b" else (b, a)
            result[key] = {
                "source": src, "target": tgt, "relation": obj["relation"],
                "label": str(obj.get("label", "")).strip()[:60], "weight": w,
                "evidence": ({"video_id": vid, "timestamp": ts} if vid else None),
            }
            done += 1
        except Exception:
            err += 1
        if done and done % 50 == 0:
            out_path.write_text(json.dumps(result, indent=1, sort_keys=True), encoding="utf-8")
            print(f"  ...{done} done")

    out_path.write_text(json.dumps(result, indent=1, sort_keys=True), encoding="utf-8")
    print(f"extract_relationships: +{done} relationships, {err} errors -> {OUT} (total {len(result)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
