---
type: source
title: "Beta Weighting 101: Simplifying Portfolio Risk Management"
video_id: oSazFJGhkKM
url: https://www.youtube.com/watch?v=oSazFJGhkKM
date: 2023-12-20
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, amc, vix, noc, xlu, spx]
concepts: [delta, beta-weighting, portfolio-first, notional-value, risk-management, directional-risk, position-sizing, leverage, delta-hedging, market-regimes]
strategies: []
saga: null
part: null
confidence: high
---

# Beta Weighting 101: Simplifying Portfolio Risk Management

## Summary

Beta weighting is a portfolio normalization tool that converts raw option and stock deltas into a common language—typically expressed as equivalent shares of SPY or another broad market index. This metric reveals true directional exposure, notional risk size, and position correlation, enabling traders to understand how their entire portfolio behaves relative to market moves and to identify oversized or misaligned positions.

## Key takeaways

- **What beta weighting solves** [00:50–01:28]: Raw deltas alone don't answer critical questions: if SPY moves 10 points, what happens to your portfolio? What is the true notional risk across all positions? Beta weighting answers both.

- **Raw delta vs. beta-weighted delta** [01:28–02:23]: Raw delta is whatever the options chain shows; beta-weighted delta converts that into equivalent shares of your reference index (typically SPY). Example: short calls in XLU show −60 raw deltas but only −20 beta-weighted deltas to SPY, meaning they behave like short 20 shares of SPY.

- **VIX inverse correlation example** [02:04–02:23]: Long deep ITM calls in VIX appear as +180 raw deltas but −200 beta-weighted deltas to SPY, revealing the inverse relationship and true portfolio hedging effect.

- **How to access beta weighting** [02:38–02:55]: In thinker swim, go to Monitor → Activity and Positions → Position Statement, tick the "beta weighting" box, and specify your reference index (SPY, SPX, VIX, or any other).

- **Notional value calculation** [04:56–05:17]: Multiply beta-weighted deltas by current price of your reference index. Example: 300 beta-weighted deltas × $430 SPY = $129,000 notional portfolio exposure.

- **P&L attribution from market moves** [07:24–08:37]: To estimate P&L from a SPY move, multiply beta-weighted deltas by the price change. Example: −20 beta-weighted deltas × $10 SPY move = −$200 P&L (in a vacuum, ignoring volatility changes).

- **Identifying position imbalances** [06:11–06:49]: Compare notional values across positions. A Northrop Grumman position at $193,500 vs. other $10,000–$20,000 trades immediately signals outsized risk, even if raw deltas appear similar.

- **Leverage detection** [09:23–09:42]: If beta-weighted notional exposure ($129,000) exceeds your account size ($50,000), you are levered and carrying more risk than capital—a critical red flag.

- **Correlation and hedging clarity** [10:01–10:23]: Beta-weighted deltas reveal which positions offset each other. Short XLU calls and a short SPX straddle may appear unrelated by raw delta but show near-perfect cancellation when beta-weighted.

- **Best practice: portfolio-level view** [05:17–05:37]: Always check both individual position beta-weighted deltas and portfolio totals. This one-stop metric reveals directional bias, notional size, and whether capital is efficiently deployed.

## Notable quotes

> "Beta weighting is a tool for helping us normalize positions into a common language so that we can see how everything fits together as a broad puzzle piece."

## Candidate wiki links

**concepts:** [[delta]], [[beta-weighting]], [[notional-value]], [[directional-risk]], [[position-sizing]], [[leverage]], [[portfolio-first]], [[risk-management]], [[delta-hedging]]

**securities:** [[spy]], [[amc]], [[vix]], [[xlu]], [[spx]]

## Regime / context

Recorded December 2023. The examples use static snapshots of a multi-leg portfolio; beta-weighted deltas update continuously as market prices and implied volatility change. This is a foundational education video applicable across all market regimes.
