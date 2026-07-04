---
type: source
title: "GameStop eBay Position & SpaceX IPO"
video_id: 05aJUfUKE5Q
url: https://www.youtube.com/watch?v=05aJUfUKE5Q
date: 2026-05-23
series: none
format: [education, analysis, market-note]
experts: [eric]
mentions: [elon-musk]
securities: [gme, ebay, spacex]
concepts: [synthetic-long, delta-neutral, leverage, derivatives, hostile-takeover, valuation, business-segments, profitability, risk-management, covered-strangle, implied-volatility, call-skew, position-sizing]
strategies: [covered-strangle, synthetic-long, short-premium]
saga: null
part: null
confidence: medium
---

# GameStop eBay Position & SpaceX IPO

## Summary

Eric reviews two major market developments: SpaceX's upcoming IPO (priced ~$1.75T valuation, trading June 11–12) with mixed profitability across three business segments (connectivity profitable, space and AI unprofitable), and GameStop's escalating derivative-based hostile takeover bid against eBay using synthetic long structures (~29M shares notional exposure via put–call pairs, ~$7B net premium deployed). The SpaceX valuation is difficult to justify on fundamentals; GameStop's eBay position is strategically interesting but capital-intensive.

## Key takeaways

### SpaceX IPO analysis [08:47–50:25]
- **Valuation context**: $1.75T implied valuation at $80B raise; would rank among most valuable public companies at debut [37:14]
- **Three business segments with divergent health** [32:24–34:17]:
  - *Connectivity (Starlink)*: $11.3B revenue, 49% YoY growth, 63% segment adjusted EBITDA — profitable and scaling
  - *Space*: $4.01B revenue (2025), $657M operating loss; capital-intensive R&D (~$3B annually for Starship)
  - *AI (XAI)*: $18M revenue, $2.4B loss; early-stage, unproven commercial viability
- **Mission vs. profit tension** [29:29–35:02]: Company's stated goal ("make life multi-planetary") is not revenue-generating; unproven technologies and significant technical complexity acknowledged in S-1 filings
- **Trading stance** [50:01–50:25]: Volatility play via options if available; not a bulk-long candidate due to valuation opacity and misaligned business unit pipelines

### GameStop eBay hostile takeover via derivatives [51:01–01:02:30]
- **Position structure** [52:07–53:40]:
  - Direct ownership: 25,000 eBay shares
  - Derivative exposure: ~29.1M shares via put–call pairs (synthetic longs)
  - Strike range: $84–$115 per share
  - Total notional premium deployed: ~$7B (larger than initially expected)
  - Combined exposure: ~6.5% of eBay's outstanding stock (up from 5%)
- **Strategic intent** [51:41–52:07]: Cohen anticipated eBay board rejection; derivatives provide leveraged exposure without requiring outright share purchases (GameStop lacks capital for direct acquisition)
- **Regulatory gate**: Hart–Scott–Rodino antitrust clearance required before derivatives convert to physical shares; GameStop currently lacks voting authority over underlying stock [53:40]
- **Market reaction** [01:03:20]: GameStop down ~2.3% on the day (22.46 → 21.96); heavy call skew persists (21-delta put ~47% vol vs. synthetic ~58–59% vol)

### Project No Code database initiative [01:00:28–01:17:27]
- Building institutional-grade options database using AI (zero human code written to date)
- Purpose: enable quantitative backtesting, anomaly detection, and strategy codification without expensive legacy data vendors
- Key constraint: data quality > cost; optimization should target clean, realistic data, not cheap data
- Architecture: raw data → parquet files → database schema → code-driven strategy testing
- Formal introduction video coming Wednesday of following week

## Notable quotes

> "The mission is going to be a little hard to financially get behind simply because if the intent is to go explore space, that's not really revenue-generating." [34:17]

> "GameStop wouldn't have enough money in order to get the exposure that they need outright by buying shares, but they're using derivatives to get the leverage. That's super interesting." [52:07]

## Candidate wiki links

**concepts:** [[synthetic-long]], [[leverage]], [[derivatives]], [[hostile-takeover]], [[valuation]], [[profitability]], [[covered-strangle]], [[implied-volatility]], [[call-skew]], [[position-sizing]], [[delta-neutral]], [[risk-management]]

**strategies:** [[covered-strangle]], [[synthetic-long]], [[short-premium]]

**securities:** [[gme]], [[ebay]], [[spacex]]

**people:** [[eric]]

## Regime / context

**Date**: 2026-05-23 (pre-SpaceX IPO pricing on June 11, trading June 12). GameStop's eBay position is an active, evolving hostile takeover bid; the $7B derivative deployment signals serious capital commitment. SpaceX valuation and business-unit profitability remain contentious ahead of public markets entry. Eric's Project No Code database initiative is concurrent work-in-progress, not yet formally launched.
