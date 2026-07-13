---
type: source
title: "Why Your Call Options Lose Even When You're Right About Direction"
video_id: 4zx4HK1i4RQ
url: https://www.youtube.com/watch?v=4zx4HK1i4RQ
date: 2026-07-12
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, coin, tsla, pltr]
concepts: [delta, gamma, theta, vega, long-call, directional-trading, strike-selection, time-to-expiration, implied-volatility, convexity, delta-decay, gamma-pnl, theta-decay, vega-exposure, moneyness, probability-of-profit, leverage, price-target-bias, greek-attribution, greek-profile]
strategies: [long-call, stock-replacement, directional-trading]
saga: null
part: null
confidence: high
---

# Why Your Call Options Lose Even When You're Right About Direction

## Summary

Long call options can lose money even when the underlying moves in your predicted direction because strike selection, time-to-expiration (DTE), and implied volatility interact to determine P&L. The most common mistake is choosing strikes based on price targets rather than the Greeks (delta, gamma, theta, vega) that match your thesis. Four structurally different long calls on the same directional move can produce wildly different outcomes—from 1000%+ gains to total loss—depending on how speed, volatility, leverage, and time align with your position.

## Key takeaways

- **Strike selection by price target is backwards** [04:58–05:25]. Don't buy a 450 call because you think the stock will hit 450. Instead, select strikes based on the Greeks exposure you need: delta for direction, gamma for convexity, theta for time decay tolerance.

- **Four structural variants of the same bullish thesis** [02:06–02:59]:
  - *Fast* (7 DTE, 25 delta): Maximum convexity, cheap, high gamma; requires speed and precision.
  - *Short-term* (21 DTE, 35 delta): Moderate runway and convexity; good for near-term directional moves.
  - *Balanced* (50 DTE, ~45 delta): Mix of time, delta, and convexity; survives slower moves better.
  - *Stock replacement* (90+ DTE, 70+ delta): Minimal convexity, expensive; behaves like stock, lower percent return.

- **Coinbase +74% in one week** [03:33–04:01]: Fast and short-term variants captured outsized returns due to high gamma and speed matching the move. Stock replacement underperformed due to lower convexity, despite being correct directionally.

- **SPY +8.9% over one month** [05:51–07:08]: Fast option lost all premium (theta decay killed it). Balanced performed better than short-term because it had more time. Stock replacement had lowest positive return due to lower convexity. Directional thesis was correct; structure was wrong.

- **SPY −9% downside scenario** [07:08–08:28]: All short-dated calls lost 100%. Stock replacement lost 73% because higher delta slows the loss (delta decays as underlying moves against you). Vega helped slightly as volatility rose; delta was the primary pain point.

- **Palantir −30% in one week** [09:16–09:42]: Fast and short-term lost everything. Balanced nearly lost everything. Stock replacement lost less in percentage terms but more in absolute dollars. Delta was the primary driver of loss; vega and gamma provided minor offsets.

- **Greeks drive P&L, not price targets** [10:37–11:31]: If you expect strong upside, prioritize delta and gamma exposure. If you expect slow upside, you need enough delta to capture the move and enough time to survive theta decay. Downside scenarios are dominated by delta loss; vega and gamma provide only partial hedges.

- **The package matters more than the prediction** [11:59–12:28]: The call is a vehicle; the exposure (delta, gamma, theta, vega profile) is the tactical investment. Match your Greeks to your thesis, not your price target to a strike.

## Notable quotes

> "You can still be completely directionally correct in your idea and still lose your entire investment." [06:18]

> "The further direction you go to the right, the more expensive they are, and the less convexity you have." [05:25]

> "It is not based on what price you think the stock is going to hit, in what time frame, and picking your DTE and strike off of that." [11:59]

## Candidate wiki links

**concepts:** [[delta]], [[gamma]], [[theta]], [[vega]], [[long-call]], [[directional-trading]], [[strike-selection]], [[time-to-expiration]], [[implied-volatility]], [[convexity]], [[delta-decay]], [[gamma-pnl]], [[theta-decay]], [[vega-exposure]], [[moneyness]], [[probability-of-profit]], [[leverage]], [[greek-attribution]], [[greek-profile]]

**strategies:** [[long-call]], [[stock-replacement]], [[directional-trading]]

**securities:** [[spy]], [[coin]], [[tsla]], [[pltr]]

## Regime / context

Dated 2026-07-12. Examples drawn from 2024–2025 market moves (Coinbase +74% in one week, SPY ±8.9% over one month, Palantir −30% in one week). The core mechanics—delta, gamma, theta, vega interaction—are regime-independent and apply across all volatility environments. This is foundational education for long-call structure selection and is evergreen.
