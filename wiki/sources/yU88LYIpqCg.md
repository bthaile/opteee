---
type: source
title: "Right but Lost: How Options Can Lose Even if You're Right"
video_id: yU88LYIpqCg
url: https://www.youtube.com/watch?v=yU88LYIpqCg
date: 2025-04-20
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [nvda]
concepts: [delta, gamma, theta, vega, greeks, implied-volatility, extrinsic-value, intrinsic-value, moneyness, days-to-expiration, volatility-clustering, pnl-attribution, price-action]
strategies: [long-call]
saga: null
part: null
confidence: high
---

# Right but Lost: How Options Can Lose Even if You're Right

## Summary

A long call on [[nvda]] moves in the correct direction (stock up ~4%) yet the position loses money. The video dissects how [[delta]], [[gamma]], [[theta]], and [[vega]] interact over the trade's lifecycle to produce a loss despite directional correctness, emphasizing the importance of monitoring the [[greeks]] continuously rather than at entry alone.

## Key takeaways

- **Directional correctness ≠ profit**: A stock moving in your favor does not guarantee an options profit; other Greeks erode value [00:00–01:04]
- **Black-Scholes inputs matter**: Stock price, strike, [[days-to-expiration]], risk-free rate, [[implied-volatility]], and dividend yield all drive option value [01:04–02:23]
- **Delta is not linear**: A 5-point move with 40 delta should yield ~$2.40 profit, but [[gamma]] curvature and path-dependency reduce realized gains [07:00–08:24]
- **Theta decay accelerates near expiration**: [[theta]] was 14¢ at entry, dropped to 11¢ when the stock moved against you (less [[extrinsic-value]]), then spiked to 37¢ one day before expiration [08:24–10:52]
- **Early adverse moves compound losses**: When the stock initially moved down, it required a larger subsequent move to recover, consuming time value in the process [08:24]
- **Vega can help or hurt**: In this example, rising [[implied-volatility]] as the stock fell provided some offset, but not enough to overcome theta bleed [10:52]
- **Build trades with Greeks lifecycle in mind**: Picking an expiration that "aligns" with your expected move window is a common mistake; monitor Greeks continuously [09:37]

## Notable quotes

> "Nothing sucks more than being right and being wrong at the same time, losing money."

> "Theta decay, if you'll recall, accelerates as we get closer to expiration."

## Candidate wiki links

**concepts:** [[delta]], [[gamma]], [[theta]], [[vega]], [[greeks]], [[implied-volatility]], [[extrinsic-value]], [[intrinsic-value]], [[moneyness]], [[days-to-expiration]], [[pnl-attribution]]

**strategies:** [[long-call]]

**securities:** [[nvda]]

## Regime / context

Dated example: 13 December 2024 (Nvidia at $135, pullback after dividend). The mechanics illustrated—path-dependency, theta acceleration, and Greeks' nonlinearity—are evergreen and apply to any long option position. The video is educational and does not constitute a market update.
