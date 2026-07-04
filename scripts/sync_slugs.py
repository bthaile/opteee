#!/usr/bin/env python3
"""
sync_slugs.py — grow schema/slugs.md to cover every slug actually used in the wiki.

The seed registry came from a 14-video sample; the full corpus legitimately surfaces many
more trading concepts. Rather than block the pipeline whenever an extractor uses a new
valid slug, this harvests all frontmatter-facet + `[[wikilink]]` slugs across `wiki/` and
regenerates the canonical lists in `slugs.md` (preserving the curated **Aliases** section),
so the lint gate passes on legitimate new topics. Drift (duplicate variants) is still cleaned
periodically by adding aliases — this only ever ADDS canonical slugs, never removes them.

Runs in the pipeline after ingest/build_topics and BEFORE lint.

    python scripts/sync_slugs.py            # regenerate registry from usage
    python scripts/sync_slugs.py --check    # report new slugs, write nothing (exit 1 if any)
"""
from __future__ import annotations

import argparse
import glob
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
SLUGS = ROOT / "schema" / "slugs.md"

# frontmatter facet field -> registry category
FACET_CAT = {
    "concepts": "concepts", "strategies": "strategies",
    "securities": "securities", "experts": "people", "mentions": "people",
}
WIKILINK_CAT = {"concepts", "strategies", "securities", "people"}
SLUG_RE = re.compile(r"[a-z0-9][a-z0-9-]*")

SECTION_NOTES = {
    "Concepts": "> subtype each as `mechanic` | `mental-model` | `process` on its page.",
    "Securities": "> real tickers where they exist; canonical name-slugs for commodities/indices "
                  "(`crude-oil`, `natural-gas`, `gold`, `nasdaq`, `russell-2000`).",
    "People": "> host default is `eric` (Outlier Trading). `experts` = featured; "
              "`mentions` = discussed-but-absent.",
}
SECTION_ORDER = [("Concepts", "concepts"), ("Strategies", "strategies"),
                 ("Securities", "securities"), ("People", "people")]


def parse_header_and_aliases(text: str):
    """Return (header-including-Aliases, alias_to_canon, alias_variants)."""
    hm = re.search(r"^(.*?)\n## Concepts", text, re.S)
    header = hm.group(1) if hm else "# slugs.md — Canonical Slug Registry\n"
    alias_to_canon: dict = {}
    variants: set = set()
    am = re.search(r"## Aliases.*", header, re.S)
    if am:
        for line in am.group(0).splitlines():
            m = re.match(r"-\s*`([^`]+)`\s*(?:←|<-)\s*(.+)", line)
            if m:
                canon = m.group(1)
                for v in re.findall(r"`([^`]+)`", m.group(2)):
                    alias_to_canon[v] = canon
                    variants.add(v)
    return header, alias_to_canon, variants


def harvest(canon) -> dict:
    used: dict = defaultdict(set)
    for f in glob.glob(str(WIKI / "**" / "*.md"), recursive=True):
        text = Path(f).read_text(encoding="utf-8")
        fm = re.search(r"^---\n(.*?)\n---", text, re.S)
        block = fm.group(1) if fm else ""
        for facet, cat in FACET_CAT.items():
            m = re.search(rf"(?m)^{facet}:\s*\[(.*?)\]", block)
            if m:
                for s in m.group(1).split(","):
                    s = s.strip().strip("\"'")
                    if s and SLUG_RE.fullmatch(s):
                        used[cat].add(canon(s))
        for cat_s, slug in re.findall(r"\[\[(concepts|strategies|securities|people)/([a-z0-9][a-z0-9-]*)", text):
            used[cat_s].add(canon(slug))
    return used


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Regenerate slugs.md canonical lists from wiki usage.")
    ap.add_argument("--check", action="store_true", help="report only; exit 1 if new slugs found")
    args = ap.parse_args(argv)

    text = SLUGS.read_text(encoding="utf-8")
    header, alias_to_canon, variants = parse_header_and_aliases(text)
    def canon(s: str) -> str: return alias_to_canon.get(s, s)

    # existing canonical slugs per section (to report what's new)
    existing: dict = defaultdict(set)
    for title, key in SECTION_ORDER:
        sec = re.search(rf"## {title}\n(.*?)(?:\n## |\Z)", text, re.S)
        if sec:
            for s in re.findall(r"-\s*`([^`]+)`", sec.group(1)):
                existing[key].add(s)

    used = harvest(canon)
    new = {k: sorted((used[k] - variants) - existing[k]) for _t, k in SECTION_ORDER}
    total_new = sum(len(v) for v in new.values())

    if args.check:
        print(f"sync_slugs --check: {total_new} new slug(s) not in registry")
        for _t, k in SECTION_ORDER:
            if new[k]:
                print(f"  {k}: {', '.join(new[k][:12])}{' …' if len(new[k]) > 12 else ''}")
        return 1 if total_new else 0

    out = header.rstrip() + "\n"
    for title, key in SECTION_ORDER:
        items = sorted(used[key] - variants)
        out += f"\n## {title}\n"
        if title in SECTION_NOTES:
            out += SECTION_NOTES[title] + "\n"
        out += "\n" + "\n".join(f"- `{x}`" for x in items) + "\n"
    SLUGS.write_text(out.rstrip() + "\n", encoding="utf-8")

    print(f"sync_slugs: registry regenerated from usage (+{total_new} new): "
          + ", ".join(f"{k}={len(used[k] - variants)}" for _t, k in SECTION_ORDER))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
