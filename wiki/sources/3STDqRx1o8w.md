---
type: source
title: "Track Your Trades Like a Pro – Build the Perfect Options Trade Log"
video_id: 3STDqRx1o8w
url: https://www.youtube.com/watch?v=3STDqRx1o8w
date: 2025-02-02
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [tqs, upro, ibit, gme, qqq]
concepts: [trading-log, trading-plan, profit-mechanism, position-sizing, pnl-attribution, realized-vs-unrealized-pnl, process-over-outcome, risk-management, emotional-discipline, confirmation-bias, mark-to-market, capital-efficiency, leverage, delta, theta, vega, implied-volatility]
strategies: [covered-strangle, long-call, ratio-call-diagonal, box-spread, short-premium]
saga: null
part: null
confidence: high
---

# Track Your Trades Like a Pro – Build the Perfect Options Trade Log

## Summary

A comprehensive walkthrough of building and maintaining a trading log as a core business practice for long-term traders. The log serves dual purposes: the process of building it forces analytical thinking about strategy mechanics, and the output provides objective data to counter cognitive biases and track true profitability across time horizons. The speaker demonstrates a multi-tab Google Sheets system that tracks individual strategy performance, aggregates portfolio-level metrics, and enables data-driven decision-making without requiring full automation.

## Key takeaways

- **Why traders skip the log** [00:00–02:05]: Most traders avoid logging because they expect trading to be "fast easy money" and perceive tracking as work. Accepting that trading requires bookkeeping—like any business—is the first mental hurdle.

- **Log complements the trading plan** [02:05–03:10]: The trading plan outlines research and backtested ideas; the log captures actual results. Together they short-circuit cognitive biases (Goldilocks analysis, disposition effect) and reveal true returns over time, especially for rolled positions.

- **Architecture: strategy tabs + C2C dashboard** [04:12–05:28]: Organize by strategy (covered strangle, single trades, box spreads, paper trading) in separate tabs. Summarize each strategy's aggregate metrics at the top, then link to a "C2C" (command-and-control) dashboard that collates all strategies into one portfolio view.

- **Data structure for analysis** [06:31–07:48]: Avoid narrative entries ("sold 5 puts for $2, made $1"). Instead, structure data as columns (entry date, strike, delta, premium, lots) so you can conduct trend analysis and identify what actually matters for each strategy.

- **Manual input with purpose** [11:18–12:31]: Color-code manual inputs (green) separately from auto-calculated fields. This makes it obvious where you need to enter data and keeps the log sustainable. Track only what impacts decisions: for covered strangles, focus on allocation, utilization (stock vs. cash-secured puts), and distance from 52-week highs—not every Greek.

- **Utilization vs. allocation** [10:14–11:18]: Allocation = money set aside for a strategy; utilization = money actually deployed. For leveraged underlyings (TQS, UPRO), also track notional exposure to understand true leverage and risk.

- **Rolling and adjustment tracking** [14:50–15:06]: Use a side calculator to track break-even prices when rolling. If you close a trade for $8.25 and open a new one at $8.50, calculate the exact price the new option must hit to wash the prior trade.

- **Multi-leg strategies** [18:15–19:13]: For ratio call diagonals or other multi-leg trades, use a dash in the strategy column to indicate a base leg is part of a larger position. Copy and paste the row structure; formulas auto-update the strategy label.

- **Portfolio-level metrics** [20:06–21:08]: Track beginning portfolio value, total theta, comparison to a reference return (SPY, QQQ), and the difference between allocation and utilization. For leveraged positions, separate notional exposure from actual dollar utilization.

- **Avoid over-tracking; iterate** [23:23–24:21]: Start by tracking more than you think you need. Over time, dial back to only what informs decisions. If the log becomes too burdensome, you won't maintain it. Use comments to clarify acronyms and intent.

- **Evolution of the log** [01:01–02:05]: The speaker's log evolved from handwritten → manual input → full automation → back to manual input with selective tracking. The process of building the log is as valuable as the output.

## Notable quotes

> "The process of building the log is really useful because it brings you closer to your strategies, closer to the information, and it makes you think analytically."

> "A trade log is essentially bookkeeping. This is what businesses do. This is how businesses make decisions and survive."

> "If you make it too annoying, it'll be a bear to deal with and you probably won't want to do it."

## Candidate wiki links

**concepts:** [[trading-log]], [[trading-plan]], [[profit-mechanism]], [[position-sizing]], [[pnl-attribution]], [[realized-vs-unrealized-pnl]], [[process-over-outcome]], [[risk-management]], [[emotional-discipline]], [[confirmation-bias]], [[mark-to-market]], [[capital-efficiency]], [[leverage]], [[delta]], [[theta]], [[vega]], [[implied-volatility]]

**strategies:** [[covered-strangle]], [[long-call]], [[ratio-call-diagonal]], [[box-spread]], [[short-premium]]

**securities:** [[tqs]], [[upro]], [[ibit]], [[gme]], [[qqq]]

## Regime / context

Recorded 2025-02-02. This is a foundational education video on trade logging best practices, applicable across market regimes. The speaker references 18 years of trading experience and demonstrates a live Google Sheets template. The specific positions shown (covered strangles in TQS, UPRO, IBIT, GME) are illustrative examples; the framework is strategy-agnostic.
