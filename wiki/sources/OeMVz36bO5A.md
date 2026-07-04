---
type: source
title: "Gamma Scalping Introduction"
video_id: OeMVz36bO5A
url: https://www.youtube.com/watch?v=OeMVz36bO5A
date: 2022-12-23
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy]
concepts: [gamma, delta, delta-hedging, theta, theta-decay, long-straddle, implied-volatility, gamma-scalping, days-to-expiration, at-the-money, moneyness, volatility-clustering, position-sizing, risk-management, transaction-costs, payment-for-order-flow]
strategies: [gamma-scalping, long-straddle, delta-neutral]
saga: null
part: null
confidence: high
---

# Gamma Scalping Introduction

## Summary

Gamma scalping is an active delta-adjustment strategy typically deployed around a long-premium base position (commonly a long straddle) to offset theta decay through tactical buying and selling of the underlying. The core mechanic: long gamma positions benefit from price movement regardless of direction, so traders harvest realized volatility by rehedging deltas at predetermined thresholds, converting gamma exposure into realized P&L that partially offsets daily theta bleed.

## Key takeaways

- **Definition & base structure** [00:19–01:06]: Gamma scalping is delta adjustment around a base trade. Long-premium traders (especially long straddles) use it to fight theta; short-premium traders rarely employ it because they want time to pass and minimal movement.

- **Delta vs. gamma mechanics** [03:25–04:40]: Delta steepens as expiration approaches (options converge to 0 or 1). Gamma is the rate of change of delta; it peaks at-the-money and increases dramatically near expiration. Gamma is highest at short DTE and low volatility; it decreases as IV rises.

- **Long gamma = long movement** [06:38–07:15]: If you're long premium (calls, puts, straddles), you're long gamma and need price to move to profit. Short gamma (short premium) traders avoid gamma scalping because they benefit from stasis, not movement.

- **Practical entry: delta-neutral hedge** [08:28–10:40]: Buy a long straddle (e.g., 419 call + put, 20 DTE, 10 contracts). Immediately sell shares of the underlying equal to the straddle's delta (~67 shares at market price) to neutralize directional exposure. This leaves you long gamma, short theta.

- **Daily rehedging workflow** [13:03–16:37]: At end of day (or at delta thresholds), check position delta. If it drifts outside your tolerance range, buy/sell shares to re-neutralize. Realize the P&L from the hedge trades; the straddle remains on. Repeat daily. Theta loss typically exceeds realized scalp gains on quiet days.

- **Costs & frequency** [12:16–12:40]: Payment-for-order-flow and bid-ask slippage are real costs even without commissions. Scalp frequency (daily vs. intraday) depends on position size, theta bleed rate, and expected move magnitude.

- **Variations & risk** [17:42–18:01]: Same concept works with long calls or long puts, but introduces directional risk. Straddles are preferred because both legs hedge each other. Gamma scalping is a small part of Eric's overall strategy, deployed mainly when expecting large moves.

## Notable quotes

> "The main enemy of any sort of long premium trade is time. We need whatever it is that we're buying to move so that we can make money."

> "Gamma scalping is a very active style strategy. We typically will try to create varying thresholds that we choose to gamma scalp on."

## Candidate wiki links

**Concepts:**
[[gamma]], [[delta]], [[delta-hedging]], [[theta]], [[theta-decay]], [[implied-volatility]], [[days-to-expiration]], [[at-the-money]], [[moneyness]], [[volatility-clustering]], [[position-sizing]], [[risk-management]], [[transaction-costs]], [[payment-for-order-flow]]

**Strategies:**
[[gamma-scalping]], [[long-straddle]], [[delta-neutral]]

**Securities:**
[[spy]]

## Regime / context

Recorded 23 December 2022. The example uses on-demand backtesting to June 2021 (20 DTE straddle on SPY ~419 strike). Eric notes gamma scalping opportunity has improved in recent years, likely reflecting elevated realized volatility post-2020. The mechanics are evergreen; the strategy is most viable when realized volatility exceeds implied volatility and when transaction costs are low.
