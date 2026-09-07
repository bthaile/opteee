---
type: source
title: "Reviewing Strategy Research | Drive-Thru Trading"
video_id: lJnZcDV4Vu4
url: https://www.youtube.com/watch?v=lJnZcDV4Vu4
date: 2026-09-03
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spy, xlf, xlp, xlk, xlv, xlu, xly, xlre, xlc, xli, xlb]
concepts: [sector-rotation, momentum, signal-identification, backtesting, profit-mechanism, regime-dependency, drawdown-management, mean-reversion, position-sizing, friction-costs, bid-ask-spread, rebalancing, hypothesis-testing, data-quality, risk-management, leverage, margin, optionality, transaction-costs, performance-analysis, greek-attribution, tail-risk, capital-preservation]
strategies: [sector-rotation, momentum, mean-reversion, trend-following, long-only, rebalancing]
saga: null
part: null
confidence: high
---

# Reviewing Strategy Research | Drive-Thru Trading

## Summary

Eric reviews CG's sector-rotation momentum strategy research, which uses the SPY 200-day moving average as a regime filter to hold the top five momentum sectors in bullish environments and the top two in bearish environments. The session focuses on critical research methodology: validating signal logic, understanding profit mechanisms, analyzing friction costs across rebalancing frequencies, and stress-testing results against historical drawdowns. Key themes include the relationship between upside capture and downside protection, the hidden costs of portfolio turnover, and the discipline required to avoid over-optimization.

## Key takeaways

### Research methodology & signal validation
- **[07:12]** Start research by mapping signals to profit mechanisms—understand *why* a signal works, not just that it works. Avoid building strategies without logical connection to the effect being traded.
- **[11:16]** A signal is any input (technical, fundamental, portfolio-level) that determines positioning. In this case, the 200-day MA filters regime; the logic is that bullish environments favor momentum leaders.
- **[12:23]** The strategy reduces exposure in bear regimes rather than going short, cutting tail risk (COVID, 2008, dot-com crashes) without requiring directional shorts.
- **[13:29]** When exploring parameter choices (e.g., why two holdings vs. one, three, or five), develop the ability to punch holes in results and reason about uncertain futures, not just accept backtested outcomes.
- **[14:41]** Understand the relationship between parameters and market regime. Over the last 20 years, tech dominance means holding too many sectors dilutes concentration; in a non-dominant-sector regime, the optimal count may shift.
- **[16:04]** The difference between mechanical and discretionary strategy: mechanical rules (top five/two rotation) are the baseline; discretion enters when you notice regime changes and adapt without over-tweaking.

### Friction & rebalancing frequency
- **[25:03]** Every portfolio adjustment has a cost—commissions, bid-ask spreads, and slippage. Brokers hide these costs well, but they are far more expensive than most traders realize.
- **[26:36]** Analyze the cost of different rebalancing frequencies (daily, weekly, monthly, conditions-based) before assuming faster rebalancing improves performance.
- **[29:13]** Monthly rebalancing may miss moves after the 200-day MA "makes a decision," but weekly rebalancing incurs higher friction. The trade-off is non-trivial.
- **[30:37]** AI can quickly model friction across frequencies. Ask it to specify cost-to-performance in each scenario and track friction explicitly. Tax treatment differs: in tax-free accounts, rebalancing frequency is purely a friction question; short-term gains are taxed the same regardless of monthly vs. weekly.
- **[41:32]** Friction analysis revealed: monthly turnover ~12 trades/year at ~8 percentage points cost; weekly ~50 trades/year at ~19 percentage points. Weekly is not 4× more expensive because many signal reviews yield no action (overlap).

### Performance analysis & metric relationships
- **[35:54]** A max drawdown of 18% vs. SPY's ~50% is not suspicious; it reflects the 200-day MA compression effect. When markets rise, the MA catches up; drawdowns occur when price-to-MA distance is already compressed, limiting downside.
- **[37:13]** To validate a surprising metric, cross-check it: pull historical prices from another source (Yahoo Finance, etc.) and spot-check the period around max drawdown. Data will never be 100% identical across sources (close prices vary by cents), but large discrepancies signal problems.
- **[48:34]** Avoid anchoring on a single underperforming metric (e.g., best month). Look at relationships: sacrificing 2 percentage points of upside to gain 7 points of downside protection is a favorable trade-off.
- **[50:50]** Distinguish between "this is the absolute best strategy" and "there is probably room to improve." Probable improvement is reasonable; definite improvement without evidence is ego-driven.
- **[52:11]** You do not need to outperform the market every year to beat it long-term. Pacing the market upside while cutting downside significantly will outperform. Pulling levers (e.g., improving best month) has ripple effects; measure the cost to average winning month, not just the headline metric.

### Data validation & research discipline
- **[38:28]** When using AI-generated backtests, acknowledge uncertainty. Ask the AI to cross-validate results using different tools or data sources. Hallucinations and data errors are real.
- **[39:34]** To verify a backtest result, overlay your strategy's performance chart with the underlying index from an independent source. You don't need the strategy chart from Yahoo Finance—just the underlying prices.
- **[44:35]** For max drawdown validation, request a table showing holdings, spot prices, and dates ±30 days around the drawdown. Cross-check those prices against Yahoo Finance or another broker. This isolates data quality from strategy logic.
- **[46:12]** Data will never be 100% accurate across sources; close prices vary by cents. Spot-check for material discrepancies, not perfection.

### Strategy refinement homework
- **[25:03]** Explore methods to improve best-month performance and quantify the cost (impact on average winning month, worst month, Sharpe ratio, etc.).
- **[25:03]** Analyze rebalancing frequency trade-offs: daily, weekly, monthly, conditions-based. Include friction and tax implications.
- **[25:03]** Build a heat map: hold top 1, 2, 3, 4, 5 performers and compare performance across both holdings count and moving-average period (150, 200, 250 days).
- **[26:56]** Codify the strategy in a formal trade plan document (strategy outline format) that explains the rule set, profit mechanism, signal logic, and relationships between parameters.

### Mindset & trader development
- **[33:31]** The difference between successful and unsuccessful traders is not just ideas but analytical discipline. Curiosity without ego is essential; attachment to ideas kills learning.
- **[53:30]** Psychological bias: the brain anchors on underperformance (e.g., best month) and wants to "fix" it immediately. Resist this; evaluate trade-offs holistically.
- **[01:08:06]** Early career (sub-30): allocate 85–90% of effort to building capital and skill. This unlocks optionality and freedom later. Money is not worthless; it enables spine surgery, charitable giving, and freedom from the 9-to-5.

## Notable quotes

> "The reason why I'm asking these questions is because when you're doing research and you're getting into back testing, you want to develop the ability to look at what's happening and not just see the end result as this configuration did well. We want to be able to punch holes in it." [14:41]

> "It's the whole package. One of the most common sources of divorce between married couples is money. It's fighting over a insignificant amount of capital and each other's spending habits. And if you ask my wife right now, how much money do we have in total? She will have no idea. And it's because it doesn't matter, right? Because we don't have to talk about it because it doesn't matter." [01:05:44]

## Candidate wiki links

### Concepts
[[sector-rotation]], [[momentum]], [[signal-identification]], [[backtesting]], [[profit-mechanism]], [[regime-dependency]], [[drawdown-management]], [[mean-reversion]], [[position-sizing]], [[friction-costs]], [[bid-ask-spread]], [[rebalancing]], [[hypothesis-testing]], [[data-quality]], [[risk-management]], [[leverage]], [[margin]], [[optionality]], [[transaction-costs]], [[performance-analysis]], [[greek-attribution]], [[tail-risk]], [[capital-preservation]], [[regime-shift]], [[moving-averages]], [[200-day-moving-average]], [[compression]], [[upside-capture]], [[downside-protection]], [[short-selling]], [[mechanical-trading]], [[discretionary-trading]], [[over-optimization]], [[parameter-sweep]], [[heat-map-analysis]], [[cross-validation]], [[spot-check]], [[data-pipeline]], [[tax-loss-harvesting]], [[short-term-vs-long-term-gains]], [[sharpe-ratio]], [[sortino-ratio]], [[max-drawdown]], [[average-winning-month]], [[best-month]], [[worst-month]], [[ego-removal]], [[analytical-discipline]]

### Strategies
[[sector-rotation]], [[momentum]], [[mean-reversion]], [[trend-following]], [[long-only]], [[rebalancing]], [[mechanical-trading]], [[discretionary-trading]]

### Securities
[[spy]], [[xlf]], [[xlp]], [[xlk]], [[xlv]], [[xlu]], [[xly]], [[xlre]], [[xlc]], [[xli]], [[xlb]]

## Regime / context

**Date:** September 3, 2026. This is a live mentoring session in the "Drive-Thru Trading" format, where Eric reviews a student's (CG's) sector-rotation research in real time. The discussion is grounded in recent backtests and emphasizes research methodology over final results.

**Key context:** CG has been exploring a sector-rotation strategy keyed to the SPY 200-day moving average, with preliminary results showing strong downside protection (18% max drawdown vs. SPY's ~50%) but slightly lower upside capture in bullish periods. The session pivots from reviewing the strategy itself to teaching *how to validate and refine research*—a meta-level skill that Eric emphasizes is the true differentiator between profitable and unprofitable traders.

**Technical note:** The stream experienced audio/video lag early on; Eric and CG briefly considered moving to Discord but continued on YouTube. Screen sharing and PDF review were used to walk through backtest results and data validation.
