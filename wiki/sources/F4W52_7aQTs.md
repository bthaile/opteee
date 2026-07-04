---
type: source
title: "How I Read the Options Chain to Build Every Trade"
video_id: F4W52_7aQTs
url: https://www.youtube.com/watch?v=F4W52_7aQTs
date: 2026-05-17
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: []
concepts: [outlier-strategy-process, outlier-trade-process, profit-mechanism, thesis-generation, days-to-expiration, delta, gamma, theta, vega, charm, moneyness, in-the-money, out-of-the-money, greeks, price-action, support-and-resistance, stop-loss, profit-taking, position-sizing, risk-management, breakout, liquidity-cycle, catalyst, catalyst-timing]
strategies: [breakout, long-call]
saga: none
part: null
confidence: high
---

# How I Read the Options Chain to Build Every Trade

## Summary

Eric walks through his discretionary trade-building process using the options chain as a planning tool. Starting with a breakout thesis in AA, he demonstrates how to model price moves and time decay by using surrogate strikes across different expirations, allowing rapid scenario analysis of delta, gamma, theta, and vega without building a full Greeks model.

## Key takeaways

- **Outlier Trade Process vs. Strategy Process** [00:59]: The Trade Process is the specific execution framework applied before placing any trade; it differs from the broader Strategy Process many traders follow.

- **Thesis generation and duration** [01:20–02:04]: Define where price might go and how it gets there. Duration is critical because options have specific DTE (days to expiration); model prior moves to estimate expected move size and timeframe (e.g., 1–2 weeks, 10–12% move).

- **Basic checks before position design** [03:04–03:31]: Confirm liquidity, identify catalysts (and plan to exit before them), then decide position structure.

- **Equity baseline** [03:54–04:48]: Start with a simple stock position to establish risk/reward: risk ~$6,000 with a stop below the gap low (~66.5) and profit target near resistance (~75.5). This gives you a reference frame.

- **Options chain as surrogate model** [05:55–07:38]: Instead of building a full Greeks model, flip between expirations and adjust strikes to simulate price moves. If price moves +$5, look at the strike $5 higher (e.g., 70 calls → 75 calls) to see how delta, gamma, theta, vega change. If price moves −$5, look at the strike $5 lower (e.g., 70 calls → 65 calls).

- **Simulating time decay** [07:57–09:25]: Jump to a later expiration (e.g., 22 May) and look at the same strike (70s) to see how Greeks evolve. Expect delta to rise (charm), gamma to rise (ATM options have higher gamma closer to expiration), theta to increase, and premium to decay.

- **Charm effect** [08:44]: In-the-money options approach delta = 1 as expiration nears; out-of-the-money options approach delta = 0.

- **Rapid scenario planning** [09:25–09:50]: This surrogate-strike method is faster than manual Greeks modeling and gives you a reference-based planning factor instead of random guessing.

## Notable quotes

> "As soon as you trade options, you're adding complexity. But there's a benefit to that complexity—you can make things fit to your idea." [01:20]

> "Options have a specific DTE, days to expiration. They have a term that they expire, which is highly relevant to how I end up wanting to build a trade." [02:04]

## Candidate wiki links

**concepts:** [[outlier-trade-process]], [[outlier-strategy-process]], [[profit-mechanism]], [[days-to-expiration]], [[delta]], [[gamma]], [[theta]], [[vega]], [[charm]], [[moneyness]], [[in-the-money]], [[out-of-the-money]], [[greeks]], [[price-action]], [[support-and-resistance]], [[stop-loss]], [[profit-taking]], [[position-sizing]], [[risk-management]], [[breakout]], [[liquidity-cycle]], [[catalyst]]

**strategies:** [[breakout]], [[long-call]]

## Regime / context

Dated 2026-05-17. Trade example uses AA (Alcoa) breakout with 18 June expiration and earnings catalyst on 16 May. Surrogate-strike method is evergreen for rapid options scenario analysis.
