You are familiar with building specialized LLM-maintained knowledge bases. I want you to build a production-grade **LLM Wiki** for my “Opteee” system — a RAG built on all Outlier Trading YouTube video transcripts.

Reference materials:
- Andrej Karpathy’s LLM Wiki gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- The video I linked (Fable 5 + Karpathy’s LLM Wiki): https://youtu.be/hQvwMj7IJe4 (shows quick build + 2D graph demo)

**Core Goal**  
Add additional functionality to the RAG system. Use the raw transcripts into a **persistent, compounding, queryable knowledge base** that an LLM maintains. 
The knowledge wiki sits exists along side the exiting RAG system. the raw transcripts will need to be processed to create/add to knowlege wiki and the RAG system. The wiki data will need to be served up via api for external websites that can navigate the wiki. downstream use (including augmenting Opteee RAG). It extracts, synthesizes, cross-references, and evolves the trading knowledge across videos instead of re-deriving connections on every query.

The wiki must be **pure filesystem + Markdown** (no Obsidian or proprietary tools required). It must be easily maintainable by an LLM agent (Cursor, Claude Code, local models via schema instructions).

**High-Level Architecture (Karpathy pattern adapted)**

1. **raw/** — Immutable source of truth (transcripts + metadata). LLM reads only.
2. **wiki/** — LLM-owned and maintained layer. All synthesis, entities, concepts, strategies, and connections live here. Heavy use of `[[wikilinks]]`.
3. **schema/** (or root `WIKI_SCHEMA.md`) — The “constitution” file. This is the most important deliverable. It contains detailed, domain-specific instructions so any LLM session can correctly ingest, update, query, and lint the wiki without drift.
4. Supporting scripts (Python preferred, matching my existing stack) for ingestion, linting, and graph generation.
5. Additionally create a api that is a REST endpoint that can service up metadata and key facts of the content and the documents as well. this will give clients ability to browser the wiki structure.

**Recommended Starting Folder Structure** (refine after you analyze the transcripts)

```
opteee/
├── transcripts/                 # All transcript files here
│   │   ├── YYYY-MM-DD_Slug_Title.md   # With YAML frontmatter
│   │   └── ...
│   └── metadata/                    # Optional: video index, playlists, etc.
├── wiki/
│   ├── index.md                     # Master catalog (categorized, LLM-updated)
│   ├── log.md                       # Append-only chronological history
│   ├── concepts/                    # Core ideas (greeks, regimes, indicators, principles)
│   ├── strategies/                  # Actionable strategies (short-strangle.md, pead.md, etc.)
│   ├── securities/                  # Ticker/asset pages (SPY.md, energy-sector.md, etc.)
│   ├── sources/                     # Per-video or per-series key takeaways + links to concepts
│   ├── syntheses/                   # Cross-video playbooks, regime notes, “Outlier method” docs
│   ├── comparisons/                 # Side-by-side analyses
│   ├── glossary.md                  # Or integrate terms into concepts
│   └── assets/                      # Generated charts, tables, images (if any)
├── schema/
│   └── WIKI_SCHEMA.md               # THE detailed instruction file for LLM maintainers
├── scripts/
│   ├── ingest.py                    # (or instructions for LLM to do it)
│   ├── build_graph.py               # 2D knowledge graph generator
│   └── lint_wiki.py
├── README.md
└── .gitignore
```

**Transcript File Format (raw)**  
Each transcript file should include clean YAML frontmatter:
```yaml
---
title: "..."
url: "https://youtube.com/..."
date: "YYYY-MM-DD"
duration: "..."
key_topics: ["short strangle", "regime detection", ...]
video_id: "..."
---
# Full transcript or cleaned version here
```

**Wiki Page Conventions (to be formalized in schema)**
- Filenames: `kebab-case.md`
- Every wiki page starts with YAML frontmatter (`type`, `related_videos`, `last_updated`, `confidence` or similar).
- Heavy, consistent use of `[[wikilinks]]` (e.g. `[[short-strangle]]`, `[[concepts/gamma-exposure|gamma exposure]]`).
- Standard sections per page type (Concept, Strategy, Security, Synthesis, Source summary).
- Explicitly note context/contradictions (e.g., “This setup works best in low-IV regimes — see [[regime-detection]] and videos from 2025-03 vs 2026-01”).

**Key Deliverables I Want**

1. **Complete folder structure** initialized with real content from my transcripts (start with a representative sample, then full batch).

2. **WIKI_SCHEMA.md** (the heart of the system) — A long, precise instruction file covering:
   - Page taxonomy and when to create/update each type.
   - Ingestion workflow (single video or batch).
   - How to synthesize across videos (consolidate all mentions of a strategy into one evolving page while preserving video-specific examples and regime context).
   - Query workflow (always read `index.md` first, follow links, cite specific videos + wiki pages).
   - Lint/maintenance rules (orphans, contradictions, stale claims, missing connections, suggested new pages/questions).
   - Trading-domain style and precision rules.
   - How to handle evolving knowledge (new videos can update or qualify older claims).

3. **Initial populated wiki** — High-quality pages for the most important concepts/strategies from the transcripts (e.g. short strangle variations, regime systems, key indicators, SPY handling, risk rules, etc.). Include `index.md` and `log.md`.

4. **2D Data Graph Generator** (`scripts/build_graph.py` or equivalent):
   - Parse all `[[wikilinks]]` across the wiki.
   - Build a graph (nodes = pages or extracted entities; edges = explicit links + strong co-occurrence).
   - Add metadata (category, link degree/importance, video count).
   - Generate a clean **2D force-directed layout** (or other readable layout).
   - Output options:
     - Interactive HTML (Plotly, vis.js, or similar — self-contained).
     - Static high-quality image (PNG/PDF).
     - Export formats (GraphML, JSON, CSV edges) for import into my existing dashboards or other tools.
   - Color/size nodes by category or centrality. Highlight clusters (e.g. “Options Strategies” cluster, “Macro/Regime” cluster).
   - Bonus: A `graph.md` or `visualizations/` page in the wiki that links to the latest graph.

5. **Augment Existing Opteee RAG** (most important integration step):
   - First, explore my current Opteee codebase (RAG pipeline, how transcripts are chunked/indexed/stored, query flow, any dashboard code).
   - Implement bridging so RAG searches can easily surface or link into the LLM Wiki:
     - Option A (recommended start): During/after indexing or in post-processing, attach `related_wiki_pages: ["[[strategies/short-strangle]]", ...]` metadata to relevant transcript chunks or search results. LLM extracts these using the wiki schema/index.
     - Option B: In RAG responses, automatically append or interleave relevant wiki excerpts + clean relative links (e.g. `[Short Strangle Strategy](../wiki/strategies/short-strangle.md)`).
     - Option C (strong): Hybrid retrieval or query routing — use wiki `index.md` + key pages for structured/high-level answers, fall back to raw transcript chunks for specifics/timestamps/examples.
     - Make links work locally (relative Markdown paths) and be human/AI friendly.
   - Goal: From a RAG search I can fluidly “bridge” into the deeper synthesized wiki knowledge and vice versa.

6. **Documentation & Usability**
   - Excellent `README.md` explaining the system, how to add a new video transcript, how to query/maintain with an LLM agent, and how the graph is regenerated.
   - Clear workflow for ongoing maintenance (ingest → update wiki → rebuild graph → optional RAG refresh).

**Workflow Expectations**
- Analyze the transcripts first (or a large sample) to refine the taxonomy before massive generation.
- Use my preferred style: clean, precise, trading-domain language. Cite sources (specific videos) where claims originate.
- Make everything work well with Cursor/Claude Code + local file access (or my local LLM setups). The `WIKI_SCHEMA.md` should be so good that future sessions can reliably maintain the wiki with minimal supervision.
- Prioritize quality over quantity in the initial build — a smaller number of excellent, well-linked pages beats hundreds of shallow ones.
- Handle contradictions and regime-dependence explicitly (this is critical for trading content).

**Non-Goals**
- No Obsidian or any GUI note app dependency.
- Keep it lightweight and file-based. Avoid heavy new databases unless they are generated on-demand (e.g. the graph).
- The wiki is the compiled knowledge layer; raw transcripts remain the source of truth.

Please start by:
1. Confirming you understand the structure and schema importance.
2. Proposing any refinements to the folder taxonomy after a quick scan of transcript themes.
3. Creating the skeleton + `WIKI_SCHEMA.md` draft.
4. Then doing the initial population + graph + RAG bridging.

This should give me a living “second brain” for the Outlier material that gets smarter over time and makes both my RAG and future AI trading agents significantly more powerful.

---

Copy the above, paste it to your developer, and give them access to the transcripts folder (and Opteee codebase if comfortable). It is written to be self-contained and actionable while giving the developer room to make good domain-specific decisions after analyzing your content.

If you want any section tightened, expanded (e.g. more detailed schema outline or example page templates), or adjusted for specific tech choices in Opteee, just tell me and I’ll refine the prompt.
