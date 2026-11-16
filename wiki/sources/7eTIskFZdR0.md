---
type: source
title: "5 Things the Option Volatility Surface Can Tell You"
video_id: 7eTIskFZdR0
url: https://www.youtube.com/watch?v=7eTIskFZdR0
date: 2026-11-15
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spx, msft]
concepts: [implied-volatility, implied-volatility-percentile, volatility-surface, volatility-term-structure, put-skew, call-skew, contango, backwardation, variance-risk-premium, realized-volatility, iv-crush, volatility-expansion, hedging-demand, earnings-volatility, positioning, tail-risk, two-standard-deviations]
strategies: [short-volatility, long-volatility, selling-premium, earnings-vol-play, call-debit-spread, volatility-trading]
saga: none
part: null
confidence: high
---

# 5 Things the Option Volatility Surface Can Tell You

## Summary

The volatility surface—the matrix of implied volatilities across all strike prices and expiration dates for an underlying—contains actionable market information beyond the uniform volatility assumption of Black-Scholes. This video presents five measurable, tradeable insights: detecting expensive vs. cheap options via implied volatility percentile, understanding how volatility expectations shift across term structure (contango vs. backwardation), pricing earnings moves relative to historical realized volatility, and reading positioning signals from put skew spikes. All five can be implemented immediately using freely available data.

## Key takeaways

- **Implied volatility percentile (IVP) vs. IV rank:** Use IVP exclusively; it is less prone to skew distortion. IVP measures the percentage of past-year days with lower IV, allowing direct comparison of current richness to historical range. [03:42]

- **High IV typically contracts within 30 days:** When IV percentile is elevated (e.g., >90th), realized vol over the next 21 trading days tends to be lower. This is a high-confidence, tradeable edge. [04:00–05:02]

- **Short premium does not automatically win after IV spikes:** Historical data (2015–2021: 62% vs. 66%; 2022–2026: 67% vs. 62%) shows that elevated IV does not shift win-rate probabilities dramatically. Risk-reward may improve, but frequency does not. [05:02–06:24]

- **Low IV expands within ~30 days:** When IV percentile is at the lower end of its range, IV expansion occurs 65–73% of the time (depending on period). Long vol trades must be sized carefully to survive quiet months. [06:24–07:49]

- **Contango vs. backwardation signals near-term fear:** Contango (normal upward-sloping term structure) reflects uncertainty over longer horizons. Backwardation (front month more expensive than back) signals near-term crisis pricing. Historically, when backwardation appears, big moves occur less often than priced in. [08:00–10:20]

- **Earnings pricing relative to realized history:** If implied vol is <0.8× the trailing 8-period realized vol, implied tends to beat realized (complacency signal; sell vol). If implied is >1.2× history, realized more often exceeds implied (underpricing signal; less tradeable). [10:20–13:04]

- **Put skew spikes predict index strength:** When put skew spikes, indices rise within 21 trading days 79% of the time (training) and 70% (holdout 2022–2026). A 50/25 delta call debit spread captures this with 19.7% return on risk. [13:04–14:31]

- **Volatility surface behavior is measurable, not qualitative:** All edges are quantified across training and out-of-sample validation periods. Indices show strongest patterns; large/mid/small-cap ETFs loosen due to idiosyncratic risk. [14:31–16:54]

- **Tail behavior differs by IV regime:** Two-standard-deviation moves are less common when IV is at extremes; probability of upside tail moves is lower when IV is already high, but higher when IV is low. [16:00–16:54]

## Notable quotes

> "Implied volatility is a common unit. So, it allows us to compare strikes and expirations directly."

> "When that curve is inverted, sometimes that vol gets really overpriced relative, and the things start to slow down at that point."

> "That is the entire difference about the way that I view markets compared to a lot of people. It's not qualitative. It's not based on a feel or hope or loose observation. Most of this stuff is based on things that I can definitively measure and point at."

## Candidate wiki links

**concepts:**
[[implied-volatility]], [[implied-volatility-percentile]], [[volatility-surface]], [[volatility-term-structure]], [[put-skew]], [[call-skew]], [[contango]], [[backwardation]], [[variance-risk-premium]], [[realized-volatility]], [[iv-crush]], [[volatility-expansion]], [[hedging-demand]], [[earnings-volatility]], [[positioning]], [[tail-risk]], [[two-standard-deviations]], [[black-scholes-merton]]

**strategies:**
[[short-volatility]], [[long-volatility]], [[selling-premium]], [[earnings-vol-play]], [[call-debit-spread]], [[volatility-trading]]

**securities:**
[[spx]], [[msft]]

## Regime / context

Recorded November 15, 2026. All backtests span two periods: training (2015–2021) and out-of-sample validation (2022–2026), with Microsoft earnings example dated October 20, 2026. Patterns are strongest in broad indices (SPX); tighten in large/mid/small-cap ETFs due to idiosyncratic noise. All metrics are freely calculable or available via O-Talk (open-source tool linked in video notes).
