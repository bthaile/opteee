---
type: source
title: "Common Options Trading Questions | Options Trading Basics"
video_id: _sYkIbkPItA
url: https://www.youtube.com/watch?v=_sYkIbkPItA
date: 2025-07-19
series: beginner-lab
format: [education, live]
experts: [eric]
mentions: []
securities: [tsla, ford, tlt, sofi, bull, unh, gme]
concepts: [delta, greeks, theta, vega, gamma, charm, implied-volatility, delta-hedging, probability-of-touch, moneyness, extrinsic-value, intrinsic-value, theta-decay, volatility-term-structure, higher-order-greeks, leaps, delta-neutral, expected-move, volatility-clustering]
strategies: [covered-call, ratio-call-diagonal, synthetic-long, short-put, long-call, short-straddle]
saga: none
part: null
confidence: high
---

# Common Options Trading Questions | Options Trading Basics

## Summary

Eric hosts a beginner-friendly Friday stream addressing viewer questions about options trading fundamentals, with a focus on the Greeks and their practical application. The session covers delta's relationship to probability of being in the money, the impact of time and volatility on option pricing, and how to structure longer-dated positions (LEAPs) with offsetting short premium to manage theta decay. Key insight: delta as a probability proxy degrades significantly with time and volatility, requiring traders to use actual probability calculations for longer expirations.

## Key takeaways

### Evergreen mechanics

- **Delta across time and volatility** [19:13–29:15]: Delta normalizes by time; the same strike at different expirations will have different deltas. The relationship between delta and probability of being in the money diverges as DTE increases and IV rises. At 7 DTE in low-IV names, delta ≈ probability; at 546 DTE, the variance can exceed 25 percentage points.

- **Why delta as probability breaks down** [23:45–41:36]: Delta is derived from the same cumulative distribution function (ND1) as probability of being in the money, but extrinsic value and time create divergence. Longer-dated options have flatter delta curves across strikes; near-term options have steeper curves (binary in/out decision). Tesla (61% IV) showed 3.5-point variance at 7 DTE; GE (29% IV) showed 1.3-point variance—volatility amplifies the gap.

- **Theta decay is not linear** [44:18–46:37]: Far out-of-the-money options near expiration can have low absolute theta despite high percentage decay, because there is insufficient extrinsic value remaining. Theta as a percentage of premium can be high while raw theta is negligible. Traders must distinguish between percentage theta decay and absolute dollar theta.

- **LEAPs holding cost and offset strategies** [57:38–01:08:30]: Long-dated calls lose money daily via theta. To subsidize this cost, sell shorter-dated calls (ratio call diagonal). Calculate daily theta carry: theta × DTE × size × multiplier. Then determine how many short contracts offset that cost. Example: 50-lot LEAP with 0.007 theta costs ~$50/month; selling 17 shorter-dated calls at 0.21 theta offsets the carry while capping upside by ~$3,300.

- **Directional thesis timing matters even for long-term holds** [50:50–53:23]: Buying a long-dated call on a declining asset incurs gamma drag on the way down (delta decreases, so recovery requires larger moves) plus theta decay. Even if the long-term thesis is correct, poor short-term timing can prevent profitability. Example: TLT call bought at 50 delta; if it drops to 20 delta before recovering, the asymmetry in gamma means the recovery move must be larger to break even.

- **Separating long-term and near-term trades on the same underlying** [16:55–18:37]: A trader can hold a 2-year LEAP call thesis while trading synthetic shorts on near-term price action, but these must be treated as separate positions with no overlap. Mixing them (e.g., selling calls against LEAPs to "take profit" without closing) muddies the thesis and adds complexity without realized P&L benefit.

- **IV rank and LEAP expense** [24:31–25:28]: Compare front-month IV to longer-dated IV. If both are elevated (e.g., UNH at 52% front, 43% LEAP, with 94% IV percentile), LEAPs are expensive. Prefer to enter long-dated directional trades when IV is lower or when price action shows support/momentum, not on declining price with high IV.

### Upcoming series overview

- **Greeks deep-dive series structure** [09:07–14:23]: Five to six episodes planned. Episode 1: overview and alignment. Episodes 2–4: individual Greeks (delta, gamma, vega, theta) in logical order; rho excluded. Advanced episode: higher-order Greeks (charm, vanna, volga) and interdependencies. Each episode covers: definition, math (to visualize inputs), use cases, and tips & tricks. Delta tips include using it as a probability proxy, understanding dealer positioning via charm, and recognizing gamma ramp behavior.

## Notable quotes

> "Options really are kind of the same thing because they really are elegant instruments. They do a lot and they're efficient at what they do." [17:15]

> "The game is always putting it all together into something that actually leads to trade decisions." [15:35]

> "I started trading options to make money. That's it." [16:00]

## Candidate wiki links

### Concepts
[[delta]], [[greeks]], [[theta]], [[vega]], [[gamma]], [[charm]], [[implied-volatility]], [[probability-of-touch]], [[moneyness]], [[extrinsic-value]], [[intrinsic-value]], [[theta-decay]], [[volatility-term-structure]], [[higher-order-greeks]], [[delta-neutral]], [[expected-move]], [[volatility-clustering]]

### Strategies
[[covered-call]], [[ratio-call-diagonal]], [[synthetic-long]], [[short-put]], [[long-call]], [[short-straddle]], [[leaps]]

### Securities
[[tsla]], [[ford]], [[tlt]], [[sofi]], [[bull]], [[unh]], [[gme]]

### People
[[eric]]

## Regime / context

Recorded 2025-07-19 as a live Friday beginner stream. The session is part of Eric's ongoing educational series and precedes a planned deeper Greeks curriculum launching in August 2025. All numeric examples (IV percentiles, delta values, P&L figures) are approximate and reflect market conditions on or near the stream date. The discussion of UNH includes reference to fraud-related news catalyst, which may have resolved or evolved since recording.
