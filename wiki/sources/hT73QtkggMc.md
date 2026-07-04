---
type: source
title: "complex order fills"
video_id: hT73QtkggMc
url: https://www.youtube.com/watch?v=hT73QtkggMc
date: 2025-06-26
series: none
format: [education]
experts: [eric]
mentions: []
securities: []
concepts: [bid-ask-spread, liquidity, counterparty, market-maker, moneyness]
strategies: []
saga: null
part: null
confidence: high
---

# complex order fills

## Summary

When closing multi-leg options strategies, submitting a single complex order for all legs simultaneously requires finding a counterparty willing to transact the entire package at a given price, which is far more difficult than exiting legs sequentially. Exiting one leg at a time allows you to find separate counterparties for each leg, dramatically improving fill probability and execution speed.

## Key takeaways

- **Complex orders require niche counterparties** [00:27] — A single order for all legs of a strategy requires a counterparty looking for that exact combination; the more legs, the harder it is to find a match.
- **Sequential exits improve liquidity access** [00:56] — Closing one leg at a time lets you find different counterparties for each leg, rather than waiting for one party to want everything.
- **Market makers balance their own books** [01:19] — The counterparty is typically a market maker whose book has varying demand for each leg; they may want more of some legs and less of others.
- **Bid-ask spreads compound across legs** [01:46] — Each leg carries its own bid-ask spread; a complex order forces you to play the mid price across all of them simultaneously, which can skew the effective price if any leg is illiquid.
- **Illiquid legs distort complex order pricing** [02:08] — If one leg is bid at a nickel and offered at 20 cents, submitting a complex order at mid price can be significantly off from the true value of the entire spread.

## Candidate wiki links

**concepts:** [[bid-ask-spread]], [[liquidity]], [[counterparty]], [[market-maker]], [[moneyness]]

## Regime / context

Educational explainer on order execution mechanics; applies across all market regimes and volatility environments.
