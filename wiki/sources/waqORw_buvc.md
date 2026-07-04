---
type: source
title: "0 DTE SPX Best Entry Time"
video_id: waqORw_buvc
url: https://www.youtube.com/watch?v=waqORw_buvc
date: 2024-05-04
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spx]
concepts: [zero-dte, delta, theta-decay, gamma-hedging, delta-hedging, expected-return, win-rate-vs-profitability, volatility-clustering, overfitting, market-regimes, expected-move]
strategies: [short-strangle, short-straddle, iron-condor]
saga: null
part: null
confidence: high
---

# 0 DTE SPX Best Entry Time

## Summary

Analysis of 25,000+ zero-DTE SPX trades from 2022–2024 reveals that later-day entries (14:00–15:00 ET) significantly outperform early-morning entries, driven by theta decay acceleration and reduced directional exposure. Single-leg strangles consistently outperform iron condors and straddles across both bear and bull market regimes, with 10-delta shorts achieving ~87% win rates despite lower per-trade profits.

## Key takeaways

- **Later entries dominate:** 14:00–15:00 ET entries show superior risk-adjusted returns across all delta strikes; 09:35 ET entries underperform consistently [00:25–05:48]
- **Theta decay is non-linear:** Early-day premium decay is slower relative to zero-DTE timeframe; parabolic acceleration occurs only near expiration [08:23–09:05]
- **Market open volatility penalty:** First 30–60 minutes feature order flow from overnight clearing and pension fund liquidations, creating unfavorable fills and directional noise [08:05–08:23]
- **Delta selection trade-off:** 10-delta strangles yield 87% win rate but lower average profit per trade; 30-delta strangles yield 66% win rate but higher per-trade gains [07:16–07:39]
- **Regime consistency:** Bear market (2022, −20% SPX) and bull market (2023, +23% SPX) both favor late-day entries; optimal entry time shifts right in bull markets [09:29–10:18]
- **Iron condors underperform:** Best iron condor (short 30-delta, long 5-delta, 15:00 ET) returned ~18.6% vs. worst single-leg 10-delta short at ~20.5%; max loss difference negligible (~$1k) [04:13–05:00]
- **Avoid straddles:** Straddles consistently underperform strangles; trend observed over multiple years [11:04–11:24]
- **Overfitting risk:** In-sample optimization across 2022–2024 may not generalize; seek trends consistent across periods, deltas, and regimes rather than perfect historical fit [06:11–07:16]

## Notable quotes

> "The first half hour to hour of a market tends to be pretty busy" — referring to overnight order clearing and pension fund liquidations [08:05–08:23]

> "It gets as parabolic as you can into expiration but that's just happening on a shortened zero DTE time frame" — explaining theta decay acceleration near close [08:46]

## Candidate wiki links

**concepts:** [[zero-dte]], [[delta]], [[theta-decay]], [[gamma-hedging]], [[delta-hedging]], [[expected-return]], [[win-rate-vs-profitability]], [[volatility-clustering]], [[overfitting]], [[market-regimes]], [[expected-move]], [[time-frames]], [[order-flow]], [[volatility-term-structure]]

**strategies:** [[short-strangle]], [[short-straddle]], [[iron-condor]]

**securities:** [[spx]]

**people:** [[eric]]

## Regime / context

Data spans 2022–2024 (through March 25), capturing both bear-market (2022: −20% SPX) and bull-market (2023: +23% SPX) regimes. Zero-DTE expirations expanded in 2022 (midweek added) and fully launched daily expirations thereafter, making 2022 the purest cohort for zero-DTE-specific analysis. No profit/loss management applied; results reflect entry-time effects only. Forward-testing and management-layer analysis deferred to future work.
