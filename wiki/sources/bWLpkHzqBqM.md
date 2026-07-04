---
type: source
title: "Why Most 0DTE Traders Get This Wrong"
video_id: bWLpkHzqBqM
url: https://www.youtube.com/watch?v=bWLpkHzqBqM
date: 2026-06-28
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spx]
concepts: [zero-dte, bid-ask-spread, implied-volatility, realized-volatility, volatility-risk-premium, delta, moneyness, liquidity-cycle, transaction-costs, volatility-skew, market-maker, fair-value]
strategies: [iron-condor, short-premium]
saga: null
part: null
confidence: high
---

# Why Most 0DTE Traders Get This Wrong

## Summary

An empirical analysis of ~970 SPX zero-DTE iron condors (2022–2026) reveals that resting orders at the mid price rather than crossing the bid-ask spread yields approximately 3% better fills on entry, though this advantage diminishes significantly if you must manage the position. The study confirms that variance risk premium capture is viable at 76% win rate, but transaction costs and liquidity constraints—especially on wider call wings—are the real friction points most traders overlook.

## Key takeaways

- **Mid-price execution advantage**: Resting at mid instead of crossing the spread saves ~$18.45 per iron condor (3% of total credit), with mid-price fills significantly outperforming crossing fills across the trade lifespan [04:54–05:27].
- **Four-leg friction**: Iron condors require crossing the bid-ask spread four times simultaneously; this is why multi-leg strategies are harder to fill well than single-leg trades [03:26–03:54].
- **Win rate vs. delta**: 76% of trades won despite 16-delta short strikes implying only 68% probability; this edge comes from realized volatility being lower than implied [07:23–07:55].
- **Call-wing liquidity crisis**: Put skew means downside wings trade more actively; call wings (especially wider ones) often have no bid, creating a pricing and execution problem [06:30–06:56].
- **Spread cost is flat over time**: Contrary to intuition, bid-ask spread costs have not tightened significantly; this is driven by market volatility regime, not just liquidity improvement [08:28–08:56].
- **Management is the killer**: If you must exit or adjust, you cross the spread again and land on the unfavorable side of the curve; minimize transactions as much as possible [09:27–09:52].
- **Fair-value pricing**: On average, you pay back ~86 cents per dollar of mid credit, indicating market makers price iron condors competitively and fairly [08:28].

## Notable quotes

> "The trick here is with an iron condor, there are four legs. So, you have to cross this gap four times. Even though you just see once if you submit it as one order on your platform, on the back end, it's happening four times."

## Candidate wiki links

**concepts:** [[zero-dte]], [[bid-ask-spread]], [[implied-volatility]], [[realized-volatility]], [[volatility-risk-premium]], [[delta]], [[moneyness]], [[liquidity-cycle]], [[transaction-costs]], [[volatility-skew]], [[market-maker]]

**strategies:** [[iron-condor]], [[short-premium]]

**securities:** [[spx]]

## Regime / context

Data spans 2022–2026, anchored to SPX daily options launch (2022). Analysis covers 10:00 a.m. to 4:00 p.m. trading hours using intraday OTAC data. Results are observational (actual fills), not simulated, and apply specifically to zero-DTE iron condors held to close. Spread costs and liquidity vary with prevailing market volatility regime.
