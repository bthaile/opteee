---
type: source
title: "Option Greeks Simplified: Vega Explained"
video_id: ld6vn5GtAeI
url: "https://www.youtube.com/watch?v=ld6vn5GtAeI"
date: "2025-11-19"
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [rgti]
concepts: [vega, implied-volatility, moneyness, extrinsic-value, intrinsic-value, volatility-term-structure, delta, theta, iv-crush, volatility-surface]
strategies: [long-call]
saga: null
part: null
confidence: high
---

# Option Greeks Simplified: Vega Explained

## Summary

Vega measures the rate of change of option premium per one-point move in implied volatility. This video demonstrates that vega is highest in at-the-money options and increases with time to expiration, but that raw volatility moves differ dramatically across the term structure—a critical mismatch that can cause profitable directional trades to lose money if volatility contracts. Understanding how volatility behaves across expirations and moneyness is essential to avoid trading the wrong term.

## Key takeaways

- **Vega definition and structure** [00:00–01:29]: Vega is the rate of change of premium per one-point change in implied volatility. Longer-dated options have higher absolute vega; vega peaks at-the-money because that's where extrinsic value is greatest and volatility can impact it.

- **Vega peaks at-the-money across all expirations** [01:29–02:43]: In any expiration, vega is highest around 50 delta (at-the-money). Far out-of-the-money options have little extrinsic value, so vega is lower. This relationship holds across 5-day, 30-day, 86-day, and 450-day expirations.

- **Term-structure mismatch trap** [02:43–04:03]: Traders often decide to buy or sell based on 30-day implied volatility but execute in 7-day options. These two terms do not move in lockstep. In the RGTI example, 30-day vol was 96% while 7-day vol was much higher—a critical disconnect that invalidates the trade thesis.

- **IV crush case study: RGTI Aug 12–13** [04:03–05:14]: An at-the-money 7-day call bought when 7-day IV was 152% lost 52% of its value one day later when IV collapsed to 91.6%, even though the underlying price and delta did not change. A $1 directional move in the call's favor was insufficient to offset the vega loss.

- **Volatility surface does not move uniformly** [05:14–07:47]: Near-term volatility moves much more dramatically than longer-dated volatility in response to catalysts. Buying far-dated options expecting large vega gains is a mistake because the back of the curve does not move as much. Match your vega exposure to the term you are actually trading.

- **Two-factor reconciliation** [07:47–08:56]: Longer-dated options have higher vega but raw volatility moves less; near-term options have lower vega but volatility moves more. You must account for both factors simultaneously to avoid losing money on directional wins.

## Notable quotes

"You can have something that moves in your favor directionally. But if you were not paying attention to the vega component to it, then you can lose money." [05:14–06:32]

## Candidate wiki links

**Concepts:**
[[vega]], [[implied-volatility]], [[moneyness]], [[extrinsic-value]], [[intrinsic-value]], [[volatility-term-structure]], [[delta]], [[theta]], [[iv-crush]], [[volatility-surface]]

**Strategies:**
[[long-call]]

**Securities:**
[[rgti]]

## Regime / context

Recorded 25 October 2025 (RGTI data example) with a case study dated 12–13 August. The video is part of the "Option Greeks Simplified" educational series and assumes familiarity with basic option mechanics (delta, theta, intrinsic vs. extrinsic value). The term-structure mismatch and volatility-surface behavior are evergreen mechanics applicable across all market regimes.
