---
type: source
title: "How to Test a Trading Strategy & Build a Trade Log"
video_id: ZTW-rWkkelk
url: https://www.youtube.com/watch?v=ZTW-rWkkelk
date: 2025-07-20
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy]
concepts: [profit-mechanism, outlier-strategy-process, backtesting, monte-carlo-simulation, paper-trading, cognitive-biases, confirmation-bias, market-regimes, regime-impact, sequence-of-returns, sample-size, win-rate-vs-profitability, expected-return, expected-value, standard-deviation-channels, coefficient-variance, max-drawdown, sharpe-ratio, sortino-ratio, return-sequence, days-to-expiration, required-trade-count, disposition-effect, trend-following, breakout, trading-log, pnl-attribution, risk-management]
strategies: [breakout, long-call, sector-rotation]
saga: none
part: null
confidence: high
---

# How to Test a Trading Strategy & Build a Trade Log

## Summary

This video walks through the systematic process for evaluating any trading strategy—from defining the profit mechanism through live testing and iteration. Eric emphasizes that most traders fail to properly analyze their strategies, confusing win-rate metrics with actual edge, and provides a complete trade-log template with key statistical metrics (expected return, standard deviation, max drawdown, Sortino ratio, required trade count) to quantify performance honestly.

## Key takeaways

- **Define the profit mechanism first** [01:02] — You must understand *what effect* you're trying to capture before testing. Without this, you cannot accurately evaluate whether your strategy is actually capturing the intended idea.

- **The outlier strategy process has five phases** [02:16] — (1) identify the profit mechanism, (2) analyze/quantify it, (3) develop and test the strategy (backtesting, Monte Carlo, forward testing), (4) apply first-round metrics analysis, (5) live test with minimal viable product, then scale.

- **Regime impact is critical** [04:42–05:44] — Different strategies perform differently in different market regimes (economy, stock market, sector, portfolio level). A strategy that loses in 2022 isn't necessarily bad; it may simply not fit that regime. Regimes can be long-term (10-year uptrend) or sub-regimes (2022 downtrend).

- **Sequence of returns vs. sample size** [07:04–08:09] — Winning 16 of 17 months looks good but may reflect a tiny sample. A zero-DTE strategy with five trades gives five data points; a once-per-year effect with five trades gives five years of data. You must account for how many instances the effect actually produces.

- **Win rate is not the full story** [09:24–17:34] — A 47% win-rate long-call strategy can be highly profitable if average wins are much larger than average losses. Focus on expected return and P&L distribution, not win rate alone.

- **Use summary statistics to spot regime shifts** [15:09–16:19] — Plot P&L over time. If the line of best fit changes slope mid-sample, something has shifted (regime change, management error). This visual check catches what raw numbers might miss.

- **Remove extremes to test robustness** [16:19] — Strip out the biggest winner and loser. If P&L changes dramatically, your strategy is tail-dependent; if not, it's more consistent. This tells you whether to manage tails or trust the core mechanism.

- **Average win vs. average loss matters more than win rate** [17:34–18:42] — If you lose 53% of the time but your average win is 3× your average loss, the math works. Know your strategy's profit mechanism so you can recognize when management changes (e.g., taking profits too early) break it.

- **Required trade count is a progress metric, not a gate** [19:46–20:52] — Calculate how many trades you need for statistical confidence (using confidence interval, downside deviation, margin of error, expected return). If the number is 10,000, don't wait—track whether it's *contracting* as you trade. Contraction means you're tightening consistency and moving in the right direction.

- **Build your own trade log** [14:02–15:09] — The template shown has input rows (live trades), calculated columns (formulas you set once), open/closed sections, and a summary by strategy. Create population (all instances) and sample (time-bound or DTE-filtered) versions to compare subsets against the total.

## Notable quotes

> "If we're testing a strategy that happens to not align well with the current regime, whatever that is, it doesn't automatically mean that that's bad. It just means that it doesn't fit that regime for some reason."

> "Win rate is only part of the equation, but the rest of the context matters a lot."

> "You have to build your own [trade log]. And it's because you learn a lot in building your own."

## Candidate wiki links

**concepts:** [[profit-mechanism]], [[outlier-strategy-process]], [[backtesting]], [[monte-carlo-simulation]], [[paper-trading]], [[cognitive-biases]], [[confirmation-bias]], [[market-regimes]], [[sequence-of-returns]], [[sample-size]], [[win-rate-vs-profitability]], [[expected-return]], [[standard-deviation-channels]], [[max-drawdown]], [[sharpe-ratio]], [[sortino-ratio]], [[return-sequence]], [[disposition-effect]], [[trend-following]], [[trading-log]], [[pnl-attribution]], [[risk-management]]

**strategies:** [[breakout]], [[long-call]], [[sector-rotation]]

**securities:** [[spy]]

**people:** [[eric]]

## Regime / context

Recorded June 2025. The video is evergreen methodology; specific regime examples (nuclear energy sector strength, 2022 bear market) are illustrative. The trade-log template and statistical framework apply across all market conditions and strategy types.
