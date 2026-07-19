---
type: source
title: "This AI Research Terminal Changed How I Trade Options | The O/TOC"
video_id: rLRUpaTcrxE
url: https://www.youtube.com/watch?v=rLRUpaTcrxE
date: 2026-07-15
series: project-no-code
format: [education, analysis]
experts: [eric]
mentions: []
securities: []
concepts: [ai-assisted-trading, algorithmic-trading, data-analysis, data-hygiene, data-quality, research-methodology, hypothesis-testing, statistical-analysis, backtesting, market-microstructure, volatility-trading, variance-risk-premium, signal-selection, overfitting, machine-learning, discretionary-trading, position-sizing, risk-management, automation, workflow-optimization]
strategies: [variance-risk-premium, short-earnings-straddle, earnings-vol-play, systematic-trading, discretionary-trading]
saga: none
part: null
confidence: high
---

# This AI Research Terminal Changed How I Trade Options | The O/TOC

## Summary

Eric walks through the O/TOC (Outlier Trading Operation Center), an AI-powered research terminal he built in May 2026 to automate market research, signal generation, and strategy development. The system uses local infrastructure (45TB of data across multiple storage tiers), integrates multiple data vendors (ORATS, Alpha Vantage, Polygon/Massive, Unusual Whales), and leverages Claude and GPT models to conduct hypothesis-driven research without requiring programming expertise. Since deployment, he has built three novel trading strategies and expanded into sports betting and prediction markets—all powered by the same infrastructure.

## Key takeaways

### Evergreen mechanics

- **AI-powered research democratization** [00:00–02:00]: The O/TOC eliminates the need to learn programming; AI handles code generation and infrastructure. Eric self-taught programming for years; now AI does it in minutes.

- **Data architecture: raw → parquet → database** [16:14–18:35]: Ingest raw data into parquet files (space-efficient, immutable source of truth), build clean tables from raw, materialize frequently-accessed views. Never mutate raw data; always preserve the source.

- **Liquid universe definition** [32:09–33:45]: Lou (Liquid Options Universe) = ~2,200 tickers; Food (Full Optionable) = ~6,000; Leu (Liquid Equity Universe) = ~5,000. Liquidity filters prevent analysis on phantom spreads and zero-volume instruments.

- **Multi-source data validation** [39:58–40:30]: Use 2–3 sources per data type (e.g., Polygon + Yahoo Finance + Alpha Vantage for price). If two agree and one diverges, the outlier is likely corrupt. Corroboration prevents silent data errors.

- **Cost structure: front-load, then scale down** [54:00–55:37]: Pay for top-tier data access (e.g., Massive Advanced at $200/month) for 1–2 months to build 20+ years of history, then downgrade to maintenance tier ($30/month). Variable cost, not fixed.

- **Daily update pipeline (Dink/Think)** [56:43–58:12]: Dink (daily ingest) runs pre-validation, downloads data to parquet, updates database—completes in <2 hours so research can happen during market close. Think (broader update) runs overnight for economic data, transcripts, etc. that don't change daily.

- **Workshop → Research → Production pipeline** [59:18–01:00:35]: Ideas start in workshop (exploration), move to research (defined criteria), then testing. Pass/fail routes to production (live capital) or recycled archive. Strategies tracked with tags for efficient retrieval via Moon (knowledge base).

- **Signal-to-profit-mechanism mapping** [01:08:32–01:09:43]: Brainstorm signals relative to a market effect, measure each signal individually against the profit mechanism, then test ensemble combinations. Use bootstrapping and hold-out periods to avoid overfitting. Practitioner standard: trade it if it's robust enough, even if you don't fully understand why.

- **Discretion tracking** [01:15:40–01:16:55]: Log every override of an automated strategy. Measure whether your discretionary intervention adds or costs money. Remove discretion from areas where you historically lose; keep it where you add alpha.

- **Minimal viable cost** [01:18:24–01:22:14]: ~$130–150/month for a retail trader: ChatGPT Plus ($20), Massive ($30), ORATS ($100), Alpha Vantage ($50), Unusual Whales optional ($13–56). Eric pays $400+/month for AI alone because he uses top tiers; don't benchmark against him.

### Dated market read (2026-07-15)

None; this is a system walkthrough, not a market update.

## Notable quotes

> "The entire purpose of project no code and the otoc is to literally empower you to make informed decisions." [08:39]

> "I have several profit mechanisms and strategies based around things that I don't know why it works... from a practitioner standpoint, I don't really fucking care as long as I can trade it." [01:10:55]

> "The thing you have to be really careful with machine learning, though, is that it's eager to overfit." [01:15:40]

## Candidate wiki links

**concepts:** [[ai-assisted-trading]], [[algorithmic-trading]], [[data-analysis]], [[data-hygiene]], [[research-methodology]], [[hypothesis-testing]], [[statistical-analysis]], [[backtesting]], [[signal-selection]], [[overfitting]], [[machine-learning]], [[discretionary-trading]], [[automation]], [[variance-risk-premium]], [[volatility-trading]]

**strategies:** [[variance-risk-premium]], [[short-earnings-straddle]], [[earnings-vol-play]], [[systematic-trading]], [[discretionary-trading]]

**people:** [[eric]]

## Regime / context

**Date:** 2026-07-15. This is a system-design and capability walkthrough, not a market analysis. The O/TOC was launched in May 2026 and has been in active use for ~2 months at the time of recording. All cost figures, storage sizes, and vendor tiers reflect mid-2026 pricing and availability.
