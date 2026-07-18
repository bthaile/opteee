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

Each generated page gets a real, grounded summary: an LLM (Haiku, same call path as
ingest_wiki) reads the `## Summary` sections of the topic's backing source pages — already
distilled, clean prose — and writes a 2-4 sentence description of the topic as this channel
teaches it. The summary lands in the page body AND in a `summary:` frontmatter field (so the
graph tooltip can show it). If no API key is set (or `--no-summary`), it degrades to the old
one-line placeholder so the soft pipeline step never breaks.

Runs in the pipeline after ingest and before annotate_chunks. Idempotent: never overwrites
an existing page (so hand-curated pages win). Aliases are resolved to canonical slugs.

    python scripts/build_topics.py                       # generate (+ summaries)
    python scripts/build_topics.py --dry-run             # report only, no LLM calls
    python scripts/build_topics.py --no-summary          # structural pages only (offline)
    python scripts/build_topics.py --force --only basis-adjustment,cost-basis   # refresh named auto pages
"""
from __future__ import annotations

import argparse
import datetime
import glob
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
SOURCES = WIKI / "sources"
SLUGS = ROOT / "schema" / "slugs.md"
TODAY = datetime.date.today().isoformat()

# When summarizing a topic, feed at most this many backing-source summaries to the LLM
# (strongest signal first). Bounds token cost; topics with hundreds of videos are common.
MAX_SOURCES_FOR_SUMMARY = 12
DEFAULT_PROVIDER = "claude"
DEFAULT_MODEL = "claude-haiku-4-5"

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


def yaml_scalar(s: str) -> str:
    """Collapse to one line and double-quote/escape for a valid YAML scalar."""
    s = re.sub(r"\s+", " ", str(s)).strip()
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return '"' + s + '"'


def read_source_summary(vid: str) -> str:
    """Return the `## Summary` prose of wiki/sources/<vid>.md (falls back to first body
    paragraph). Empty string if the page is missing/unreadable."""
    path = SOURCES / f"{vid}.md"
    if not path.is_file():
        return ""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return ""
    # strip frontmatter
    body = re.sub(r"(?s)^---\n.*?\n---\n", "", text, count=1)
    m = re.search(r"(?ms)^##\s+Summary\s*\n(.*?)(?=\n##\s|\Z)", body)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    # fallback: first non-heading paragraph
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if p and not p.startswith("#"):
            return re.sub(r"\s+", " ", p).strip()
    return ""


SUMMARY_SYSTEM = (
    "You write concise, encyclopedia-style summaries of options-trading topics for a "
    "knowledge wiki built from one trading channel's videos. Given how the channel discusses "
    "a topic across several videos, write a tight 2-4 sentence summary of what the topic IS "
    "and how it is used in options trading, grounded ONLY in the supplied material — do not "
    "invent specific numbers, dates, or claims. Output plain prose only: no heading, no "
    "preamble, no markdown, no bullet points, no first person."
)

SUMMARY_PERSON_SYSTEM = (
    "You write concise, encyclopedia-style bios of people interviewed on an options-trading "
    "channel. Given how a guest is discussed across several videos, write a tight 2-4 sentence "
    "summary of who they are and their distinctive views/approach as presented, grounded ONLY "
    "in the supplied material — do not invent biography. Output plain prose only: no heading, "
    "no preamble, no markdown, no first person."
)


def generate_summary(title: str, page_type: str, folder: str, related: list[str],
                     titles: dict, call_llm, provider: str, model: str) -> str | None:
    """Ask the LLM for a grounded topic summary from the backing source pages' summaries.

    Returns the summary text, or None on any failure / no usable material (caller then
    keeps the placeholder). `call_llm` is ingest_wiki.call_llm (lazy-imported by the caller).
    """
    blocks: list[str] = []
    for vid in related[:MAX_SOURCES_FOR_SUMMARY]:
        s = read_source_summary(vid)
        if s:
            vt = wiki_label(titles.get(vid, vid))
            blocks.append(f'- "{vt}": {s[:700]}')
    if not blocks:
        return None
    kind = "interviewed guest" if folder == "people" else f"{page_type} topic"
    human = (
        f'Topic: "{title}" (an options-trading {kind}).\n\n'
        f"Here is how it is discussed across {len(blocks)} video(s) in the corpus "
        "(each line is one video's summary):\n\n"
        + "\n".join(blocks)
        + f'\n\nWrite the 2-4 sentence summary of "{title}" now.'
    )
    system = SUMMARY_PERSON_SYSTEM if folder == "people" else SUMMARY_SYSTEM
    try:
        raw = call_llm(system, human, provider, model)
    except Exception:
        raise  # let the caller decide whether to disable summaries for the rest of the run
    text = re.sub(r"\s+", " ", str(raw)).strip()
    # guard against the model echoing a heading or wrapping in quotes/fences
    text = re.sub(r"^```.*?\n|```$", "", text).strip().strip('"').strip()
    if len(text) < 20:
        return None
    return text[:1200]


def render_page(page_type: str, folder: str, slug: str, related: list[str],
                titles: dict | None = None, summary: str | None = None) -> str:
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
    if summary:
        head.append(f"summary: {yaml_scalar(summary)}")
    if folder == "people":
        head.append("category: interviews")
        head.append("role: interviewed guest")
    head.append("---")
    body = [f"# {title}", ""]
    if summary:
        body.append(summary.strip())
        body.append("")
        body.append(
            f"*Auto-generated summary from {len(related)} source video(s); "
            "pending curated synthesis.*"
        )
    elif folder == "people":
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
    ap.add_argument("--no-summary", action="store_true",
                    help="skip LLM summaries; write structural placeholder pages only (offline)")
    ap.add_argument("--only", metavar="SLUGS",
                    help="comma-separated slug allowlist — only (re)generate these pages")
    ap.add_argument("--provider", default=DEFAULT_PROVIDER)
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"summary model (default {DEFAULT_MODEL})")
    for facet, (_folder, _typ, default) in CATS.items():
        ap.add_argument(f"--min-{facet}", type=int, default=default,
                        help=f"min videos for a {facet} page (default {default})")
    args = ap.parse_args(argv)

    only = {s.strip() for s in args.only.split(",")} if args.only else None

    # Lazy-load the LLM call path once (loads .env). Summaries degrade to placeholders if
    # the key/library is missing, so the soft pipeline step never fails on this.
    summarize = not (args.no_summary or args.dry_run)
    call_llm = None
    if summarize:
        try:
            sys.path.insert(0, str(ROOT / "scripts"))
            import ingest_wiki  # provides call_llm() + loads .env
            call_llm = ingest_wiki.call_llm
        except Exception as e:  # noqa: BLE001
            print(f"  (summaries disabled: could not load LLM path: {type(e).__name__}: {e})")
            summarize = False

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

    created = skipped = summarized = summ_failed = 0
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
            if only is not None and slug not in only:
                continue
            path = outdir / f"{slug}.md"
            if path.exists():
                # never overwrite curated pages; with --force, refresh auto-generated ones
                is_auto = "auto_generated: true" in path.read_text(encoding="utf-8")
                if not (args.force and is_auto):
                    skipped += 1
                    continue
            related = sorted(vids)
            # Strongest signal first for the summary: videos this topic recurs across most.
            summary = None
            if summarize and call_llm is not None:
                try:
                    summary = generate_summary(prettify(slug, folder), page_type, folder,
                                               related, titles, call_llm, args.provider, args.model)
                    if summary:
                        summarized += 1
                    else:
                        summ_failed += 1
                except Exception as e:  # noqa: BLE001 — key/quota/etc: stop trying, keep going
                    print(f"  (summary for {folder}/{slug} failed: {type(e).__name__}: {e}; "
                          "disabling summaries for the rest of this run)")
                    summarize = False
                    summ_failed += 1
            page = render_page(page_type, folder, slug, related, titles, summary)
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
    if summarize or summarized or summ_failed:
        print(f"  summaries: {summarized} written, {summ_failed} fell back to placeholder")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
