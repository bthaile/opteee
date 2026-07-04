---
type: source
title: "Evaluating a Trading Strategy | Options Trading Basics"
video_id: B48KOikbTs8
url: https://www.youtube.com/watch?v=B48KOikbTs8
date: 2025-06-21
series: beginner-lab
format: [education, live]
experts: [eric]
mentions: []
securities: [spy, russell-2000]
concepts: [profit-mechanism, process-over-outcome, regime-impact, path-dependency, small-sample-bias, goldilocks-analysis, strategy-hopping, win-rate-vs-profitability, expected-value, standard-deviation-channels, downside-deviation, sharpe-ratio, sortino-ratio, coefficient-variance, sample-size, law-of-large-numbers, max-drawdown, trading-log, trading-plan, backtesting, paper-trading, market-regimes, volatility-clustering, emotional-discipline]
strategies: [long-call, short-strangle, long-straddle, covered-call, iron-condor, zero-dte]
saga: null
part: null
confidence: high
---

# Evaluating a Trading Strategy | Options Trading Basics

## Summary

This session walks through a systematic framework for evaluating trading strategies, emphasizing that most retail traders fail because they lack a defined process for strategy review. The core lesson: you cannot evaluate a strategy without first understanding the profit mechanism you're trying to monetize, and you must account for regime, path dependency, and sample size before drawing conclusions from backtest or live results.

## Key takeaways

- **Start with the profit mechanism, not the strategy** [15:38] — Before testing or evaluating, you must have a clear idea of what market inefficiency or edge you're trying to exploit. Without this, you're just clicking buttons and getting lucky.

- **Regime matters enormously** [21:31–24:18] — A long-call strategy that crushes in 2020 (stimulus, low rates, uptrend) will fail in 2022 (bear market). Analyze regimes across economic, geopolitical, sector, and portfolio levels. Always set the backdrop first.

- **Path dependency will catch everyone** [28:58–32:27] — A strategy can show stellar returns over 6 months or even 6 years by pure luck, then blow up. The market can mask poor edge for extended periods. This is why consistent long-term traders are rare.

- **Small sample size is meaningless** [34:25–35:05] — 18 months, 17 months, even 2 weeks of results tell you almost nothing. Use the law of large numbers and central limit theorem: you need enough trades for the line of best fit to represent actual strategy performance, not noise.

- **Goldilocks analysis: your brain will lie to you** [37:33–40:29] — When backtesting, toggling conditional filters on/off can swing returns from 15% to 4%. Your brain wants to see success so badly it will skip red flags. Be ruthlessly objective; turn off the toggles and look at the real numbers.

- **Win rate is a trap** [41:21–44:17] — Retail traders obsess over high win rates (16/17 months, 18-month streak). But a 47% win-rate strategy can be highly profitable if losses are small and wins are large. Focus on expected value, not win percentage.

- **Build a minimal viable product (MVP) trading log** [45:08–51:31] — Track: trade count, win/loss %, total P&L, average P&L (overall, wins, losses), extremes (max/min), standard deviation, downside deviation, max drawdown, Sharpe ratio, Sortino ratio, coefficient of variance, and required trade count for 90% confidence.

- **Standard deviation vs. coefficient of variance** [16:07–20:40] — Standard deviation shows absolute dispersion from the mean; coefficient of variance shows relative variability as a percentage of the mean. Both matter; they answer different questions.

- **Use moving averages on required trade count** [57:01–58:05] — If the number of required trades is tightening over time, your strategy is becoming more consistent. If it's expanding, performance is degrading. This trend is more useful than the absolute number.

- **Iterate on trade plan changes systematically** [13:30–14:42] — When you change an exit rule (e.g., from hold-to-expiry to 50% loss), track the change in your log with a date. Then re-run your metrics to see how win rate, average P&L, and other stats shift. This reveals whether the change helped or hurt.

- **Detect regime and path shifts with visuals and date-bound analysis** [06:44–09:10] — Create graphs and date-filtered views of your metrics (population vs. sample). Screenshot or snapshot your log periodically so you can see how performance changes as market conditions shift.

- **Strategy hopping is nefarious** [14:10–14:36] — Most people jump between strategies because building one takes time and effort. This prevents you from ever accumulating enough data to know if a strategy actually works.

## Notable quotes

> "If you don't have this [a defined idea of the profit mechanism], then you can't evaluate what you're doing. And again, most people, my guess, like this person, they don't have this. So they're just starting to click buttons." [15:38]

> "Path will catch everyone. Literally everyone. If you stay in the markets, path will catch you." [31:57]

> "The overwhelming majority of options traders, they disgustingly exhibit a gross overemphasis on high win rate." [41:21]

## Candidate wiki links

**concepts:**
[[profit-mechanism]], [[process-over-outcome]], [[regime-impact]], [[path-dependency]], [[small-sample-bias]], [[goldilocks-analysis]], [[strategy-hopping]], [[win-rate-vs-profitability]], [[expected-value]], [[standard-deviation-channels]], [[downside-deviation]], [[sharpe-ratio]], [[sortino-ratio]], [[coefficient-variance]], [[sample-size]], [[law-of-large-numbers]], [[max-drawdown]], [[trading-log]], [[trading-plan]], [[backtesting]], [[paper-trading]], [[market-regimes]], [[emotional-discipline]]

**strategies:**
[[long-call]], [[short-strangle]], [[long-straddle]], [[covered-call]], [[iron-condor]], [[zero-dte]]

**securities:**
[[spy]], [[russell-2000]]

**people:**
[[eric]]

## Regime / context

Recorded 2025-06-21 (live stream). The discussion references 2020 (stimulus, low rates, bull market) vs. 2025 (higher rates, Trump administration, tariff uncertainty) as regime contrasts. This is a foundational education session on strategy evaluation methodology; the principles are evergreen, though specific market examples are dated to mid-2025.
