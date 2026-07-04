#!/usr/bin/env python3
"""
build_topics.py — auto-generate the knowledge/topic layer from the source-page corpus.

The graph shows knowledge-layer pages only. Curated synthesis is slow, so this script
gives the graph its real topic landscape immediately: it aggregates the
concepts/strategies/securities/experts slugs across every wiki/sources/*.md and, for each
that recurs in >= THRESHOLD videos, generates a lightweight knowledge page (unless one
already exists) carrying `related_videos`. That fills the graph AND expands the RAG bridge
(each topic page bridges its videos). Curated synthesis can later deepen any page.

People (interviewed guests, from `experts:`) become the **Interviews** group (type: person,
folder people/), kept distinct from concept/strategy/security topics.

Runs in the pipeline after ingest and before annotate_chunks. Idempotent: never overwrites
an existing page (so hand-curated pages win). Aliases are resolved to canonical slugs.

    python scripts/build_topics.py            # generate
    python scripts/build_topics.py --dry-run  # report only
"""
from __future__ import annotations

import argparse
import datetime
import glob
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
SOURCES = WIKI / "sources"
SLUGS = ROOT / "schema" / "slugs.md"
TODAY = datetime.date.today().isoformat()

# facet in source frontmatter -> (knowledge folder, page type, default min videos)
CATS = {
    "concepts":   ("concepts",   "concept",  6),
    "strategies": ("strategies", "strategy", 3),
    "securities": ("securities", "security", 5),
    "experts":    ("people",     "person",   2),
}

# The channel host(s) are not interview guests — never make them an "Interviews" node.
HOST_EXCLUDE = {"eric", "outlier-trading", "eric-stu"}


def load_alias_map() -> dict:
    """canonical <- variants, from schema/slugs.md 'Aliases' section."""
    alias = {}
    text = SLUGS.read_text(encoding="utf-8")
    m = re.search(r"## Aliases.*?\n(.*?)\n## ", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            am = re.match(r"-\s*`([^`]+)`\s*(?:←|<-)\s*(.+)", line)
            if am:
                canon = am.group(1)
                for v in re.findall(r"`([^`]+)`", am.group(2)):
                    alias[v] = canon
    return alias


def fm_list(fm: str, key: str) -> list[str]:
    m = re.search(rf"(?m)^{key}:\s*\[(.*?)\]", fm)
    if not m:
        return []
    return [x.strip().strip("\"'") for x in m.group(1).split(",") if x.strip()]


def prettify(slug: str, folder: str) -> str:
    if folder == "securities" and re.fullmatch(r"[a-z0-9]{1,5}", slug):
        return slug.upper()  # ticker
    return slug.replace("-", " ").replace("_", " ").title()


def wiki_label(title: str) -> str:
    """Sanitize a video title for use as a [[sources/id|label]] wikilink label."""
    t = str(title).replace("[", "(").replace("]", ")").replace("|", "/")
    t = re.sub(r"\s+", " ", t).strip()
    return t or title


def render_page(page_type: str, folder: str, slug: str, related: list[str],
                titles: dict | None = None) -> str:
    titles = titles or {}
    title = prettify(slug, folder)
    vids = ", ".join(f'"{v}"' for v in related)
    head = [
        "---",
        f"type: {page_type}",
        f'title: "{title}"',
        f"related_videos: [{vids}]",
        f"last_updated: {TODAY}",
        "confidence: auto",
        "auto_generated: true",
    ]
    if folder == "people":
        head.append("category: interviews")
        head.append("role: interviewed guest")
    head.append("---")
    body = [f"# {title}", ""]
    if folder == "people":
        body.append(
            f"**Interviewed guest** — appears in {len(related)} video(s) in the corpus. "
            "Auto-generated stub pending curated synthesis of this person's distinctive views."
        )
    else:
        body.append(
            f"**Auto-generated {page_type} topic** — discussed across {len(related)} video(s). "
            "Pending curated synthesis; the backing source pages are linked below."
        )
    body += ["", "## Discussed in", ""]
    body += [f"- [[sources/{v}|{wiki_label(titles.get(v, v))}]]" for v in related]
    body.append("")
    return "\n".join(head + [""] + body)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Auto-generate the wiki topic layer from source pages.")
    ap.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing AUTO-generated pages (never touches curated pages)")
    for facet, (_folder, _typ, default) in CATS.items():
        ap.add_argument(f"--min-{facet}", type=int, default=default,
                        help=f"min videos for a {facet} page (default {default})")
    args = ap.parse_args(argv)

    alias = load_alias_map()
    def canon(s: str) -> str: return alias.get(s, s)

    agg = {facet: defaultdict(set) for facet in CATS}  # facet -> slug -> {video_id}
    titles: dict = {}  # video_id -> title (for readable "Discussed in" links)
    files = glob.glob(str(SOURCES / "*.md"))
    for f in files:
        text = Path(f).read_text(encoding="utf-8")
        m = re.search(r"^---\n(.*?)\n---", text, re.S)
        if not m:
            continue
        fm = m.group(1)
        vm = re.search(r'(?m)^video_id:\s*"?([^"\n]+)"?', fm)
        vid = vm.group(1).strip() if vm else Path(f).stem
        tm = re.search(r"(?m)^title:\s*(.+?)\s*$", fm)
        if tm:
            t = tm.group(1).strip()
            if len(t) >= 2 and t[0] == '"' and t[-1] == '"':
                t = t[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            elif len(t) >= 2 and t[0] == "'" and t[-1] == "'":
                t = t[1:-1]
            titles[vid] = t
        for facet in CATS:
            for slug in fm_list(fm, facet):
                agg[facet][canon(slug)].add(vid)

    created = skipped = 0
    per_cat = {}
    for facet, (folder, page_type, _d) in CATS.items():
        threshold = getattr(args, f"min_{facet}")
        outdir = WIKI / folder
        n = 0
        for slug, vids in sorted(agg[facet].items()):
            if len(vids) < threshold:
                continue
            if facet == "experts" and slug in HOST_EXCLUDE:
                continue
            path = outdir / f"{slug}.md"
            if path.exists():
                # never overwrite curated pages; with --force, refresh auto-generated ones
                is_auto = "auto_generated: true" in path.read_text(encoding="utf-8")
                if not (args.force and is_auto):
                    skipped += 1
                    continue
            page = render_page(page_type, folder, slug, sorted(vids), titles)
            if not args.dry_run:
                outdir.mkdir(parents=True, exist_ok=True)
                path.write_text(page, encoding="utf-8")
            created += 1
            n += 1
        per_cat[folder] = n

    verb = "would create" if args.dry_run else "created"
    print(f"build_topics: scanned {len(files)} source pages; {verb} {created}, skipped {skipped} existing")
    for folder, n in per_cat.items():
        print(f"  {folder:12} +{n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
