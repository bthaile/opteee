---
type: source
title: "Problems with 0 DTE SPX Options"
video_id: fauTAoPtXZo
url: https://www.youtube.com/watch?v=fauTAoPtXZo
date: 2022-10-26
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spx]
concepts: [zero-dte, volatility-risk-premium, implied-volatility, realized-volatility, short-volatility, delta, risk-management, backtesting, expected-value, edge]
strategies: [short-strangle, short-straddle, iron-condor, short-premium]
saga: null
part: null
confidence: high
---

# Problems with 0 DTE SPX Options

## Summary

Eric breaks down three critical mistakes traders make when deploying zero-DTE SPX spreads: using spreads to hedge when the core thesis is to harvest volatility risk premium (which contradicts itself), entering indiscriminately without checking whether implied volatility is actually elevated relative to realized volatility, and combining spreads with stop-losses in ways that destroy strategy expectancy. The core insight is that zero-DTE premium selling only works when IV is genuinely overstated; mechanical execution without a volatility edge is hope, not strategy.

## Key takeaways

- **Spreads contradict the thesis [01:53–03:18]**: When trading zero-DTE to harvest volatility risk premium, using a spread (e.g., short 10-delta put + long further-OTM put) means you're simultaneously selling and buying the same "overpriced" volatility. This negates the entire edge. If you must hedge tail risk, use data to decide (e.g., hedge only the put side, since markets crash harder than they rally).

- **Non-discerning entry is the critical mistake [04:08–05:22]**: Implied volatility is not always elevated relative to realized volatility. Blindly trading zero-DTE every day ignores periods when IV < RV, where the strategy has no edge. Compare 30-day realized volatility to implied volatility before entering; only trade when IV is genuinely overstated.

- **Stops on spreads kneecap expectancy [05:44–07:01]**: Adding stop-losses to zero-DTE spreads changes the math significantly. Backtests miss slippage and don't account for periods when IV is/isn't elevated. Stops prevent the trade from breathing, forcing you to exit small losses frequently while rare large losses overwhelm the frequent small wins. The result: negative expectancy despite a high win rate.

- **Without a volatility edge, you're hoping [07:25–07:47]**: If you don't have a systematic way to identify when IV is truly overstated, you're not trading—you're gambling. Optimize the strategy and become discerning; don't run it mechanically.

## Notable quotes

> "The entire purpose of the zero DTE strategies is we are attempting to trade the typical overstatement of implied volatility to historic volatility."

> "If you're trading a spread, you're selling the volatility in this 10 delta short put but then you're buying the very same volatility that you think is overpriced—that's the first problem."

> "If you've blindly followed something mechanically, you step into periods exactly like this that don't make any sense for the strategy to be deployed."

## Candidate wiki links

**Concepts:**
[[zero-dte]], [[volatility-risk-premium]], [[implied-volatility]], [[realized-volatility]], [[short-volatility]], [[delta]], [[risk-management]], [[backtesting]], [[expected-value]], [[edge]]

**Strategies:**
[[short-strangle]], [[short-straddle]], [[iron-condor]], [[short-premium]]

**Securities:**
[[spx]]

## Regime / context

Recorded 2022-10-26 (Sunday, no live market). The analysis is evergreen: zero-DTE premium selling is a volatility-harvesting strategy that only has positive expectancy when implied volatility is genuinely elevated relative to realized volatility. The three mistakes (spreads that contradict the thesis, indiscriminate entry, stops that destroy expectancy) apply across all market regimes but are most costly in low-IV or rising-RV environments.
