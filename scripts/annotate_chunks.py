#!/usr/bin/env python3
"""annotate_chunks.py -- the RAG bridge for the OPTEEE LLM Wiki.

Implements the two data contracts described in schema/WIKI_SCHEMA.md section 12:

  Job 1 - Build the reverse map ``wiki/related_videos.json``:
          ``{ video_id: [wiki_page_path, ...] }`` produced by inverting the
          ``related_videos:`` frontmatter list of *every* knowledge page under
          wiki/{concepts,strategies,securities,people,macro,syntheses}/*.md.
          A page at ``wiki/strategies/covered-strangle.md`` contributes the
          path ``strategies/covered-strangle`` to each of its related videos.
          Lists (and the map keys) are sorted for deterministic output.

  Job 2 - Stamp chunks: for every ``processed_transcripts/{video_id}_processed.json``
          (a JSON list of chunk dicts, each carrying a ``video_id`` field), add or
          replace ``related_wiki_pages: [...]`` on each chunk using the reverse map
          keyed by that chunk's own ``video_id`` (``[]`` when the video maps nowhere).
          Files are rewritten with the same formatting style (indent=2,
          ensure_ascii=False) plus a trailing newline. No other chunk field or
          ordering is disturbed, and re-running yields byte-identical files.

Because create_vector_store.py stores the entire chunk dict as FAISS metadata,
``related_wiki_pages`` rides through to the retriever automatically. This script
must therefore run AFTER preprocess_transcripts.py and BEFORE the vectors step.

CLI:
  (no args)           full scan: refresh the reverse map and stamp all chunk files
  --dry-run           compute the map + report what WOULD change; write nothing
  --video ID          refresh the reverse map and stamp only that one video's file
  --rebuild-map-only  write related_videos.json only; do not touch any chunk files
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

# --- Paths (this script lives in <repo>/scripts/) --------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
PROCESSED_DIR = REPO_ROOT / "processed_transcripts"
REVERSE_MAP_PATH = WIKI_DIR / "related_videos.json"

# Knowledge-layer subdirectories whose pages carry ``related_videos`` frontmatter.
# (wiki/sources/, wiki/index.md and wiki/log.md are deliberately excluded.)
KNOWLEDGE_DIRS = ["concepts", "strategies", "securities", "people", "macro", "syntheses"]


# --- Frontmatter parsing ---------------------------------------------------
def parse_frontmatter(text: str) -> dict:
    """Return the YAML frontmatter block of a markdown file as a dict.

    Returns an empty dict if the file has no leading ``---`` fence, the fence
    is unterminated, or the block does not parse to a mapping.
    """
    if not text.startswith("---"):
        return {}
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def page_path_id(md_path: Path) -> str:
    """``wiki/strategies/covered-strangle.md`` -> ``strategies/covered-strangle``."""
    return md_path.relative_to(WIKI_DIR).with_suffix("").as_posix()


def iter_knowledge_pages():
    """Yield every knowledge-page markdown path in deterministic order."""
    for sub in KNOWLEDGE_DIRS:
        directory = WIKI_DIR / sub
        if not directory.is_dir():
            continue
        for md_path in sorted(directory.glob("*.md")):
            yield md_path


# --- Job 1: build the reverse map ------------------------------------------
def build_reverse_map():
    """Invert every knowledge page's ``related_videos``.

    Returns ``(reverse_map, pages_inverted)`` where ``reverse_map`` maps each
    ``video_id`` to a sorted list of wiki page paths, and ``pages_inverted`` is
    the number of knowledge pages that contributed at least one video.
    """
    reverse: dict[str, set] = {}
    pages_inverted = 0
    for md_path in iter_knowledge_pages():
        try:
            text = md_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"  ! skip {md_path}: {exc}", file=sys.stderr)
            continue
        videos = parse_frontmatter(text).get("related_videos")
        if not isinstance(videos, list):
            continue
        page_id = page_path_id(md_path)
        contributed = False
        for vid in videos:
            if vid is None:
                continue
            vid = str(vid).strip()
            if not vid:
                continue
            reverse.setdefault(vid, set()).add(page_id)
            contributed = True
        if contributed:
            pages_inverted += 1
    reverse_sorted = {vid: sorted(pages) for vid, pages in reverse.items()}
    return reverse_sorted, pages_inverted


def render_reverse_map(reverse_map: dict) -> str:
    # sort_keys => deterministic key order; values already sorted.
    return json.dumps(reverse_map, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


# --- Job 2: stamp chunk files ----------------------------------------------
def stamp_file(path: Path, reverse_map: dict, dry_run: bool):
    """Stamp ``related_wiki_pages`` onto every chunk in one processed file.

    Returns ``(file_changed, chunks_changed, n_chunks)``. Existing chunk fields
    and their ordering are preserved; only ``related_wiki_pages`` is set. The
    file is rewritten only when its bytes would actually change (and never when
    ``dry_run`` is True), which is what makes re-runs idempotent.
    """
    try:
        original = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"  ! skip {path.name}: {exc}", file=sys.stderr)
        return False, 0, 0
    try:
        data = json.loads(original)
    except json.JSONDecodeError as exc:
        print(f"  ! skip {path.name}: invalid JSON ({exc})", file=sys.stderr)
        return False, 0, 0
    if not isinstance(data, list):
        print(f"  ! skip {path.name}: expected a JSON list of chunks", file=sys.stderr)
        return False, 0, 0

    chunks_changed = 0
    for chunk in data:
        if not isinstance(chunk, dict):
            continue
        new_pages = list(reverse_map.get(chunk.get("video_id"), []))
        if chunk.get("related_wiki_pages") != new_pages:
            chunks_changed += 1
        # Assigning an existing key preserves its position; a new key is appended.
        chunk["related_wiki_pages"] = new_pages

    new_text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    file_changed = new_text != original
    if file_changed and not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return file_changed, chunks_changed, len(data)


# --- Orchestration ---------------------------------------------------------
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Build wiki/related_videos.json and stamp related_wiki_pages onto chunks.",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Compute the map and report what would change; write nothing.")
    parser.add_argument("--video", metavar="ID",
                        help="Stamp only processed_transcripts/{ID}_processed.json.")
    parser.add_argument("--rebuild-map-only", action="store_true",
                        help="Write related_videos.json only; do not touch chunk files.")
    args = parser.parse_args(argv)

    reverse_map, pages_inverted = build_reverse_map()
    videos_mapped = len(reverse_map)

    # --- Job 1: the reverse-map artifact (skipped only under --dry-run) ---
    map_text = render_reverse_map(reverse_map)
    map_existing = REVERSE_MAP_PATH.read_text(encoding="utf-8") if REVERSE_MAP_PATH.exists() else None
    map_would_change = map_existing != map_text
    if args.dry_run:
        map_status = "would write" if map_would_change else "unchanged"
    else:
        if map_would_change:
            REVERSE_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
            REVERSE_MAP_PATH.write_text(map_text, encoding="utf-8")
            map_status = "written"
        else:
            map_status = "unchanged"

    # --- Job 2: stamp chunk files (skipped under --rebuild-map-only) ---
    files_scanned = files_changed = chunks_changed = chunks_total = 0
    if not args.rebuild_map_only:
        if args.video:
            target = PROCESSED_DIR / f"{args.video}_processed.json"
            if not target.exists():
                print(f"error: {target} not found", file=sys.stderr)
                return 1
            targets = [target]
        else:
            targets = sorted(PROCESSED_DIR.glob("*_processed.json"))
        for path in targets:
            files_scanned += 1
            fchanged, cchanged, n = stamp_file(path, reverse_map, dry_run=args.dry_run)
            chunks_total += n
            chunks_changed += cchanged
            if fchanged:
                files_changed += 1

    # --- Summary ---
    if args.dry_run:
        mode = "dry-run"
    elif args.rebuild_map_only:
        mode = "rebuild-map-only"
    elif args.video:
        mode = f"video={args.video}"
    else:
        mode = "full-scan"
    verb = "would update" if args.dry_run else "updated"
    stamp_verb = "would stamp" if args.dry_run else "stamped"

    print(f"annotate_chunks [{mode}]")
    print(f"  pages inverted   : {pages_inverted}")
    print(f"  videos mapped    : {videos_mapped}")
    print(f"  reverse map      : {REVERSE_MAP_PATH.relative_to(REPO_ROOT)} ({map_status})")
    if not args.rebuild_map_only:
        print(f"  chunk files      : {files_scanned} scanned")
        print(f"  files {verb:<12}: {files_changed}")
        print(f"  chunks {stamp_verb:<11}: {chunks_changed} of {chunks_total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
