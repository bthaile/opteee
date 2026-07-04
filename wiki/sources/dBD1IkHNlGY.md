---
type: source
title: "Backtesting Basics for Trading Options"
video_id: dBD1IkHNlGY
url: https://www.youtube.com/watch?v=dBD1IkHNlGY
date: 2025-06-15
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [sofi, tqqq]
concepts: [backtesting, overfitting, robustness, profit-mechanism, post-earnings-drift, expected-move, annualized-return, volatility-clustering, stress-testing, monte-carlo-simulation, paper-trading, forward-testing, process-over-outcome, outlier-strategy-process]
strategies: [long-call]
saga: null
part: null
confidence: high
---

# Backtesting Basics for Trading Options

## Summary

This video provides a foundational framework for backtesting trading ideas, emphasizing that backtesting is a tool to eliminate bad ideas rather than find optimized strategies. Eric walks through the critical shortfalls (overfitting, false confidence, lack of robustness) and demonstrates a practical workflow using SoFi pre-earnings drift as a case study, leveraging AI tools to accelerate the analysis from profit-mechanism validation through strategy simulation.

## Key takeaways

### Evergreen mechanics

- **Purpose of backtesting** [00:00–01:06]: Backtesting is for viability screening—determining whether an idea is worth pursuing—not for finding the "best" strategy. The past is nuanced and relevant only to itself; the future may resemble the past but never replicates it.

- **Backtesting vs. strategy hopping** [02:19–03:19]: Understanding a strategy through backtesting prevents emotional abandonment during drawdowns. Traders who backtest develop confidence in the approach and can distinguish normal variance from strategy failure.

- **Overfitting as the primary shortfall** [03:19–04:35]: Adding filters iteratively shapes a strategy to historical data, creating false confidence. A backtest showing 66.6% CAGR with 6% max drawdown signals severe overfitting; such performance is not robust to out-of-sample (forward/live) conditions.

- **Robustness testing via segmentation** [12:13–14:28]: Split historical data into progressively smaller time windows (e.g., 10 years → 5 years → 2.5 years) and retest the strategy. If performance degrades significantly when parameters shift slightly (e.g., 30 DTE to 31 DTE), the strategy lacks robustness. This detects smoothing effects that mask drawdown severity.

- **Stress testing and tail risk** [14:28–15:47]: Use historical worst-case moves (e.g., TQQQ's 82%+ drawdown) and pad them further with standard-error bands. Stress tests must align with the specific strategy being tested.

- **Profit mechanism first** [06:44–07:55]: Start with a profit mechanism (e.g., pre-earnings drift), not with option parameters (delta, DTE, IV). The profit mechanism is agnostic to the instrument; options are overlaid later.

- **Eyeball test and research** [07:55–09:01]: Visually inspect price charts around catalysts (e.g., earnings) to spot patterns. Cross-reference with peer-reviewed research (SSRN, academic papers) to avoid reinventing the wheel and to identify which variables matter.

- **Data sourcing and AI acceleration** [10:12–11:12]: Options data is expensive and large; for many strategies, you can test the underlying stock move and infer option behavior using options knowledge. ChatGPT can extract earnings dates and analyze price behavior, but always fact-check AI outputs.

- **Isolating the earnings move** [19:56–21:04]: Remove baseline drift by comparing random non-catalyst periods to earnings periods. This isolates excess move attributable to the catalyst. Median aggregation is more robust than mean when outliers exist.

- **Annualized returns for fair comparison** [22:18]: When comparing holding periods of different lengths, normalize to annualized return basis to account for compounding and time decay.

### Dated market read (2025-06-15)

- **SoFi pre-earnings drift observation** [07:55–09:01]: A community member observed potential upside drift into SoFi earnings releases. Eyeball inspection of recent earnings suggested positive price movement pre-release, warranting deeper analysis.

- **Trend in pre-earnings moves** [21:04]: Analysis of SoFi's pre-earnings moves over time shows the magnitude of excess drift is *decreasing* both upside and downside, likely due to increased information coverage and analyst consensus reducing surprise.

## Notable quotes

> "The entire concept of back testing, I think, is widely misunderstood. Most people would think of it as, oh, this is a way for me to find if this strategy works or this is for me to find the optimized strategy, the best strategy. That's really not the point at all." [00:00–01:06]

> "The past is always nuance and relevant to the past. The future can look like flavors of the past, but it's never the past." [01:06]

> "If you look at buy and hold in something like TQ's, it might look something like this. And you might see something like a gajillion% return because three times leverage tech has done well. But this move here can be very minimized compared to what it actually was." [13:12–14:28]

## Candidate wiki links

**concepts:** [[backtesting]], [[overfitting]], [[robustness]], [[profit-mechanism]], [[post-earnings-drift]], [[expected-move]], [[annualized-return]], [[volatility-clustering]], [[stress-testing]], [[monte-carlo-simulation]], [[paper-trading]], [[forward-testing]], [[process-over-outcome]], [[outlier-strategy-process]]

**strategies:** [[long-call]]

**securities:** [[sofi]], [[tqqq]]

**people:** [[eric]]

## Regime / context

Recorded 2025-06-15. This is a foundational education video on backtesting methodology, not a market-specific call. The SoFi pre-earnings drift example is illustrative; the framework applies to any profit mechanism. The emphasis on AI-assisted backtesting (ChatGPT) reflects tools available as of mid-2025. Robustness testing and overfitting warnings are evergreen; the specific SoFi trend (declining pre-earnings moves) is time-bound and may not persist.
