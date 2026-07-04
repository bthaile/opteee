---
type: source
title: "Implied Volatility Rank (IVR) vs Implied Volatility Percentile (IVP)"
video_id: Uu3DwGTOYHY
url: https://www.youtube.com/watch?v=Uu3DwGTOYHY
date: 2022-06-11
series: none
format: [education]
experts: [eric]
mentions: []
securities: [aapl, hut]
concepts: [implied-volatility, implied-volatility-percentile, implied-volatility-rank, volatility-mean-reversion, mean-reversion, sentiment, strategy-selection, premium, volatility-clustering, expected-move]
strategies: [short-premium, long-premium]
saga: null
part: null
confidence: high
---

# Implied Volatility Rank (IVR) vs Implied Volatility Percentile (IVP)

## Summary

This video explains the critical distinction between implied volatility percentile (IVP) and implied volatility rank (IVR)—two metrics traders often use interchangeably but which are calculated differently and have different practical applications. Eric demonstrates why IVP is superior for strategy selection and sentiment analysis, and shows how to use implied volatility to inform directional bias and exploit mean reversion.

## Key takeaways

- **Implied volatility is forward-looking** [01:09]: IV is the market's projection of future price variance, distinct from historical volatility which measures what already happened.
- **Raw IV numbers lack context** [02:35]: A stock like HUT with 490% IV and Apple with 46% IV cannot be compared directly without a reference frame—you cannot tell if premiums are "juiced" without context.
- **IVP formula: count trading days below current IV, divide by 252** [04:25]: This gives a percentile scale over a rolling year, making it comparable across all securities.
- **IVR formula: (current IV − 52-week low) / (52-week high − 52-week low)** [04:50]: This method is susceptible to extreme outlier skew; the 52-week high can distort the metric for months after a volatility spike (e.g., COVID crash).
- **IVP is more robust than IVR** [05:22]: IVP avoids the skew problem because it uses all 252 days rather than just the extreme high/low anchors.
- **Use IVP for strategy selection** [07:43]: When IVP is high (e.g., 98 on Apple), drift toward short-premium strategies because IV is likely to mean-revert downward; when IVP is low, favor long-premium strategies to capture IV expansion.
- **High IV = high premiums + wider expected price range** [10:28]: Traders should interpret elevated IV as both expensive options and larger anticipated moves.
- **Volatility term structure reveals earnings** [11:17]: A spike in IV for a specific expiration month (e.g., 60% front month dropping to 41%, then rising to 48%) signals an upcoming earnings event, even if not yet announced.

## Notable quotes

> "Implied volatility percentile hands down" — on which metric is superior for trading decisions [04:25]

> "Implied volatility is one of the more mean reverting aspects of the market" — justifying why extremes in IVP inform strategy selection [09:07]

## Candidate wiki links

**concepts:** [[implied-volatility]], [[implied-volatility-percentile]], [[implied-volatility-rank]], [[mean-reversion]], [[volatility-mean-reversion]], [[sentiment]], [[expected-move]], [[premium]]

**strategies:** [[short-premium]], [[long-premium]]

**securities:** [[aapl]], [[hut]]

## Regime / context

Recorded 11 June 2022 (stated as "11th of May" in transcript, likely ASR error; metadata confirms June 11). Market context: post-correction environment with relatively stable conditions. The COVID-crash reference (March 2020) illustrates how extreme IV spikes can distort IVR for extended periods—a key reason IVP is preferred for consistent signal generation across market regimes.
