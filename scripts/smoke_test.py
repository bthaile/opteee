#!/usr/bin/env python3
"""
smoke_test.py — post-weekly-refresh verification for the OPTEEE LLM Wiki + RAG bridge.

Run this after `weekly-refresh.sh` (or any manual rebuild) to confirm the system is
healthy and internally consistent. Exits 0 iff every non-optional check passes, so it
can be wired into automation.

Checks, grouped:
  CONTENT   coverage (every processed transcript has a source page), graph.json, related_videos.json
  GATE      lint_wiki.py exits 0 (wiki is publishable)
  BRIDGE    the FAISS store metadata actually carries the current related_wiki_pages
            (catches a stale reindex — the #1 silent weekly failure) + a deterministic
            retrieval proof (query a bridged chunk's own text -> it comes back with links)
  API       the live app serves /api/health, /api/wiki/*, /wiki, and blocks path traversal
  CHAT      (optional, --with-chat) one real /api/chat call returns an answer + sources

Usage:
  .venv-native/bin/python scripts/smoke_test.py                 # full (needs the app running)
  .venv-native/bin/python scripts/smoke_test.py --no-api        # offline checks only
  .venv-native/bin/python scripts/smoke_test.py --with-chat     # also do a live LLM chat query
  .venv-native/bin/python scripts/smoke_test.py --base-url http://127.0.0.1:7860

Run with the SERVE venv (.venv-native) — it imports rag_pipeline for the retrieval check.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import pickle
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Ensure repo-root modules (rag_pipeline, config) import regardless of how we're invoked
# (running `python scripts/smoke_test.py` puts scripts/ on sys.path, not the repo root).
sys.path.insert(0, str(ROOT))

WIKI = ROOT / "wiki"
PROCESSED = ROOT / "processed_transcripts"
VECTOR_META = ROOT / "vector_store" / "transcript_metadata.pkl"
KNOWLEDGE_CATS = ["concepts", "strategies", "securities", "people", "macro", "syntheses"]

# Fraction of processed videos that must have a source page (allows a few LLM rejects).
COVERAGE_MIN = 0.98

results: list[tuple[str, str, str]] = []  # (name, status, detail); status: PASS|FAIL|WARN|SKIP


def record(name: str, status: str, detail: str = "") -> None:
    results.append((name, status, detail))
    icon = {"PASS": "✓", "FAIL": "✗", "WARN": "!", "SKIP": "·"}[status]
    print(f"  [{icon}] {name:28} {status:4} {detail}")


# --------------------------------------------------------------------------- CONTENT
def check_coverage() -> None:
    processed = {Path(p).name[: -len("_processed.json")] for p in glob.glob(str(PROCESSED / "*_processed.json"))}
    sources = {Path(p).stem for p in glob.glob(str(WIKI / "sources" / "*.md"))}
    if not processed:
        record("content.coverage", "FAIL", "no processed transcripts found")
        return
    missing = processed - sources
    cov = 1 - len(missing) / len(processed)
    detail = f"{len(sources)} source pages for {len(processed)} videos ({cov:.1%}); {len(missing)} missing"
    if cov < COVERAGE_MIN:
        record("content.coverage", "FAIL", detail + f" (< {COVERAGE_MIN:.0%})")
    elif missing:
        record("content.coverage", "WARN", detail + " — likely LLM rejects, retry next run")
    else:
        record("content.coverage", "PASS", detail)


def check_graph() -> None:
    gf = WIKI / "graph.json"
    if not gf.is_file():
        record("content.graph", "FAIL", "wiki/graph.json missing")
        return
    try:
        g = json.loads(gf.read_text())
    except Exception as e:
        record("content.graph", "FAIL", f"invalid JSON: {e}")
        return
    n_pages = sum(len(list((WIKI / c).glob("*.md"))) for c in KNOWLEDGE_CATS if (WIKI / c).is_dir())
    n_nodes = len(g.get("nodes", []))
    if n_nodes != n_pages:
        record("content.graph", "FAIL", f"{n_nodes} graph nodes != {n_pages} knowledge pages")
    else:
        record("content.graph", "PASS", f"{n_nodes} nodes, {len(g.get('edges', []))} edges")


def _parse_index_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def check_index() -> None:
    index_file = WIKI / "index.md"
    graph_file = WIKI / "graph.json"
    if not index_file.is_file():
        record("content.index", "FAIL", "wiki/index.md missing")
        return
    if not graph_file.is_file():
        record("content.index", "FAIL", "wiki/graph.json missing")
        return
    try:
        frontmatter = _parse_index_frontmatter(index_file.read_text(encoding="utf-8"))
        graph = json.loads(graph_file.read_text(encoding="utf-8"))
    except Exception as e:
        record("content.index", "FAIL", f"could not parse index/graph: {e}")
        return

    expected_nodes = len(graph.get("nodes", []))
    expected_sources = len(list((WIKI / "sources").glob("*.md")))
    got_nodes = int(frontmatter.get("knowledge_page_count") or -1)
    got_sources = int(frontmatter.get("source_count") or -1)
    generated_by = frontmatter.get("generated_by")

    if generated_by != "scripts/build_wiki_index.py":
        record("content.index", "FAIL", "index.md is not marked as generated by build_wiki_index.py")
    elif got_nodes != expected_nodes:
        record("content.index", "FAIL", f"knowledge_page_count={got_nodes}, graph nodes={expected_nodes}")
    elif got_sources != expected_sources:
        record("content.index", "FAIL", f"source_count={got_sources}, source pages={expected_sources}")
    else:
        record("content.index", "PASS", f"{got_nodes} graph nodes, {got_sources} source pages")


def check_reverse_map() -> None:
    rf = WIKI / "related_videos.json"
    if not rf.is_file():
        record("content.reverse_map", "FAIL", "wiki/related_videos.json missing")
        return None
    try:
        rv = json.loads(rf.read_text())
    except Exception as e:
        record("content.reverse_map", "FAIL", f"invalid JSON: {e}")
        return None
    processed = {Path(p).name[: -len("_processed.json")] for p in glob.glob(str(PROCESSED / "*_processed.json"))}
    stray = [v for v in rv if v not in processed]
    if stray:
        record("content.reverse_map", "WARN", f"{len(rv)} videos mapped; {len(stray)} not in processed_transcripts")
    else:
        record("content.reverse_map", "PASS", f"{len(rv)} videos mapped to wiki pages")
    return rv


# --------------------------------------------------------------------------- GATE
def check_lint() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "lint_wiki.py")],
        capture_output=True, text=True,
    )
    last = (proc.stdout.strip().splitlines() or ["(no output)"])[-1]
    if proc.returncode == 0:
        record("gate.lint", "PASS", last)
    else:
        record("gate.lint", "FAIL", f"exit {proc.returncode} — {last}")


# --------------------------------------------------------------------------- BRIDGE
def check_bridge_metadata(rv: dict | None) -> None:
    """The FAISS store metadata must match the CURRENT reverse map (fresh reindex)."""
    if not VECTOR_META.is_file():
        record("bridge.metadata", "FAIL", "vector_store/transcript_metadata.pkl missing")
        return
    if not rv:
        record("bridge.metadata", "SKIP", "no reverse map to compare")
        return
    try:
        meta = pickle.load(open(VECTOR_META, "rb"))
    except Exception as e:
        record("bridge.metadata", "FAIL", f"cannot load metadata pkl: {e}")
        return
    by_vid: dict[str, list] = {}
    for m in meta:
        vid = m.get("video_id")
        if vid in rv:
            by_vid.setdefault(vid, []).append(m)
    mismatches = []
    checked = 0
    for vid, pages in rv.items():
        chunks = by_vid.get(vid)
        if not chunks:
            continue  # video not in store (no chunks) — skip
        checked += 1
        want = sorted(pages)
        for m in chunks:
            got = sorted(m.get("related_wiki_pages") or [])
            if got != want:
                mismatches.append(vid)
                break
    if checked == 0:
        record("bridge.metadata", "WARN", "no bridged videos found in store metadata")
    elif mismatches:
        record("bridge.metadata", "FAIL",
               f"{len(mismatches)}/{checked} bridged videos STALE in FAISS "
               f"(reindex did not pick up annotations): {mismatches[:3]}")
    else:
        record("bridge.metadata", "PASS", f"{checked} bridged videos consistent in FAISS store")


def check_bridge_retrieval(rv: dict | None, sample: int = 2) -> None:
    """Query the retriever with a bridged chunk's own text; it must come back with links."""
    if not rv:
        record("bridge.retrieval", "SKIP", "no bridged videos")
        return
    try:
        from rag_pipeline import CustomFAISSRetriever
    except Exception as e:
        record("bridge.retrieval", "SKIP", f"cannot import retriever ({type(e).__name__}); run under .venv-native")
        return
    try:
        r = CustomFAISSRetriever(top_k=1)
    except SystemExit:
        record("bridge.retrieval", "FAIL", "retriever init failed (vector store files missing?)")
        return
    except Exception as e:
        record("bridge.retrieval", "FAIL", f"retriever init error: {e}")
        return
    tested = 0
    for vid in list(rv)[:sample]:
        pf = PROCESSED / f"{vid}_processed.json"
        if not pf.is_file():
            continue
        chunks = json.loads(pf.read_text())
        if not chunks:
            continue
        probe = chunks[len(chunks) // 2].get("text", "")
        if not probe:
            continue
        docs = r.get_relevant_documents(probe)
        tested += 1
        top = docs[0].metadata if docs else {}
        if not top.get("related_wiki_pages"):
            record("bridge.retrieval", "FAIL",
                   f"{vid}: top hit {top.get('video_id')} had no related_wiki_pages")
            return
    if tested == 0:
        record("bridge.retrieval", "WARN", "no bridged transcripts available to probe")
    else:
        record("bridge.retrieval", "PASS", f"{tested} bridged chunk(s) round-tripped with wiki links")


# --------------------------------------------------------------------------- API
def _client(base_url: str):
    try:
        import httpx
    except Exception:
        return None
    return httpx.Client(base_url=base_url, timeout=15.0)


def check_api(base_url: str) -> None:
    client = _client(base_url)
    if client is None:
        record("api", "SKIP", "httpx not available")
        return
    try:
        r = client.get("/api/health")
        if r.status_code == 200 and "health" in r.json().get("status", "").lower():
            record("api.health", "PASS", base_url)
        else:
            record("api.health", "FAIL", f"status={r.status_code} body={r.text[:60]}")
            record("api.*", "SKIP", "app unhealthy — skipping remaining API checks")
            return
    except Exception as e:
        record("api.health", "FAIL", f"app unreachable at {base_url} ({type(e).__name__})")
        record("api.*", "SKIP", "app not running — start it, or use --no-api")
        return

    try:
        j = client.get("/api/wiki/index").json()
        record("api.wiki_index", "PASS" if j.get("page_count", 0) > 0 else "FAIL",
               f"pages={j.get('page_count')} sources={j.get('source_count')}")
    except Exception as e:
        record("api.wiki_index", "FAIL", str(e)[:60])

    try:
        doc = client.get("/api/wiki/index/document").json()
        ok = (
            doc.get("frontmatter", {}).get("generated_by") == "scripts/build_wiki_index.py"
            and len(doc.get("markdown", "")) > 100
        )
        record("api.wiki_index_doc", "PASS" if ok else "FAIL",
               f"markdown={len(doc.get('markdown', ''))} chars")
    except Exception as e:
        record("api.wiki_index_doc", "FAIL", str(e)[:60])

    try:
        g = client.get("/api/wiki/graph.json").json()
        record("api.graph", "PASS" if "nodes" in g else "FAIL", f"nodes={len(g.get('nodes', []))}")
    except Exception as e:
        record("api.graph", "FAIL", str(e)[:60])

    # a real knowledge page
    kp = None
    for c in KNOWLEDGE_CATS:
        files = list((WIKI / c).glob("*.md"))
        if files:
            kp = f"{c}/{files[0].stem}"
            break
    if kp:
        r = client.get(f"/api/wiki/pages/{kp}")
        ok = r.status_code == 200 and len(r.json().get("html", "")) > 0
        record("api.wiki_page", "PASS" if ok else "FAIL", f"{kp} -> {r.status_code}")
        rj = client.get(f"/api/wiki/pages/{kp}?format=json")
        try:
            pj = rj.json()
        except Exception:
            pj = {}
        okj = (
            rj.status_code == 200
            and len(pj.get("markdown", "")) > 0
            and len(pj.get("html", "")) > 0
            and isinstance(pj.get("wikilinks"), list)
        )
        record("api.wiki_page_json", "PASS" if okj else "FAIL",
               f"{kp}?format=json -> {rj.status_code}")
        # standalone page view (target of chat 'Wiki References' links)
        rv = client.get(f"/wiki/page/{kp}")
        okv = rv.status_code == 200 and "<article>" in rv.text
        record("api.wiki_page_view", "PASS" if okv else "FAIL", f"/wiki/page/{kp} -> {rv.status_code}")

    r = client.get("/api/wiki/pages/../../config.py")
    record("api.traversal_guard", "PASS" if r.status_code == 404 else "FAIL",
           f"../../config.py -> {r.status_code} (want 404)")

    r = client.get("/wiki")
    record("api.graph_page", "PASS" if r.status_code == 200 else "FAIL", f"/wiki -> {r.status_code}")


def check_chat(base_url: str) -> None:
    client = _client(base_url)
    if client is None:
        record("chat", "SKIP", "httpx not available")
        return
    try:
        r = client.post("/api/chat", json={"query": "What is a covered strangle?", "num_results": 5},
                        timeout=90.0)
        if r.status_code != 200:
            record("chat.query", "FAIL", f"status={r.status_code}")
            return
        j = r.json()
        n_sources = len(j.get("raw_sources", []))
        bridged = sum(1 for s in j.get("raw_sources", []) if s.get("related_wiki_pages"))
        wiki_refs = j.get("wiki_references", [])
        ok = bool(j.get("answer")) and n_sources > 0 and "wiki_references" in j
        record("chat.query", "PASS" if ok else "FAIL",
               f"answer={len(j.get('answer',''))} chars, {n_sources} sources, "
               f"{bridged} bridged, {len(wiki_refs)} wiki_references")
    except Exception as e:
        record("chat.query", "FAIL", f"{type(e).__name__}: {str(e)[:60]}")


# --------------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="OPTEEE wiki + RAG-bridge post-refresh smoke test.")
    ap.add_argument("--base-url", default=os.getenv("OPTEEE_URL", "http://127.0.0.1:7860"))
    ap.add_argument("--no-api", action="store_true", help="skip live-app API checks")
    ap.add_argument("--no-retrieval", action="store_true", help="skip the retriever round-trip (faster)")
    ap.add_argument("--with-chat", action="store_true", help="also run one live /api/chat query (uses the LLM)")
    args = ap.parse_args(argv)

    print("OPTEEE wiki smoke test\n" + "=" * 60)
    print("CONTENT")
    check_coverage()
    check_graph()
    check_index()
    rv = check_reverse_map()
    print("GATE")
    check_lint()
    print("BRIDGE")
    check_bridge_metadata(rv)
    if args.no_retrieval:
        record("bridge.retrieval", "SKIP", "--no-retrieval")
    else:
        check_bridge_retrieval(rv)
    print("API")
    if args.no_api:
        record("api", "SKIP", "--no-api")
    else:
        check_api(args.base_url)
        if args.with_chat:
            check_chat(args.base_url)

    fails = [r for r in results if r[1] == "FAIL"]
    warns = [r for r in results if r[1] == "WARN"]
    print("=" * 60)
    print(f"RESULT: {len(fails)} fail, {len(warns)} warn, "
          f"{sum(1 for r in results if r[1]=='PASS')} pass, "
          f"{sum(1 for r in results if r[1]=='SKIP')} skip")
    if fails:
        print("FAILED: " + ", ".join(r[0] for r in fails))
        return 1
    print("SMOKE TEST PASSED" + (" (with warnings)" if warns else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
