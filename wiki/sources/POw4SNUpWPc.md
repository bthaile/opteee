---
type: source
title: "3 of my FAVORITE Options Analysis Tools"
video_id: POw4SNUpWPc
url: https://www.youtube.com/watch?v=POw4SNUpWPc
date: 2024-12-29
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [lunar, aapl, gme, spy, spx]
concepts: [probability-cone, delta, implied-volatility, implied-volatility-percentile, implied-volatility-rank, volatility-skew, volatility-surface, realized-volatility, volatility-risk-premium, moneyness, open-interest, volume-analysis, market-maker, leverage, information-and-price]
strategies: []
saga: null
part: null
confidence: high
---

# 3 of my FAVORITE Options Analysis Tools

## Summary

This video presents three core tools for analyzing options markets to make better-informed trading decisions: probability analysis (using probability cones and delta approximations), volatility analysis (including IV percentile, IV rank, volatility skew, and term structure), and volume/open-interest positioning. The host emphasizes that options markets attract sophisticated capital and that understanding these tools—even for non-options traders—reveals valuable information about market expectations and dealer positioning.

## Key takeaways

### Probability Analysis
- **Probability cones quantify directional moves** [02:31]: Plot days-to-expiration on the x-axis and price on the y-axis, showing the probability of touching a given strike within a standard-deviation range. Example: [[lunar]] has ~24.71% probability of hitting $15 within 14 days.
- **Delta is an approximation, not exact** [03:33]–[05:37]: A 48-delta option does not have exactly 48% probability of finishing in-the-money; the actual probability depends heavily on volatility and time-to-expiration. For [[lunar]] at 9 DTE, a 48-delta call had only 41.34% actual probability; for [[aapl]] at 191 DTE, a 46-delta had 39% probability. The variance widens with time and volatility.
- **Use probability cones to structure trades** [02:31]: Compare expected returns at different price levels against the probability of reaching them to make informed position decisions.

### Volatility Analysis
- **Volatility smile and surface reveal market expectations** [06:52]–[07:59]: Plot implied volatility across strikes and expirations. Normally, out-of-the-money puts are more expensive than OTM calls (put skew). When this inverts—calls more expensive than puts—the market is pricing in upside risk. [[gme]] currently shows this inversion, indicating expected upside.
- **Implied volatility percentile is superior to IV rank** [09:02]–[10:23]: IV percentile compares current IV to the past year's distribution; IV rank uses extremes and is prone to skew. [[gme]] shows 61% IV percentile (volatility elevated) but only 20% IV rank (distorted by past squeeze events).
- **Implied volatility vs. realized volatility captures variance risk premium** [10:23]–[11:37]: When IV is consistently higher than realized volatility, the market is pricing bigger moves than actually occur. Sellers can monetize this; buyers pay a premium.
- **Expiration volatility and strike-level skew reveal event expectations** [11:37]–[13:44]: Elevated IV at specific expirations or strikes (e.g., 116% IV at one expiration vs. lower nearby) often signals expected events or concentrated positioning. Compare delta-matched puts and calls: [[gme]] 30-delta puts at 88.7% IV vs. 30-delta calls at 135% IV confirms inverse skew and upside bias.

### Volume and Open Interest
- **Liquidity clusters at round strikes** [13:44]–[14:58]: Strikes ending in 0 or 5 (e.g., $20, $25) have disproportionately high open interest due to human preference for round numbers. Use this to identify liquid contracts.
- **Concentration of OI reveals market expectations** [14:58]–[16:16]: If most OI is in near-term expirations, the market expects near-term price movement. If concentrated in longer-dated expirations, it suggests longer-term positioning.
- **Call/put OI ratio indicates directional bias** [14:58]–[16:16]: More calls than puts suggests upside expectation. [[gme]] shows this pattern. [[spy]] shows 2:1 puts-to-calls (normal hedging); a 4:1 or 5:1 ratio would signal panic hedging.
- **Context matters for put concentration** [16:16]: [[spy]] has 12M puts vs. 6.2M calls not because of crash expectations, but because portfolio managers hedge broad equity exposure using index puts.

## Notable quotes

> "Options are really informed markets—we can glean a lot of information even if you're not an options trader."

> "If you have an educated opinion and you're trying to monetize it, most people who are strongly convicted in that educated opinion are going to look for leverage."

> "Delta is used as an approximation for probability of in-the-money, but it's not perfect—volatility really exacerbates this phenomenon."

## Candidate wiki links

**Concepts:**
[[probability-cone]], [[delta]], [[moneyness]], [[implied-volatility]], [[implied-volatility-percentile]], [[implied-volatility-rank]], [[volatility-skew]], [[volatility-surface]], [[volatility-term-structure]], [[realized-volatility]], [[volatility-risk-premium]], [[open-interest]], [[volume-analysis]], [[leverage]], [[information-and-price]]

**Securities:**
[[lunar]], [[aapl]], [[gme]], [[spy]], [[spx]]

## Regime / context

Recorded 2024-12-29. All numeric examples (strike prices, probabilities, IV levels, open-interest counts) are approximate and reflect market conditions on or near that date. The video is educational and tool-focused; no specific trade recommendations are made. The host indicates this is "the tip of the iceberg" and suggests a follow-up video exploring deeper volatility mechanics.
