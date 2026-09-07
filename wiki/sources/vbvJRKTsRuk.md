---
type: source
title: "I Tested the Cost of Hedging With Puts Over 19 Years So You Don't Have To"
video_id: vbvJRKTsRuk
url: https://www.youtube.com/watch?v=vbvJRKTsRuk
date: 2026-08-09
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spy]
concepts: [hedging, protective-puts, put-skew, implied-volatility-skew, drawdown-protection, cost-of-carry, deductible, delta, risk-management, portfolio-construction, scaling-in, scaling-out, diversification, put-premium, volatility-risk-premium, position-sizing]
strategies: [protective-puts, scaling-in, scaling-out, diversified-strategies, long-puts]
saga: null
part: null
confidence: high
---

# I Tested the Cost of Hedging With Puts Over 19 Years So You Don't Have To

## Summary

A comprehensive 19.5-year backtest of long-put hedging on SPY reveals that perpetual downside protection via puts is prohibitively expensive, costing 2.9–5.1% annually net of payouts depending on strike selection and duration. The analysis demonstrates that while puts occasionally provide significant protection during crises, the persistent drag from put skew, rolling costs, and the shifting deductible problem makes buy-and-hold hedging economically unviable for most portfolios. The presenter proposes three alternatives: scenario-based hedging, dynamic scaling in/out, and diversified strategy construction.

## Key takeaways

- **Perpetual put hedging cost**: 10% out-of-the-money puts cost ~5.1% annually in premium; net cost after payouts is ~2.9% per year [03:07–04:32]
- **Put skew premium**: Downside strikes trade 3.5–5.8 IV points above at-the-money, reflecting constant institutional demand for protection [08:05–09:05]
- **The deductible problem**: As the underlying rallies, the strike's deductible (max loss before protection kicks in) drifts upward, requiring costly re-hedging to maintain the same protection level [06:15–07:43]
- **Low payout frequency**: Over 78 quarterly rolls, only 8 actually paid at expiration; 28-quarter losing streaks occurred even during 2008–2009 [04:32]
- **At-the-money hedging is prohibitive**: ATM puts cost nearly double the annual S&P return (~8.9%), leaving almost nothing after friction [10:22]
- **Longer-dated options strike better balance**: 91-day puts offer improved Sharpe ratio and drawdown mitigation relative to shorter-dated alternatives [05:07]
- **Timing paradox**: Puts show highest returns precisely when you most want to sell them for protection, forcing a difficult choice between profit-taking and maintaining hedge [07:43]
- **Drawdown reduction is modest**: Even 10% OTM puts reduce max drawdown only from 56% to 50% (10% relative improvement) [10:22]
- **Alternative 1 – Scenario hedging**: Buy puts only around anticipated stress periods rather than perpetually [11:41]
- **Alternative 2 – Dynamic scaling**: Reduce position size and lock in profits during weakness instead of carrying puts [12:49]
- **Alternative 3 – Diversified strategies**: Combine long-delta and short-delta strategies to achieve natural balance without expensive put overlay [12:49]

## Notable quotes

> "Protection in the stock market is not free and conversely it's actually very expensive."

> "The reason why it helps you so much here is because at this point, you've not actually accumulated any profits cuz the test literally just started in 2007."

> "You're paid to take risk."

## Candidate wiki links

**concepts:**
[[hedging]], [[protective-puts]], [[put-skew]], [[implied-volatility-skew]], [[drawdown-protection]], [[cost-of-carry]], [[delta]], [[risk-management]], [[portfolio-construction]], [[scaling-in]], [[scaling-out]], [[diversification]], [[put-premium]], [[volatility-risk-premium]], [[position-sizing]], [[deductible]], [[put-call-ratio]], [[volatility-term-structure]]

**strategies:**
[[protective-puts]], [[scaling-in]], [[scaling-out]], [[diversified-strategies]], [[long-puts]], [[portfolio-first]]

**securities:**
[[spy]]

## Regime / context

This backtest spans 2007–2026, encompassing the global financial crisis (2008–2009), the COVID-19 crash (Q1 2020), the 2022 bear market, and the 2025 tariff-driven volatility. The analysis assumes mid-price execution for 734 rolls; bid-ask spread impact is shown separately. All results are gross of commissions and taxes. The findings are specific to index-level hedging (SPY); single-stock hedging dynamics may differ due to lower put skew and different liquidity profiles.
