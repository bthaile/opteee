---
type: source
title: "Is Low VIX a Trap? I Ran 19 Years of Data"
video_id: MJX5QoAfLMw
url: https://www.youtube.com/watch?v=MJX5QoAfLMw
date: 2026-09-27
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [vix, spy]
concepts: [implied-volatility, volatility-risk-premium, premium-selling, short-premium, delta-hedging, position-sizing, kelly-criterion, volatility-clustering, volatility-term-structure, risk-management, drawdown-management, margin-requirement, iv-rank, iv-percentile, market-regimes, volatility-regime, tail-risk, variance-risk-premium, expected-value, directional-risk, hedging, rebalancing, bid-ask-spread, market-microstructure, volatility-persistence, shock-recovery, entry-conditions, sizing-decisions, risk-reward, efficiency-frontier]
strategies: [short-straddle, short-strangle, short-put, put-vertical-spread, iron-condor, long-put, delta-hedging, protective-puts, rolling-options, half-kelly]
saga: none
part: null
confidence: high
---

# Is Low VIX a Trap? I Ran 19 Years of Data

## Summary

This analysis examines whether selling premium during low-VIX environments is inherently risky by testing 9,227 trading days from 1990–2026 across five VIX bands. The data shows that low VIX does not eliminate premium, but sellers face asymmetric risk: frequent small gains punctuated by rare, outsized losses. Proper position sizing, delta hedging, and entry gates can improve risk-adjusted returns without sacrificing terminal wealth.

## Key takeaways

- **VIX distribution is non-linear**: The market spends significant time sub-16, but the relationship between calm and panic is arch-shaped (thin at extremes, peaked in the middle), not a ramp [03:49]
- **Low VIX still pays premium**: Sub-13 VIX environments yield ~2.6 volatility points forward, compared to 7.8+ at 28+ VIX; the issue is magnitude of worst-case loss, not absence of premium [06:49]
- **Calm periods carry hidden directional risk**: Years beginning with VIX under 16 show median seller returns near zero, while elevated-start years average +21%; 2020, 2022, and 2028 were severe drawdown years [05:05]
- **Volatility clusters and persists**: Shock half-life is ~34 days; even after major events (2008, 2020, 2023 bear market), elevated vol lingers, making tail risk real for unhedged sellers [08:17]
- **Spread cost hurts more when vol is cheap**: When bid-ask spread is a percentage of premium, the floor doesn't compress further in calm markets, making execution efficiency critical [10:52]
- **Short straddle at low VIX**: Collecting ~2.1% premium against worst-case loss of −2.4% (loss exceeds gain); at 28+ VIX, collect 7.8% against −4.7% worst case [13:38]
- **Entry gates improve ride smoothness**: Gating trades (e.g., via IV rank, 200-day trend, VRP z-score) doesn't materially change terminal wealth but reduces drawdown volatility and improves per-trade deployment [15:02]
- **Buying-side hedge cost**: Rolling 25-delta S&P puts show cheapest cost in calm periods (13–16 VIX handle) but best efficiency (cost vs. payoff) at that same level [16:20]
- **Short puts outperform short strangles**: Selling 16-delta puts wins most years with significant variance risk premium; short strangles collapse due to call-side losses; iron condors underperform due to double cost [17:48]
- **Half-Kelly sizing cuts drawdown in half while retaining 67% of growth**: Margin requirements drop in calm periods, tempting over-sizing; instead, size down when risk-reward is poor [19:05]

## Notable quotes

> "Premium doesn't erase when things get calm. What you'll find is the calm decile tends to have like 3.2 volatility points against like 4.05."

> "If you're selling premium, if you're selling a put, selling a call, selling a straddle strangle, generally speaking, if there's no hedging that you're doing at all during that, your trade actually has a lot of directional detail to it."

> "Just because you can put more on in that period because your broker is requiring less is not a great time to do it."

## Candidate wiki links

**concepts:**
[[implied-volatility]], [[volatility-risk-premium]], [[premium-selling]], [[delta-hedging]], [[position-sizing]], [[kelly-criterion]], [[volatility-clustering]], [[tail-risk]], [[variance-risk-premium]], [[expected-value]], [[directional-risk]], [[rebalancing]], [[bid-ask-spread]], [[volatility-persistence]], [[risk-reward]], [[efficiency-frontier]], [[iv-rank]], [[iv-percentile]], [[market-regimes]], [[volatility-regime]], [[entry-conditions]], [[sizing-decisions]], [[margin-requirement]], [[drawdown-management]]

**strategies:**
[[short-straddle]], [[short-strangle]], [[short-put]], [[put-vertical-spread]], [[iron-condor]], [[long-put]], [[delta-hedging]], [[protective-puts]], [[rolling-options]], [[half-kelly]]

**securities:**
[[vix]], [[spy]]

## Regime / context

This analysis spans 1990–2026 (36 years, 9,227 trading days) and focuses on index volatility (VIX) and S&P 500 options. The findings are specific to VIX and index options; the author explicitly cautions against extrapolating to single-stock options, which have different microstructure. The data includes major regime shifts: 2008 financial crisis, 2020 COVID shock, 2022 bear market, and 2023 recovery, all of which show volatility clustering and persistence. The analysis is agnostic to market direction but emphasizes that unhedged short-premium positions carry significant directional exposure, especially in calm environments where complacency masks tail risk.
