# OPTEEE LLM Wiki — Design

**Status:** Draft (design agreed via brainstorming, not yet implemented)
**Date:** 2026-07-03
**Supersedes:** the generic prompt in `docs/LLM_WIKI.md` (that was written before analyzing the codebase; several of its technical assumptions are wrong for OPTEEE — see "Corrections" below).

## 1. What this is

A **compounding, LLM-maintained knowledge layer** over the Outlier Trading corpus that sits *alongside* the existing RAG system. Where the RAG re-derives connections on every query from raw chunks, the wiki extracts, synthesizes, and cross-references trading knowledge into durable Markdown pages that get smarter as new videos land.

**v1 audience: the owner, for personal trading / investing / research.** Not a public product. Optimize for the owner's reading + querying, not external consumers.

### Goals
- Turn ~1000 noisy transcripts into a small set of *excellent*, well-linked concept/strategy pages (quality over coverage).
- Bridge the wiki into RAG answers so chat can surface synthesized knowledge, not just chunks.
- A single-page interactive graph to navigate high-level concepts and drill down to the video moment.

### Non-goals (v1)
- No public/external API hardening, auth, or multi-tenant concerns.
- No Obsidian/GUI dependency. Pure filesystem + Markdown.
- No static image exports (PNG/PDF) or GraphML/CSV — the graph is interactive HTML only.
- No new database. The graph and reverse links are generated build artifacts.

## 2. Phasing (agreed)

- **Phase 1** — the synthesized wiki + RAG bridge. Prove the content is good.
- **Phase 2** — expose the browse/graph REST layer once content proves out.

Same knowledge layer, two consumers over time.

## 3. Key decisions

| Decision | Choice | Why |
|---|---|---|
| v1 target | Personal research tool, phased | Owner is the only consumer; RAG bridge is highest value |
| Maintenance | **Hybrid** — cheap auto source-pass + curated agent synthesis | Automation gives coverage; agent gives quality synthesis |
| Taxonomy | Folders = knowledge; series/format/date/experts = frontmatter facets | Outlier content has two axes; only knowledge belongs in the tree |
| Graph serving | **Static, precomputed at build**, served as files; interactive client-side | Data changes only at build (weekly); per-request compute is wasted |
| Graph output | Interactive HTML + `graph.json` only | Drill-in is the point; images are dead weight |
| RAG bridge | **Chunk-embedded** `related_wiki_pages` (SOW Option A), baked in weekly | Weekly re-embed cost is acceptable; links ride along in `raw_sources` |
| Source of truth | Existing `processed_transcripts/*.json` + `outlier_trading_videos_metadata.json` | Already chunked, timestamped, `video_id`-keyed |

## 4. Corrections to the original prompt (`docs/LLM_WIKI.md`)

The prompt assumed a corpus and structure OPTEEE doesn't have. Corrected here:

- **Raw format.** Prompt assumed `raw/*.md` with YAML frontmatter named `YYYY-MM-DD_Slug_Title.md`. Reality: `transcripts/*.txt` (1143 files) named by **video_id**, plus chunked `processed_transcripts/{video_id}_processed.json` (1140), plus `outlier_trading_videos_metadata.json` (1027 videos). The wiki reads the processed JSON + metadata; **no `raw/` tree is created**.
- **Transcript quality is the dominant cost.** Text is raw YouTube auto-captions with tripled/repeated lines, no punctuation, no speaker labels. De-noising over 1000 videos drives cost and quality far more than folders or graph layout. Prototype extraction quality first.
- **REST API was underspecified.** The prompt names it in the architecture and goals but omits it from the numbered deliverables and gives no endpoints/schemas. Specified here (§8).
- **Graph reframed.** Prompt framed it as a static-file generator with image/GraphML exports. Reframed as a live-navigable interactive HTML view served as static artifacts (§8).
- **Freshness missing.** `weekly-refresh.sh` adds videos every Sunday; the wiki needs an incremental build step wired into it (§9), or it goes stale in a week.

## 5. Folder structure & schema

### Layout
```
wiki/
├── index.md              # GENERATED Markdown index of the knowledge graph
├── log.md                # append-only ingest history
├── concepts/             # volatility-and-iv, greeks, gex-dex-dealer-flow,
│                         #   options-chain-reading, market-regimes, technicals
├── strategies/           # covered-strangle (signature), covered-call, short-put-wheel,
│                         #   zero-dte, credit-spread, early-exercise, earnings-pead
├── securities/           # gme-saga, spx-spy, spacex-spcx, nvda, tsla, sector-etfs
├── people/               # tom-sosnoff, david-hunter, euan-sinclair, brian-shannon
├── macro/                # melt-up-bust, fed-rates-inflation, recession, ai-changes-trading
├── syntheses/            # the-outlier-method, how-outlier-trades-earnings, gme-saga-timeline
└── sources/              # one page per video — {video_id}.md (coverage layer)

schema/WIKI_SCHEMA.md     # the constitution (§7)
scripts/                  # ingest / annotate / build_graph / lint
```

The taxonomy is grounded in a scan of all 1027 titles. Dominant real themes: education/beginners (159 titles), podcast interviews with recurring experts (80; Sosnoff 22, Hunter 17, Sinclair 11), the GME/meme/Roaring Kitty saga (102 GME titles), volatility/IV (51), the signature covered strangle (24), 0DTE, GEX/DEX dealer flow, and "Project No Code" AI-trading.

### `index.md` contract
`index.md` is the **Markdown/LLM-readable projection of the knowledge graph**. It is not a hand-maintained prototype page and it is not the browser's graph data source.

- `/wiki` loads `wiki/graph.json` for the interactive browser.
- `wiki/index.md` mirrors the same graph in Markdown so agents and humans can read the graph without opening the browser.
- It must be generated on every wiki build from `wiki/graph.json`, materialized knowledge pages, and source-page frontmatter.
- It should group the graph by top-level knowledge categories (`concepts`, `strategies`, `securities`, `people`, `macro`, `syntheses`) and show source-derived candidate nodes under those categories.
- Each materialized node entry should include a link to the page, one-line summary, graph degree / linked neighbors, and backing source count.
- Source pages remain backing evidence, not default graph nodes. They should appear as coverage/facet summaries and can be listed in a collapsed source catalog if useful.
- Acceptance rule: `index.md` must not report stale prototype counts. Its knowledge-page count must match the graph node count, and its source count must match `wiki/sources/*.md`.

### Facets (Axis B — controlled vocabulary, mainly on `sources/`)
Series and format are *tags*, not folders, because a series like "The Options Trench" spans concepts + strategies + people.
```yaml
---
type: source
title: "Expert Guide to Technical Analysis with Brian Shannon"
video_id: "_bB29g2ofI0"
date: 2020-xx-xx
series: options-trench      # options-trench | outlier-podcast | beginner-lab |
                            #   project-no-code | market-update | small-stacks |
                            #   stock-watch | money-talks | unhedged | none
format: interview           # education | interview | market-note | live | analysis | strategy-breakdown
experts: [brian-shannon]    # controlled slugs → people/
securities: [spy]           # controlled ticker slugs → securities/
concepts: [technicals, volatility-and-iv]   # → concepts/
confidence: medium
---
```

### Knowledge pages
`concepts/ strategies/ securities/ people/ macro/ syntheses/` carry:
```yaml
type: strategy
related_videos: ["_bB29g2ofI0", "bWLpkHzqBqM"]  # the RAG-bridge join key
last_updated: 2026-07-03
confidence: high
regime: low-iv              # strategies/macro only — makes regime-dependence explicit
```
`related_videos` is the pivot for both the RAG bridge (§6) and the graph (§8).

## 6. RAG bridge (chunk-embedded)

**Approach:** during the weekly build, stamp each transcript chunk with the wiki pages that reference its video, then re-embed. The mapping is video-level (`video_id → [wiki pages]`, inverted from every page's `related_videos`), materialized onto each chunk of that video.

- Result: every retrieved source in a RAG answer already carries `related_wiki_pages` in its metadata → surfaces directly in `raw_sources` with **zero query-time lookup**.
- `RAGService` / `formatters.py` append these as clean relative links (`../wiki/strategies/covered-strangle.md`) beneath the answer, and can optionally interleave a short synthesized excerpt (SOW Option B) for high-level questions.
- Cost: a full re-embed on each build. **Accepted** — the pipeline rebuilds weekly and build latency is not a concern.

Chunk annotation is a new pipeline step **before** `vectors`. It reads the current wiki state, so it picks up whatever synthesis pages exist at build time (synthesis itself is curated/periodic — §9).

## 7. `WIKI_SCHEMA.md` — the constitution

The highest-leverage deliverable. Any LLM session must be able to ingest, update, query, and lint the wiki from this file alone. Required sections:

1. **Page taxonomy** — each page type, when to create vs update, required frontmatter, standard section skeleton (Concept / Strategy / Security / Person / Macro / Synthesis / Source).
2. **Controlled vocabularies** — the facet lists (series, format, experts, securities slugs) and how to add a new term.
3. **Ingestion workflow** — single video and batch; how to write a `sources/` page; how to propose candidate concepts/strategies without prematurely creating shallow pages.
4. **Synthesis rules** — consolidate all mentions of a strategy into one evolving page while preserving video-specific examples and regime context; always cite the originating `video_id`(s).
5. **Evolving knowledge & contradictions** — newer videos may qualify/override older claims; record both with dates and `regime:`; never silently overwrite. Critical for trading content.
6. **De-noising rules** — how to read tripled/garbled auto-caption text; never quote garbled text as an "exact quote" (respect the existing RAG exact-quote contract in `config.py`).
7. **Query workflow** — read generated `index.md` first as the Markdown knowledge graph, follow `[[wikilinks]]`, cite specific videos + wiki pages.
8. **Lint rules** — orphans, broken wikilinks, stale claims, missing `related_videos`, contradictions, suggested new pages/questions. Encoded in `scripts/lint_wiki.py`.
9. **Trading-domain style** — precise, sourced, learner-friendly; define terms on first use.

## 8. Graph + REST layer (Phase 2)

**Static, precomputed at build; interactive client-side; served as files.**

Endpoints (new routes in `main.py`, backed by `app/services/wiki_service.py`):
```
GET /wiki                    → self-contained interactive HTML: 2D force-directed
                               node-link graph + side reading panel
GET /api/wiki/graph.json     → nodes[{id,label,category,theme,size,video_count,degree,x,y}],
                               edges[{source,target,type,weight,label,shared_source_count?}]
                               (layout baked at build)
GET /api/wiki/pages/{slug}   → one page as JSON; default includes rendered HTML
GET /api/wiki/pages/{slug}?format=json
                              → one page as JSON with frontmatter + markdown + HTML + wikilinks
GET /api/wiki/index          → JSON catalog for browse
GET /api/wiki/index/document → generated index.md as JSON for agents
```

**Graph scope = knowledge layer only** (`concepts/ strategies/ securities/ people/ macro/ syntheses/`) — dozens–low-hundreds of nodes, readable on one screen. The ~1000 `sources/` pages are NOT nodes; a node's **size = its `related_videos` count** (provenance as weight). `?include=sources` expands on demand.

- Node color = folder/category (the clusters). Edges = explicit `[[wikilinks]]` + generated co-occurrence (topics sharing enough backing videos). Edge labels come from `type` and exact co-occurrence metadata: `wikilink` = explicit page relationship, `cooccurrence` = `shared source videos: N`.
- The `/wiki` browser should start in a decluttered, zoomed-in view of the highest-signal nodes. It should keep the full graph available by pan/zoom/search, but show secondary node labels and relationship labels only when zoomed in or when a node/edge is inspected.
- **Drill-in interactions:** overview → hover tooltip → click node (focus ego-view + load page in side panel) → expand to reveal backing `sources/` → each source deep-links to the YouTube timestamp via existing metadata → filter by category/facet → search by name.
- Rendering: vendored `cytoscape.js` or `vis-network`, all client-side. No CDN, no external calls.

`scripts/build_graph.py` writes `wiki/graph.json` (with baked x/y from a one-time force layout) during the build. FastAPI serves it and the HTML shell as static files (`StaticFiles`/`FileResponse`, browser-cacheable). Zero per-request compute.

`scripts/build_wiki_index.py` should write `wiki/index.md` from the built graph plus wiki frontmatter. This is the same knowledge graph expressed as Markdown for LLM/query workflows. It prevents the current failure mode where `/wiki` correctly loads `graph.json`, but `wiki/index.md` remains a stale 14-source / 4-page prototype catalog.

Agents should consume the JSON forms instead of scraping HTML: `/api/wiki/index/document` for the graph-backed Markdown entrypoint, `/api/wiki/pages/{path}?format=json` for page bodies, frontmatter, and structured wikilinks, and `/api/wiki/graph.json` for topology/relationship metadata.

## 9. Freshness — wiring into the existing weekly build

The wiki hooks into the scripts that already run every Sunday, not a new scheduler:

```
launchd com.opteee.weekly-refresh (Sun 23:00)
  → weekly-refresh.sh   (lock, git pull if clean, run pipeline, refresh .venv-native,
                         restart native app, health check, commit+push artifacts)
      → run_transcripts.sh   (the actual content pipeline)
          → run_pipeline.py --step scrape / transcripts / preprocess / vectors
          → retry_and_whisper.py
```

> **Scheduler note.** The build is driven by launchd `com.opteee.weekly-refresh` → `weekly-refresh.sh` — **not** by hermes. The hermes cron jobs (`outlier-daily-lesson` @ 15:00 daily, `daily-ta-lesson`, `weekly-ta-lesson-generation`, `aar-learning-digest`) are *consumers* that query the live OPTEEE API at `localhost:7860`; none run the build scripts. Side benefit: once the RAG bridge lands, those agents get `related_wiki_pages` in their `/api/chat` responses for free, and the Phase-2 `/api/wiki/*` endpoints give them structured wiki access — the wiki upgrades an existing consumer ecosystem, not just interactive use.

Two files change.

### `run_transcripts.sh` — insert wiki steps around `vectors`

Order is load-bearing: `ingest` + `annotate` must run **before** `vectors` so the re-embed bakes `related_wiki_pages` into the FAISS metadata; `build_graph` runs **after** so it reads the final wiki state.

```sh
python3 run_pipeline.py --step scrape --non-interactive
python3 run_pipeline.py --step transcripts --non-interactive
python3 retry_and_whisper.py
python3 run_pipeline.py --step preprocess --non-interactive
# --- LLM Wiki: coverage layer + RAG bridge, BEFORE vectors ---
python3 scripts/ingest_wiki.py --non-interactive      # auto sources/{video_id}.md for NEW videos
python3 scripts/annotate_chunks.py                    # stamp related_wiki_pages onto processed chunks
# -------------------------------------------------------------
python3 run_pipeline.py --step vectors --non-interactive   # re-embed WITH wiki metadata
python3 scripts/build_graph.py                        # write wiki/graph.json (baked layout)
python3 scripts/build_wiki_index.py                   # write wiki/index.md from graph + frontmatter
```
(`retry_and_whisper.py` is already a standalone script called directly here, so adding standalone `scripts/*.py` matches the existing pattern. They could equally become `run_pipeline.py --step {wiki,annotate,graph}`.)

### `weekly-refresh.sh` — commit the wiki like the other generated artifacts

Add `wiki` to the `REFRESH_ARTIFACTS` array (covers `wiki/graph.json`) so `commit_refresh_artifacts()` stages, commits, and pushes it:
```sh
REFRESH_ARTIFACTS=(
  "outlier_trading_videos.json"
  "outlier_trading_videos_metadata.json"
  "transcripts"
  "processed_transcripts"
  "vector_store"
  "wiki"                       # NEW: built wiki + graph.json
)
```

### What the cron does vs. what stays manual
- **Automated weekly path** maintains *coverage*: new `sources/` pages, `related_wiki_pages` stamped from the current wiki state, reindex, graph.
- **Curated synthesis** (`concepts/`, `strategies/`, `syntheses/`) is agent-in-session work done by the owner between refreshes (§11). Those pages land in `wiki/` and get committed by the next weekly run. The annotate step picks up whatever synthesis exists at build time.
- **Generated index** (`wiki/index.md`) is not curated prose. It is rebuilt from the graph/frontmatter every run so the LLM query entrypoint reflects the current graph instead of the original prototype.

### Two caveats
- **Dependency:** `scripts/ingest_wiki.py` calls an LLM, so the pipeline venv (`venv/`, `requirements.txt`) must include the chosen client (`langchain-anthropic` or `langchain-ollama`). Those currently live only in `requirements-serve.txt` — add the one you use to `requirements.txt`, or have ingest run under `.venv-native`.
- **Pull-skip compounding:** `weekly-refresh.sh` already skips `git pull` whenever the worktree is dirty, and it's usually dirty because generated data is tracked. Adding `wiki/` makes that worse. If reliable weekly *code* pulls matter, untrack generated data per the existing note in `weekly-refresh.sh` / `DEPLOYMENT.md`.

## 10. Extraction model & cost (recommendation)

- **Auto source-pass** (~1000 videos, cheap structured extraction): reuse the existing provider config. Recommend **Claude Haiku** for reliability on noisy ASR, or **local Ollama** (`OLLAMA_BASE_URL` on the M1 Pro) for zero-cost/private batch given latency is acceptable. Output per video is small (summary + candidate entities), so total cost is modest.
- **Synthesis pass**: done agent-in-session (Claude Code) — no per-call API metering — or a stronger model for the hardest consolidations.

## 11. AI agent role — build-time, not runtime

The wiki's value *is* LLM synthesis; the folders, graph, REST API, and scripts are scaffolding with no value until an LLM turns transcripts into knowledge. So an AI agent is required — but under the hybrid decision it splits into two roles, and **both are build-time only**.

- **Programmatic LLM (automated batch)** — `scripts/ingest.py` calls an LLM per video (via the existing provider config) to write `sources/{video_id}.md`. No human in the loop; runs inside the weekly refresh. LLM-as-a-function.
- **Interactive agent (curated synthesis)** — a Claude Code / Cursor session reads `WIKI_SCHEMA.md` + candidate source pages and writes/updates the high-value `concepts/`, `strategies/`, `syntheses/` pages. Periodic, owner-driven. The Karpathy "LLM maintains the wiki" model; the source of quality.

Implications:
- **Build-time dependency only.** Serving the wiki, browsing the graph, and answering RAG queries touch no agent. The agent runs at ingest/synthesis; the output is static Markdown + a static graph + chunk-embedded links.
- **No new infrastructure.** Claude Code covers synthesis; the existing Claude/OpenAI/Ollama config covers the batch pass. `WIKI_SCHEMA.md` keeps any session consistent — and portable to a local Ollama model later.
- **`WIKI_SCHEMA.md` exists *because* the wiki is agent-maintained.** Without an agent there is no need for a constitution; it is the instruction set that prevents drift across sessions and models.
- The §13 prototype is literally one of these synthesis sessions — not future tooling, but the immediate workflow.

## 12. Open items / to decide during build

- Exact provider for the auto source-pass (Haiku vs local Ollama) — decide after a 10–20 video quality prototype.
- Whether synthesized excerpts are interleaved into RAG answers (Option B) or shown only as links — decide after the bridge is visible in chat.
- Graph lib choice (cytoscape.js vs vis-network) — implementation detail.

## 13. First implementation step

Before mass generation: run the hybrid auto source-pass on a **representative 10–20 video sample** across the main themes (a covered-strangle strategy video, a Sosnoff/Hunter/Sinclair interview, a GME-saga video, a volatility/IV explainer, a Project-No-Code AI video, a dated market update). Hand-synthesize 3–4 excellent knowledge pages from them. That validates the schema, the de-noising, and the extraction quality before committing to all 1000.

## 14. Prototype results (2026-07-03) — DONE

Ran the §13 prototype: **14 videos**, one parallel reader-agent each → 14 `wiki/sources/*.md`, then synthesized **4 flagship knowledge pages** ([[concepts/volatility-risk-premium]], [[concepts/implied-volatility]], [[strategies/covered-strangle]], [[people/euan-sinclair]]) + `index.md` + `log.md`.

**Validated:**
- **De-noising works.** Every agent collapsed the 2–3× auto-caption tripling and read the content coherently; all reported high confidence on thematic substance. Failure mode: **live numeric figures** (share counts, P&L) are ASR-garbled (rendered as calendar dates) — reliable for logic, not for exact numbers. Schema must tell extractors to flag numeric uncertainty, never quote garbled text (respects the existing exact-quote RAG contract).
- **Cost/latency profile.** Per-video agent: ~60k–230k tokens, ~2–6 min. Confirms the auto source-pass is viable to run over the full corpus on a cheap model (Haiku/local Ollama).
- **Cross-video synthesis is real.** Frequency map over the 14 pages: `volatility-risk-premium` in 6, `implied-volatility` in 6, `covered-strangle` in 3, `euan-sinclair` in 3 — objective synthesis targets, not guesses.
- **Contradiction handling works.** A "Contested / open questions" section with ⚠️ markers, plus an "owner page" assignment in `index.md`, captured 3 real cross-source contradictions (GEX actionable vs nonsense; mean-reversion; 0DTE wings) without smoothing them over.

**Schema refinements the prototype forced (feed directly into `WIKI_SCHEMA.md`, §7):**
1. **Split `experts` from `mentions`.** `experts` = featured guests/hosts only; people merely *discussed* (Roaring Kitty, Taleb, Masayoshi Son) go in a separate `mentions` field. Default host is **"Eric"** (Outlier Trading) — use a canonical host slug, not empty `experts`.
2. **`format` becomes a list.** Videos are routinely `live` + `education` + `strategy-breakdown`; `series` carries the recurring/live fact.
3. **Canonical slug registry + `aliases`.** Prevent drift: `covered-strangle`↔`coverage-triangle`, `short-put`↔`cash-secured-put`, `zero-dte`/`vix` (concept-vs-strategy/security). Demonstrated via `aliases:` frontmatter on knowledge pages; needs a `schema/slugs.md` registry.
4. **`series` enum is extensible** — add `gme-analysis` ("GameStop Analysis Live" ≠ `meme-stock-watch`); rule for classifying untitled channel interviews.
5. **Saga ordering metadata** — `saga: gme`, `part: N`, `prev`/`next` on source pages; `syntheses/gme-saga-timeline` is the index.
6. **Concept `subtype`** — `mechanic` (IV, delta, GEX) vs `mental-model` (risk-taking, decision-volume) vs `process` (process-over-outcome, context-window-management). Interviews/AI videos overflow the mechanics namespace otherwise.
7. **Structured `predictions:` block for macro** — (security, target, deadline, status) so Hunter's "S&P 8000 by 2025" is machine-checkable for contradiction-tracking, not buried in prose.
8. **Securities registry** — only substantively-analyzed tickers; real tickers where they exist, canonical name-slugs for commodities/indices (`gold`, `crude-oil`, `natural-gas`).
9. **Tiered concepts (primary/secondary)** — broad videos (beginner live) emit ~40 flat concept slugs with no centrality signal; tier them.
10. **Market-note two-subsection pattern** — "Dated market read" vs "Evergreen mechanics" — standard for `market-update`/`live` pages so synthesis can pull the timeless part cleanly.

**Next:** write `WIKI_SCHEMA.md` incorporating 1–10, then scale the auto source-pass to the full corpus and build `scripts/{ingest_wiki,annotate_chunks,build_graph}.py`.

## 15. Hardening Tasks

These are the remaining engineering tasks before treating the LLM Wiki refresh as production-grade.

- **Make wiki bridge failures explicit.** Decide which wiki steps are allowed to degrade. At minimum, `scripts/annotate_chunks.py` must be a hard gate before `vectors`; otherwise the weekly run can rebuild FAISS without `related_wiki_pages`.
- **Validate source pages before writing.** `scripts/ingest_wiki.py` should parse generated YAML frontmatter, verify controlled vocab values, and reject unregistered slugs before writing `wiki/sources/{video_id}.md`. Regex-only key checks are not enough.
- **Quarantine bad LLM outputs.** Failed source pages should land in a review directory or error log, not in `wiki/sources/`, so one malformed page cannot poison the lint gate.
- **Finish the RAG response bridge.** Default HTML responses currently preserve `related_wiki_pages` in `raw_sources`, but do not render visible wiki links. JSON/bot formatting must preserve the field too, so downstream agents receive it.
- **Decide weekly ingest shape.** The manual `--shard i/N` path worked for batch backfill, but the scheduled weekly path is still a single `--new-only` process. Choose a weekly policy: single small incremental pass, sharded workers, or manual bulk ingest only.
- **Make the publish contract atomic.** Avoid committing `processed_transcripts/` and `vector_store/` derived from a wiki state while withholding `wiki/` because lint failed. Either publish all three together or keep the previous known-good wiki bridge.
- **Exercise a full dry-run mode.** Add a non-committing, non-pushing weekly test mode that runs the complete ordering through graph build and health checks without restarting production or pushing artifacts.
- **Keep generated-data pulls reliable.** The dirty-worktree guard still skips `git pull` whenever tracked generated artifacts change. Decide whether generated artifacts should stay tracked; if yes, document the operational cost.
- **Vendor the graph dependency.** `templates/wiki_graph.html` should use a local Cytoscape/vis-network asset, not a CDN, to match the no-external-calls design.
- **Add acceptance checks to the weekly log.** After vectors, report counts for source pages, lint errors, chunks with `related_wiki_pages`, non-empty wiki-linked chunks, graph nodes/edges, and API endpoint status after restart.
- **Generate `index.md` from the graph.** Add `scripts/build_wiki_index.py`, run it after `build_graph.py`, and fail the build if `wiki/index.md` reports counts that do not match `wiki/graph.json` and `wiki/sources/*.md`.

### Status (2026-07-03)

| # | Task | Status |
|---|---|---|
| 1 | Wiki bridge failures explicit / annotate hard-gate before vectors | ✅ done — `run_transcripts.sh` aborts if annotate fails |
| 2 | Validate source pages before writing (YAML, vocab, slugs) | ◻️ partial — `normalize_frontmatter.py` self-heals title YAML + `lint_wiki.py` blocks bad slugs/vocab at the gate; in-`ingest` YAML validation not yet added |
| 3 | Quarantine bad LLM outputs to a review dir | ◻️ remaining — rejects are logged + skipped (not written), but no `wiki/_quarantine/` |
| 4 | Finish the RAG response bridge (visible wiki links, JSON/bot preserve field) | ✅ done — `wiki_references` in HTML + API + `/wiki/page/<path>` view (new tab) |
| 5 | Decide weekly ingest shape | ✅ decided — weekly = single `--new-only`; `--shard i/N` is for manual bulk backfill (WIKI_SCHEMA §7) |
| 6 | Atomic publish contract | ✅ done — lint hard-gates before vectors; content + `wiki/` commit together |
| 7 | Full dry-run mode (no commit/push/restart) | ◻️ remaining |
| 8 | Reliable generated-data pulls (dirty-worktree skips `git pull`) | ◻️ remaining — pre-existing; decision: untrack generated data |
| 9 | Vendor the graph dependency (Cytoscape CDN → local) | ◻️ remaining |
| 10 | Weekly-log acceptance checks | ◻️ partial — `scripts/smoke_test.py` asserts all of these; not yet wired into `weekly-refresh.sh` |
| 11 | Generated graph-backed `wiki/index.md` | ◻️ remaining — `/wiki` loads `graph.json`, but `index.md` is still the stale prototype; add `scripts/build_wiki_index.py` and count checks |
