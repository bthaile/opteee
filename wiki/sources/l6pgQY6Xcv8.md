---
type: source
title: "Outlier Trading Operations Center 6-Month Update"
video_id: l6pgQY6Xcv8
url: https://www.youtube.com/watch?v=l6pgQY6Xcv8
date: 2026-10-11
series: project-no-code
format: [education, market-note]
experts: [eric]
mentions: []
securities: []
concepts: [ai-assisted-trading, algorithmic-trading, backtesting, data-analysis, data-hygiene, data-quality, data-mining, machine-learning, portfolio-construction, research-methodology, statistical-analysis, systematic-trading]
strategies: [systematic-trading, algorithmic-trading, post-earnings-drift, mean-reversion, momentum]
saga: none
part: null
confidence: high
---

# Outlier Trading Operations Center 6-Month Update

## Summary

Eric presents a comprehensive 6-month retrospective on the Outlier Trading Operations Center (OTOC), a data warehouse and research infrastructure built with AI assistance. The system now contains 561 tables, 50+ billion rows of market data, 60+ terabytes of storage, and has generated 194 original research studies and 16 strategies. The update covers data ingestion architecture, the Hugan UI platform, research methodology, and demonstrates how one person with no prior coding background can accomplish ~176 programmer-years of work using AI tools.

## Key takeaways

- **Scale of infrastructure**: 561 tables, 50+ billion rows, 60+ terabytes, 657,000 parquet files, 194 research studies, 16 strategies developed in 146 days [11:07]
- **AI productivity**: 2.2 million lines of production code written in 146 days (~176 programmer-years) using Claude and Codeex with internal code review agents [13:51]
- **Data ingestion strategy**: Four methods—streaming listeners, intraday polls (refresh buttons), daily incremental (DINK, ~2 hours), and full incremental (3–7 hours overnight) [18:08]
- **Data sources**: Free (FRED macro series 200+), commercial (OATS, Unusual Whales, Massive/Polygon, Alpha Vantage), and hedge fund proprietary data; emphasis on multi-source validation [20:45]
- **Data cleaning essentials**: Standardization across sources (delta conventions, split adjustments, dividend handling, earnings timing), validation via redundancy, raw files never modified [52:31]
- **Hugan UI architecture**: Python-based (Streamlit 1.57, Plotly 67, DuckDB), 271 charts across 63 subtabs, 77 reachable views; precomputation reduces render times from 131 seconds to 0.01 seconds [36:30]
- **Storage strategy**: Hot data (internal SSD for active analysis), external SSD (slower backup), external HDD (master + mirror for redundancy); weekly full backups [28:13]
- **Research findings**: High win-rate credit spreads often negative EV; simple moving average crossovers frequently fail out-of-sample; put selling underperforms buy-and-hold; call selling likely negative EV [33:30]
- **Strategy portfolio performance**: Combined suite of post-earnings drift, earnings longfall, and related strategies yields ~22% CAGR with 12% volatility and 11% max drawdown [15:13]
- **Organization as critical edge**: Disorganization can undo all data advantages; strict naming conventions for AI sessions and research folders prevent duplication and enable efficient retrieval [32:07]
- **Basic School curriculum**: 957-slide educational resource (modeled on Marine Corps Basic School) covering market mechanics and trading fundamentals; designed as comprehensive onboarding [46:27]

## Notable quotes

> "It is an enabler that's hard to fully comprehend. And it's something that I think is really useful for pretty much everybody regardless of what level of depth you choose to go into." [13:51]

> "You cannot expect any data that you get to be fully clean. Any data. It is an expectation that you have to go through and make sure that it's cleaned." [54:50]

> "If it's slow, not going to use it." [38:14]

## Candidate wiki links

**concepts:**
[[ai-assisted-trading]], [[algorithmic-trading]], [[backtesting]], [[data-analysis]], [[data-hygiene]], [[data-quality]], [[data-mining]], [[machine-learning]], [[portfolio-construction]], [[research-methodology]], [[statistical-analysis]], [[systematic-trading]], [[api-gating]], [[automation]], [[workflow-optimization]], [[organization]], [[naming-conventions]]

**strategies:**
[[systematic-trading]], [[post-earnings-drift]], [[mean-reversion]], [[momentum]], [[covered-strangle]], [[short-put]], [[short-call]]

**tools/platforms:**
Hugan (Streamlit-based UI), Artemis (scanner suite), Munan (documentation), DuckDB (data warehouse), Claude/Codeex (AI code generation)

## Regime / context

**Date context (2026-10-11):** This update reflects 146 days of development from ~May 17, 2026. The OTOC is a living system; performance metrics and code volume are snapshots at this moment. The Basic School curriculum (957 slides) is in final review and expected to launch soon. The infrastructure is designed for continuous expansion; the host expects growth to plateau in the next 6-month cycle but remain substantial.

**Methodological note:** All numeric figures (rows, terabytes, lines of code, strategy returns) are approximate due to ASR transcription; treat as order-of-magnitude indicators rather than exact values. The 22% CAGR and 12% volatility figures are backtested results on a combined strategy suite, not live performance.
