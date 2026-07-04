---
type: source
title: "Searching for the Best 0DTE SPX Options Strategy"
video_id: IM2LefSdT5g
url: https://www.youtube.com/watch?v=IM2LefSdT5g
date: 2024-07-27
series: none
format: [education, analysis, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spx]
concepts: [volatility-risk-premium, implied-volatility, realized-volatility, variance-risk-premium, zero-dte, delta, short-volatility, transaction-costs, risk-management, stop-loss, profit-mechanism, win-rate-vs-profitability, overfitting, robustness, volatility-clustering, position-sizing, delta-hedging, tail-risk]
strategies: [short-straddle, short-strangle, zero-dte, short-premium]
saga: null
part: null
confidence: high
---

# Searching for the Best 0DTE SPX Options Strategy

## Summary

Eric explores zero-DTE SPX options strategies through systematic backtesting and live trading data, finding that **short strangles and short straddles** capture variance risk premium most effectively. The core profit mechanism relies on implied volatility consistently pricing above realized volatility. By applying tail-risk management (300% max loss stops) and optimizing entry timing (afternoon entries near market close), the strategy becomes robust across market regimes, though year-over-year performance varies significantly by structure.

## Key takeaways

### Profit mechanism & market structure
- **Variance risk premium is the edge:** implied volatility trades above realized volatility most of the time; sell-side strategies capture this gap [01:04]
- **SPX preferred over SPY:** tax advantages (Section 1256) and position sizing efficiency reduce transaction costs, which are hidden in fills and slippage rather than commissions [02:43]
- **Transaction costs are severe in 0DTE:** hidden in market impact and entry slippage; minimize trade frequency and position count [03:03]

### Delta selection & structure comparison
- **15-delta short strangles outperform** across most conditions; 5-delta calls have higher win rates but collect insufficient premium [05:08]
- **Adding wings (straddles) helps straddles but hurts strangles:** straddles reduce max loss from ~12k to ~6k, but strangles already have wide profit zones [05:31]
- **Unrealized P&L trap:** a 15-delta short strangle shows −$1,200 unrealized loss at breakeven but profits $2 at expiration; premature stop-loss exits kill winners [06:31]

### Risk management & tail control
- **200–300% max loss stops are robust:** cutting extreme losses improves all strategies across the board; 200% works but 300% prevents whipsaws on late-day entries [08:44, 11:53]
- **Stop-loss timing matters:** combining afternoon entry + 300% stops avoids prematurely exiting trades that recover by close [12:20]
- **Volatility clustering creates entry windows:** historic volatility crossing above implied volatility clusters for 2–3 days; can add momentum factor to entry timing, but mechanical entry (dollar-cost-averaging style) also works [04:04]

### Entry timing & seasonal robustness
- **Afternoon entries (2 PM ET onward) perform best:** straddles become top performers near market close, suggesting end-of-day volatility repricing [11:05]
- **Year-over-year flip-flopping:** straddles rank 1st → 2nd-worst → 1st across 2022H2, 2023, 2024; short strangles show more consistent performance [13:11]
- **Robustness check:** segment backtest data by year to detect overfitting; avoid strategies with high year-over-year variance [08:18]

### Practical refinements
- **Intraday volatility sampling:** forecast end-of-day vol using moving-average logic to size positions dynamically [13:57]
- **Catalyst downsizing:** reduce size on big news days (elevated IV already compensates) [13:57]
- **Delta rebalancing protocol:** early-stage testing shows promise but too early to conclude [14:20]

## Notable quotes

> "It's normally there until it's not and then it generally comes back pretty quickly—that being variance risk premia." [04:42]

> "The fact that this positively impacts everything across the board to varying degrees, it tells me that we're on the right track in terms of what adjustments we're applying." [09:32]

## Candidate wiki links

**concepts:**
- [[volatility-risk-premium]]
- [[implied-volatility]]
- [[realized-volatility]]
- [[zero-dte]]
- [[delta]]
- [[transaction-costs]]
- [[risk-management]]
- [[stop-loss]]
- [[overfitting]]
- [[volatility-clustering]]
- [[position-sizing]]
- [[tail-risk]]
- [[win-rate-vs-profitability]]

**strategies:**
- [[short-strangle]]
- [[short-straddle]]
- [[short-premium]]
- [[zero-dte]]

**securities:**
- [[spx]]

**people:**
- [[eric]]

## Regime / context

Backtest period: launch of daily SPX expirations through June 4, 2024. Data segmented by year (2022H2, 2023, 2024) to assess robustness. Year-over-year performance variance is high for straddles but lower for 15-delta and 10-delta short strangles, suggesting the latter are more regime-agnostic. No profit/loss management protocols applied in initial analysis; tail-risk stops (200–300% max loss) added in refinement phase. Live trading data incorporated alongside backtest to validate findings.
