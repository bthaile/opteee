"""
wiki_service.py — Phase-2 browse/graph layer for the OPTEEE LLM Wiki.

Pure functions over the on-disk ``wiki/`` directory (no DB, no RAG, no network).
Backs the ``/wiki`` browser and the ``/api/wiki/*`` REST endpoints
(see schema/WIKI_SCHEMA.md §8 and §12).

Frontmatter parsing prefers PyYAML when available (correct for nested blocks
such as the macro ``predictions:`` list) and falls back to a small built-in
parser so the service works even where PyYAML is not installed.
"""

import html
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import markdown

# Project root is two parents up from app/services/wiki_service.py.
WIKI_DIR = (Path(__file__).resolve().parents[2] / "wiki")

# Knowledge-page buckets (folders). Source pages live under sources/ and are
# catalogued separately (they are not graph nodes — see §12).
KNOWLEDGE_CATEGORIES = [
    "concepts",
    "strategies",
    "securities",
    "people",
    "macro",
    "syntheses",
]

# [[category/slug]] or [[category/slug|label]] (also [[sources/id]]).
_WIKILINK_RE = re.compile(r"\[\[\s*([^\]\|]+?)\s*(?:\|\s*([^\]]+?)\s*)?\]\]")

try:  # PyYAML is a project dependency and present in the serve env.
    import yaml  # type: ignore

    _HAS_YAML = True
except Exception:  # pragma: no cover - fallback path
    _HAS_YAML = False


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------
def _split_frontmatter(text: str) -> (str, str):
    """Return (frontmatter_text, body). Empty frontmatter if none present."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[1], parts[2]
    return "", text


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    if (value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'"):
        return value[1:-1]
    low = value.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "none", "~"):
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def _split_inline_list(inner: str) -> List[str]:
    """Split ``a, b, "c, d"`` respecting quotes."""
    items: List[str] = []
    buf = ""
    quote: Optional[str] = None
    for ch in inner:
        if quote:
            buf += ch
            if ch == quote:
                quote = None
        elif ch in ('"', "'"):
            quote = ch
            buf += ch
        elif ch == ",":
            items.append(buf)
            buf = ""
        else:
            buf += ch
    if buf.strip():
        items.append(buf)
    return items


def _parse_value(value: str) -> Any:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(x) for x in _split_inline_list(inner)]
    return _parse_scalar(value)


def _simple_parse_frontmatter(fm_text: str) -> Dict[str, Any]:
    """Minimal YAML-ish parser: top-level ``key: value`` and ``- item`` blocks.

    Handles scalars, inline lists, and block lists of scalars. Deeply nested
    dict blocks are not reconstructed here (PyYAML handles those in the serve
    env); such a key is stored with its scalar/None value best-effort.
    """
    data: Dict[str, Any] = {}
    current_list_key: Optional[str] = None
    for raw_line in fm_text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        stripped = line.strip()
        # Block-list continuation: "  - item" under the previous key.
        if stripped.startswith("- ") or stripped == "-":
            if current_list_key is not None:
                item = stripped[1:].strip()
                data.setdefault(current_list_key, [])
                if isinstance(data[current_list_key], list):
                    data[current_list_key].append(_parse_scalar(item))
            continue
        if ":" not in line:
            continue
        # Only treat leading (unindented) keys as top-level.
        if line[0] in (" ", "\t"):
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest == "":
            # Could be the start of a block list; mark it and default to [].
            data[key] = []
            current_list_key = key
        else:
            data[key] = _parse_value(rest)
            current_list_key = None
    return data


def _parse_frontmatter(fm_text: str) -> Dict[str, Any]:
    if _HAS_YAML:
        try:
            loaded = yaml.safe_load(fm_text)
            if isinstance(loaded, dict):
                return loaded
        except Exception:
            pass
    return _simple_parse_frontmatter(fm_text)


def _read_frontmatter(md_file: Path) -> Dict[str, Any]:
    try:
        text = md_file.read_text(encoding="utf-8")
    except Exception:
        return {}
    fm_text, _ = _split_frontmatter(text)
    return _parse_frontmatter(fm_text)


# ---------------------------------------------------------------------------
# Wikilink rendering
# ---------------------------------------------------------------------------
def _render_wikilinks(md_body: str) -> str:
    """Convert ``[[target]]`` / ``[[target|label]]`` into navigable anchors.

    The full target (e.g. ``concepts/volatility-risk-premium`` or
    ``sources/AJP8M8DQ_1U``) is preserved in ``data-page`` so the front-end can
    fetch the page; the visible label defaults to the final path segment.
    """

    def repl(match: "re.Match") -> str:
        target = match.group(1).strip()
        label = match.group(2)
        if label is not None:
            label = label.strip()
        else:
            label = target.split("/")[-1]
        return (
            f'<a href="#" class="wikilink" '
            f'data-page="{html.escape(target, quote=True)}">'
            f"{html.escape(label)}</a>"
        )

    return _WIKILINK_RE.sub(repl, md_body)


def _extract_wikilinks(md_body: str) -> List[Dict[str, str]]:
    """Return structured wikilinks for JSON/agent consumers."""
    links: List[Dict[str, str]] = []
    for match in _WIKILINK_RE.finditer(md_body):
        target = match.group(1).strip()
        label = (match.group(2) or target.split("/")[-1]).strip()
        category, _, slug = target.partition("/")
        links.append(
            {
                "target": target,
                "label": label,
                "category": category if slug else "",
                "slug": slug,
            }
        )
    return links


# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------
def _safe_page_path(rel_path: str) -> Optional[Path]:
    """Resolve ``rel_path`` to a ``.md`` file strictly under ``wiki/``.

    Returns ``None`` for anything outside wiki/ (path traversal), guarding
    against requests like ``../config.py``.
    """
    if rel_path is None:
        return None
    rel = rel_path.strip().strip("/")
    if not rel:
        return None
    if rel.endswith(".md"):
        rel = rel[:-3]
    wiki_root = WIKI_DIR.resolve()
    candidate = (wiki_root / (rel + ".md")).resolve()
    try:
        candidate.relative_to(wiki_root)
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    return candidate


def _rel_id(candidate: Path) -> str:
    """`.../wiki/concepts/foo.md` -> `concepts/foo`."""
    rel = candidate.resolve().relative_to(WIKI_DIR.resolve())
    return rel.with_suffix("").as_posix()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def get_graph() -> Dict[str, Any]:
    """Load ``wiki/graph.json``; return an empty graph if missing/invalid."""
    graph_file = WIKI_DIR / "graph.json"
    empty = {"nodes": [], "edges": []}
    if not graph_file.is_file():
        return empty
    try:
        data = json.loads(graph_file.read_text(encoding="utf-8"))
    except Exception:
        return empty
    if not isinstance(data, dict):
        return empty
    data.setdefault("nodes", [])
    data.setdefault("edges", [])
    return data


def list_index() -> Dict[str, Any]:
    """Catalog of knowledge pages plus the source-page list.

    Each knowledge page: ``{id, title, category, type, video_count}``.
    ``category`` is the folder bucket; ``type`` is the frontmatter ``type``.
    ``video_count`` is the length of ``related_videos``.
    """
    pages: List[Dict[str, Any]] = []
    for category in KNOWLEDGE_CATEGORIES:
        cat_dir = WIKI_DIR / category
        if not cat_dir.is_dir():
            continue
        for md_file in sorted(cat_dir.glob("*.md")):
            fm = _read_frontmatter(md_file)
            slug = md_file.stem
            related = fm.get("related_videos")
            video_count = len(related) if isinstance(related, list) else 0
            pages.append(
                {
                    "id": f"{category}/{slug}",
                    "title": fm.get("title") or slug,
                    "category": category,
                    "type": fm.get("type") or category.rstrip("s"),
                    "video_count": video_count,
                }
            )

    sources: List[Dict[str, Any]] = []
    src_dir = WIKI_DIR / "sources"
    if src_dir.is_dir():
        for md_file in sorted(src_dir.glob("*.md")):
            fm = _read_frontmatter(md_file)
            vid = md_file.stem
            sources.append(
                {
                    "id": f"sources/{vid}",
                    "video_id": fm.get("video_id") or vid,
                    "title": fm.get("title") or vid,
                    "date": fm.get("date"),
                    "series": fm.get("series"),
                }
            )

    return {
        "pages": pages,
        "sources": sources,
        "page_count": len(pages),
        "source_count": len(sources),
    }


def get_index_document(include_html: bool = False) -> Optional[Dict[str, Any]]:
    """Return generated ``wiki/index.md`` as structured JSON for agents."""
    index_file = WIKI_DIR / "index.md"
    if not index_file.is_file():
        return None
    try:
        text = index_file.read_text(encoding="utf-8")
    except Exception:
        return None
    fm_text, body = _split_frontmatter(text)
    result: Dict[str, Any] = {
        "path": "index",
        "frontmatter": _parse_frontmatter(fm_text),
        "markdown": body,
        "wikilinks": _extract_wikilinks(body),
    }
    if include_html:
        result["html"] = markdown.markdown(
            _render_wikilinks(body),
            extensions=["extra", "sane_lists"],
        )
    return result


def get_page(
    rel_path: str,
    include_markdown: bool = False,
    include_html: bool = True,
) -> Optional[Dict[str, Any]]:
    """Render a wiki page.

    Returns structured JSON or ``None`` when the page is missing or resolves
    outside ``wiki/`` (path traversal).
    """
    candidate = _safe_page_path(rel_path)
    if candidate is None:
        return None
    try:
        text = candidate.read_text(encoding="utf-8")
    except Exception:
        return None

    fm_text, body = _split_frontmatter(text)
    frontmatter = _parse_frontmatter(fm_text)
    result: Dict[str, Any] = {
        "path": _rel_id(candidate),
        "frontmatter": frontmatter,
        "wikilinks": _extract_wikilinks(body),
    }
    if include_markdown:
        result["markdown"] = body
    if include_html:
        result["html"] = markdown.markdown(
            _render_wikilinks(body),
            extensions=["extra", "sane_lists"],
        )
    return result


_STANDALONE_TEMPLATE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — OPTEEE Wiki</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         max-width: 760px; margin: 0 auto; padding: 24px 20px 64px; color: #1a1a1a; background: #fff; }}
  @media (prefers-color-scheme: dark) {{ body {{ color: #e6e6e6; background: #16181c; }} }}
  .wiki-nav {{ margin-bottom: 8px; }}
  .wiki-nav a {{ color: #0f766e; text-decoration: none; font-size: 14px; }}
  .wiki-meta {{ color: #6b7280; font-size: 13px; margin-bottom: 20px; }}
  .wiki-meta .tag {{ background: #0f766e1a; color: #0f766e; border-radius: 4px; padding: 1px 7px; margin-right: 6px; }}
  article h1, article h2, article h3 {{ line-height: 1.3; }}
  article code {{ background: #8881; padding: 1px 5px; border-radius: 4px; }}
  a.wikilink {{ color: #0f766e; border-bottom: 1px dotted #0f766e88; text-decoration: none; }}
  blockquote {{ border-left: 3px solid #0f766e55; margin: 1em 0; padding: 2px 0 2px 14px; color: #555; }}
  @media (prefers-color-scheme: dark) {{ blockquote {{ color: #aaa; }} }}
  table {{ border-collapse: collapse; }} td, th {{ border: 1px solid #8883; padding: 4px 8px; }}
</style></head><body>
<nav class="wiki-nav"><a href="/wiki">← Wiki graph</a></nav>
<div class="wiki-meta">{meta}</div>
<article>{body}</article>
</body></html>"""


def render_page_html(rel_path: str) -> Optional[str]:
    """Standalone HTML rendering of a wiki page (target of chat 'Wiki References' links).

    Wikilinks inside the page become real navigable links to other /wiki/page/ views.
    Returns None if the page is missing or resolves outside wiki/.
    """
    page = get_page(rel_path)
    if page is None:
        return None
    fm = page.get("frontmatter") or {}
    body = page.get("html") or ""
    # Turn the get_page() `<a href="#" data-page="X">` anchors into real navigable links.
    body = re.sub(
        r'<a href="#" class="wikilink" data-page="([^"]+)">',
        r'<a class="wikilink" href="/wiki/page/\1">',
        body,
    )
    bits: List[str] = []
    if fm.get("type"):
        bits.append(f'<span class="tag">{html.escape(str(fm["type"]))}</span>')
    rv = fm.get("related_videos")
    if isinstance(rv, list) and rv:
        bits.append(f"{len(rv)} source video(s)")
    if fm.get("confidence"):
        bits.append(f'confidence: {html.escape(str(fm["confidence"]))}')
    title = str(fm.get("title") or page.get("path") or rel_path)
    return _STANDALONE_TEMPLATE.format(title=html.escape(title), meta=" · ".join(bits), body=body)
