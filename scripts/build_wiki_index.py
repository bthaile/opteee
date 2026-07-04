#!/usr/bin/env python3
"""Build wiki/index.md from wiki/graph.json and wiki frontmatter.

The browser reads graph.json. This script creates the Markdown/LLM-readable
projection of that same graph so index.md does not drift into a stale hand
maintained catalog.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import quote


REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
GRAPH_PATH = WIKI_DIR / "graph.json"
OUTPUT_PATH = WIKI_DIR / "index.md"
SLUG_REGISTRY = REPO_ROOT / "schema" / "slugs.md"

KNOWLEDGE_FOLDERS = {
    "concepts": "concept",
    "strategies": "strategy",
    "securities": "security",
    "people": "person",
    "macro": "macro",
    "syntheses": "synthesis",
}

CATEGORY_ORDER = [
    ("concepts", "concept", "Concepts"),
    ("strategies", "strategy", "Strategies"),
    ("securities", "security", "Securities"),
    ("people", "person", "People"),
    ("macro", "macro", "Macro"),
    ("syntheses", "synthesis", "Syntheses"),
]

SOURCE_FACETS = {
    "concepts": ("concepts",),
    "strategies": ("strategies",),
    "securities": ("securities",),
    "people": ("experts", "mentions"),
}
REGISTRY_FOLDERS = set(SOURCE_FACETS)

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
FRONTMATTER_RE = re.compile(r"^\ufeff?---\s*\n(.*?)\n---\s*\n", re.DOTALL)

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional fallback
    yaml = None

try:
    from lint_wiki import parse_registry
except Exception:  # pragma: no cover - optional fallback
    parse_registry = None


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item) for item in split_inline_list(inner)]
    if value.lower() in {"true", "yes"}:
        return True
    if value.lower() in {"false", "no"}:
        return False
    return value


def split_inline_list(value: str) -> list[str]:
    parts: list[str] = []
    buf = ""
    quote = ""
    for char in value:
        if quote:
            buf += char
            if char == quote:
                quote = ""
        elif char in {"'", '"'}:
            quote = char
            buf += char
        elif char == ",":
            parts.append(buf.strip())
            buf = ""
        else:
            buf += char
    if buf.strip():
        parts.append(buf.strip())
    return parts


def simple_frontmatter(fm_text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw in fm_text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.strip()
        if stripped.startswith("- ") and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(parse_scalar(stripped[2:]))
            continue
        if raw[0] in {" ", "\t"} or ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        value = value.strip()
        if value:
            data[key] = parse_scalar(value)
            current_key = None
        else:
            data[key] = []
            current_key = key
    return data


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    fm_text = match.group(1)
    if yaml is not None:
        try:
            loaded = yaml.safe_load(fm_text)
            if isinstance(loaded, dict):
                return loaded, text[match.end():]
        except Exception:
            pass
    return simple_frontmatter(fm_text), text[match.end():]


def read_markdown(path: Path) -> tuple[dict[str, Any], str]:
    return split_frontmatter(path.read_text(encoding="utf-8"))


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()] if str(value).strip() else []


def strip_wikilinks(value: str) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        label = match.group(2)
        return (label or target.split("/")[-1]).strip()

    value = WIKILINK_RE.sub(replace, value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"[*_#>]+", "", value)
    return re.sub(r"\s+", " ", value).strip()


def md_cell(value: Any) -> str:
    return strip_wikilinks("" if value is None else str(value)).replace("|", "\\|")


def md_link_label(value: Any) -> str:
    return md_cell(value).replace("[", "\\[").replace("]", "\\]")


def truncate(value: str, limit: int = 180) -> str:
    value = value.strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def extract_section(body: str, headings: set[str]) -> str:
    lines = body.splitlines()
    start = None
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") and stripped[3:].strip().lower() in headings:
            start = idx + 1
            break
    if start is None:
        return ""
    collected: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        if line.strip():
            collected.append(line.strip())
        elif collected:
            break
    return strip_wikilinks(" ".join(collected))


def first_paragraph(body: str) -> str:
    collected: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            if collected:
                break
            continue
        collected.append(stripped)
    return strip_wikilinks(" ".join(collected))


def summarize(body: str, is_source: bool) -> str:
    headings = {"summary"} if is_source else {"summary", "definition", "structure"}
    summary = extract_section(body, headings) or first_paragraph(body)
    return truncate(summary or "No summary available.")


def wikilink(page_id: str, label: str | None = None) -> str:
    if label and label != page_id:
        return f"[[{page_id}|{label.replace('|', '/')}]]"
    return f"[[{page_id}]]"


def markdown_page_link(page_id: str, label: str | None = None) -> str:
    return f"[{md_link_label(label or page_id)}](/wiki/page/{quote(page_id, safe='/')})"


def registered_page_ids(registry: dict[str, set[str]]) -> set[str]:
    page_ids: set[str] = set()
    for folder, slugs in registry.items():
        page_ids.update(f"{folder}/{slug}" for slug in slugs)
    return page_ids


def page_ref(page_id: str, label: str | None, registered_ids: set[str]) -> str:
    folder = page_id.split("/", 1)[0]
    if folder not in REGISTRY_FOLDERS or page_id in registered_ids:
        return wikilink(page_id, label)
    return markdown_page_link(page_id, label)


def load_graph(path: Path) -> dict[str, Any]:
    if not path.is_file():
        sys.exit(f"graph not found: {path}")
    try:
        graph = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        sys.exit(f"invalid graph JSON: {exc}")
    if not isinstance(graph, dict):
        sys.exit("invalid graph JSON: root is not an object")
    graph.setdefault("nodes", [])
    graph.setdefault("edges", [])
    return graph


def load_knowledge_pages(wiki_dir: Path) -> dict[str, dict[str, Any]]:
    pages: dict[str, dict[str, Any]] = {}
    for folder in KNOWLEDGE_FOLDERS:
        folder_dir = wiki_dir / folder
        if not folder_dir.is_dir():
            continue
        for path in sorted(folder_dir.glob("*.md")):
            page_id = f"{folder}/{path.stem}"
            fm, body = read_markdown(path)
            pages[page_id] = {
                "id": page_id,
                "folder": folder,
                "title": str(fm.get("title") or path.stem),
                "summary": summarize(body, is_source=False),
                "related_videos": as_list(fm.get("related_videos")),
            }
    return pages


def load_sources(wiki_dir: Path) -> list[dict[str, Any]]:
    sources_dir = wiki_dir / "sources"
    if not sources_dir.is_dir():
        return []
    sources: list[dict[str, Any]] = []
    for path in sorted(sources_dir.glob("*.md")):
        fm, body = read_markdown(path)
        video_id = str(fm.get("video_id") or path.stem)
        sources.append(
            {
                "id": f"sources/{path.stem}",
                "video_id": video_id,
                "title": str(fm.get("title") or path.stem),
                "date": fm.get("date") or "",
                "series": fm.get("series") or "none",
                "format": as_list(fm.get("format")),
                "summary": summarize(body, is_source=True),
                "frontmatter": fm,
            }
        )
    return sources


def load_slug_registry(path: Path) -> dict[str, set[str]]:
    if parse_registry is None or not path.is_file():
        return {folder: set() for folder in SOURCE_FACETS}
    category_slugs, _aliases = parse_registry(path)
    return {
        "concepts": set(category_slugs.get("concepts", set())),
        "strategies": set(category_slugs.get("strategies", set())),
        "securities": set(category_slugs.get("securities", set())),
        "people": set(category_slugs.get("people", set())),
    }


def registry_folder(slug: str, raw_folder: str, registry: dict[str, set[str]]) -> str | None:
    matches = [folder for folder, slugs in registry.items() if slug in slugs]
    if not matches:
        return None
    if raw_folder in matches:
        return raw_folder
    return matches[0]


def source_facet_counts(
    sources: list[dict[str, Any]],
    registry: dict[str, set[str]],
) -> tuple[dict[str, Counter[str]], dict[str, Counter[str]], int]:
    registered = {folder: Counter() for folder in SOURCE_FACETS}
    unregistered = {folder: Counter() for folder in SOURCE_FACETS}
    recategorized = 0
    for source in sources:
        fm = source["frontmatter"]
        for folder, fields in SOURCE_FACETS.items():
            for field in fields:
                for slug in as_list(fm.get(field)):
                    actual = registry_folder(slug, folder, registry)
                    if actual is None:
                        unregistered[folder][slug] += 1
                        continue
                    registered[actual][slug] += 1
                    if actual != folder:
                        recategorized += 1
    return registered, unregistered, recategorized


def coverage_counts(sources: list[dict[str, Any]]) -> tuple[Counter[str], Counter[str]]:
    series = Counter(str(source["series"] or "none") for source in sources)
    formats: Counter[str] = Counter()
    for source in sources:
        formats.update(source["format"])
    return series, formats


def neighbor_map(graph: dict[str, Any]) -> dict[str, list[str]]:
    neighbors: dict[str, list[str]] = defaultdict(list)
    node_ids = {str(node.get("id")) for node in graph["nodes"]}
    for edge in graph["edges"]:
        source = str(edge.get("source"))
        target = str(edge.get("target"))
        if source in node_ids and target in node_ids:
            neighbors[source].append(target)
            neighbors[target].append(source)
    return neighbors


def format_neighbors(
    page_id: str,
    neighbors: dict[str, list[str]],
    titles: dict[str, str],
    registered_ids: set[str],
    limit: int = 8,
) -> str:
    items = sorted(set(neighbors.get(page_id, [])))
    if not items:
        return "none"
    rendered = [page_ref(item, titles.get(item, item), registered_ids) for item in items[:limit]]
    if len(items) > limit:
        rendered.append(f"{len(items) - limit} more")
    return ", ".join(rendered)


def format_sources(video_ids: list[str], existing_source_ids: set[str], limit: int = 10) -> str:
    if not video_ids:
        return "none"
    rendered = [
        wikilink(f"sources/{video_id}") if video_id in existing_source_ids else f"`{video_id}`"
        for video_id in video_ids[:limit]
    ]
    if len(video_ids) > limit:
        rendered.append(f"{len(video_ids) - limit} more")
    return ", ".join(rendered)


def render_index(wiki_dir: Path, graph_path: Path) -> str:
    graph = load_graph(graph_path)
    pages = load_knowledge_pages(wiki_dir)
    sources = load_sources(wiki_dir)
    source_video_ids = {source["video_id"] for source in sources}
    registry = load_slug_registry(SLUG_REGISTRY)
    registered_ids = registered_page_ids(registry)
    facet_counts, unregistered_counts, recategorized_count = source_facet_counts(sources, registry)
    series_counts, format_counts = coverage_counts(sources)
    neighbors = neighbor_map(graph)
    node_titles = {str(node.get("id")): str(node.get("label") or node.get("id")) for node in graph["nodes"]}
    node_degree = {str(node.get("id")): int(node.get("degree") or 0) for node in graph["nodes"]}

    nodes_by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in graph["nodes"]:
        nodes_by_category[str(node.get("category"))].append(node)

    lines = [
        "---",
        "type: index",
        'title: "OPTEEE Wiki - Knowledge Graph Index"',
        f"last_updated: {date.today().isoformat()}",
        "status: generated",
        "generated_by: scripts/build_wiki_index.py",
        f"knowledge_page_count: {len(graph['nodes'])}",
        f"source_count: {len(sources)}",
        f"graph_edge_count: {len(graph['edges'])}",
        "---",
        "",
        "# OPTEEE Wiki - Knowledge Graph Index",
        "",
        "This is the Markdown index of the OPTEEE knowledge graph. The browser at `/wiki` loads `wiki/graph.json`; this file mirrors that graph for LLM and human navigation.",
        "",
        "Start here, choose relevant graph nodes or source-derived candidate nodes, then drill into linked pages and cite backing source videos.",
        "",
        "## Graph summary",
        "",
        f"- Materialized knowledge nodes: {len(graph['nodes'])}",
        f"- Knowledge edges: {len(graph['edges'])}",
        f"- Source pages: {len(sources)}",
        f"- Registry-recategorized source mentions: {recategorized_count}",
        "",
        "| top-level category | materialized graph nodes | registered candidate slugs | registered source mentions | unregistered raw slugs |",
        "|---|---:|---:|---:|---:|",
    ]

    for folder, graph_category, label in CATEGORY_ORDER:
        candidate_count = len(facet_counts.get(folder, Counter()))
        mention_count = sum(facet_counts.get(folder, Counter()).values())
        unregistered_count = len(unregistered_counts.get(folder, Counter()))
        lines.append(
            f"| {label} | {len(nodes_by_category.get(graph_category, []))} | "
            f"{candidate_count} | {mention_count} | {unregistered_count} |"
        )

    lines.extend(
        [
            "",
            "## Materialized graph nodes",
            "",
            "These pages are currently in `wiki/graph.json` and therefore appear in the interactive graph.",
            "",
        ]
    )

    for folder, graph_category, label in CATEGORY_ORDER:
        nodes = sorted(
            nodes_by_category.get(graph_category, []),
            key=lambda node: (-int(node.get("video_count") or 0), str(node.get("label"))),
        )
        if not nodes:
            continue
        lines.extend([f"### {label}", ""])
        for node in nodes:
            page_id = str(node.get("id"))
            page = pages.get(page_id, {})
            title = str(node.get("label") or page.get("title") or page_id)
            related_videos = as_list(page.get("related_videos"))
            lines.append(
                f"- {page_ref(page_id, title, registered_ids)} - {page.get('summary', 'No summary available.')} "
                f"(sources: {len(related_videos)}, degree: {node_degree.get(page_id, 0)})"
            )
            lines.append(f"  - links: {format_neighbors(page_id, neighbors, node_titles, registered_ids)}")
            lines.append(f"  - backing sources: {format_sources(related_videos, source_video_ids)}")
        lines.append("")

    lines.extend(
        [
            "## Source-derived candidate graph",
            "",
            "These candidate nodes are source-page mentions that resolve to `schema/slugs.md`. Linked items already have materialized pages; code-form items are registered synthesis backlog.",
            "",
        ]
    )

    existing_pages = set(pages)
    for folder, _graph_category, label in CATEGORY_ORDER[:4]:
        counts = facet_counts.get(folder, Counter())
        if not counts:
            continue
        lines.extend([f"### {label}", ""])
        for slug, count in counts.most_common():
            page_id = f"{folder}/{slug}"
            rendered = wikilink(page_id, slug) if page_id in existing_pages else f"`{slug}`"
            lines.append(f"- {rendered} - {count} source mention(s)")
        lines.append("")

    lines.extend(
        [
            "## Unregistered extraction backlog",
            "",
            "These raw source-pass slugs did not resolve to `schema/slugs.md`. Review them before treating them as graph categories; many should become aliases, registry additions, or corrected source frontmatter.",
            "",
        ]
    )

    for folder, _graph_category, label in CATEGORY_ORDER[:4]:
        counts = unregistered_counts.get(folder, Counter())
        if not counts:
            continue
        lines.extend([f"### {label}", ""])
        for slug, count in counts.most_common(100):
            lines.append(f"- `{slug}` - {count} raw mention(s)")
        if len(counts) > 100:
            lines.append(f"- ... {len(counts) - 100} more unregistered slug(s)")
        lines.append("")

    lines.extend(["## Source coverage facets", "", "### Series", ""])
    for name, count in series_counts.most_common():
        lines.append(f"- `{name}` - {count} source page(s)")
    lines.extend(["", "### Format", ""])
    for name, count in format_counts.most_common():
        lines.append(f"- `{name}` - {count} source page(s)")

    lines.extend(
        [
            "",
            "## Source page catalog",
            "",
            "<details>",
            f"<summary>All source pages ({len(sources)})</summary>",
            "",
            "| source | date | series | one-line summary |",
            "|---|---|---|---|",
        ]
    )

    for source in sorted(sources, key=lambda item: (str(item["date"]), item["title"])):
        lines.append(
            f"| {wikilink(source['id'], md_cell(source['title']))} | "
            f"{md_cell(source['date'])} | `{md_cell(source['series'])}` | "
            f"{md_cell(source['summary'])} |"
        )
    lines.extend(["", "</details>", ""])

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build graph-backed wiki/index.md.")
    parser.add_argument("--wiki-dir", type=Path, default=WIKI_DIR)
    parser.add_argument("--graph", type=Path, default=GRAPH_PATH)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args(argv)

    wiki_dir = args.wiki_dir.resolve()
    graph_path = args.graph.resolve()
    output_path = args.output.resolve()

    if not wiki_dir.is_dir():
        sys.exit(f"wiki directory not found: {wiki_dir}")

    rendered = render_index(wiki_dir, graph_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered + "\n", encoding="utf-8")

    print(f"Wrote {output_path}")
    print(f"  knowledge nodes: {len(load_graph(graph_path)['nodes'])}")
    print(f"  source pages: {len(load_sources(wiki_dir))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
