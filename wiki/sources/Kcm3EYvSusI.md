---
type: source
title: "How to Build a Trade"
video_id: Kcm3EYvSusI
url: "https://www.youtube.com/watch?v=Kcm3EYvSusI"
date: null
series: beginner-lab
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, spx]
concepts: [open-interest, volume-analysis, profit-mechanism, outlier-strategy-process, delta, gamma, implied-volatility, trend-identification, support-and-resistance, price-action, expected-move, position-sizing, portfolio-first, trading-plan, repeatable, market-regimes, volatility-clustering, mean-reversion]
strategies: [zero-dte, long-put, directional-trading]
saga: null
part: null
confidence: high
---

# How to Build a Trade

## Summary

This session covers the foundational process for constructing options trades, emphasizing that successful trading begins with identifying a **profit mechanism** (the underlying market effect you're trading) before selecting specific option structures. The host walks through the **Outlier Strategy Process**, demonstrating how to research directional ideas, test option structures against historical scenarios, and align trade construction with portfolio needs—using a zero-DTE directional put example on SPX to illustrate the complete workflow.

## Key takeaways

### Foundational concepts
- **Open interest vs. volume** [00:00–13:58]: Open interest is the total number of existing contracts; volume is contracts traded in a period. OI updates overnight and is static during the day; volume moves all day and resets overnight.
- **Volume-to-OI ratio** [13:58–21:19]: A ratio > 1 signals elevated activity relative to existing positions, indicating shifting supply/demand. Use platforms like Unusual Whales, O Rats, or Bar Chart to track this metric.
- **Repeatable process is critical** [22:43–27:12]: Your capacity as a trader is determined by how well you execute a repeatable task. Without repeatability, you cannot distinguish luck from edge; the market will eventually expose inconsistency.

### Building a trade (the Outlier Strategy Process)
- **Step 1: Identify the profit mechanism** [31:29–34:43]: Define the underlying market effect you're trading (e.g., directional momentum, mean reversion, volatility expansion). Most traders skip this and jump straight to picking strikes—a critical error.
- **Step 2: Research and test structures** [43:10–01:09:09]: Use historical data to test how different option structures (delta, strike, DTE) perform under your profit mechanism. Example: comparing 2-delta, 50-delta, and 60-delta puts on a down day to see which compounds best given expected move size.
- **Step 3: Align with market regime** [01:06:44–01:09:09]: Volatility and average daily range vary by regime (up-trending vs. down-trending). In low-volatility up-trends, far-OTM options decay too fast; in high-volatility down-moves, they compound faster. Build accordingly.
- **Step 4: Portfolio fit first** [01:10:25–01:11:51]: Always review your portfolio before placing a trade. Determine what exposures you need, want to add, or should avoid.

### Research workflow using ChatGPT
- **Rapid hypothesis testing** [01:12:59–01:30:13]: Download historical data (e.g., 5 years of SPX daily), upload to ChatGPT, and ask for pattern analysis (e.g., "What is the probability of reversal after two consecutive down days?"). Example output: 55% reversal vs. 44% continuation after two down days; average third-day move is +0.078% (vs. −0.016% after two up days).
- **Refine with follow-on questions**: Ask about volatility correlation, average move size, and regime-specific behavior to build edge.

### Zero-DTE directional example
- **The setup** [36:09–51:23]: Trader wants to buy puts on SPX after a down day, zero DTE. Test multiple strikes: 2-delta (cheap, needs large move), 50-delta (mid-range), 60-delta deep-ITM (expensive, dollar-for-dollar move).
- **Position sizing by structure** [01:04:03–01:05:17]: If capping max loss at $62.50, a 1-lot of the expensive put equals a 4-lot of the mid-delta, or a 54-lot of the cheap put. Same notional risk, different gamma exposure.
- **Regime matters** [01:06:44–01:07:54]: On low-volatility up-trend days, far-OTM puts decay too fast; prefer higher-delta. On high-volatility down-move days, gamma compounds faster; can use cheaper, lower-delta puts.

## Notable quotes

> "Your capacity as a trader is how well you can execute a repeatable task."

> "All the work is done before you ever place a trade."

> "The process of actually trading is mind numbingly easy. It's so easy. There's effectively very little thought that has to go into things."

## Candidate wiki links

**concepts:**
[[open-interest]], [[volume-analysis]], [[profit-mechanism]], [[outlier-strategy-process]], [[delta]], [[gamma]], [[implied-volatility]], [[trend-identification]], [[support-and-resistance]], [[price-action]], [[expected-move]], [[position-sizing]], [[portfolio-first]], [[trading-plan]], [[repeatable]], [[market-regimes]], [[volatility-clustering]], [[mean-reversion]], [[large-language-model]], [[prompt-engineering]]

**strategies:**
[[zero-dte]], [[long-put]], [[directional-trading]]

**securities:**
[[spy]], [[spx]]

**people:**
[[eric]]

## Regime / context

This is an educational session from the Beginner Lab series, part of a multi-part curriculum on options trading fundamentals. The host references two prior videos: "Outlier Strategy Process" and "Outlier Trade Process," which provide deeper detail on the framework presented here. The session uses historical SPX data (primarily March 3, 2024 example) and live chat interaction to illustrate concepts; exact numeric figures (e.g., OI counts, move percentages) are approximate due to transcript quality and platform technical issues (thinkorswim disconnection mid-session). The ChatGPT analysis at the end demonstrates modern AI-assisted research workflow for rapid hypothesis testing on historical patterns.
