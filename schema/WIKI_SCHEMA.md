# WIKI_SCHEMA.md — The OPTEEE Wiki Constitution

This file is the single source of truth for how the OPTEEE LLM Wiki is built, updated, queried, and linted. Any LLM session (Claude Code, Cursor, or an automated script) must be able to maintain the wiki correctly from this file alone. If you change a convention here, update [`slugs.md`](slugs.md) and the scripts in `scripts/` to match.

Design rationale and history: [`../docs/plans/2026-07-03-llm-wiki-design.md`](../docs/plans/2026-07-03-llm-wiki-design.md).

---

## 0. Mental model

- **`processed_transcripts/*.json` + `outlier_trading_videos_metadata.json` are the immutable source of truth.** The wiki only reads them.
- **`wiki/` is the compiled, LLM-owned knowledge layer.** Everything in it is synthesis.
- Two kinds of pages: **source pages** (one per video, automated coverage) and **knowledge pages** (concepts/strategies/securities/people/macro/syntheses, curated synthesis).
- Folders describe *knowledge*. Series/format/date/experts are *frontmatter facets*, not folders.

## 1. Directory layout

```
wiki/
├── index.md            # GENERATED Markdown projection of graph.json (query entrypoint)
├── log.md              # append-only ingest history, newest first
├── related_videos.json # GENERATED reverse map: video_id -> [wiki page paths] (the RAG bridge)
├── graph.json          # GENERATED graph for the /wiki view (nodes+edges+baked layout)
├── sources/            # {video_id}.md — one per video (automated source-pass)
├── concepts/           # options mechanics + mental-models + process (see subtype)
├── strategies/         # actionable structures
├── securities/         # tickers / assets / sagas
├── people/             # recurring guests, hosts, referenced figures
├── macro/              # regime & macro theses (time-sensitive; use predictions)
└── syntheses/          # cross-video playbooks, timelines, "the Outlier method"
```

Filenames: knowledge pages `kebab-case.md`; source pages `{video_id}.md` (the video_id is the RAG join key). Human titles live in frontmatter, never in the source filename.

## 2. Source pages (`sources/{video_id}.md`)

Produced by the automated source-pass (`scripts/ingest_wiki.py`). Frontmatter:

```yaml
---
type: source
title: "<exact title from the transcript's title field>"
video_id: "<id>"
url: "https://www.youtube.com/watch?v=<id>"
date: "YYYY-MM-DD"                 # from metadata upload_date
series: <slug|none>               # controlled — §4
format: [<slug>, ...]             # LIST, controlled — §4 (a video is often live+education)
experts: [<people-slug>, ...]     # FEATURED guests/hosts only (host default: eric)
mentions: [<people-slug>, ...]    # people discussed but not present (Taleb, Roaring Kitty…)
securities: [<security-slug>, ...] # substantively-discussed only; registry slugs
concepts: [<concept-slug>, ...]   # candidate concept links (registry slugs)
strategies: [<strategy-slug>, ...]
saga: <slug|none>                 # e.g. gme — set when part of a multi-part saga
part: <int|null>                  # saga part number if applicable
confidence: <high|medium|low>     # extractor confidence given transcript quality
---
```

Body sections (in order):
1. `# <title>`
2. `## Summary` — 2–4 sentences, precise trading language.
3. `## Key takeaways` — concrete, usable bullets with `[mm:ss]` timestamps. For **market-update / live** videos, split into `### Dated market read (YYYY-MM-DD)` and `### Evergreen mechanics`.
4. `## Notable quotes` — 0–3 SHORT verbatim quotes, **only if cleanly reconstructable**. Omit if the text is too garbled. (See §6.)
5. `## Candidate wiki links` — grouped `concepts:` / `strategies:` / `securities:` / `people:` `[[wikilinks]]`.
6. `## Regime / context` — date/regime caveats; for saga videos, note prev/next part.

## 3. Knowledge pages

Types: `concept`, `strategy`, `security`, `person`, `macro`, `synthesis`. Common frontmatter:

```yaml
---
type: <concept|strategy|security|person|macro|synthesis>
title: "<Human Title>"
aliases: [<slug>, ...]            # alternate slugs that resolve here — prevents drift
related_videos: ["<video_id>", ...]  # THE RAG-bridge key — every backing video
related_concepts: [<slug>, ...]
related_strategies: [<slug>, ...]
last_updated: YYYY-MM-DD
confidence: <high|medium|low>
regime_dependent: <true|false>    # strategies/macro especially
subtype: <mechanic|mental-model|process>   # concepts ONLY (§4)
---
```

- **concept** — one idea. `subtype` required: `mechanic` (IV, delta, GEX), `mental-model` (risk-taking, decision-volume), or `process` (process-over-outcome, no-code workflow).
- **strategy** — structure, when-to-use, management playbook, regime dependence, risks.
- **security** — ticker/asset/saga page; for sagas include a timeline.
- **person** — who they are, core positions, **distinctive/contested stances** (feeds contradiction tracking), where they agree with the mainstream.
- **macro** — thesis + a structured `predictions:` block (§9).
- **synthesis** — cross-video playbook / timeline / "the Outlier method."

Standard body: `## Definition/Summary`, topic sections with `[[links]]` + `[[sources/<id>]]` citations and `[mm:ss]`, `## Contested / open questions` (if any), `## Regime / caveats`, `## See also`.

**Every claim cites its origin** as `[[sources/<video_id>]]` + timestamp.

## 4. Controlled vocabularies

- **series**: `options-trench`, `outlier-podcast`, `beginner-lab`, `project-no-code`, `market-update`, `meme-stock-watch`, `gme-analysis`, `small-stacks`, `stock-watch`, `money-talks`, `unhedged`, `none`. Rule: channel interviews without "Ep##" branding → `outlier-podcast` if clearly that show, else `none`. Add new values here + in `slugs.md`.
- **format** (list): `education`, `interview`, `market-note`, `live`, `analysis`, `strategy-breakdown`.
- **concept subtype**: `mechanic`, `mental-model`, `process`.

## 5. Slugs & aliases

- kebab-case, canonical, singular where natural.
- **Every slug must exist in [`slugs.md`](slugs.md) or be added there in the same change.** This is the drift guardrail — the lint gate fails on unregistered slugs.
- Merge synonyms via `aliases:` on the canonical page (e.g. `coverage-triangle` → `covered-strangle`; `cash-secured-put` and `short-put`; `vwap` → `anchored-vwap` only if intended). Never create two pages for the same idea.

## 6. De-noising rules (critical)

Transcripts are YouTube auto-captions: **each phrase repeats 2–3× across rolling windows, no punctuation, lowercase**, with predictable garbles ("vol"→"ball/vault", "bid ass"→bid-ask). To extract:
- Collapse the repetition; read for meaning; **never reproduce the tripling**.
- **Live numeric figures (share counts, P&L, prices) are frequently ASR-garbled** (rendered as calendar dates). Treat exact numbers as approximate; flag uncertainty in the page; do not assert false precision.
- **Exact-quote contract:** only put a line in `## Notable quotes` if you can reconstruct it verbatim with confidence. This preserves OPTEEE's existing highlight contract (see `config.py` SYSTEM_PROMPT) — a garbled "quote" breaks source highlighting downstream.

## 7. Ingestion workflow (automated source-pass)

`scripts/ingest_wiki.py` (provider defaults to `claude` / `claude-haiku-4-5`):
- **Incremental by default** (`--new-only`): only videos in `processed_transcripts/` with no existing `wiki/sources/{video_id}.md`.
- `--limit N` for testing; `--force` to re-do existing; `--video <id>` for one.
- Per video: read the processed transcript, de-noise, emit the source page per §2 using only registry slugs (propose new ones to `slugs.md`).
- Idempotent: re-running with `--new-only` is a no-op when nothing is new.

## 8. Synthesis workflow (curated, agent-in-session)

Not on the weekly cron — run by the owner in a Claude Code session:
- Consolidate all mentions of a concept/strategy into **one evolving page**, preserving video-specific examples and regime context, citing each `[[sources/<video_id>]]`.
- Prefer to strengthen an existing page over creating a thin new one.
- Update `related_videos` (drives the bridge) and `aliases`.
- Append a `log.md` entry.

## 9. Contradictions, evolving & regime knowledge

Trading truth is regime-dependent — **surface tensions, do not smooth them over**:
- When sources disagree, add a `## Contested / open questions` section with a ⚠️ marker on the relevant knowledge page, name both sides with `[[sources/<id>]]`, and assign an **owner page** in `index.md`'s contradiction tracker.
- Newer videos may qualify/override older claims: record both with dates and `regime_dependent: true`; never silently overwrite.
- **macro `predictions:` block** — machine-checkable for later resolution:
  ```yaml
  predictions:
    - who: david-hunter
      claim: "S&P 8000"
      security: spx
      target: 8000
      deadline: "2025-12-31"
      status: open   # open | confirmed | missed
      source: "6Sp4eF9ahW8"
  ```

## 10. Query workflow

Read `index.md` first → follow `[[wikilinks]]` → answer citing **both** the wiki page and the specific `[[sources/<video_id>]]` (+ timestamp). Raw transcripts remain the source of truth for verbatim detail.

## 11. Lint rules (`scripts/lint_wiki.py` — the weekly gate)

**Hard-fail (non-zero exit → weekly build stops before commit/reindex):**
- a `[[wikilink]]` whose slug is **not registered** in `slugs.md` (canonical or alias) — this catches typos and drift,
- duplicate canonical pages for the same idea (two pages sharing an alias),
- a knowledge page with empty body or missing required frontmatter,
- malformed frontmatter / invalid `series`/`format`/`subtype` value.

**Warn (report, don't fail):**
- a `[[wikilink]]` to a **registered slug that has no page yet** — this is the normal growth backlog (each source seeds future pages), not an error,
- dangling `[[sources/<id>]]` link to a video not yet ingested,
- orphan knowledge pages (no inbound links), source pages with `confidence: low`, `predictions` past `deadline` still `open`, concepts with no `subtype`.

Rationale: a growing wiki is *mostly* forward-references to uncreated pages. Failing on those would make the gate red forever; failing on unregistered slugs is what actually catches quality regressions.

## 12. Data contracts (generated artifacts)

- **`wiki/related_videos.json`** — built by `annotate_chunks.py` (or a helper) by inverting every knowledge page's `related_videos`:
  ```json
  { "AJP8M8DQ_1U": ["strategies/covered-strangle", "concepts/volatility-risk-premium"], ... }
  ```
- **Chunk annotation** — `annotate_chunks.py` adds `related_wiki_pages: [...]` to each chunk dict in `processed_transcripts/{video_id}_processed.json`, keyed by the chunk's `video_id`, **before** the `vectors` step. Because `create_vector_store.py` stores the whole chunk dict as FAISS metadata, the field rides through to `doc.metadata['related_wiki_pages']` and into `/api/chat` `raw_sources` with no retriever changes. Runs full-scan every build (cheap, no LLM) to refresh links from current wiki state.
- **`wiki/graph.json`** — built by `build_graph.py`; knowledge-layer nodes only:
  ```json
  {
    "nodes": [{"id":"concepts/volatility-risk-premium","label":"Volatility Risk Premium",
               "category":"concept","size":6,"video_count":6,"degree":9,"x":0.0,"y":0.0}],
    "edges": [{"source":"strategies/covered-strangle","target":"concepts/volatility-risk-premium",
               "type":"wikilink","weight":1,"label":"wiki link"}]
  }
  ```
  `size`/`video_count` = length of `related_videos`; edges = explicit `[[wikilinks]]` between knowledge pages plus generated co-occurrence relationships. Co-occurrence edges include `shared_source_count` and `label` (for example `shared source videos: 7`) while `weight` remains a capped visual weight. `x`/`y` = baked force-layout coordinates. Source pages are NOT nodes (served via `?include=sources` expansion).
- **`wiki/index.md`** — built by `build_wiki_index.py` from `wiki/graph.json`, materialized knowledge-page frontmatter, and source-page frontmatter. `/wiki` loads `graph.json`; `index.md` is the Markdown/LLM-readable form of the same knowledge graph. It must report counts matching `graph.json` and `wiki/sources/*.md`, group nodes by `concepts` / `strategies` / `securities` / `people` / `macro` / `syntheses`, and show source-derived candidate nodes as the synthesis backlog.
- **Agent JSON API** — `/api/wiki/index/document` returns generated `wiki/index.md` as `{path, frontmatter, markdown, wikilinks}`; `/api/wiki/pages/{path}?format=json` returns `{path, frontmatter, markdown, html, wikilinks}`. Browser clients may keep using the default page response HTML, while agents should use the JSON/Markdown fields and structured `wikilinks`.
