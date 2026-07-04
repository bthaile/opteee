---
type: source
title: "Build Winning 0DTE Option Strategies"
video_id: gonrT_M7wCo
url: https://www.youtube.com/watch?v=gonrT_M7wCo
date: 2025-08-24
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spx]
concepts: [zero-dte, number-of-occurrences, greeks, vega, profit-mechanism, volatility-risk-premium, implied-volatility, realized-volatility, market-structure, liquidity-cycle, opening-range-breakout, catalyst, delta, gamma, theta, theta-decay, overfitting, path-dependency, position-sizing, risk-management, assignment, expected-move, moneyness, delta-neutral]
strategies: [zero-dte, short-premium, short-straddle, short-strangle, iron-condor, long-call, ratio-write]
saga: null
part: null
confidence: high
---

# Build Winning 0DTE Option Strategies

## Summary

Zero DTE (day-to-expiration) options offer high-frequency trading opportunities but require systematic edge-building rather than haphazard directional bets. This video walks through a research-driven framework for constructing profitable zero DTE strategies: identifying profit mechanisms (volatility, catalysts, market structure), conducting statistical analysis, selecting appropriate structures, and managing position sizing and tail risk. The approach emphasizes that Greeks become parabolic in the final day, amplifying both opportunity and risk.

## Key takeaways

- **The zero DTE problem** [00:00–01:14]: Most traders size up recklessly, chase random directional ideas, bounce between strategies, and accumulate no demonstrable edge. The paradigm shift is treating zero DTE like any other expiration but in the most compressed timeframe.

- **Greeks amplify parabolically** [02:24–03:41]: Vega (and all Greeks) follow a parabolic curve as expiration approaches. The slope from 11 DTE to 1 DTE is steeper than 39 to 11 DTE; zero DTE is steeper still. All options must resolve in-the-money or out-of-the-money by end of day, creating extreme sensitivity to price and time.

- **Four profit mechanisms** [03:41–05:06]: Market structure & liquidity demand (opening/closing behavior), volatility trading, directional styles, and catalysts. The speaker focuses on volatility and catalyst lenses. These are starting points; deep research is required to build robustness.

- **Research framework: outlier strategy process** [05:06–07:40]: (1) Brainstorm monetization ideas; (2) search academic research (SSRN, prefer bank/institutional/academic sources over trading-group papers); (3) define the profit mechanism; (4) conduct holistic statistical analysis (e.g., opening range breakout behavior across timeframes); (5) fit structures (straddles, strangles, iron condors, verticals) to the mechanism; (6) backtest and avoid overfitting.

- **Variance risk premium as a zero DTE play** [07:40–08:46]: Implied volatility tends to trade over realized volatility. Capture this via short-premium structures (straddles, strangles, iron condors). Analyze how each structure behaves against your profit mechanism, then test.

- **Trade example 1: Iron condor on volatility signals** [10:02–12:18]: 20 June trade on [[spx]]. Opened 10 iron condors at ~25 delta short, 15 points wide, for $4.20 credit. Max profit $4,200 (38.9% ROIC), max loss $10,800. Expired worthless. Short-premium strategies can have high win rates but require tail control to avoid negative expected value.

- **Trade example 2: Ratio long calls on Trump tariff catalyst** [12:18–16:28]: 3 April [[spx]] trade. Bought 5 ATM 5500 calls, 10 slightly OTM 5400 calls, 25 far OTM 5300 calls (with short calls as hedge). Rationale: ATM has decent profit odds; further OTM has lower odds but higher gamma compounding. Managed dynamically: 5500s expired for $34k profit; 5400s closed early for $7.60 (bought $6.55); 5300s expired worthless due to theta decay. Net small profit. Demonstrates importance of understanding which structures fit the idea.

- **Position sizing discipline** [10:02–11:05]: All positions scaled to <1% account risk. Smaller accounts must scale appropriately; do not chase nominal dollar amounts.

- **Avoid assignment risk on zero DTE** [11:05–12:18]: Use [[spx]] (cash-settled) rather than equity options to preserve choice to hold into expiration. Markets can widen dramatically in final 1–2 minutes.

- **Dynamic management and path dependency** [14:59–16:28]: Monitor intraday moves; be willing to close early if thesis changes or theta decay erodes value faster than expected. Understand that far OTM purchases can become drag if the underlying doesn't move as anticipated.

## Notable quotes

> "Everything becomes parabolic in this ending time frame." [03:41]

> "If you do not go through a careful profit mechanism analysis portion to what you're doing this, then I wouldn't understand what options would make sense to buy." [16:28]

## Candidate wiki links

**Concepts:**
[[zero-dte]], [[number-of-occurrences]], [[greeks]], [[vega]], [[delta]], [[gamma]], [[theta]], [[theta-decay]], [[profit-mechanism]], [[volatility-risk-premium]], [[implied-volatility]], [[realized-volatility]], [[market-structure]], [[liquidity-cycle]], [[opening-range-breakout]], [[catalyst]], [[moneyness]], [[delta-neutral]], [[overfitting]], [[path-dependency]], [[position-sizing]], [[risk-management]], [[assignment]], [[expected-move]]

**Strategies:**
[[zero-dte]], [[short-premium]], [[short-straddle]], [[short-strangle]], [[iron-condor]], [[long-call]], [[ratio-write]]

**Securities:**
[[spx]]

**People:**
[[eric]]

## Regime / context

Recorded 24 August 2025. This is a foundational education video on zero DTE strategy construction, not a market-specific trade call. The two trade examples (20 June and 3 April) are historical illustrations of the framework in action; they are not recommendations. The framework applies across market regimes but requires regime-aware profit mechanism selection (e.g., volatility mean-reversion vs. catalyst-driven moves).
