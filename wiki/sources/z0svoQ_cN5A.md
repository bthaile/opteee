---
type: source
title: "Not Even Subscribing to Cboe Data Makes GEX Viable for Predictions"
video_id: z0svoQ_cN5A
url: https://www.youtube.com/watch?v=z0svoQ_cN5A
date: 2026-10-01
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: []
concepts: [market-microstructure, options-flow, dealer-positioning, data-quality, market-internals, information-asymmetry, gamma-exposure]
strategies: []
saga: null
part: null
confidence: medium
---

# Not Even Subscribing to Cboe Data Makes GEX Viable for Predictions

## Summary

The video examines the limitations of using gamma exposure (GEX) as a predictive tool for options markets, focusing on data quality constraints. Even with direct access to Cboe Trade Bulletin Tape (TBT) transaction-level data, the fundamental problem remains: Cboe and ICE combined represent only ~37% of total options volume, leaving the majority of dealer positioning opaque and rendering aggregate GEX estimates too noisy for reliable prediction.

## Key takeaways

- **TBT data structure** [00:00]: Cboe's Trade Bulletin Tape captures individual trade events with full detail—timestamps, OSI identifiers, trade price/size, buy/sell indicators, participant capacity, and trade type—unlike summary-level products (open/close) that aggregate by participant.
- **Exchange concentration problem** [00:00]: Cboe and ICE combined control only ~37% of options volume; the remaining ~63% occurs on other venues, creating a fundamental data gap.
- **Dealer book opacity** [00:00]: No single data source provides insight into the entire dealer book across all venues, making aggregate GEX estimates inherently noisy and unreliable for prediction.
- **Data subscription cost vs. signal quality** [00:00]: Even paying for premium TBT access does not solve the core problem—missing the majority of market flow undermines the viability of GEX as a predictive signal.

## Candidate wiki links

**concepts:** [[market-microstructure]], [[options-flow]], [[dealer-positioning]], [[data-quality]], [[market-internals]], [[information-asymmetry]], [[gamma-exposure]], [[gamma-risk]]

**securities:** [[cboe]], [[ice]]

## Regime / context

Date: 2026-10-01. This analysis reflects the fragmented U.S. options market structure, where multiple venues (Cboe, ICE, NASDAQ OMX, EDGX, MEMX, etc.) compete for order flow. The speaker emphasizes that structural market fragmentation—not data subscription cost—is the binding constraint on GEX predictability.
