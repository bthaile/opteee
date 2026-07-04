---
type: source
title: "LEAPS Option Trading Strategies"
video_id: a14UA4oN82E
url: https://www.youtube.com/watch?v=a14UA4oN82E
date: 2025-08-31
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, sofi, avgo]
concepts: [leaps, delta, gamma, theta, vega, moneyness, extrinsic-value, implied-volatility, implied-volatility-percentile, volatility-term-structure, stock-replacement, leverage, profit-mechanism, fundamental-growth, earnings-growth, multiple-expansion, technical-analysis, probability-cone, position-sizing, risk-management, outlier-strategy-process]
strategies: [ratio-call-diagonal, long-call]
saga: null
part: null
confidence: high
---

# LEAPS Option Trading Strategies

## Summary

LEAPS (long-term equity anticipation securities) are options with expiration greater than one year, designed as leveraged stock replacements. This video walks through the Greeks across long-dated expirations, how to select strikes and expiration cycles, and demonstrates a ratio call diagonal strategy that captures fundamental growth while managing theta decay through near-term short legs.

## Key takeaways

- **What LEAPS are** [00:00–01:18]: LEAPS are options expiring >1 year out; they provide leverage (e.g., control $62k of SPY exposure for $7k premium) and are commonly used by institutional traders like Nancy Pelosi's fund.

- **Delta behavior at long expirations** [02:43–05:09]: Delta moves slowly far out in time because gamma is much lower (~0.003 for 551-day ATM vs. ~0.012 for 33-day ATM). This means each dollar move in the underlying generates less delta acceleration, so strike selection matters more than picking where you think the stock will go.

- **Theta decay is cheaper but slower** [06:24–07:30]: Daily theta on 551-day ATM options is ~0.074 (cheap holding cost), but 33-day ATM theta is ~0.212 (3× higher). Long-dated options decay slowly in absolute terms but have lower relative daily cost.

- **Vega term mismatch trap** [08:54–10:10]: Implied volatility percentile reported by platforms uses 1-year IV, not the IV of your LEAPS expiration. Buying LEAPS when 30-day IV percentile is cheap can mean buying expensive 365-day IV. Always compare IV percentiles across the same term structure.

- **Liquidity and IV selection for expiration** [10:10–11:21]: Bid-ask spreads widen as you go further out. Use IV term structure tools to find cheaper expirations (e.g., 180-day IV at 18.8% vs. 18-day IV at 20.26%). Vega risk is high on long-dated options, so buying cheap IV is critical.

- **Profit mechanisms for LEAPS** [12:49–13:57]: Primary mechanisms are fundamental growth (earnings growth, multiple expansion), drift (long-term market uptrend), and volatility trading. Ratio call diagonals capture these by holding long-dated calls and layering short near-term calls.

- **Ratio call diagonal structure** [15:18–16:32]: Long leg >90 days out (often 180+ days); short legs closer in time. The ratio (e.g., 100 long : 10 short) is sized so short calls offset theta decay without capping upside. Do not sell too many shorts or you lose directional exposure.

- **Theta offset calculation** [17:48–19:11]: Calculate daily theta on long legs, find near-term short legs that can overcome it over their duration. Example: 100 long 22-calls (0.007 theta/day = $70/day loss) offset by 10 short calls collecting $28/day = net $42/day loss, recoverable over 39 days of short premium.

- **Position management and scaling** [19:11–21:55]: Use stops to scale out, not exit entirely. Set profit targets using probability cones (e.g., 1 standard deviation move over 180 days) or prior consolidation patterns. Max risk = bought-to-open premium; allow room for long-term thesis to play out.

- **Common mistakes** [23:07]: Selling too many short calls against long calls (creates unwanted directional risk in your favor); overemphasizing upfront credit collection (slows the move you want). Keep ratio light early in strong directional moves.

## Notable quotes

> "LEAPS is an acronym and it stands for long-term equity anticipation security. This is essentially designed to be a stock replacement. Just gives you a little bit of leverage."

> "The way to decide the strike is based on the Greek profile that you want. Understanding how the Greeks work."

> "Don't let that confuse you. And if what I just said is a little confusing, you can either ask a question in the comments or just rewind what we just talked about because it's really, really important."

## Candidate wiki links

**Concepts:**
[[leaps]], [[delta]], [[gamma]], [[theta]], [[vega]], [[moneyness]], [[extrinsic-value]], [[implied-volatility]], [[implied-volatility-percentile]], [[volatility-term-structure]], [[stock-replacement]], [[leverage]], [[profit-mechanism]], [[fundamental-growth]], [[earnings-growth]], [[multiple-expansion]], [[technical-analysis]], [[probability-cone]], [[position-sizing]], [[risk-management]], [[outlier-strategy-process]]

**Strategies:**
[[ratio-call-diagonal]], [[long-call]]

**Securities:**
[[spy]], [[sofi]], [[avgo]]

**People:**
[[eric]]

## Regime / context

Recorded 2025-08-31. Educational content on long-dated options mechanics and strategy construction. No specific market regime dependency; Greeks and ratio mechanics are evergreen. Ratio call diagonal example uses SOFI as a live trade snapshot (mid-July 2025 timeframe).
