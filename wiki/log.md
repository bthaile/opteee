# Wiki Ingest Log

Append-only chronological history of wiki builds. Newest first.

## 2026-07-03 — Prototype build (14-video sample)

**Auto source-pass** (14 parallel reader agents, one per video) → 14 `sources/*.md` pages spanning all major Outlier themes: covered strangle, IV/vega, 0DTE, GEX/DEX, the GME/Roaring-Kitty saga, the Sosnoff/Hunter/Sinclair/Shannon interviews, Project No Code, covered calls, earnings/FOMC, and a beginners live.

**Agent synthesis** → 4 flagship knowledge pages:
- [[concepts/volatility-risk-premium]]
- [[concepts/implied-volatility]]
- [[strategies/covered-strangle]]
- [[people/euan-sinclair]]

**Purpose:** validate `WIKI_SCHEMA` conventions (frontmatter, facets, slugs, de-noising, contradiction handling) against real noisy auto-caption transcripts before scaling to the full corpus.

**Transcript quality:** all 14 de-noised cleanly (YouTube captions triple each phrase across rolling windows); confidence high on thematic content, low on some live numeric figures (ASR renders share counts/P&L as calendar dates). No garbled text was quoted.

**Schema friction captured for `WIKI_SCHEMA.md`** (see design doc §12 learnings): `experts` vs mentioned-people; multi-valued `format`; securities slug registry (tickers vs commodity/index name-slugs); `series` enum gap (`gme-analysis`); saga ordering metadata; mechanics-vs-philosophy concept split; interview `stances`; macro structured `predictions:` block; canonical slug registry + aliases.

**Three contradictions surfaced** (see [[index]]): GEX actionable vs nonsense; mean-reversion; 0DTE wings.
