---
type: source
title: "The Position Sizing Mistake That's Killing Your Returns (Volatility Sizing Explained)"
video_id: 6-xlQeiQWSg
url: https://www.youtube.com/watch?v=6-xlQeiQWSg
date: 2026-04-26
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, tsla]
concepts: [implied-volatility, implied-volatility-percentile, position-sizing, probability-cone, standard-deviation-move, volatility-clustering, expected-move, realized-volatility, risk-management, pnl-attribution]
strategies: [risk-first]
saga: null
part: null
confidence: high
---

# The Position Sizing Mistake That's Killing Your Returns (Volatility Sizing Explained)

## Summary

Equal dollar allocation across positions with different volatility profiles creates vastly different P&L outcomes and risk exposure. By sizing positions relative to their implied volatility—using probability cones, expected-move formulas, and volatility-cap methods—traders can ensure that portfolio risk is distributed logically and that management plans align with actual position behavior.

## Key takeaways

- **Equal dollars ≠ equal risk** [00:00–00:24]: Putting $10k into SPY and $10k into Tesla creates identical notional exposure but dramatically different P&L volatility because the assets move at different rates.

- **IV percentile reveals relative volatility context** [00:24–01:08]: SPY at 30% IV (95th percentile) is historically high; Tesla at 50% IV (27th percentile) is relatively calm despite the higher absolute number. 12-month range: SPY 44.8%, Tesla 132.8%.

- **Probability cones and expected-move formula** [01:38–02:47]: Use `spot price × IV × √(days/365)` to calculate one-standard-deviation moves over a given timeframe. Over 30 days: SPY expects ~$57.80 (8.6% move), Tesla ~$56.80 (14.3% move)—same dollars, different percentages.

- **P&L volatility scales with position size and asset volatility** [03:40–04:19]: A $10k position in Tesla generates ±$1,433 P&L swing vs. ±$860 in SPY—a 40% variance. This compounds when using stop-losses and management plans.

- **Volatility-cap method (institutional approach)** [06:45–08:31]: Set a target volatility (e.g., 40%) for each trade. Allocate capital as `(original capital × target V) / asset V`. SPY gets $13,333, Tesla gets $8,000 to equalize expected volatility impact.

- **Equal-risk-unit method (retail-friendly)** [08:49–10:28]: Allocate total capital inversely to volatility ratio. With $20k across SPY (30% V) and Tesla (50% V): SPY gets $12,500, Tesla gets $7,500. Both positions then exhibit ~$500 P&L swings for equivalent moves.

- **Risk-unit ratio shortcut** [10:48–11:13]: Divide the higher-volatility asset's IV by the base asset's IV (50% / 30% = 1.67). SPY position must be 1.67× the size of Tesla to achieve equivalent risk exposure.

## Notable quotes

> "If I input $10,000 even between these, I am going to experience more P&L volatility in Tesla than SPY." [03:40]

> "The point of doing this is to make sure that what you're sizing is logical across the curve because if you're putting equal dollar amounts, your actual risk is quite different." [10:28]

## Candidate wiki links

**concepts:** [[implied-volatility]], [[implied-volatility-percentile]], [[position-sizing]], [[probability-cone]], [[expected-move]], [[standard-deviation-move]], [[realized-volatility]], [[risk-management]], [[pnl-attribution]], [[volatility-clustering]]

**strategies:** [[risk-first]]

**securities:** [[spy]], [[tsla]]

## Regime / context

Recorded 2026-04-26. Volatility levels (SPY 30% IV at 95th percentile, Tesla 50% IV at 27th percentile) are illustrative; the methodology applies across all market regimes. The volatility-cap and equal-risk-unit methods are timeless position-sizing tools, with the former more common in institutional settings and the latter more accessible to retail traders.
