---
type: source
title: "thinkorswim Guide for Options Trading - Tips & Tricks"
video_id: mdhbae8WXgI
url: https://www.youtube.com/watch?v=mdhbae8WXgI
date: 2023-06-27
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [nvda, spy, walmart, target, spx]
concepts: [delta, gamma, theta, vega, implied-volatility, implied-volatility-rank, implied-volatility-percentile, probability-of-touch, open-interest, volume-analysis, order-flow, market-maker, technical-analysis, linear-regression-channels, moving-averages, volume-profile, support-and-resistance, earnings-move, market-breadth, price-action, volatility-surface, volatility-term-structure, moneyness, expected-move, zero-dte]
strategies: [pairs-trade, short-put, box-spread]
saga: null
part: null
confidence: high
---

# thinkorswim Guide for Options Trading - Tips & Tricks

## Summary

Eric walks through the thinkorswim platform's core features for options traders, covering the Trade tab (options chains, Greeks, order flow), Analyze tab (risk profiles, probability cones), and charting setup. He emphasizes customization of columns, understanding the distinction between IV rank and IV percentile, and building a clean chart with linear regression channels, moving averages, and volatility overlays to support systematic trading decisions.

## Key takeaways

- **Trade Tab Setup** [00:49–01:26]: Use the Trade Grid to drop Level 2 data and order book; customize the options chain columns to display bid/ask/last, Greeks (delta, gamma, theta, vega, rho), open interest, volume, implied volatility, probability of in-the-money, and probability of touch. Display at least 50 strikes to avoid missing price levels on expensive products like SPX.

- **Delta vs. Probability of In-The-Money** [02:26–03:47]: Delta is a useful approximation for probability of in-the-money, but the relationship breaks down over time and volatility regimes. A 30-delta short put at 13 DTE shows ~30% probability of in-the-money, but at 104 DTE the same delta shows ~33% probability—a 10% relative difference. Probability of touch is roughly 2× delta but can vary; use both metrics to refine edge assessment.

- **IV Rank vs. IV Percentile Mislabeling** [05:06–05:24]: thinkorswim's "Current IV Percentile" label actually displays IV rank, not IV percentile. The difference matters most during large underlying moves. Use both IV high/low and HV (historical volatility) percentile as context tools.

- **Volume and Open Interest Breakdown** [06:06–06:24]: Monitor call vs. put volume, delta transaction bands, and open interest distribution to spot anomalies and understand typical flow patterns. The book call ratio is a useful tool for detecting unusual activity.

- **Time and Sales Filtering** [06:53–07:25]: Use the Time and Sales window to identify spreads, large orders, and exchange-specific flow. Filter by exchange, call/put, or time period to isolate relevant transactions.

- **Product Depth Tool** [07:44–08:44]: Split product depth by call/put volume to see where volume and open interest centralize. Observe zero-DTE concentration, put/call open interest ratios (e.g., 2:1 put skew), and implied volatility surface across expirations and strikes.

- **Active Trader Tab for Intraday** [09:24–09:41]: Pair a chart (with ichimoku cloud or MACD) with an order book to see resting orders and size during market open. Useful for intraday execution and order flow reading.

- **Pairs Trader Setup** [10:01–10:38]: Compare two securities (e.g., Walmart vs. Target) by displaying a ratio on one side and individual charts on the other. Build correlation matrices across multiple time frames (3, 5, 10, 30, 60, 90 days) to quickly assess relative strength and mean reversion opportunities.

- **Analyze Tab: Risk Profile and Probability Cone** [10:59–11:41]: View open position P&L day-by-day across multiple expirations. Use probability cones to visualize one standard deviation price bands by expiration date; adjust for in-the-money, out-of-the-money, or touch probabilities.

- **Economic Data and Fundamentals** [12:02–13:45]: Access house price indexes, commercial banking data, and fundamental metrics (earnings, revenue, margins, segment breakdown, forward projections). Track earnings dates, actual vs. consensus, and at-the-money straddle performance to synthesize information quickly.

- **Stock Hacker Scan Setup** [14:41–14:58]: Build custom columns combining fundamental indicators (P/E, ROE, etc.) and technical think scripts (above 50-day MA, 150-day MA slope, etc.) to screen stocks efficiently.

- **Chart Customization: Time Frames and Indicators** [16:26–17:13]: Use multiple time frame buttons for quick hypothesis switching. Include earnings and dividend markers for context. Layer volume, MACD histogram, and IV/HV subgraphs with intraday IV calculators to track volatility throughout the day.

- **Linear Regression Channels and Volume Profile** [18:01–18:56]: Overlay linear regression channels and volume profile (with reduced opacity and custom colors) to identify support/resistance and liquidity clusters without visual clutter. Avoid extra noise like value areas and high/low profiles.

- **Moving Average Stack** [19:18–19:42]: Use a 9-day SMA for short-term trend, 22-day EMA for intermediate, 50-day EMA for medium-term, and 150–200-day EMA for long-term structure. Keep the chart simple; add anchored VWAPs or Bollinger Bands only when needed.

- **Chart Labels and Context Metrics** [19:58–21:01]: Display IV percentile/rank, expected move (dollar and %), average daily range (ADR), average true range (ATR), weekly/monthly highs/lows, at-the-money put/call ratio, earnings-per-share trends, ROE, distance from 200-day MA, and correlation to SPY. These labels provide quick context without cluttering the price action.

## Notable quotes

> "I've had over 16 years on it [thinkorswim], I've gone to a bunch of different webinars on it, I even participate in some of the alphas for new features that they're releasing because I like it overall it's pretty robust." [00:00–00:18]

> "The problem with using Delta as an approximation is that relationship doesn't hold true over all periods of time and it actually breaks down the further out you go." [03:13–03:31]

> "I purposely keep it [the chart] that way because there's a lot of stuff out there and I find this stuff to work pretty well." [19:42–19:58]

## Candidate wiki links

**Concepts:**
[[delta]], [[gamma]], [[theta]], [[vega]], [[implied-volatility]], [[implied-volatility-rank]], [[implied-volatility-percentile]], [[probability-of-touch]], [[open-interest]], [[volume-analysis]], [[order-flow]], [[technical-analysis]], [[linear-regression-channels]], [[moving-averages]], [[volume-profile]], [[earnings-move]], [[market-breadth]], [[price-action]], [[volatility-surface]], [[volatility-term-structure]], [[moneyness]], [[expected-move]], [[zero-dte]], [[support-and-resistance]]

**Strategies:**
[[pairs-trade]], [[short-put]], [[box-spread]]

**Securities:**
[[nvda]], [[spy]], [[spx]]

**People:**
[[eric]]

## Regime / context

Recorded June 2023. The video is a platform walkthrough and does not depend on market regime; all mechanics and setup recommendations are evergreen. thinkorswim is a mature, feature-rich platform maintained by TD Ameritrade; the UI and available tools may evolve, but the core concepts (Greeks, order flow, charting) remain stable.
