#!/usr/bin/env python3
"""build_graph.py — generate ``wiki/graph.json`` for the interactive ``/wiki`` view.

Implements the ``graph.json`` data contract from ``schema/WIKI_SCHEMA.md`` §12.

The graph is the *knowledge layer only*: one node per knowledge page under
``wiki/{concepts,strategies,securities,people,macro,syntheses}/*.md``. Source
pages (``wiki/sources/*.md``) are NOT nodes by default — they are added on
demand behind ``--include-sources`` (the ``?include=sources`` expansion).

Edges are the explicit ``[[wikilinks]]`` between knowledge pages. Node
positions (``x``/``y``) are baked here with a small, dependency-free
Fruchterman-Reingold force layout implemented in pure numpy with a FIXED seed,
so running the script twice produces byte-identical coordinates.

Usage::

    python scripts/build_graph.py                  # knowledge nodes only
    python scripts/build_graph.py --include-sources # + source-page nodes

This script deliberately does NOT depend on networkx (which may not be
installed); numpy is the only third-party import.
"""

from __future__ import annotations

import argparse
import datetime
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import numpy as np
except ImportError:  # pragma: no cover - environment guard
    sys.exit(
        "build_graph.py requires numpy. Run it with the project venv, e.g.\n"
        "    ./.venv/bin/python scripts/build_graph.py"
    )

try:
    import yaml  # PyYAML — preferred frontmatter parser
    _HAVE_YAML = True
except ImportError:  # pragma: no cover - fallback path
    _HAVE_YAML = False


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"
OUTPUT_PATH = WIKI_DIR / "graph.json"

# folder name -> singular category label (per §12 / §3). `category` stays folder-based so
# build_wiki_index.py's category grouping works; the thematic L0 lives in `theme` (below).
KNOWLEDGE_FOLDERS = {
    "concepts": "concept",
    "strategies": "strategy",
    "securities": "security",
    "people": "person",
    "macro": "macro",
    "syntheses": "synthesis",
}
SOURCES_FOLDER = "sources"

# --- Curated theme taxonomy (L0 categories for the hierarchical /wiki graph) ------------
# Each knowledge node gets a `theme` = its top-level category. The graph keeps ONE node per
# page (so `nodes == page files`); the browser groups by `theme` and drills L0→L1→L2.
# Folders map directly where clean; the big `concepts` bucket is split by keyword.
THEME_TITLES = {
    "options-strategies": "Options Strategies",
    "options-mechanics":  "Options Mechanics",
    "volatility-iv":      "Volatility & IV",
    "greeks":             "Greeks",
    "securities":         "Securities",
    "risk-psychology":    "Risk & Psychology",
    "market-structure":   "Market Structure",
    "regimes-macro":      "Regimes & Macro",
    "technical-analysis": "Technical Analysis",
    "process-method":     "Process & Method",
    "interviews":         "Interviews",
}
# Ordered (theme, substrings) rules for concept slugs; first match wins.
_CONCEPT_THEME_RULES = [
    ("greeks", ["delta", "gamma", "theta", "rho", "vanna", "charm", "vega", "greek"]),
    ("volatility-iv", ["volatil", "implied-vol", "iv-", "-iv", "vrp", "variance-risk", "skew",
                        "term-structure", "realized-vol", "vix", "vol-", "kurtosis", "fat-tail"]),
    ("market-structure", ["gamma-exposure", "gex", "dex", "dealer", "order-flow", "market-maker",
                           "moneyness", "pin", "squeeze", "payment-for-order", "internaliz",
                           "bid-ask", "liquidity-provider", "hedging"]),
    ("technical-analysis", ["vwap", "support", "resistance", "trend", "moving-average", "fibonacci",
                             "pivot", "candlestick", "technical", "price-action", "chart",
                             "linear-regression", "standard-deviation-channel", "higher-highs",
                             "volume-profile", "supply-and-demand"]),
    ("risk-psychology", ["risk", "position-siz", "stop", "disciplin", "psycholog", "emotion",
                          "disposition", "kelly", "drawdown", "tolerance", "confirmation-bias",
                          "longevity", "mindset", "sequence-of-returns"]),
    ("regimes-macro", ["regime", "macro", "\bfed", "rate", "inflation", "recession", "tariff",
                        "melt-up", "liquidity-cycle", "yield", "bust", "deflation", "reshoring",
                        "bond-vigil", "disinflation", "cpi", "fomc", "sofr", "risk-free",
                        "contrarian", "sector-rotation", "market-breadth"]),
    ("process-method", ["process", "trading-plan", "backtest", "occurrence", "number-of", "journal",
                         "trading-log", "review", "probabil", "expected-value", "expected-return",
                         "win-rate", "paper-trading", "quantitative", "monte-carlo", "overfit",
                         "survivorship", "edge", "forecasting", "sample-size", "market-efficiency",
                         "information-and-price", "research", "law-of-large", "mean-reversion",
                         "momentum", "market-timing", "equity-anomalies", "pnl", "total-return"]),
]


def theme_for(folder: str, slug: str) -> str:
    """Assign a knowledge page to a top-level theme (L0 category)."""
    if folder == "strategies":
        return "options-strategies"
    if folder == "securities":
        return "securities"
    if folder == "people":
        return "interviews"
    if folder == "macro":
        return "regimes-macro"
    if folder == "syntheses":
        return "process-method"
    # concepts: keyword match, else options-mechanics
    s = slug.lower()
    for theme, subs in _CONCEPT_THEME_RULES:
        for sub in subs:
            if sub.lstrip("\\b") in s:
                return theme
    return "options-mechanics"


# Relationship edges: connect each topic to its strongest co-occurring topics.
COOCCUR_MIN_SHARED = 3   # min shared videos to link two topics
COOCCUR_TOP_K = 5        # per node, keep its strongest K relationships

# Deterministic layout knobs — DO NOT change casually; changing them re-bakes
# every coordinate. The fixed seed + fixed iteration count is what guarantees
# reproducibility (acceptance test 2).
LAYOUT_SEED = 42
LAYOUT_ITERATIONS = 250
COORD_PRECISION = 6  # decimal places for baked x/y

_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
_FRONTMATTER_RE = re.compile(r"^﻿?---\s*\n(.*?)\n---\s*\n", re.DOTALL)


# --------------------------------------------------------------------------- #
# Parsing helpers
# --------------------------------------------------------------------------- #

def _fallback_parse(fm_text: str) -> dict:
    """Minimal YAML-ish frontmatter parser for the keys we need.

    Only used when PyYAML is unavailable. Handles ``key: "value"`` and
    ``key: [a, b, c]`` flow lists, which is all the wiki frontmatter uses for
    the fields this script reads (title, related_videos, aliases).
    """
    data: dict = {}
    for line in fm_text.splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            data[key] = [
                item.strip().strip('"').strip("'")
                for item in inner.split(",")
                if item.strip()
            ]
        else:
            data[key] = val.strip().strip('"').strip("'")
    return data


def parse_frontmatter(text: str) -> dict:
    """Return the frontmatter mapping for a wiki markdown file (may be empty)."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fm_text = match.group(1)
    if _HAVE_YAML:
        try:
            data = yaml.safe_load(fm_text)
            if isinstance(data, dict):
                return data
        except yaml.YAMLError:
            pass
    return _fallback_parse(fm_text)


def _as_list(value) -> list[str]:
    """Coerce a frontmatter scalar/list into a clean list of strings."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    return [str(value)]


# --------------------------------------------------------------------------- #
# Page collection
# --------------------------------------------------------------------------- #

def collect_knowledge_pages(wiki_dir: Path) -> dict:
    """Scan the knowledge folders and return ``{page_id: page_dict}``.

    ``page_id`` is the path-style id, e.g. ``concepts/volatility-risk-premium``.
    """
    pages: dict = {}
    for folder, category in KNOWLEDGE_FOLDERS.items():
        folder_dir = wiki_dir / folder
        if not folder_dir.is_dir():
            continue
        for md_path in sorted(folder_dir.glob("*.md")):
            slug = md_path.stem
            page_id = f"{folder}/{slug}"
            text = md_path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            related_videos = _as_list(fm.get("related_videos"))
            pages[page_id] = {
                "id": page_id,
                "folder": folder,
                "category": category,
                "theme": theme_for(folder, slug),
                "label": str(fm.get("title") or slug),
                "related_videos": related_videos,
                "video_count": len(related_videos),
                "aliases": _as_list(fm.get("aliases")),
                # scan the whole file; only bodies contain [[wikilinks]]
                "wikilinks": _WIKILINK_RE.findall(text),
            }
    return pages


def build_resolver(pages: dict) -> dict:
    """Map every ``category/slug`` (canonical + registered aliases) to its page id.

    Aliases (§5) are registered under the owning page's folder so that a link
    like ``[[strategies/coverage-triangle]]`` resolves to
    ``strategies/covered-strangle``. Canonical ids always win over aliases.
    """
    resolver: dict = {}
    # aliases first, then overwrite with canonical ids so canonical wins
    for page_id, page in pages.items():
        for alias in page["aliases"]:
            resolver.setdefault(f"{page['folder']}/{alias}", page_id)
    for page_id in pages:
        resolver[page_id] = page_id
    return resolver


# --------------------------------------------------------------------------- #
# Edge construction
# --------------------------------------------------------------------------- #

def build_wikilink_edges(pages: dict, resolver: dict) -> list:
    """Undirected-deduplicated ``wikilink`` edges between knowledge pages.

    Parses ``[[category/slug]]`` and ``[[category/slug|alias]]`` targets.
    Ignores ``[[sources/...]]`` links and links to not-yet-created pages.
    Direction of the first occurrence is preserved in the edge list, but the
    pair is deduplicated undirectedly.
    """
    seen: set = set()
    edges: list = []
    for page_id in sorted(pages):
        for raw in pages[page_id]["wikilinks"]:
            target = raw.split("|", 1)[0].strip()  # drop |alias display text
            if "/" not in target:
                continue
            folder = target.split("/", 1)[0]
            if folder == SOURCES_FOLDER or folder not in KNOWLEDGE_FOLDERS:
                continue  # source links + non-knowledge folders are not edges
            resolved = resolver.get(target)
            if resolved is None or resolved == page_id:
                continue  # unresolved (backlog page) or self-link
            key = frozenset((page_id, resolved))
            if key in seen:
                continue
            seen.add(key)
            edges.append(
                {"source": page_id, "target": resolved,
                 "type": "wikilink", "weight": 1, "label": "wiki link"}
            )
    return edges


def build_cooccurrence_edges(pages: dict, existing: list) -> list:
    """Relationship edges: link each page to its top-K co-occurring topics (shared videos).

    This is what makes the graph reflect the *relationships* in the body of knowledge —
    two topics discussed together in enough videos are related.
    """
    seen = {frozenset((e["source"], e["target"])) for e in existing}
    vid_sets = {pid: set(p["related_videos"]) for pid, p in pages.items()}
    ids = sorted(pages)
    edges: list = []
    for a in ids:
        va = vid_sets[a]
        if not va:
            continue
        scored = []
        for b in ids:
            if b == a:
                continue
            n = len(va & vid_sets[b])
            if n >= COOCCUR_MIN_SHARED:
                scored.append((n, b))
        scored.sort(key=lambda t: (-t[0], t[1]))
        for n, b in scored[:COOCCUR_TOP_K]:
            key = frozenset((a, b))
            if key in seen:
                continue
            seen.add(key)
            edges.append({"source": a, "target": b, "type": "cooccurrence",
                          "weight": min(int(n), 5),
                          "shared_source_count": int(n),
                          "label": f"shared source videos: {int(n)}"})
    return edges


def collect_source_ids(pages: dict, wiki_dir: Path) -> list:
    """Source video ids to expose as nodes under ``--include-sources``.

    Union of (a) every ``sources/{video_id}.md`` file on disk and (b) every
    video id referenced by a knowledge page's ``related_videos`` (so every
    source edge has an endpoint even if the source page is missing).
    """
    ids: set = set()
    sources_dir = wiki_dir / SOURCES_FOLDER
    if sources_dir.is_dir():
        for md_path in sources_dir.glob("*.md"):
            ids.add(md_path.stem)
    for page in pages.values():
        ids.update(page["related_videos"])
    return sorted(ids)


def source_label(video_id: str, wiki_dir: Path) -> str:
    """Human label for a source node — its title if the page exists, else the id."""
    md_path = wiki_dir / SOURCES_FOLDER / f"{video_id}.md"
    if md_path.is_file():
        title = parse_frontmatter(md_path.read_text(encoding="utf-8")).get("title")
        if title:
            return str(title)
    return video_id


def build_source_edges(pages: dict, source_ids: set) -> list:
    """Edges from each knowledge page to the sources in its ``related_videos``."""
    seen: set = set()
    edges: list = []
    for page_id in sorted(pages):
        for video_id in pages[page_id]["related_videos"]:
            if video_id not in source_ids:
                continue
            target = f"{SOURCES_FOLDER}/{video_id}"
            key = (page_id, target)
            if key in seen:
                continue
            seen.add(key)
            edges.append(
                {"source": page_id, "target": target,
                 "type": "source", "weight": 1, "label": "backing source"}
            )
    return edges


# --------------------------------------------------------------------------- #
# Deterministic force-directed layout (Fruchterman-Reingold, pure numpy)
# --------------------------------------------------------------------------- #

def compute_layout(node_ids: list, edge_pairs: list,
                   seed: int = LAYOUT_SEED,
                   iterations: int = LAYOUT_ITERATIONS) -> dict:
    """Bake 2D coordinates with FR force layout, normalized to ~[-1, 1].

    Determinism guarantees:
      * ``node_ids`` is consumed in a fixed (sorted) order by the caller, so
        each node maps to a fixed matrix row.
      * initial positions come from ``np.random.RandomState(seed)`` — a fixed
        seed, fixed count of draws.
      * fixed iteration count, no wall-clock / no set iteration order.
      * final coords are rounded to a fixed precision.
    Same inputs on the same machine therefore yield identical coordinates.
    """
    n = len(node_ids)
    if n == 0:
        return {}
    if n == 1:
        return {node_ids[0]: (0.0, 0.0)}

    rng = np.random.RandomState(seed)
    pos = rng.uniform(-1.0, 1.0, size=(n, 2)).astype(np.float64)

    index = {nid: i for i, nid in enumerate(node_ids)}
    pairs = [(index[a], index[b]) for a, b in edge_pairs
             if a in index and b in index]
    edges = (np.array(pairs, dtype=np.int64)
             if pairs else np.zeros((0, 2), dtype=np.int64))

    area = 1.0
    k = math.sqrt(area / n)          # ideal edge length
    temperature = 0.1                # max displacement / iteration
    cooling = temperature / (iterations + 1)

    for _ in range(iterations):
        # --- repulsion between every pair of nodes ---
        diff = pos[:, None, :] - pos[None, :, :]          # (n, n, 2)
        dist = np.sqrt((diff ** 2).sum(axis=2))           # (n, n)
        np.fill_diagonal(dist, np.inf)                    # ignore self-pairs
        dist = np.maximum(dist, 1e-9)
        rep = (k * k) / dist                              # (n, n)
        disp = ((diff / dist[:, :, None]) * rep[:, :, None]).sum(axis=1)

        # --- attraction along edges ---
        if edges.shape[0]:
            d = pos[edges[:, 0]] - pos[edges[:, 1]]       # (m, 2)
            dlen = np.maximum(np.sqrt((d ** 2).sum(axis=1)), 1e-9)
            att = (dlen * dlen) / k                       # (m,)
            force = (d / dlen[:, None]) * att[:, None]
            np.add.at(disp, edges[:, 0], -force)
            np.add.at(disp, edges[:, 1], force)

        # --- limit movement by the (cooling) temperature ---
        step = np.maximum(np.sqrt((disp ** 2).sum(axis=1)), 1e-9)
        pos += (disp / step[:, None]) * np.minimum(step, temperature)[:, None]
        temperature -= cooling

    # normalize to roughly [-1, 1] preserving aspect ratio
    pos -= pos.mean(axis=0)
    max_abs = float(np.max(np.abs(pos)))
    if max_abs > 0:
        pos /= max_abs

    coords: dict = {}
    for i, nid in enumerate(node_ids):
        x = round(float(pos[i, 0]), COORD_PRECISION)
        y = round(float(pos[i, 1]), COORD_PRECISION)
        # normalize -0.0 to 0.0 for clean, stable output
        coords[nid] = (x + 0.0, y + 0.0)
    return coords


def compute_theme_layout(node_ids: list, theme_by_id: dict) -> dict:
    """Deterministic theme-clustered layout — each theme forms its own spatial cluster.

    Cluster centers sit on a circle; within a cluster the nodes fan out on concentric
    rings (ordered for determinism), so same-theme topics group together and the graph
    reads as ~N tidy neighborhoods instead of one uniform blob. Normalized to ~[-1, 1].
    Deterministic (sorted order + fixed trig) → byte-identical across runs.
    """
    if not node_ids:
        return {}
    by_theme: dict = defaultdict(list)
    for nid in node_ids:
        by_theme[theme_by_id.get(nid, "other")].append(nid)
    themes = sorted(by_theme)
    n_themes = len(themes)
    # Cluster centers on a circle whose radius is large relative to cluster spread, so
    # neighborhoods are well separated (declutter). Ring spacing widens the interior too.
    cluster_r = 3.0
    coords: dict = {}
    for ti, theme in enumerate(themes):
        members = sorted(by_theme[theme])
        m = len(members)
        cang = (2 * math.pi * ti) / max(1, n_themes)
        cx, cy = cluster_r * math.cos(cang), cluster_r * math.sin(cang)
        local = 0.18 + 0.55 * min(1.0, m / 120.0)         # bigger clusters spread wider
        idx, ring = 0, 0
        while idx < m:
            ring += 1
            cap = max(1, ring * 6)
            r = local * ring / 3.0
            for kk in range(cap):
                if idx >= m:
                    break
                a = (2 * math.pi * kk) / cap + ti         # rotate each cluster to avoid alignment
                coords[members[idx]] = (cx + r * math.cos(a), cy + r * math.sin(a))
                idx += 1
    xs = [c[0] for c in coords.values()]
    ys = [c[1] for c in coords.values()]
    mx = max([abs(v) for v in xs + ys] or [1.0]) or 1.0
    for nid in coords:
        x, y = coords[nid]
        coords[nid] = (round(x / mx, COORD_PRECISION) + 0.0, round(y / mx, COORD_PRECISION) + 0.0)
    return coords


def load_relationships(wiki_dir: Path) -> dict:
    """Grounded, typed relationships from extract_relationships.py (may be absent)."""
    rf = wiki_dir / "relationships.json"
    if not rf.is_file():
        return {}
    try:
        data = json.loads(rf.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def enrich_edges_with_relationships(edges: list, rels: dict) -> list:
    """Replace co-occurrence labels with the real relationship meaning where available.

    A co-occurrence edge gains `relation` (typed), `label` (the phrase the /wiki graph shows),
    `evidence` (citing the video), and is oriented in the relationship's direction. Edges
    without an extracted relationship keep their co-occurrence weight (labelled by the UI).
    """
    for e in edges:
        if e.get("type") != "cooccurrence":
            continue
        r = rels.get("||".join(sorted([e["source"], e["target"]])))
        if not r:
            continue
        e["relation"] = r.get("relation")
        if r.get("label"):
            e["label"] = r["label"]
        if r.get("evidence"):
            e["evidence"] = r["evidence"]
        if r.get("source") and r.get("target"):
            e["source"], e["target"] = r["source"], r["target"]  # undirected degree unaffected
    return edges


# --------------------------------------------------------------------------- #
# Graph assembly
# --------------------------------------------------------------------------- #

def build_graph(wiki_dir: Path, include_sources: bool = False) -> dict:
    pages = collect_knowledge_pages(wiki_dir)
    resolver = build_resolver(pages)

    edges = build_wikilink_edges(pages, resolver)
    edges = edges + build_cooccurrence_edges(pages, edges)
    edges = enrich_edges_with_relationships(edges, load_relationships(wiki_dir))

    # node id -> node dict (knowledge nodes first)
    node_records: dict = {}
    for page_id in sorted(pages):
        page = pages[page_id]
        node_records[page_id] = {
            "id": page_id,
            "label": page["label"],
            "category": page["category"],
            "theme": page["theme"],
            "size": page["video_count"],       # per §12: = len(related_videos)
            "video_count": page["video_count"],
        }

    if include_sources:
        source_ids = collect_source_ids(pages, wiki_dir)
        source_id_set = set(source_ids)
        for video_id in source_ids:
            node_id = f"{SOURCES_FOLDER}/{video_id}"
            node_records[node_id] = {
                "id": node_id,
                "label": source_label(video_id, wiki_dir),
                "category": "source",
                "theme": "source",
                "size": 1,
                "video_count": 1,
            }
        edges = edges + build_source_edges(pages, source_id_set)

    # degree (undirected) over the final edge set
    degree = {node_id: 0 for node_id in node_records}
    for edge in edges:
        degree[edge["source"]] += 1
        degree[edge["target"]] += 1

    node_ids = sorted(node_records)
    # Theme-clustered layout keeps same-theme nodes together (declutter). Sources (theme
    # "source") cluster on their own; knowledge nodes group into their ~11 themes.
    theme_by_id = {nid: node_records[nid].get("theme", "other") for nid in node_records}
    layout = compute_theme_layout(node_ids, theme_by_id)

    nodes = []
    for node_id in node_ids:
        record = node_records[node_id]
        x, y = layout.get(node_id, (0.0, 0.0))
        nodes.append({
            "id": record["id"],
            "label": record["label"],
            "category": record["category"],
            "theme": record.get("theme", record["category"]),
            "size": record["size"],
            "video_count": record["video_count"],
            "degree": degree[node_id],
            "x": x,
            "y": y,
        })

    edges_sorted = sorted(edges, key=lambda e: (e["source"], e["target"], e["type"]))
    return {"nodes": nodes, "edges": edges_sorted}


# --------------------------------------------------------------------------- #
# Reporting / CLI
# --------------------------------------------------------------------------- #

def print_summary(graph: dict, output_path: Path) -> None:
    nodes = graph["nodes"]
    edges = graph["edges"]
    breakdown: dict = {}
    for node in nodes:
        breakdown[node["category"]] = breakdown.get(node["category"], 0) + 1

    print(f"Wrote {output_path}")
    print(f"  nodes: {len(nodes)}")
    print(f"  edges: {len(edges)}")
    edge_types: dict = {}
    for edge in edges:
        edge_types[edge["type"]] = edge_types.get(edge["type"], 0) + 1
    if edge_types:
        print("  edge types: "
              + ", ".join(f"{t}={c}" for t, c in sorted(edge_types.items())))
    print("  category breakdown:")
    for category in sorted(breakdown):
        print(f"    {category:<10} {breakdown[category]}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Build wiki/graph.json (precomputed knowledge graph for /wiki)."
    )
    parser.add_argument(
        "--include-sources", action="store_true",
        help="also add source-page nodes + edges from related_videos "
             "(the ?include=sources expansion; default off).",
    )
    parser.add_argument(
        "--wiki-dir", type=Path, default=WIKI_DIR,
        help="path to the wiki/ directory (default: repo wiki/).",
    )
    parser.add_argument(
        "--output", type=Path, default=None,
        help="output path (default: <wiki-dir>/graph.json).",
    )
    args = parser.parse_args(argv)

    wiki_dir = args.wiki_dir.resolve()
    output_path = (args.output or (wiki_dir / "graph.json")).resolve()

    if not wiki_dir.is_dir():
        sys.exit(f"wiki directory not found: {wiki_dir}")

    graph = build_graph(wiki_dir, include_sources=args.include_sources)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")

    print_summary(graph, output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
