#!/usr/bin/env python3
"""
normalize_frontmatter.py — deterministic self-heal for wiki source-page frontmatter.

LLM extractors (Haiku) intermittently emit a `title:` value with an unquoted colon
(e.g. `title: GME Surges Towards $30: Options Breakdown`), which is invalid YAML and
fails the lint gate. This pass wraps any source-page `title:` value in double quotes
unless it is already quoted, escaping embedded double quotes. Idempotent.

Runs in the weekly pipeline right after ingest_wiki.py and before lint_wiki.py, so the
gate never trips on this recurring LLM formatting quirk. Also usable standalone:

    python scripts/normalize_frontmatter.py            # fix all source pages
    python scripts/normalize_frontmatter.py --check    # report only, exit 1 if any need fixing
"""
from __future__ import annotations

import argparse
import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "wiki" / "sources"

_FM_RE = re.compile(r"^(---\n)(.*?)(\n---)", re.S)
_TITLE_RE = re.compile(r"^(title:[ \t]*)(.*?)[ \t]*$", re.M)


def _needs_quoting(value: str) -> bool:
    v = value.strip()
    if not v:
        return False
    # Already a quoted scalar (double or single) -> leave as-is.
    if (v[0] == '"' and v[-1] == '"' and len(v) >= 2) or (
        v[0] == "'" and v[-1] == "'" and len(v) >= 2
    ):
        return False
    return True


def _quote_title(value: str) -> str:
    """Return a double-quoted, YAML-safe scalar for the title value."""
    v = value.strip()
    v = v.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{v}"'


def normalize_text(text: str) -> tuple[str, bool]:
    """Return (new_text, changed) with the frontmatter title quoted if needed."""
    fm_match = _FM_RE.match(text)
    if not fm_match:
        return text, False
    head, body, tail = fm_match.group(1), fm_match.group(2), fm_match.group(3)

    changed = False

    def repl(m: "re.Match") -> str:
        nonlocal changed
        prefix, value = m.group(1), m.group(2)
        if _needs_quoting(value):
            changed = True
            return prefix + _quote_title(value)
        return m.group(0)

    new_body = _TITLE_RE.sub(repl, body, count=1)
    if not changed:
        return text, False
    return text[: fm_match.start()] + head + new_body + tail + text[fm_match.end() :], True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Quote unquoted wiki source-page titles (self-heal).")
    ap.add_argument("--check", action="store_true", help="report only; exit 1 if any need fixing")
    args = ap.parse_args(argv)

    files = sorted(glob.glob(str(SOURCES / "*.md")))
    fixed = []
    for f in files:
        text = Path(f).read_text(encoding="utf-8")
        new_text, changed = normalize_text(text)
        if changed:
            fixed.append(f)
            if not args.check:
                Path(f).write_text(new_text, encoding="utf-8")

    verb = "would fix" if args.check else "fixed"
    print(f"normalize_frontmatter: {len(files)} source pages scanned, {verb} {len(fixed)}")
    for f in fixed[:10]:
        print(f"  - {Path(f).name}")
    if len(fixed) > 10:
        print(f"  ... and {len(fixed) - 10} more")
    if args.check and fixed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
