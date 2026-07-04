---
type: source
title: "Using Options to Get Long and Short Pt2 | Outlier Options Trading Beginner Lab"
video_id: erYCMg8mwzI
url: https://www.youtube.com/watch?v=erYCMg8mwzI
date: 2026-01-18
series: beginner-lab
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [crm, rklb]
concepts: [profit-mechanism, long-call, short-put, short-call-spread, delta, implied-volatility, volatility-skew, price-action, support-and-resistance, expected-move, win-rate-vs-profitability, trading-psychology, backtesting, paper-trading, delta-neutral, moneyness, volatility-percentile, risk-premium, realized-vs-unrealized-pnl]
strategies: [long-call, short-put, short-call-spread, breakout, momentum]
saga: none
part: null
confidence: high
---

# Using Options to Get Long and Short Pt2 | Outlier Options Trading Beginner Lab

## Summary

This session builds on the previous framework for selecting option structures by exploring the decision tree for choosing between long and short premium, and between long and short directional exposure. Eric walks through how to use backtesting, paper trading, and options market structure (delta distribution, skew, volatility percentile) to validate strategy choices before deploying capital, using CRM as a live case study.

## Key takeaways

- **Profit mechanism drives structure selection** [11:02–12:27]: Define what you're trying to capture (e.g., velocity + severity + quick duration for breakouts), then measure duration, move size, and distribution. This analysis determines DTE, delta, and whether you want capped or uncapped profit.

- **Test all permutations agnostically before committing** [13:32–17:35]: Don't decide on a structure during the trade. Run historical analysis (backtesting or paper trading) on all candidate structures (long calls, synthetic longs, spreads, etc.) under your profit mechanism, then build a playbook with context-dependent rules (liquidity, volatility, portfolio fit).

- **Probability of the option ≠ probability of your trade** [23:15–29:00]: Long options have lower intrinsic probability of expiring ITM, but if your directional analysis is sound, you can achieve high win rates with long options. Win rate and profitability are decoupled; focus on expected return, not the Greeks' embedded probability.

- **Exit before expiration changes the math** [25:21–25:56]: A long call that loses $861 at expiration can make $232 today if the underlying ticks up. Holding to expiration vs. exiting early fundamentally changes the payoff profile and the relevance of theoretical probabilities.

- **Low win rates are acceptable if asymmetric** [30:34–33:33]: Breakout strategies can have 40% win rates but remain profitable if winners are large and losers are small. Requires active management (bouncing in and out) and emotional discipline to accept frequent small losses.

- **Use options market structure to validate thesis** [39:24–45:42]: Plot delta across strikes to see the market's expected distribution. Steeper slope on one side indicates skew; compare 10-delta strikes to gauge how far the market expects the move. For CRM, the flatter downside slope suggests the market is pricing in a floor.

- **Volatility percentile and risk premium matter more than raw IV** [46:03–47:22]: CRM's 30-day IV percentile is 48% (middle of range), not high. Realized volatility is trending over implied, and risk premium percentile is low—all reasons to avoid short premium here despite the decline.

- **Match structure to directional bias** [35:06–37:45]: Cash-secured put is bullish (wants upside); short call spread is bearish (wants downside). If you think CRM will oscillate sideways after a floor, short puts make sense only if you're willing to take assignment and hold long-term. Otherwise, a short call spread better matches the thesis.

- **Confirm at support before entering** [38:10–50:30]: Don't front-run a hypothesized floor. Wait for price to approach it and observe how it behaves. The probability of being correct early is lower than the edge gained by waiting for confirmation.

- **Paper trading for a year builds usable data** [20:47–21:34]: You don't need a rigorous backtest; one year of paper trading gives you solid sample size and real-world insights, though with limitations. Better than nothing if you can't commit to formal backtesting.

- **Overpaying for an option increases your effective IV** [51:00–52:25]: Bad fills or wide bid-ask spreads raise your breakeven. Compute your actual IV using Black-Scholes with your entry price to see what volatility you paid for.

## Notable quotes

> "The ideal scenario is literally to do this kind of process and to have a strategy outline. In the strategy outline, we want to have at least some parameters for each strategy that I trade and some of the details that are relevant to it." [11:24]

> "Don't worry so much about the baked-in probabilities of what they are because it actually might not be super relevant to you. What's more important is whatever your strategy is and whatever the analysis that you do—part of your setup." [29:00]

> "There's a massive difference between win rate and profitability. And I care way more about profitability." [33:09]

## Candidate wiki links

**concepts:** [[profit-mechanism]], [[delta]], [[implied-volatility]], [[volatility-skew]], [[expected-move]], [[win-rate-vs-profitability]], [[trading-psychology]], [[backtesting]], [[paper-trading]], [[moneyness]], [[volatility-percentile]], [[risk-premium]], [[price-action]], [[support-and-resistance]], [[realized-vs-unrealized-pnl]], [[assignment]]

**strategies:** [[long-call]], [[short-put]], [[short-call-spread]], [[breakout]], [[momentum]]

**securities:** [[crm]], [[rklb]]

**people:** [[eric]]

## Regime / context

Recorded 2026-01-18. Part 2 of a two-part beginner series on option structure selection. Part 1 (previous session) covered the process for choosing long structures; this session extends to short premium and directional bias, with live market examples (CRM, RKLB) and options market analysis.
