---
type: source
title: "Option Volatility Explained | What is IV Rank (IVR) and IV Percentile (IVP)?"
video_id: efWEgEzrBAI
url: https://www.youtube.com/watch?v=efWEgEzrBAI
date: 2024-03-13
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [msft, tsla, aapl]
concepts: [implied-volatility, implied-volatility-rank, implied-volatility-percentile, realized-volatility, volatility-clustering, standard-deviation-move, linear-regression-channels, extrinsic-value, intrinsic-value, volatility-skew]
strategies: []
saga: null
part: null
confidence: high
---

# Option Volatility Explained | What is IV Rank (IVR) and IV Percentile (IVP)?

## Summary

This video breaks down the core types of option volatility—implied, historic, realized, future realized, and forecast—and explains why understanding the distinction between [[implied-volatility-rank]] and [[implied-volatility-percentile]] is critical for retail options traders. IV Rank uses 52-week extremes and is prone to skew; IV Percentile ranks current IV against historical trading days and provides a more accurate relative assessment, especially in volatile markets.

## Key takeaways

- **Volatility is dispersion.** It measures deviation from a mean; in trading, it quantifies how much a security's price moves relative to its average [00:40].
- **Implied volatility (IV)** is expected volatility inferred from option prices; it lives in the extrinsic (time) value of an option and can be isolated per strike and per expiration cycle [01:52].
- **Historic volatility** measures realized volatility over a specific past period (e.g., HV2, HV5, HV21 for different timeframes) [03:15].
- **Realized volatility** is the statistical volatility actually observed in the underlying; **future realized volatility** is the realized outcome of a volatility forecast [04:09].
- **Forecast volatility** is a trader's own assessment of future volatility, distinct from the market's implied volatility [04:38].
- **IV Rank formula:** (Current IV − 52-week low) / (52-week high − 52-week low). Uses extremes; prone to skew in volatile regimes [06:30].
- **IV Percentile formula:** Count of trading days below current IV / total trading days (typically 252). Ranks current IV against historical distribution; less skew-prone [06:56].
- **Critical difference:** During COVID, IV Rank was 3.26% while IV Percentile was 66% for the same product—a massive divergence. IV Percentile is the superior metric [08:50].
- **Thinkorswim labeling error:** The platform incorrectly labels IV Rank as "IV Percentile"; verify calculations independently [07:19].
- **Practical use:** IV Percentile gives a clearer picture of whether current IV is high or low relative to a security's own history, especially in extreme markets [05:08].

## Notable quotes

> "IV Rank is much more skew prone than IV Percentile. You are going to get a better assessment of IV's performance against itself in an individual product via percentile versus IV Rank."

## Candidate wiki links

**Concepts:**
- [[implied-volatility]]
- [[implied-volatility-rank]]
- [[implied-volatility-percentile]]
- [[realized-volatility]]
- [[volatility-skew]]
- [[extrinsic-value]]
- [[intrinsic-value]]
- [[standard-deviation-move]]
- [[linear-regression-channels]]

**Securities:**
- [[msft]]
- [[tsla]]
- [[aapl]]

**People:**
- [[eric]]

## Regime / context

Recorded March 2024 in a relatively low-volatility market environment. The video references a historical COVID-era example (2020) to illustrate the extreme divergence between IV Rank and IV Percentile; that skew is less pronounced in normal regimes but remains structurally important. The Thinkorswim platform labeling issue persists as of the video date.
