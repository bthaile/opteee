---
type: source
title: "Managing In the Money Short Calls in GameStop"
video_id: chpZ11DjfSU
url: https://www.youtube.com/watch?v=chpZ11DjfSU
date: 2024-12-09
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [gme]
concepts: [assignment, capped-upside, delta, extrinsic-value, intrinsic-value, early-exercise, implied-volatility, moneyness, opportunity-cost, position-sizing, profit-mechanism, risk-management, theta-decay, volatility-clustering]
strategies: [ratio-call-diagonal, covered-call, ratio-write]
saga: gme-saga
part: 2
confidence: high
---

# Managing In the Money Short Calls in GameStop

## Summary

This video demonstrates how to manage short calls that move in-the-money when running a [[ratio-call-diagonal|ratio covered call]] strategy on [[gme|GameStop]]. Eric walks through a live example from April–November 2024 where the stock doubled after entry, showing how to roll positions for basis adjustments, recognize early assignment risk, and maintain share ownership through disciplined adjustments rather than forced assignment.

## Key takeaways

- **Ratio structure preserves upside:** Holding more than 100 shares (e.g., 1,100 shares with 4 short calls) leaves uncovered shares to capture gains above the short strike [04:32–05:34].
- **Intrinsic vs. extrinsic value:** A short call's premium splits into intrinsic (how far ITM) and extrinsic (time + volatility). Early assignment risk rises when extrinsic value drops below ~$0.05 per contract [08:00–09:19].
- **Early assignment is irrational without dividends:** Exercising a call to capture intrinsic value throws away remaining extrinsic value; only dividend yield exceeding extrinsic value makes exercise rational [10:34–14:21].
- **Roll at-the-money for maximum flexibility:** When stock price equals strike price, extrinsic value is highest and you have the most roll options; rolling deep ITM calls forces you to buy back intrinsic value with limited choices [21:43–25:05].
- **Patience and basis adjustment:** In the example, the position went from +$96 profit (first roll) to −$5,964 loss (second roll), then recovered by increasing lot size from 4 to 6 contracts to improve basis by $1 despite 60% stock appreciation [28:35–36:28].
- **Always have an exit:** If rolling becomes untenable, you can let shares be called away at the short strike and still profit from uncovered shares bought at lower cost basis [33:18–37:42].
- **Break-even calculation:** Track the premium needed on the next roll to offset prior realized losses; divide realized loss by lot size and new premium to find the per-contract target [40:06–43:34].
- **Volatility expansion complicates rolls:** As stock rallies sharply, implied volatility rises, making all strikes more expensive and reducing basis improvement opportunities [26:16–27:18].

## Notable quotes

> "If you're in the camp like this scenario that we're talking about and we use the scenario of gaining entry on 16 April when the stock was around 10 a half and this person bought a thousand shares… you always have that exit window of just let it get assigned just let it be done." [34:25]

## Candidate wiki links

**Concepts:**
[[assignment]], [[capped-upside]], [[delta]], [[early-exercise]], [[extrinsic-value]], [[implied-volatility]], [[intrinsic-value]], [[moneyness]], [[opportunity-cost]], [[position-sizing]], [[profit-mechanism]], [[risk-management]], [[theta-decay]], [[volatility-clustering]]

**Strategies:**
[[covered-call]], [[ratio-call-diagonal]], [[ratio-write]]

**Securities:**
[[gme]]

**People:**
[[eric]]

## Regime / context

**Date:** April–November 2024 (example trades); video published December 9, 2024.

**Market context:** GameStop experienced a sharp rally from ~$10.50 (April 16) to ~$29 (May 13) and beyond, creating a challenging environment for short call management. The example deliberately uses the worst entry point (stock at lows) to demonstrate adjustment discipline in adverse conditions.

**Saga note:** This is part 2 of a mini-series on trading options in GameStop. Part 1 (linked in description) introduces the [[ratio-call-diagonal|ratio covered call]] structure; this video focuses on real-time management and rolling mechanics when the stock moves sharply against the short calls.
