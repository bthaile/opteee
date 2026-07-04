#!/usr/bin/env python3
"""
ingest_wiki.py — OPTEEE LLM Wiki automated "source-pass".

For each video, read its processed transcript, de-noise the YouTube rolling-caption
repetition in Python (to save tokens/cost), then call an LLM to produce a
`wiki/sources/{video_id}.md` page conforming to WIKI_SCHEMA.md §2.

Authoritative conventions live in `schema/WIKI_SCHEMA.md` (esp. §2 source-page spec,
§4 controlled vocab, §5 slugs, §6 de-noising) and `schema/slugs.md` (the slug registry).
This script embeds those sections into the LLM prompt so the extractor stays in sync.

Provider:
  - default: provider=claude, model=claude-haiku-4-5, via langchain_anthropic.ChatAnthropic
    (reads CLAUDE_API_KEY or ANTHROPIC_API_KEY).
  - --provider ollama uses langchain_ollama.ChatOllama (reads OLLAMA_BASE_URL).
  The provider libraries are imported LAZILY inside the call path so that --self-test
  and --dry-run work with no libraries or API keys installed.

  ⚠️  `langchain-anthropic` (and `langchain-ollama` for the ollama provider) must be present
  in the pipeline venv — see requirements.txt (langchain-anthropic is already pinned there).

CLI (see --help):
  --new-only (DEFAULT)  only videos with a processed transcript and NO existing source page
  --force               redo existing source pages too
  --video ID            operate on a single video
  --limit N             cap the selection
  --provider / --model  override the LLM
  --dry-run             print the selection plan; make no LLM calls, write nothing
  --self-test           denoise + prompt-build + frontmatter-validate + file-write using a
                        CANNED LLM response (no API/keys); writes to a throwaway temp path

Idempotent: re-running with --new-only is a no-op when nothing is new.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

# Load .env so CLAUDE_API_KEY/ANTHROPIC_API_KEY are available in the automated weekly
# pipeline (the other pipeline scripts load_dotenv() too). Optional; a no-op if absent.
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

# --------------------------------------------------------------------------------------
# Paths (repo root = parent of this scripts/ directory)
# --------------------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "processed_transcripts"
METADATA_PATH = REPO_ROOT / "outlier_trading_videos_metadata.json"
SOURCES_DIR = REPO_ROOT / "wiki" / "sources"
SLUGS_PATH = REPO_ROOT / "schema" / "slugs.md"
SCHEMA_PATH = REPO_ROOT / "schema" / "WIKI_SCHEMA.md"

PROCESSED_SUFFIX = "_processed.json"

DEFAULT_PROVIDER = "claude"
DEFAULT_MODEL = "claude-haiku-4-5"
MAX_OUTPUT_TOKENS = 4096

# Frontmatter keys that MUST be present on every source page (the example prototype page
# wiki/sources/AJP8M8DQ_1U.md carries exactly these core keys; mentions/saga/part are
# optional and omitted when unused).
REQUIRED_FRONTMATTER_KEYS = [
    "type",
    "title",
    "video_id",
    "url",
    "date",
    "series",
    "format",
    "confidence",
]

# Bad LLM outputs go here (Hardening §15 #3) — never left in wiki/sources/ where they
# would poison the lint gate. Isolated from the knowledge folders + git (see .gitignore).
QUARANTINE_DIR = REPO_ROOT / "wiki" / "_quarantine"

# Controlled vocabularies (WIKI_SCHEMA §4) — closed sets the extractor must respect.
VALID_SERIES = {
    "options-trench", "outlier-podcast", "beginner-lab", "project-no-code",
    "market-update", "meme-stock-watch", "gme-analysis", "small-stacks",
    "stock-watch", "money-talks", "unhedged", "none",
}
VALID_FORMAT = {"education", "interview", "market-note", "live", "analysis", "strategy-breakdown"}
VALID_SUBTYPE = {"mechanic", "mental-model", "process"}

# De-noise tuning: longest repeated word n-gram to collapse. YouTube caption chunks are
# short (typically 3-8 words); 15 gives comfortable headroom without over-merging.
DENOISE_MAX_WINDOW = 15


# --------------------------------------------------------------------------------------
# De-noising
# --------------------------------------------------------------------------------------
def denoise(text: str, max_window: int = DENOISE_MAX_WINDOW) -> str:
    """Collapse the YouTube rolling-caption repetition.

    Auto-captions repeat each phrase 2-3x across overlapping windows. This greedily
    walks the word stream and, whenever the next run of words exactly duplicates the
    run just emitted (largest window first), skips it. That collapses immediately-
    repeated word n-grams / consecutive duplicate lines while leaving genuine text
    intact. Robust to partial (sliding) window overlap, not just whole-line triples.
    """
    if not text:
        return ""
    words = text.split()
    n = len(words)
    out: list[str] = []
    i = 0
    while i < n:
        matched = False
        # Try the largest possible repeat window first so we skip the full repeated
        # phrase rather than a spurious short sub-match.
        w_max = min(max_window, len(out), n - i)
        for w in range(w_max, 0, -1):
            if out[-w:] == words[i : i + w]:
                i += w  # the next w words duplicate the tail we already have — skip them
                matched = True
                break
        if not matched:
            out.append(words[i])
            i += 1
    return " ".join(out)


# --------------------------------------------------------------------------------------
# Loading transcripts + metadata
# --------------------------------------------------------------------------------------
def list_processed_ids() -> list[str]:
    """All video_ids that have a processed transcript, sorted."""
    if not PROCESSED_DIR.is_dir():
        return []
    ids = []
    for p in PROCESSED_DIR.glob(f"*{PROCESSED_SUFFIX}"):
        ids.append(p.name[: -len(PROCESSED_SUFFIX)])
    return sorted(ids)


def list_source_ids() -> set[str]:
    """All video_ids that already have a wiki source page."""
    if not SOURCES_DIR.is_dir():
        return set()
    return {p.stem for p in SOURCES_DIR.glob("*.md")}


def processed_path(video_id: str) -> Path:
    return PROCESSED_DIR / f"{video_id}{PROCESSED_SUFFIX}"


def load_transcript(video_id: str) -> list[dict]:
    """Load the processed transcript (a JSON list of chunk dicts)."""
    with open(processed_path(video_id), "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{processed_path(video_id)} is not a JSON list")
    return data


def load_metadata_map() -> dict[str, dict]:
    """Map video_id -> metadata dict from outlier_trading_videos_metadata.json."""
    if not METADATA_PATH.exists():
        return {}
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = {}
    for m in data:
        vid = m.get("video_id")
        if vid:
            out[vid] = m
    return out


def _yyyymmdd_to_iso(raw) -> str:
    """Convert 'YYYYMMDD' -> 'YYYY-MM-DD'. Pass through anything already dashed/blank."""
    if not raw:
        return ""
    s = str(raw)
    if re.fullmatch(r"\d{8}", s):
        return f"{s[0:4]}-{s[4:6]}-{s[6:8]}"
    return s


def resolve_video_meta(video_id: str, chunks: list[dict], metadata_map: dict) -> dict:
    """Resolve title/date/url for a video.

    Title comes from the transcript's `title` field (per the task). Date/url prefer the
    metadata file, falling back to fields carried on the transcript chunks themselves.
    """
    first = chunks[0] if chunks else {}
    meta = metadata_map.get(video_id, {})

    title = (first.get("title") or meta.get("title") or "").strip()

    date = _yyyymmdd_to_iso(meta.get("upload_date")) or _yyyymmdd_to_iso(
        first.get("upload_date")
    )

    url = (
        meta.get("url")
        or first.get("video_url")
        or f"https://www.youtube.com/watch?v={video_id}"
    )

    return {"video_id": video_id, "title": title, "date": date, "url": url}


def build_transcript_text(chunks: list[dict]) -> str:
    """Build a timestamped, de-noised transcript to feed the LLM.

    Each chunk is de-noised independently (the dominant caption repetition is intra-chunk)
    and prefixed with its [mm:ss] start timestamp so the LLM can cite timestamps in the
    Key takeaways / quotes sections.
    """
    lines = []
    for c in chunks:
        ts = c.get("start_timestamp") or ""
        cleaned = denoise(c.get("text", ""))
        if not cleaned:
            continue
        prefix = f"[{ts}] " if ts else ""
        lines.append(f"{prefix}{cleaned}")
    return "\n".join(lines)


# --------------------------------------------------------------------------------------
# Schema / slug loading for the prompt
# --------------------------------------------------------------------------------------
def _extract_schema_section(schema_text: str, header_prefix: str) -> str:
    """Extract a top-level '## N.' section (up to the next top-level '## ' header)."""
    lines = schema_text.splitlines()
    out: list[str] = []
    capturing = False
    for line in lines:
        if capturing:
            if line.startswith("## ") and not line.startswith(header_prefix):
                break
            out.append(line)
        elif line.startswith(header_prefix):
            capturing = True
            out.append(line)
    return "\n".join(out).strip()


def load_schema_excerpts() -> dict:
    """Load §2 (source pages), §4 (controlled vocab), §6 (de-noising) from WIKI_SCHEMA."""
    schema_text = SCHEMA_PATH.read_text(encoding="utf-8")
    return {
        "section2": _extract_schema_section(schema_text, "## 2."),
        "section4": _extract_schema_section(schema_text, "## 4."),
        "section6": _extract_schema_section(schema_text, "## 6."),
    }


def load_slug_registry() -> str:
    """The full slug registry text, embedded verbatim into the prompt."""
    return SLUGS_PATH.read_text(encoding="utf-8")


# --------------------------------------------------------------------------------------
# Prompt construction
# --------------------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are the OPTEEE wiki source-pass extractor. You read one options-trading video "
    "transcript and emit a single Markdown 'source page' that conforms EXACTLY to the "
    "WIKI_SCHEMA §2 template supplied below.\n\n"
    "Hard rules:\n"
    "1. Output ONLY the Markdown page — starting with the '---' frontmatter and ending "
    "with the last body section. No preamble, no explanation, no code fences.\n"
    "2. Use ONLY slugs that appear in the supplied slug registry (canonical or alias) for "
    "every frontmatter facet and [[wikilink]]. If a genuinely needed concept/strategy/"
    "security/person is missing from the registry, add a final section titled "
    "'## Proposed new slugs' listing each as `category: proposed-slug — one-line rationale`, "
    "and do NOT invent unlisted slugs anywhere else.\n"
    "3. Apply the §6 de-noising rules: read the de-noised transcript for meaning, never "
    "reproduce caption repetition, treat live numeric figures as approximate (they are "
    "frequently ASR-garbled), and only include a line under '## Notable quotes' if you can "
    "reconstruct it verbatim with confidence (0-3 quotes; omit the section if the text is "
    "too garbled).\n"
    "4. Fill the frontmatter honestly: series/format from the §4 controlled vocabulary, "
    "host default expert `eric`, confidence reflecting transcript quality."
)


def build_prompt(meta: dict, transcript_text: str, schema: dict, slug_registry: str) -> str:
    """Assemble the human-turn prompt (returned as a single string)."""
    parts = [
        "# WIKI_SCHEMA §2 — Source-page template (produce a page in EXACTLY this shape)",
        schema["section2"],
        "",
        "# WIKI_SCHEMA §4 — Controlled vocabularies (series / format / subtype)",
        schema["section4"],
        "",
        "# WIKI_SCHEMA §6 — De-noising & exact-quote rules",
        schema["section6"],
        "",
        "# Slug registry (schema/slugs.md) — use ONLY these slugs (canonical or alias)",
        slug_registry,
        "",
        "# Video metadata (use these verbatim in the frontmatter)",
        f"title: {meta['title']}",
        f"video_id: {meta['video_id']}",
        f"url: {meta['url']}",
        f"date: {meta['date']}",
        "",
        "# De-noised transcript (timestamps are [mm:ss] you may cite; numbers are approximate)",
        transcript_text,
        "",
        "# Task",
        "Produce the complete Markdown source page now, following the §2 template exactly. "
        "Begin with the '---' frontmatter line.",
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------------------
# LLM call (lazy imports)
# --------------------------------------------------------------------------------------
def call_llm(system_prompt: str, human_prompt: str, provider: str, model: str) -> str:
    """Invoke the configured LLM and return the raw text content.

    Imports the provider library lazily so --self-test / --dry-run never need it.
    """
    messages = [("system", system_prompt), ("human", human_prompt)]

    if provider == "claude":
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError as e:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "langchain-anthropic is required for --provider claude. "
                "Install it into the pipeline venv (see requirements.txt)."
            ) from e
        api_key = os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "No API key found: set CLAUDE_API_KEY or ANTHROPIC_API_KEY."
            )
        llm = ChatAnthropic(
            model=model,
            api_key=api_key,
            temperature=0,
            max_tokens=MAX_OUTPUT_TOKENS,
        )
    elif provider == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError as e:  # pragma: no cover - environment dependent
            raise RuntimeError(
                "langchain-ollama is required for --provider ollama."
            ) from e
        base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        llm = ChatOllama(model=model, base_url=base_url, temperature=0)
    else:
        raise ValueError(f"Unknown provider: {provider}")

    resp = llm.invoke(messages)
    content = getattr(resp, "content", resp)
    if isinstance(content, list):
        # Some chat models return a list of content blocks.
        content = "".join(
            b.get("text", "") if isinstance(b, dict) else str(b) for b in content
        )
    return str(content)


# --------------------------------------------------------------------------------------
# Output cleaning + validation
# --------------------------------------------------------------------------------------
def strip_code_fences(text: str) -> str:
    """Strip an outer ```markdown / ``` fence if the model wrapped the page in one."""
    s = text.strip()
    if s.startswith("```"):
        lines = s.splitlines()
        # drop the opening fence line
        lines = lines[1:]
        # drop a trailing fence line if present
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        s = "\n".join(lines).strip()
    return s


def extract_frontmatter(page: str) -> str | None:
    """Return the raw text between the leading '---' fences, or None if absent."""
    s = page.lstrip()
    if not s.startswith("---"):
        return None
    lines = s.splitlines()
    # lines[0] is the opening '---'
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx])
    return None


def validate_frontmatter(page: str, required_keys=REQUIRED_FRONTMATTER_KEYS) -> tuple[bool, list[str]]:
    """Check the page opens with frontmatter containing every required key.

    Uses a light regex per key (`^key:`) rather than a YAML dependency so --self-test
    runs with no third-party libraries.
    """
    fm = extract_frontmatter(page)
    if fm is None:
        return False, list(required_keys)
    missing = []
    for key in required_keys:
        if not re.search(rf"(?m)^{re.escape(key)}\s*:", fm):
            missing.append(key)
    return (len(missing) == 0), missing


def normalize_title_inline(page: str) -> str:
    """Quote an unquoted `title:` value so the frontmatter is valid YAML (inline self-heal,
    matching scripts/normalize_frontmatter.py so ingest writes valid pages directly)."""
    m = re.search(r"(?ms)^---\n(.*?)\n---", page)
    if not m:
        return page
    fm = m.group(1)

    def repl(mt):
        prefix, val = mt.group(1), mt.group(2).strip()
        if not val or (val[0] == '"' and val[-1] == '"') or (val[0] == "'" and val[-1] == "'"):
            return mt.group(0)
        val = val.replace("\\", "\\\\").replace('"', '\\"')
        return prefix + '"' + val + '"'

    new_fm = re.sub(r"(?m)^(title:[ \t]*)(.*?)[ \t]*$", repl, fm, count=1)
    if new_fm == fm:
        return page
    return page[: m.start(1)] + new_fm + page[m.end(1) :]


def validate_page(page: str) -> tuple[bool, list[str]]:
    """Validate a generated page before writing (Hardening §15 #2): required keys,
    parseable YAML frontmatter, and controlled series/format/subtype values."""
    problems: list[str] = []
    ok_keys, missing = validate_frontmatter(page)
    if not ok_keys:
        problems.append(f"missing frontmatter keys: {missing}")
    m = re.search(r"(?ms)^---\n(.*?)\n---", page)
    fm_text = m.group(1) if m else ""
    data: dict = {}
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(fm_text) if fm_text else None
        if isinstance(loaded, dict):
            data = loaded
        else:
            problems.append("frontmatter is not a valid YAML mapping")
    except Exception as e:  # invalid YAML (e.g. unquoted colon that survived normalize)
        problems.append(f"invalid YAML frontmatter: {str(e)[:60]}")

    series = data.get("series")
    if series is not None and str(series) not in VALID_SERIES:
        problems.append(f"invalid series: {series!r}")
    fmt = data.get("format")
    fmts = fmt if isinstance(fmt, list) else ([fmt] if fmt is not None else [])
    bad_fmt = [f for f in fmts if str(f) not in VALID_FORMAT]
    if bad_fmt:
        problems.append(f"invalid format value(s): {bad_fmt}")
    subtype = data.get("subtype")
    if subtype is not None and str(subtype) not in VALID_SUBTYPE:
        problems.append(f"invalid subtype: {subtype!r}")
    return (len(problems) == 0), problems


def quarantine_page(video_id: str, page: str, problems: list[str]) -> Path:
    """Write a rejected page to wiki/_quarantine/ + append to its log (Hardening §15 #3)."""
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
    path = QUARANTINE_DIR / f"{video_id}.md"
    path.write_text(page.rstrip() + "\n", encoding="utf-8")
    with (QUARANTINE_DIR / "_log.txt").open("a", encoding="utf-8") as f:
        f.write(f"{video_id}\t{'; '.join(problems)}\n")
    return path


def source_page_path(video_id: str) -> Path:
    return SOURCES_DIR / f"{video_id}.md"


def write_source_page(video_id: str, page: str, out_dir: Path | None = None) -> Path:
    out_dir = out_dir or SOURCES_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{video_id}.md"
    body = page.rstrip() + "\n"
    path.write_text(body, encoding="utf-8")
    return path


# --------------------------------------------------------------------------------------
# Selection
# --------------------------------------------------------------------------------------
def select_videos(args, processed_ids: list[str], source_ids: set[str]) -> list[str]:
    if args.video:
        if args.video not in processed_ids:
            print(
                f"ERROR: no processed transcript for --video {args.video} "
                f"(expected {processed_path(args.video)})",
                file=sys.stderr,
            )
            return []
        candidates = [args.video]
    else:
        candidates = processed_ids

    if args.force:
        selected = list(candidates)
    else:
        selected = [v for v in candidates if v not in source_ids]

    # Shard i/N: deterministic disjoint slice by index, for running parallel workers.
    shard = getattr(args, "shard", None)
    if shard:
        i, n = shard
        selected = [v for idx, v in enumerate(selected) if idx % n == i]

    if args.limit is not None:
        selected = selected[: args.limit]
    return selected


# --------------------------------------------------------------------------------------
# Self-test (no API, no keys, no libs)
# --------------------------------------------------------------------------------------
CANNED_PAGE_TEMPLATE = """---
type: source
title: "{title}"
video_id: "{video_id}"
url: "{url}"
date: "{date}"
series: none
format: [education]
experts: [eric]
mentions: []
securities: []
concepts: [implied-volatility]
strategies: [short-premium]
saga: none
part: null
confidence: medium
---

# {title}

## Summary
Canned self-test summary. This page exercises the write + frontmatter-validation path.

## Key takeaways
- A de-noised takeaway with a timestamp. [00:00]

## Candidate wiki links
- concepts: [[concepts/implied-volatility]]
- strategies: [[strategies/short-premium]]

## Regime / context
- Self-test fixture; not a real extraction.
"""


def _pick_self_test_video(processed_ids: list[str]) -> str | None:
    if "AJP8M8DQ_1U" in processed_ids:
        return "AJP8M8DQ_1U"
    return processed_ids[0] if processed_ids else None


def run_self_test() -> int:
    print("=== ingest_wiki self-test (no API / no keys required) ===\n")
    failures = 0

    processed_ids = list_processed_ids()
    metadata_map = load_metadata_map()
    schema = load_schema_excerpts()
    slug_registry = load_slug_registry()

    # ---- 1. denoise on a real transcript --------------------------------------------
    vid = _pick_self_test_video(processed_ids)
    if vid is None:
        print("  [FAIL] no processed transcripts found to test denoise")
        return 1
    chunks = load_transcript(vid)
    raw_full = " ".join(c.get("text", "") for c in chunks)
    denoised_full = denoise(raw_full)
    raw_wc = len(raw_full.split())
    den_wc = len(denoised_full.split())
    ratio = (den_wc / raw_wc) if raw_wc else 0.0
    print(f"  denoise on {vid}: raw words={raw_wc}  denoised words={den_wc}  "
          f"kept={ratio:.1%}  collapsed={1 - ratio:.1%}")
    if den_wc >= raw_wc or den_wc == 0:
        print("  [FAIL] denoise did not collapse the transcript")
        failures += 1
    else:
        print("  [PASS] denoise collapsed the rolling-caption repetition\n")

    # tiny synthetic sanity check
    synth = "hello world hello world hello world foo bar foo bar"
    synth_out = denoise(synth)
    if synth_out == "hello world foo bar":
        print(f"  [PASS] denoise synthetic: {synth!r} -> {synth_out!r}\n")
    else:
        print(f"  [FAIL] denoise synthetic: {synth!r} -> {synth_out!r} "
              "(expected 'hello world foo bar')\n")
        failures += 1

    # ---- 2. prompt build -------------------------------------------------------------
    meta = resolve_video_meta(vid, chunks, metadata_map)
    transcript_text = build_transcript_text(chunks)
    prompt = build_prompt(meta, transcript_text, schema, slug_registry)
    checks = [
        ("§2 template", "type: source" in prompt),
        ("§4 vocab", "market-update" in prompt),
        ("§6 rules", "Notable quotes" in prompt or "verbatim" in prompt),
        ("slug registry", "covered-strangle" in prompt),
        ("video title", meta["title"] in prompt if meta["title"] else True),
        ("de-noised transcript", len(transcript_text) > 0),
    ]
    ok = all(v for _, v in checks)
    for name, v in checks:
        print(f"    {'ok ' if v else 'MISS'} prompt contains {name}")
    if ok:
        print("  [PASS] prompt embeds schema template, vocab, rules, and slug registry\n")
    else:
        print("  [FAIL] prompt missing required content\n")
        failures += 1

    # ---- 3. canned LLM response -> validate -> write (throwaway path) -----------------
    canned = CANNED_PAGE_TEMPLATE.format(
        title=meta["title"] or "Self Test Video",
        video_id=meta["video_id"],
        url=meta["url"],
        date=meta["date"] or "2025-01-01",
    )
    # simulate a model that wrapped output in a code fence
    canned_fenced = "```markdown\n" + canned + "\n```"
    cleaned = strip_code_fences(canned_fenced)
    valid, missing = validate_frontmatter(cleaned)
    if valid:
        print("  [PASS] frontmatter validation accepts the canned page")
    else:
        print(f"  [FAIL] frontmatter validation rejected valid page; missing={missing}")
        failures += 1

    # negative case: a page missing a required key must be rejected
    bad_page = cleaned.replace("confidence: medium\n", "")
    bad_valid, bad_missing = validate_frontmatter(bad_page)
    if (not bad_valid) and ("confidence" in bad_missing):
        print("  [PASS] frontmatter validation rejects a page missing 'confidence'")
    else:
        print(f"  [FAIL] frontmatter validation should have rejected missing 'confidence' "
              f"(valid={bad_valid}, missing={bad_missing})")
        failures += 1

    # write to a throwaway temp dir (NEVER touch real wiki/sources)
    tmp_dir = Path(tempfile.mkdtemp(prefix="ingest_wiki_selftest_"))
    written = write_source_page(meta["video_id"], cleaned, out_dir=tmp_dir)
    readback = written.read_text(encoding="utf-8")
    rb_valid, _ = validate_frontmatter(readback)
    real_page = source_page_path(meta["video_id"])
    if written.exists() and rb_valid and str(written) != str(real_page):
        print(f"  [PASS] wrote + re-validated throwaway page at {written}")
        print(f"         (did NOT overwrite real page {real_page})\n")
    else:
        print(f"  [FAIL] throwaway write/validate failed (path={written})\n")
        failures += 1

    print("=== self-test:", "PASS ===" if failures == 0 else f"FAIL ({failures}) ===")
    return 0 if failures == 0 else 1


# --------------------------------------------------------------------------------------
# Dry-run
# --------------------------------------------------------------------------------------
def run_dry_run(args, processed_ids, source_ids, selected) -> int:
    total = len(processed_ids)
    existing = len(source_ids)
    new_count = len([v for v in processed_ids if v not in source_ids])
    print("=== ingest_wiki dry-run (no LLM calls, nothing written) ===")
    print(f"  processed transcripts : {total}")
    print(f"  existing source pages : {existing}")
    print(f"  new (no source page)  : {new_count}")
    print(f"  provider/model        : {args.provider} / {args.model}")
    mode = "force (redo existing)" if args.force else "new-only (default)"
    if args.video:
        mode += f" | --video {args.video}"
    if args.limit is not None:
        mode += f" | --limit {args.limit}"
    print(f"  selection mode        : {mode}")
    print(f"  would process         : {len(selected)} video(s)")
    preview = selected[:20]
    for v in preview:
        print(f"      - {v}")
    if len(selected) > len(preview):
        print(f"      ... and {len(selected) - len(preview)} more")
    if not selected:
        print("  nothing to do (idempotent no-op).")
    return 0


# --------------------------------------------------------------------------------------
# Main processing loop
# --------------------------------------------------------------------------------------
def run_ingest(args, selected) -> int:
    metadata_map = load_metadata_map()
    schema = load_schema_excerpts()
    slug_registry = load_slug_registry()

    processed = skipped = errors = quarantined = 0

    for i, vid in enumerate(selected, 1):
        prefix = f"[{i}/{len(selected)}] {vid}"
        try:
            chunks = load_transcript(vid)
            if not chunks:
                print(f"{prefix}: SKIP (empty transcript)")
                skipped += 1
                continue

            meta = resolve_video_meta(vid, chunks, metadata_map)
            transcript_text = build_transcript_text(chunks)
            prompt = build_prompt(meta, transcript_text, schema, slug_registry)

            raw = call_llm(SYSTEM_PROMPT, prompt, args.provider, args.model)
            page = normalize_title_inline(strip_code_fences(raw))

            valid, problems = validate_page(page)
            if not valid:
                qpath = quarantine_page(vid, page, problems)
                print(f"{prefix}: QUARANTINED ({'; '.join(problems)}) -> {qpath}")
                quarantined += 1
                continue

            path = write_source_page(vid, page)
            print(f"{prefix}: OK -> {path}")
            processed += 1
        except Exception as e:  # noqa: BLE001 - one bad video shouldn't kill the run
            print(f"{prefix}: ERROR ({type(e).__name__}: {e})")
            errors += 1

    print("\n=== summary ===")
    print(f"  processed   : {processed}")
    print(f"  skipped     : {skipped}")
    print(f"  quarantined : {quarantined}")
    print(f"  errors      : {errors}")
    return 0 if errors == 0 else 1


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------
def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="OPTEEE wiki automated source-pass (WIKI_SCHEMA §2).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--new-only",
        action="store_true",
        help="only videos with a processed transcript and NO existing source page (DEFAULT)",
    )
    p.add_argument("--force", action="store_true", help="redo existing source pages too")
    p.add_argument("--video", metavar="ID", help="operate on a single video id")
    p.add_argument("--limit", type=int, metavar="N", help="cap the number of videos processed")
    p.add_argument(
        "--shard",
        metavar="i/N",
        help="process only shard i of N (0-indexed), e.g. 0/5 — run N workers in parallel",
    )
    p.add_argument("--provider", default=DEFAULT_PROVIDER, choices=["claude", "ollama"])
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"default: {DEFAULT_MODEL}")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="print the selection plan; make no LLM calls and write nothing",
    )
    p.add_argument(
        "--self-test",
        action="store_true",
        help="denoise + prompt-build + validate + throwaway write using a canned response",
    )
    return p


def main(argv=None) -> int:
    args = build_arg_parser().parse_args(argv)

    # Parse --shard "i/N" into a (i, n) tuple; validate.
    if getattr(args, "shard", None):
        try:
            i_str, n_str = str(args.shard).split("/")
            i, n = int(i_str), int(n_str)
            assert n > 0 and 0 <= i < n
            args.shard = (i, n)
        except Exception:
            print(f"ERROR: --shard must be 'i/N' with 0<=i<N (got {args.shard!r})", file=sys.stderr)
            return 2
    else:
        args.shard = None

    if args.self_test:
        return run_self_test()

    processed_ids = list_processed_ids()
    source_ids = list_source_ids()
    selected = select_videos(args, processed_ids, source_ids)

    if args.dry_run:
        return run_dry_run(args, processed_ids, source_ids, selected)

    if not selected:
        # idempotent no-op
        run_dry_run(args, processed_ids, source_ids, selected)
        return 0

    return run_ingest(args, selected)


if __name__ == "__main__":
    sys.exit(main())
