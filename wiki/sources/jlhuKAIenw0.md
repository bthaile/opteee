---
type: source
title: "Andrew Mack on How to Build an Options Trading Strategy | The Outlier Podcast"
video_id: jlhuKAIenw0
url: https://www.youtube.com/watch?v=jlhuKAIenw0
date: 2026-03-18
series: outlier-podcast
format: [education, interview]
experts: []
mentions: [euan-sinclair, nassim-taleb]
securities: [spy, vix]
concepts: [implied-volatility, volatility-term-structure, delta, gamma, theta, vega, greeks, straddle-price, zero-dte, market-effect, profit-mechanism, edge, options-instrument-selection, trading-psychology, dunning-krueger-effect, echo-chambers, contrarian-sentiment, mean-reversion, order-flow, price-impact, realized-volatility, volatility-clustering, kelly-criterion, sortino-ratio, sharpe-ratio, average-favorable-excursion, mean-adverse-excursion, position-sizing, risk-management, backtesting, monte-carlo-simulation, volatility-modeling, garch-models, volatility-forecasting, technical-analysis, order-book, market-maker, liquidity-cycle, bid-ask-spread, momentum, trend-following, breakout, scalping, paper-trading, trading-log, process-over-outcome, emotional-discipline, trust-your-plan, win-rate-vs-profitability]
strategies: [long-call, short-premium, short-straddle, zero-dte, scalping, momentum, trend-following, breakout, mean-reversion, order-book-sweep]
saga: none
part: null
confidence: high
---

# Andrew Mack on How to Build an Options Trading Strategy | The Outlier Podcast

## Summary

Andrew Mack discusses the foundational principles for building a robust options trading strategy, emphasizing that traders should identify a market effect first, then select the instrument (options, futures, or delta-one) that best captures it. He covers volatility modeling, tenor selection, psychological discipline, and the critical distinction between learning theory and generating profitable edge—arguing that most retail traders approach the problem backwards by choosing an instrument before understanding the underlying market effect they want to exploit.

## Key takeaways

### Evergreen mechanics

- **Instrument selection is backwards for most traders** [02:19–05:22]: Start with a market effect and profit mechanism, then choose the best instrument to capture it. Don't pick options first and force a strategy around them. As Euan Sinclair says, "You're a trader, not an options trader."

- **False dichotomy of premium-selling vs. directional trading** [02:19–03:31]: Options offer nuanced positioning beyond the binary choice of "theta gang" or "directional." Avoid tribal thinking that locks you into one approach for life.

- **VIX clustering and regime awareness** [06:44–11:22]: When VIX is elevated (~25–26), ATM IV and straddle prices rise. The most interesting moves occur as VIX crosses 19 on the way up; once clustering occurs and volatility becomes expected, range contracts despite high IV. High VIX doesn't guarantee profitable directional plays—monitor whether conditions favor straddle sellers or buyers.

- **Zero-DTE vs. multi-day tenor selection** [11:49–13:13]: Use zero-DTE when you believe the range will exceed current pricing; use multi-day (1–2 DTE) for specific gap-fill plays. Zero-DTE scalping only works in elevated VIX; in low-VIX environments, it's a fast way to blow an account.

- **Volatility modeling doesn't require superiority** [13:35–16:51]: You don't need a better model than hedge funds—just one that keeps pace with market consensus. Track daily ATM IV and straddle prices against your estimate; record whether each is above/below your model. Over time, you'll identify which conditions favor which strategies, even with a basic GARCH model.

- **Theory vs. money-making are different activities** [17:44–21:35]: Learning Greeks, volatility surfaces, and distributions is essential background, but chasing tiny Greek mismatches or model deviations is not where money is made. The sausage is made from simple operations: buy at 10, sell at 12, repeat while managing risk. Avoid the trap of perfectionism in modeling.

- **Dunning-Kruger effect and echo chambers** [26:30–35:21]: Early learning creates false confidence. Actively seek opposing viewpoints; if everyone agrees with you, that's a bad sign. Maintain a "white belt" mentality—always learning, never certain. Tribalism (political, market, sports) blinds traders to profitable contrarian ideas.

- **Psychology-first strategy selection** [38:49–42:45]: Stratify strategies by skew and win rate. Low-win-rate, high-payoff strategies (trend, breakout, ~25–35% win rate) suit traders comfortable holding losers. High-win-rate strategies (scalping, mean reversion, ~60–80% win rate) suit those needing daily income feel. Choose based on your psychological makeup, not abstract superiority.

- **Go deep on one thing, not shallow on five** [36:41–38:18]: Become deadly at one skill (e.g., orderbook scalping) and apply it across instruments and markets. Shallow competence across five strategies leaves you confused about what to focus on daily and dilutes edge.

- **Tenor selection and competitive advantage** [54:12–55:48]: Avoid 30–90 day options where large operators concentrate capital. Look for extremes: very short-dated (zero-DTE, 1 DTE) or very long-dated (LEAPS). Wider spreads in less-liquid tenors can signal fewer sharp competitors and better opportunity.

- **Liquidity is not the only metric** [56:33–59:25]: Tight spreads indicate competitive markets; wider spreads may indicate less competition despite lower liquidity. Watch for spread widening in short-dated options—it often precedes large order flow. Balance liquidity against competitive intensity.

- **Optimization metrics scale with account size** [01:02:33–01:03:30]: For small accounts, optimize for Sortino ratio and Kelly criterion, not Sharpe ratio. Sortino focuses on downside volatility; Kelly maximizes long-term growth. Sharpe becomes relevant as accounts grow larger.

- **Average Favorable Excursion (AFE) for zero-DTE directional trades** [01:05:18–01:06:02]: Optimize for how far moves go in your favor vs. against you. Extract as much as possible without holding so long that mean reversion takes effect. Monitor AFE and Mean Adverse Excursion (MAE) ratios.

- **Hammer the fast ball while it works** [01:07:10–01:08:32]: If a strategy is working, exploit it intensively. All effects have seasons; momentum, mean reversion, and volatility selling all cycle. When performance slows, monitor rolling Sharpe ratios across strategies and timeframes to identify regime shifts.

- **Monitor strategy performance cycles** [01:08:54–01:10:43]: Track rolling 1-month, 3-month, 6-month, 12-month Sharpe ratios for strategies. Notice patterns: "short premium cleaned up the last week" or "we broke the straddle three times in four days." The market adjusts to strategy performance; watch these cycles to anticipate what works next.

- **Start with well-studied effects** [01:11:25–01:15:36]: Begin with momentum or orderbook sweeps—effects documented on SSRN with real academic backing. Momentum is universally understood; orderbook sweeps are observable and teachable. Avoid esoteric, unproven effects when you lack validation skills. Paper-trade orderbook sweeps for 100+ reps to learn more than reading 100 books.

- **Realized volatility is price impact** [01:13:02–01:15:14]: Volatility is not a pure statistical artifact—it's the result of people buying and selling. Price impact drives realized volatility. Understanding the orderbook, order flow, and how sweeps create price impact is the essence of market mechanics.

## Notable quotes

> "You're not an options trader, you're a trader. Options happen to be an instrument that you can trade." — Andrew Mack, paraphrasing Euan Sinclair [04:43]

> "If you want to make money, that's some of the dumbest stuff you could possibly spend your time on" — referring to chasing tiny Greek mismatches [18:25]

> "If everybody agrees with you, that is usually a pretty bad sign." [29:01]

## Candidate wiki links

**concepts:** [[implied-volatility]], [[volatility-term-structure]], [[greeks]], [[delta]], [[gamma]], [[theta]], [[vega]], [[straddle-price]], [[zero-dte]], [[market-effect]], [[profit-mechanism]], [[edge]], [[trading-psychology]], [[dunning-krueger-effect]], [[echo-chambers]], [[contrarian-sentiment]], [[mean-reversion]], [[order-flow]], [[price-impact]], [[realized-volatility]], [[volatility-clustering]], [[kelly-criterion]], [[sortino-ratio]], [[sharpe-ratio]], [[average-favorable-excursion]], [[position-sizing]], [[risk-management]], [[backtesting]], [[volatility-modeling]], [[garch-models]], [[volatility-forecasting]], [[order-book]], [[liquidity-cycle]], [[bid-ask-spread]], [[momentum]], [[trend-following]], [[breakout]], [[scalping]], [[paper-trading]], [[process-over-outcome]], [[emotional-discipline]], [[trust-your-plan]], [[win-rate-vs-profitability]]

**strategies:** [[long-call]], [[short-premium]], [[short-straddle]], [[zero-dte]], [[scalping]], [[momentum]], [[trend-following]], [[breakout]], [[mean-reversion]]

**securities:** [[spy]], [[vix]]

**people:** [[euan-sinclair]]

## Regime / context

Recorded 2026-03-18. VIX was elevated (~25–26) at time of recording, with clustering above 20 since early March. Discussion reflects market conditions of elevated volatility and muted range despite high IV. Principles are evergreen; specific VIX levels and market snapshots are dated.
