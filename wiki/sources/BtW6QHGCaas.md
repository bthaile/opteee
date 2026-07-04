---
type: source
title: "Live Options Strategy Testing Pt2 | Options Trading for Beginners"
video_id: BtW6QHGCaas
url: https://www.youtube.com/watch?v=BtW6QHGCaas
date: 2026-05-17
series: beginner-lab
format: [education, live, strategy-breakdown]
experts: [eric]
mentions: []
securities: [dvn, vrtx, lumn, ea, smci, mstr, anet, upst]
concepts: [backtesting, sample-size, coefficient-variance, power-analysis, straddle-price, implied-volatility, iv-crush, expected-value, win-rate-vs-profitability, edge, small-sample-analysis, volatility-term-structure, momentum, trend-following, position-sizing, capital-efficiency]
strategies: [short-straddle, earnings-vol-play]
saga: null
part: null
confidence: medium
---

# Live Options Strategy Testing Pt2 | Options Trading for Beginners

## Summary

Part two of a manual earnings straddle-selling backtest across 21 positions over two trading days. The host walks through data entry, position sizing (normalized to spot price), and preliminary analysis showing a profitable edge: higher win rate with smaller average losses than wins, despite small sample size. The session emphasizes statistical rigor—coefficient of variance, power analysis, and sample-size caveats—before scaling to Python automation.

## Key takeaways

- **Manual data collection & sizing discipline** [01:59–23:00]: Normalize position size to the largest underlying's spot price (assign it 1 lot, scale others down). Track entry/exit premiums, implied volatility, and straddle price change to measure vol crush.
- **Straddle IV as a metric** [26:54–27:54]: Calculate entry and exit straddle IV by averaging put and call IV; track the percentage change to isolate vol decay independent of directional move.
- **Sample-size honesty & coefficient of variance** [15:27–21:33]: Small samples (21 trades over 2 days) can reveal trends but not statistical significance. Use coefficient of variance or power analysis to estimate how many samples you need before claiming edge.
- **Earnings catalyst robustness** [25:48–35:37]: Earnings catalysts are strong on their own—they inject new information. Uptrend vs. downtrend pre-earnings matters less than the catalyst itself; front-running directional moves through earnings is risky.
- **Momentum classification first** [37:19–40:34]: Before trading momentum, define which *type* of momentum (time-series vs. cross-sectional). Capital flow matters more than "conviction"; pension rebalancing can drive price movement with zero conviction.
- **Preliminary results** [58:11–01:16:28]: 21 positions, mostly profitable. Nearly all showed IV crush (straddle IV down). Win rate high, average loss < 50% of average win. This is a legitimate edge, but small sample—next step is Python-scale testing.
- **Edge is not rare** [54:42–56:09]: Finding edge is straightforward; the problem is it rarely looks as good as hoped. Expect modest returns, not home runs.

## Notable quotes

> "Finding edge actually isn't that difficult. The problem is the edge that you find generally doesn't look as good as you might want it to look."

> "You can still detect trends with a small sample. You just have to couch it in your mind in the context that it is—you can't definitively say just about anything."

## Candidate wiki links

**concepts:** [[backtesting]], [[sample-size]], [[coefficient-variance]], [[power-analysis]], [[straddle-price]], [[implied-volatility]], [[iv-crush]], [[expected-value]], [[win-rate-vs-profitability]], [[edge]], [[volatility-term-structure]], [[momentum]], [[position-sizing]], [[capital-efficiency]]

**strategies:** [[short-straddle]], [[earnings-vol-play]]

**securities:** [[dvn]], [[vrtx]], [[lumn]], [[smci]], [[mstr]], [[anet]], [[upst]]

## Regime / context

**Date:** 2026-05-17 (live stream, testing week of May 5 earnings cycle).

**Part 2 of manual earnings straddle project:** Part 1 (previous day) established the framework; this session completes data entry for 21 positions and runs preliminary analysis. Next phase (following Friday) will scale to Python automation. The host notes API rate-limit issues with Claude Code forced a pivot to manual testing, which is pedagogically useful anyway.

**Small-sample caveat:** 21 trades over 2 days is insufficient for statistical significance. Results show a promising trend (high win rate, favorable loss/win ratio, consistent IV crush) but require 100+ samples before claiming robust edge. Coefficient of variance and power analysis are the tools to estimate required sample size.
