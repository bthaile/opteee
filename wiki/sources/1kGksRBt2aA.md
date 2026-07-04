---
type: source
title: "Charm (Delta Decay) Explained in 12 Minutes – The Greek Most Traders Ignore"
video_id: 1kGksRBt2aA
url: https://www.youtube.com/watch?v=1kGksRBt2aA
date: 2025-12-02
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy]
concepts: [charm, delta, delta-decay, gamma, moneyness, days-to-expiration, implied-volatility, probability-of-touch, at-the-money, out-of-the-money, in-the-money, greeks, higher-order-greeks]
strategies: [ratio-call-diagonal]
saga: null
part: null
confidence: high
---

# Charm (Delta Decay) Explained in 12 Minutes – The Greek Most Traders Ignore

## Summary

Charm, also called delta decay, is a second-order Greek that measures how delta changes with the passage of time rather than underlying price movement. As expiration approaches, out-of-the-money options lose delta rapidly and non-linearly—the decay accelerates sharply in the final weeks. Understanding charm is critical for position management because even with favorable price moves, reduced delta near expiration can significantly diminish profit potential.

## Key takeaways

- **Charm is delta decay over time** [01:16]: Charm measures the rate of change of delta per unit of time passing, analogous to how gamma measures delta's rate of change per point of underlying movement.

- **Delta changes non-linearly as expiration approaches** [02:28]–[03:47]: For a 700-strike call on SPY (spot ~682), delta declines from 0.56 at 441 DTE to 0.42 at 91 DTE (350 days, 0.14 delta loss), then 0.26 at 28 DTE (63 days, 0.16 delta loss), then 0.04 at 7 DTE (21 days, 0.22 delta loss). The decay accelerates sharply in the final weeks.

- **Charm reduces profit on favorable moves** [05:12]–[06:18]: A 42-delta call bought 91 DTE for $14.98 decays to 26 delta after 60 days. If SPY moves 50 points, the original position would capture ~$21 in premium gain; the decayed position captures only ~$13—a 38% reduction despite the accommodating move.

- **At-the-money options resist charm** [09:35]: ATM options (0.50 delta) show minimal delta decay near expiration because they retain high probability of finishing ITM. Off-the-money strikes decay sharply; in-the-money strikes gain delta as expiration nears.

- **Charm accelerates in the final 3 weeks** [07:59]–[09:35]: From 28 to 7 DTE (21 days), a 700-strike call loses 0.22 delta; from 7 to 3 DTE (4 days), it loses another 0.04 delta. The slope of decay becomes nearly vertical in the final week.

- **Position-sizing implication for ratio diagonals** [10:51]: When holding ratio call diagonals for duration, prefer at-the-money or slightly in-the-money strikes to minimize delta loss and preserve profit potential if the underlying moves favorably.

## Notable quotes

> "As time is passing, if nothing else changes, your Delta is declining pretty significantly. Now, your premium is also declining pretty significantly." [05:12]

> "As you get closer in time, this accelerates very meaningfully." [07:59]

## Candidate wiki links

**Concepts:**
[[charm]], [[delta]], [[delta-decay]], [[gamma]], [[greeks]], [[higher-order-greeks]], [[days-to-expiration]], [[moneyness]], [[at-the-money]], [[out-of-the-money]], [[in-the-money]], [[implied-volatility]], [[probability-of-touch]]

**Strategies:**
[[ratio-call-diagonal]]

**Securities:**
[[spy]]

**People:**
[[eric]]

## Regime / context

Recorded 2025-12-02. Examples use SPY spot ~682. Charm is a foundational mechanic for all option traders but is frequently overlooked in favor of delta, gamma, and theta. The non-linear acceleration of charm in the final 3 weeks is particularly relevant for swing traders and position holders managing duration risk.
