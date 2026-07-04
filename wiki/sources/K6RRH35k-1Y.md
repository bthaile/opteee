---
type: source
title: "Small Stacks #2: Building a $5K Portfolio from Scratch"
video_id: K6RRH35k-1Y
url: "https://www.youtube.com/watch?v=K6RRH35k-1Y"
date: "2023-01-06"
series: small-stacks
format: [education, analysis, strategy-breakdown]
experts: [eric]
mentions: []
securities: [tqqq, spy, cisco, pfizer, sofi, ford, ewz, aapl, amzn, msft, googl, nvda, orcl, pypl, zm, ccl, sym]
concepts: [position-sizing, risk-management, risk-tolerance, capital-efficiency, expected-value, delta, implied-volatility, portfolio-first, trading-plan, process-over-outcome, trading-psychology, mark-to-market, realized-vs-unrealized-pnl, annualized-return, expected-return, probability-of-touch, moneyness, days-to-expiration, margin, cost-basis, profit-mechanism, no-code-tools, prompt-engineering, context-window-management]
strategies: [covered-strangle, ratio-call-diagonal, long-call, call-credit-spread, short-put, box-spread, vertical-spread]
saga: small-stacks
part: 2
confidence: high
---

# Small Stacks #2: Building a $5K Portfolio from Scratch

## Summary

Eric builds a live $5K options portfolio from January 2023 forward, demonstrating core/speculative allocation splits, position-sizing constraints, and the trade-offs inherent in small-account trading. The session covers covered strangles on TQQQ, directional spreads on Cisco and Pfizer, and the mechanics of rolling positions as they move against delta targets. Key theme: realistic expectations and process discipline matter more than absolute dollar returns.

## Key takeaways

- **Target return benchmark [00:00]**: Start with 8–10% annual return (market average) as an interim goal before scaling to higher targets; measure success via risk-adjusted returns (max drawdown, Sharpe/Sortino), not absolute returns alone.

- **Risk tolerance for small accounts [08:39]**: A $5K account should mentally prepare to lose the entire amount; set a portfolio-level circuit breaker (e.g., 50% max drawdown = $2,500 stop-loss) rather than unrealistic 30% targets.

- **Core vs. speculative allocation [11:15]**: Allocate ~70% to core (index ETF or covered strangle on liquid name like TQQQ); ~30% to speculative (directional trades, earnings plays). Covered strangles and ratio diagonals are primary strategies for small accounts.

- **Liquidity constraints [13:31]**: Scanning for tradeable names is critical; TQQQ at <$20 is accessible for covered strangles; avoid illiquid tickers. Watch lists replace automated scans when platform limitations exist.

- **Position entry: TQQQ core [18:49]**: Buy 100 shares at $16.72 (cost $1,672); sell 15-delta put at $1.20 (collect $120); sell 25-delta call at $0.59 (collect $59). Margin requirement = stock cost; risk = full position size.

- **Spreadsheet automation [28:31]**: Use AI (Gemini/ChatGPT) to build cost-calculation formulas that differentiate equity (size × price) from options (size × premium × 100); preserve all inputs for later analysis.

- **Margin vs. risk tracking [35:32]**: For covered strangles, margin and risk are identical (cash requirement). For spreads, margin is the width minus premium. Track debits/credits separately to calculate realized return per trade.

- **Expected value on spreads [56:44]**: Vertical spreads often have negative expected value (e.g., −$35 on a $50 max-win trade); this means you must be directionally correct—no inherent edge. Size accordingly (4% portfolio risk on a $50 win is suboptimal).

- **Rolling puts as stock rallies [01:09:12]**: When TQQQ rallies, short puts lose delta fast (17→13 delta in days). Rolling up to maintain delta requires additional capital; small accounts face hard choices: buy shares outright or accept reduced delta coverage.

- **Managing short calls [01:18:39]**: Close short calls when stock moves significantly ITM (e.g., TQQQ at $21.66 vs. $21 strike). Roll to later expiration and higher strike if needed; accept small losses to preserve core position.

- **Realized P&L tracking [01:20:21]**: Close trades in the log immediately; use conditional formulas (IF not blank, exclude from margin sum) to avoid manual deletion of useful data. Track net debits/credits and return % on capital deployed.

- **Watch-list discipline [01:30:15]**: Ford (consolidating, no entry yet), SoFi (long calls on breakout above $4.22), EWZ (call credit spread if breaks support). Avoid trading consolidation; wait for directional confirmation.

- **Box spreads vs. savings [01:35:17]**: Box spreads yield ~5.8% annualized on risk-free capital; compare to current yield curve. Trade spreads yourself rather than using a ticker like BOX for better execution.

- **Expectation management [01:41:58]**: $71.71 gross profit (1.42% return over ~20 days) is good in context but feels trivial in dollars. Most small-account traders fail because they expect fast, large returns; discipline requires accepting modest percentage gains.

- **Paper trading in parallel [01:48:06]**: Even while live-trading a $5K account, run a paper-trading account at larger scale to test strategies and position-sizing without risking real capital.

## Notable quotes

> "The job, the entire goal of what we're doing is to make money. So yeah, I don't disagree though. Ford, it's massively boring." [01:43:37]

> "The way to think about prompt engineering, it's literally the same exact thing as trading. All of the work is done in the prep." [01:34:23]

> "Most people that start with a small account just start with the completely wrong expectations, which is really what the first session was about." [01:45:05]

## Candidate wiki links

**concepts:**
[[position-sizing]], [[risk-management]], [[risk-tolerance]], [[capital-efficiency]], [[expected-value]], [[delta]], [[implied-volatility]], [[portfolio-first]], [[trading-plan]], [[process-over-outcome]], [[trading-psychology]], [[mark-to-market]], [[realized-vs-unrealized-pnl]], [[annualized-return]], [[expected-return]], [[probability-of-touch]], [[moneyness]], [[days-to-expiration]], [[margin]], [[cost-basis]], [[profit-mechanism]], [[no-code-tools]], [[prompt-engineering]], [[context-window-management]]

**strategies:**
[[covered-strangle]], [[ratio-call-diagonal]], [[long-call]], [[call-credit-spread]], [[short-put]], [[box-spread]], [[vertical-spread]]

**securities:**
[[tqqq]], [[spy]], [[cisco]], [[pfizer]], [[sofi]], [[ford]], [[ewz]], [[aapl]], [[amzn]], [[msft]], [[googl]], [[nvda]], [[orcl]], [[pypl]], [[zm]], [[ccl]], [[sym]]

**people:**
[[eric]]

## Regime / context

**Date:** January 2023 (post-2022 bear market; market rallying into 2023).

**Part 2 of Small Stacks series.** Part 1 (referenced at [01:39:36]) covers foundational expectations and goal-setting; this episode executes live portfolio construction and trade management over ~20 trading days. Subsequent episodes will focus on strategy toolkit development across varying market conditions.

**Platform:** On Demand (backtesting/paper-trading tool with limitations: no scanning, limited historical data depth, no IV percentile/rank display).

**Key constraint:** $5K account size forces use of spreads (verticals, ratio diagonals) instead of outright long options; margin and liquidity become binding constraints on position count and size.
