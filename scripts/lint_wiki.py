#!/usr/bin/env python3
"""lint_wiki.py — the OPTEEE LLM Wiki weekly build gate.

Validates ``wiki/`` against ``schema/WIKI_SCHEMA.md`` (§11 Lint rules) and the
canonical slug registry ``schema/slugs.md`` (§5). Exits non-zero when any
HARD-FAIL is present so the weekly pipeline stops before commit / reindex.

Spec implemented (WIKI_SCHEMA.md §11):

  HARD-FAIL (collect all, then exit 1 if any):
    * a ``[[wikilink]]`` whose slug is NOT registered in slugs.md (canonical or
      alias) — for categories concepts/strategies/securities/people. Links to
      ``sources/<id>`` and the bare ``[[index]]`` are exempt.
    * duplicate canonical pages for the same idea: two knowledge pages sharing an
      ``aliases:`` entry, or a page whose slug equals another page's alias.
    * a knowledge page (concepts/strategies/securities/people/macro/syntheses)
      with an empty body or missing required frontmatter keys
      (type, title, related_videos, last_updated).
    * malformed frontmatter, or an invalid series / format / subtype value
      (validated against the §4 controlled lists).

  WARN (reported, never fails unless --strict):
    * a ``[[wikilink]]`` to a registered slug that has no page yet (growth backlog),
    * a dangling ``[[sources/<id>]]`` to a video with no wiki/sources/<id>.md,
    * orphan knowledge pages (no inbound wikilink),
    * source pages with ``confidence: low``,
    * predictions past their ``deadline`` still ``status: open``,
    * concepts missing ``subtype``.

Usage:
    python scripts/lint_wiki.py [--root wiki] [--slugs schema/slugs.md]
                                [--strict] [--self-test] [--quiet]

Exit code: 0 if no hard-fails (warnings OK); 1 otherwise. ``--strict`` promotes
warnings to failures.
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import sys
import tempfile

# ---------------------------------------------------------------------------
# Optional PyYAML (present in the weekly .venv-native and the repo venvs). We
# degrade to a tiny built-in parser if it is missing so the gate still runs.
# ---------------------------------------------------------------------------
try:
    import yaml  # type: ignore

    _HAVE_YAML = True
except Exception:  # pragma: no cover - only when PyYAML absent
    yaml = None  # type: ignore
    _HAVE_YAML = False


# ---------------------------------------------------------------------------
# Controlled vocabularies (WIKI_SCHEMA.md §4)
# ---------------------------------------------------------------------------
SERIES_VALUES = {
    "options-trench", "outlier-podcast", "beginner-lab", "project-no-code",
    "market-update", "meme-stock-watch", "gme-analysis", "small-stacks",
    "stock-watch", "money-talks", "unhedged", "none",
}
FORMAT_VALUES = {
    "education", "interview", "market-note", "live", "analysis",
    "strategy-breakdown",
}
SUBTYPE_VALUES = {"mechanic", "mental-model", "process"}

# Folders that hold curated knowledge pages (§1 / §3).
KNOWLEDGE_CATEGORIES = {
    "concepts", "strategies", "securities", "people", "macro", "syntheses",
}
# Categories whose slugs are validated against the registry (§11 + task spec).
REGISTRY_CATEGORIES = {"concepts", "strategies", "securities", "people"}
# Required frontmatter keys on every knowledge page (§11 hard-fail list).
REQUIRED_KNOWLEDGE_KEYS = ("type", "title", "related_videos", "last_updated")

WIKILINK_RE = re.compile(r"\[\[([^\]]+?)\]\]")
# Inline `code` spans hold illustrative `[[wikilinks]]` in prose (e.g. schema
# examples) — strip them so they are not treated as real links.
INLINE_CODE_RE = re.compile(r"`[^`]*`")


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------
class Finding:
    __slots__ = ("severity", "kind", "path", "line", "message")

    def __init__(self, severity, kind, path, line, message):
        self.severity = severity  # "ERROR" | "WARN"
        self.kind = kind          # short machine label
        self.path = path          # display path (may be None)
        self.line = line          # int or None
        self.message = message

    def location(self):
        if self.path is None:
            return "-"
        if self.line:
            return "{}:{}".format(self.path, self.line)
        return self.path


# ---------------------------------------------------------------------------
# Frontmatter handling
# ---------------------------------------------------------------------------
def split_frontmatter(text):
    """Return (frontmatter_text, body) or (None, text) if no valid block.

    A valid block starts with a ``---`` line and ends with a ``---`` line.
    An unterminated opening ``---`` yields (None, text) -> caller treats as
    malformed.
    """
    if not text.startswith("---"):
        return None, text
    lines = text.split("\n")
    if lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm_text = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1:])
            return fm_text, body
    return None, text  # opened but never closed -> malformed


def _fallback_yaml(fm_text):
    """Minimal frontmatter parser for environments without PyYAML.

    Handles ``key: scalar``, ``key: [a, b, c]`` inline lists, and ``- item``
    block lists. Nested maps (e.g. predictions) are not fully expanded; this is
    an insurance path only — PyYAML is present in the weekly pipeline.
    """
    data = {}
    lines = fm_text.split("\n")
    i = 0
    key_re = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")
    while i < len(lines):
        raw = lines[i]
        i += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        m = key_re.match(raw)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val == "":
            # Possibly a block list / nested block following.
            items = []
            while i < len(lines) and re.match(r"^\s*-\s+", lines[i]):
                items.append(re.sub(r"^\s*-\s+", "", lines[i]).strip().strip('"\''))
                i += 1
            data[key] = items if items else None
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [x.strip().strip('"\'') for x in inner.split(",") if x.strip()] if inner else []
        else:
            data[key] = val.strip().strip('"\'')
    return data


def parse_frontmatter(fm_text):
    """Parse frontmatter text to a dict. Raises ValueError on malformed input."""
    if _HAVE_YAML:
        try:
            data = yaml.safe_load(fm_text)
        except Exception as exc:  # yaml.YAMLError and friends
            raise ValueError(str(exc))
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise ValueError("frontmatter is not a mapping")
        return data
    return _fallback_yaml(fm_text)


# ---------------------------------------------------------------------------
# Slug registry (schema/slugs.md)
# ---------------------------------------------------------------------------
def parse_registry(slugs_path):
    """Parse slugs.md -> (category_slugs, alias_to_canonical).

    ``category_slugs`` maps each of concepts/strategies/securities/people to a
    set of registered slugs (canonicals AND alias variants). ``alias_to_canonical``
    maps every variant to its canonical slug.
    """
    with open(slugs_path, "r", encoding="utf-8") as fh:
        text = fh.read()

    category_slugs = {c: set() for c in ("concepts", "strategies", "securities", "people")}
    alias_to_canonical = {}
    alias_pairs = []  # (canonical, [variants])

    current = None
    in_aliases = False
    bullet_re = re.compile(r"^-\s*`([^`]+)`")
    alias_re = re.compile(r"^-\s*`([^`]+)`\s*(?:←|<-|<=|&larr;)\s*(.+)$")

    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("## "):
            name = stripped[3:].strip().lower()
            in_aliases = name.startswith("alias")
            if name.startswith("concept"):
                current = "concepts"
            elif name.startswith("strateg"):
                current = "strategies"
            elif name.startswith("securit"):
                current = "securities"
            elif name.startswith("people"):
                current = "people"
            else:
                current = None
            continue
        if stripped.startswith("#"):
            continue
        if in_aliases:
            m = alias_re.match(stripped)
            if m:
                canon = m.group(1).strip()
                variants = re.findall(r"`([^`]+)`", m.group(2))
                alias_pairs.append((canon, variants))
            continue
        if current and stripped.startswith("- "):
            m = bullet_re.match(stripped)
            if m:
                category_slugs[current].add(m.group(1).strip())

    # Assign each alias pair to the category of its canonical. If the canonical
    # is not found in any category list, register the whole pair in every
    # category (lenient) so a registry-listed alias never triggers a false fail.
    for canon, variants in alias_pairs:
        cats = [c for c, s in category_slugs.items() if canon in s]
        target_cats = cats if cats else list(category_slugs.keys())
        for c in target_cats:
            category_slugs[c].add(canon)
            for v in variants:
                category_slugs[c].add(v)
        for v in variants:
            alias_to_canonical[v] = canon

    return category_slugs, alias_to_canonical


# ---------------------------------------------------------------------------
# Wiki page model
# ---------------------------------------------------------------------------
class Page:
    __slots__ = ("path", "rel", "category", "stem", "kind", "text",
                 "frontmatter", "body", "fm_error")

    def __init__(self, path, rel, category, stem, kind):
        self.path = path
        self.rel = rel
        self.category = category
        self.stem = stem
        self.kind = kind  # "knowledge" | "source" | "structural"
        self.text = ""
        self.frontmatter = None
        self.body = ""
        self.fm_error = None


def classify(rel_path):
    """Return (category, stem, kind) for a wiki-relative .md path."""
    parts = rel_path.split(os.sep)
    stem = os.path.splitext(parts[-1])[0]
    if len(parts) >= 2:
        category = parts[-2]
        if category == "sources":
            return category, stem, "source"
        if category in KNOWLEDGE_CATEGORIES:
            return category, stem, "knowledge"
    return None, stem, "structural"


def load_pages(wiki_root):
    pages = []
    for dirpath, _dirs, files in os.walk(wiki_root):
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, wiki_root)
            category, stem, kind = classify(rel)
            page = Page(full, rel, category, stem, kind)
            try:
                with open(full, "r", encoding="utf-8") as fh:
                    page.text = fh.read()
            except Exception as exc:
                page.fm_error = "could not read file: {}".format(exc)
                pages.append(page)
                continue
            fm_text, body = split_frontmatter(page.text)
            page.body = body
            if fm_text is None:
                page.frontmatter = None
                # Only knowledge/source pages are required to have frontmatter.
                if page.kind in ("knowledge", "source"):
                    page.fm_error = "missing or malformed frontmatter delimiters"
            else:
                try:
                    page.frontmatter = parse_frontmatter(fm_text)
                except ValueError as exc:
                    page.frontmatter = None
                    page.fm_error = "invalid YAML frontmatter: {}".format(exc)
            pages.append(page)
    return pages


def iter_wikilinks(page):
    """Yield (line_number, target, label) for each [[wikilink]] in the page."""
    for lineno, line in enumerate(page.text.split("\n"), start=1):
        line = INLINE_CODE_RE.sub(" ", line)
        for m in WIKILINK_RE.finditer(line):
            inner = m.group(1).strip()
            if "|" in inner:
                target, label = inner.split("|", 1)
                target = target.strip()
                label = label.strip()
            else:
                target, label = inner, None
            yield lineno, target, label


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


# ---------------------------------------------------------------------------
# Core linter
# ---------------------------------------------------------------------------
def run_lint(wiki_root, slugs_path, today=None):
    """Return a list of Finding objects for the given wiki root."""
    if today is None:
        today = datetime.date.today()
    findings = []

    category_slugs, alias_to_canonical = parse_registry(slugs_path)
    pages = load_pages(wiki_root)

    knowledge_pages = [p for p in pages if p.kind == "knowledge"]
    source_ids = {p.stem for p in pages if p.kind == "source"}

    # page_key -> True for every existing knowledge page (category/stem)
    knowledge_keys = {"{}/{}".format(p.category, p.stem) for p in knowledge_pages}

    def canonical(slug):
        return alias_to_canonical.get(slug, slug)

    def knowledge_page_exists(category, slug):
        canon = canonical(slug)
        if "{}/{}".format(category, canon) in knowledge_keys:
            return True
        # tolerate a page filed under the alias slug itself
        return "{}/{}".format(category, slug) in knowledge_keys

    # ----- frontmatter / body / vocab checks -------------------------------
    # collect alias declarations for duplicate detection
    alias_declarers = {}   # alias_value -> list[page_key]
    page_aliases = {}      # page_key -> set(alias)

    for page in knowledge_pages:
        page_key = "{}/{}".format(page.category, page.stem)

        if page.fm_error:
            findings.append(Finding("ERROR", "malformed-frontmatter", page.rel, 1,
                                    page.fm_error))
            continue  # cannot check keys/vocab without frontmatter

        fm = page.frontmatter or {}

        # required keys
        missing = [k for k in REQUIRED_KNOWLEDGE_KEYS
                   if k not in fm or fm.get(k) in (None, "", [])]
        if missing:
            findings.append(Finding("ERROR", "missing-frontmatter", page.rel, 1,
                                    "missing/empty required frontmatter key(s): {}"
                                    .format(", ".join(missing))))

        # empty body
        if not page.body.strip():
            findings.append(Finding("ERROR", "empty-body", page.rel, 1,
                                    "knowledge page has empty body"))

        # subtype (concepts): missing -> WARN, present-but-invalid -> ERROR
        if page.category == "concepts":
            subtype = fm.get("subtype")
            if subtype in (None, "", []):
                findings.append(Finding("WARN", "concept-no-subtype", page.rel, 1,
                                        "concept page missing `subtype` "
                                        "(mechanic|mental-model|process)"))
            elif str(subtype) not in SUBTYPE_VALUES:
                findings.append(Finding("ERROR", "invalid-subtype", page.rel, 1,
                                        "invalid subtype '{}' (must be one of {})"
                                        .format(subtype, sorted(SUBTYPE_VALUES))))

        # series / format validity (rare on knowledge pages, but validate if set)
        _check_series_format(fm, page, findings)

        # collect aliases
        aliases = set()
        for a in as_list(fm.get("aliases")):
            a = str(a).strip()
            if not a:
                continue
            aliases.add(a)
            alias_declarers.setdefault(a, []).append(page_key)
        page_aliases[page_key] = aliases

    # ----- source-page checks ---------------------------------------------
    for page in pages:
        if page.kind != "source":
            continue
        if page.fm_error:
            findings.append(Finding("ERROR", "malformed-frontmatter", page.rel, 1,
                                    page.fm_error))
            continue
        fm = page.frontmatter or {}
        _check_series_format(fm, page, findings)
        conf = fm.get("confidence")
        if conf is not None and str(conf).lower() == "low":
            findings.append(Finding("WARN", "low-confidence-source", page.rel, 1,
                                    "source page has confidence: low"))
        # predictions rarely live on source pages, but check if present
        _check_predictions(fm, page, today, findings)

    # ----- macro predictions ----------------------------------------------
    for page in knowledge_pages:
        if page.category == "macro" and not page.fm_error:
            _check_predictions(page.frontmatter or {}, page, today, findings)

    # ----- duplicate-canonical detection -----------------------------------
    # (a) two knowledge pages sharing an aliases entry
    for alias_value, declarers in sorted(alias_declarers.items()):
        uniq = sorted(set(declarers))
        if len(uniq) > 1:
            findings.append(Finding("ERROR", "duplicate-alias", None, None,
                                    "alias '{}' is declared by multiple pages: {} "
                                    "(duplicate canonical for the same idea)"
                                    .format(alias_value, ", ".join(uniq))))

    # (b) a page whose slug equals another page's alias
    for page_key, aliases in sorted(page_aliases.items()):
        for other_key, other_aliases in page_aliases.items():
            if other_key == page_key:
                continue
            other_stem = other_key.split("/", 1)[1]
            if other_stem in aliases:
                findings.append(Finding("ERROR", "slug-equals-alias", None, None,
                                        "page '{}' declares alias '{}' which is the "
                                        "slug of page '{}' (duplicate canonical)"
                                        .format(page_key, other_stem, other_key)))

    # ----- wikilink validation + backlog / dangling / orphan ---------------
    inbound = {}  # knowledge page_key -> set(source rel paths, excluding self)

    for page in pages:
        for lineno, target, _label in iter_wikilinks(page):
            if target == "" or target == "index":
                continue  # bare [[index]] is exempt
            if "/" not in target:
                findings.append(Finding("WARN", "uncategorized-link", page.rel, lineno,
                                        "wikilink '[[{}]]' has no category prefix"
                                        .format(target)))
                continue
            category, slug = target.split("/", 1)
            category = category.strip()
            slug = slug.strip()

            if category == "sources":
                if slug not in source_ids:
                    findings.append(Finding("WARN", "dangling-source", page.rel, lineno,
                                            "[[sources/{}]] has no wiki/sources/{}.md "
                                            "(video not yet ingested)".format(slug, slug)))
                continue

            if category in REGISTRY_CATEGORIES:
                if slug not in category_slugs[category]:
                    findings.append(Finding("ERROR", "unregistered-slug", page.rel, lineno,
                                            "[[{}/{}]] slug not registered in slugs.md "
                                            "(canonical or alias)".format(category, slug)))
                    continue
                # registered -> record inbound for orphan check
                canon = canonical(slug)
                page_key = "{}/{}".format(category, canon)
                if page.rel != _rel_for_key(page_key):
                    inbound.setdefault(page_key, set()).add(page.rel)
                # backlog: registered slug but no page yet
                if not knowledge_page_exists(category, slug):
                    findings.append(Finding("WARN", "backlog-link", page.rel, lineno,
                                            "[[{}/{}]] is registered but has no page yet "
                                            "(growth backlog)".format(category, slug)))
                continue

            if category in KNOWLEDGE_CATEGORIES:
                # macro / syntheses: no slug registry -> only page-existence warn
                page_key = "{}/{}".format(category, slug)
                if page.rel != _rel_for_key(page_key):
                    inbound.setdefault(page_key, set()).add(page.rel)
                if page_key not in knowledge_keys:
                    findings.append(Finding("WARN", "backlog-link", page.rel, lineno,
                                            "[[{}/{}]] has no page yet (growth backlog)"
                                            .format(category, slug)))
                continue

            # unknown category prefix
            findings.append(Finding("WARN", "unknown-category-link", page.rel, lineno,
                                    "wikilink '[[{}]]' uses unknown category '{}'"
                                    .format(target, category)))

    # ----- orphan knowledge pages -----------------------------------------
    for page in knowledge_pages:
        page_key = "{}/{}".format(page.category, page.stem)
        if not inbound.get(page_key):
            findings.append(Finding("WARN", "orphan-page", page.rel, 1,
                                    "orphan knowledge page (no inbound wikilink)"))

    return findings


def _rel_for_key(page_key):
    """Map a knowledge page_key (category/stem) to its wiki-relative .md path."""
    return page_key.replace("/", os.sep) + ".md"


def _check_series_format(fm, page, findings):
    series = fm.get("series")
    if series is not None:
        sval = str(series).strip()
        if sval and sval not in SERIES_VALUES:
            findings.append(Finding("ERROR", "invalid-series", page.rel, 1,
                                    "invalid series '{}' (see WIKI_SCHEMA §4)".format(sval)))
    if "format" in fm and fm.get("format") is not None:
        for f in as_list(fm.get("format")):
            fval = str(f).strip()
            if fval and fval not in FORMAT_VALUES:
                findings.append(Finding("ERROR", "invalid-format", page.rel, 1,
                                        "invalid format '{}' (see WIKI_SCHEMA §4)".format(fval)))


def _check_predictions(fm, page, today, findings):
    preds = fm.get("predictions")
    if not isinstance(preds, list):
        return
    for pred in preds:
        if not isinstance(pred, dict):
            continue
        status = str(pred.get("status", "")).strip().lower()
        deadline = pred.get("deadline")
        if status != "open" or deadline is None:
            continue
        dl = _to_date(deadline)
        if dl is not None and dl < today:
            findings.append(Finding("WARN", "stale-prediction", page.rel, 1,
                                    "prediction '{}' past deadline {} still status: open"
                                    .format(pred.get("claim", pred.get("who", "?")), dl)))


def _to_date(value):
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.datetime.strptime(str(value).strip(), "%Y-%m-%d").date()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def report(findings, wiki_root, strict, quiet=False):
    errors = [f for f in findings if f.severity == "ERROR"]
    warnings = [f for f in findings if f.severity == "WARN"]

    def sort_key(f):
        return (f.path or "", f.line or 0, f.kind)

    out = sys.stdout
    if not quiet:
        out.write("OPTEEE wiki lint — root: {}\n".format(wiki_root))
        out.write("=" * 72 + "\n")

        out.write("\nERRORS (hard-fails): {}\n".format(len(errors)))
        if errors:
            for f in sorted(errors, key=sort_key):
                out.write("  [{}] {} — {}\n".format(f.kind, f.location(), f.message))
        else:
            out.write("  (none)\n")

        out.write("\nWARNINGS: {}\n".format(len(warnings)))
        if warnings:
            # group by kind for readability
            by_kind = {}
            for f in warnings:
                by_kind.setdefault(f.kind, []).append(f)
            for kind in sorted(by_kind):
                group = by_kind[kind]
                out.write("  {} ({})\n".format(kind, len(group)))
                for f in sorted(group, key=sort_key):
                    out.write("    {} — {}\n".format(f.location(), f.message))
        else:
            out.write("  (none)\n")

        out.write("\n" + "-" * 72 + "\n")

    gate_fail = bool(errors) or (strict and bool(warnings))
    verdict = "FAIL" if gate_fail else "PASS"
    out.write("Summary: {} error(s), {} warning(s). GATE: {}{}\n".format(
        len(errors), len(warnings), verdict,
        " (--strict: warnings promoted to failures)" if strict else ""))
    return gate_fail


# ---------------------------------------------------------------------------
# Self-test — proves the hard-fail path without leaving artifacts behind.
# ---------------------------------------------------------------------------
def self_test(slugs_path):
    """Build a throwaway wiki with injected faults and confirm the linter flags
    them (unregistered slug, duplicate alias, empty/missing frontmatter,
    invalid series). Exit 0 if the linter behaves correctly, 1 otherwise."""
    tmp = tempfile.mkdtemp(prefix="lint_wiki_selftest_")
    try:
        os.makedirs(os.path.join(tmp, "concepts"))
        os.makedirs(os.path.join(tmp, "sources"))
        # A good page so the linker has a valid baseline + an inbound link.
        with open(os.path.join(tmp, "concepts", "delta.md"), "w", encoding="utf-8") as fh:
            fh.write("---\n"
                     "type: concept\n"
                     "title: \"Delta\"\n"
                     "subtype: mechanic\n"
                     "related_videos: [\"vid1\"]\n"
                     "last_updated: 2026-07-03\n"
                     "---\n\n"
                     "# Delta\n\nA good page linking [[concepts/theta]] and "
                     "[[concepts/not-a-real-slug]].\n")
        # A bad page: missing required keys + empty body + bad series.
        with open(os.path.join(tmp, "concepts", "bad.md"), "w", encoding="utf-8") as fh:
            fh.write("---\n"
                     "type: concept\n"
                     "series: not-a-series\n"
                     "aliases: [delta]\n"   # collides with delta.md slug
                     "---\n")
        findings = run_lint(tmp, slugs_path)
        kinds = {f.kind for f in findings if f.severity == "ERROR"}
        expected = {
            "unregistered-slug",   # [[concepts/not-a-real-slug]]
            "missing-frontmatter", # bad.md lacks title/related_videos/last_updated
            "empty-body",          # bad.md empty body
            "invalid-series",      # series: not-a-series
            "slug-equals-alias",   # bad.md aliases:[delta] == delta.md slug
        }
        missing = expected - kinds
        gate = report(findings, tmp, strict=False)
        print("\nSELF-TEST expected error kinds: {}".format(sorted(expected)))
        print("SELF-TEST observed error kinds:  {}".format(sorted(kinds)))
        if missing:
            print("SELF-TEST FAILED — linter did not catch: {}".format(sorted(missing)))
            return 1
        if not gate:
            print("SELF-TEST FAILED — gate did not fail on injected hard-fails")
            return 1
        print("SELF-TEST PASSED — all injected hard-fails detected; gate correctly FAILs.")
        return 0
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def default_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    return (os.path.join(repo_root, "wiki"),
            os.path.join(repo_root, "schema", "slugs.md"))


def main(argv=None):
    default_root, default_slugs = default_paths()
    parser = argparse.ArgumentParser(
        description="Lint the OPTEEE LLM wiki (weekly build gate).")
    parser.add_argument("--root", default=default_root,
                        help="wiki root directory (default: <repo>/wiki)")
    parser.add_argument("--slugs", default=default_slugs,
                        help="path to slugs.md registry (default: <repo>/schema/slugs.md)")
    parser.add_argument("--strict", action="store_true",
                        help="promote warnings to failures (exit 1 on any warning)")
    parser.add_argument("--quiet", action="store_true",
                        help="print only the summary line")
    parser.add_argument("--self-test", action="store_true",
                        help="run built-in fault-injection test and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test(args.slugs)

    if not os.path.isdir(args.root):
        sys.stderr.write("error: wiki root not found: {}\n".format(args.root))
        return 2
    if not os.path.isfile(args.slugs):
        sys.stderr.write("error: slug registry not found: {}\n".format(args.slugs))
        return 2

    findings = run_lint(args.root, args.slugs)
    gate_fail = report(findings, args.root, args.strict, quiet=args.quiet)
    return 1 if gate_fail else 0


if __name__ == "__main__":
    sys.exit(main())
