---
type: source
title: "End to End Trade Building | Options Trading for Beginners Pt6"
video_id: QQ5DeQdx0yo
url: https://www.youtube.com/watch?v=QQ5DeQdx0yo
date: 2024-07-13
series: beginner-lab
format: [education, live]
experts: [eric]
mentions: [roaring-kitty, nancy-pelosi]
securities: [spy, tsla, wmt, smci, ge, aapl, amd, nvda, sofi, hood]
concepts: [implied-volatility, implied-volatility-percentile, implied-volatility-rank, volatility-surface, margin, leverage, delta, gamma, theta, theta-decay, extrinsic-value, intrinsic-value, expected-move, probability-of-touch, expected-value, risk-management, position-sizing, profit-mechanism, edge, backtesting, signal-testing, technical-analysis, moving-averages, support-and-resistance, price-action, volatility-clustering, volatility-term-structure, moneyness, delta-neutral, portfolio-first, process-over-outcome, trading-plan, trading-psychology, emotional-discipline]
strategies: [long-call, short-put, covered-call, covered-strangle, ratio-call-diagonal, buy-and-hold, momentum, breakout]
saga: none
part: null
confidence: high
---

# End to End Trade Building | Options Trading for Beginners Pt6

## Summary

This session walks through the complete end-to-end process of building a trading strategy from concept to execution. Eric covers how to define a strategy's purpose, isolate profit mechanisms, test candidate structures, codify rule sets, and evaluate trades using expected value and probability analysis. The discussion emphasizes starting simple, testing rigorously, and aligning position structure (strike, expiration, size) with thesis and risk tolerance.

## Key takeaways

### Margin and leverage in options
- **Margin requirement vs. cash securing** [05:34–08:16]: Options positions use margin requirements (a fraction of notional value), not actual borrowing. A short put on SPY at $552 requires ~$7,300 margin but controls $55,200 of exposure. Brokers automatically default to margin; you must notify them to cash-secure.
- **Leverage through options** [09:13–10:49]: Buying a 70-delta call for $1,531 gives exposure equivalent to 70 shares (~$38,570 at strike), demonstrating leverage without borrowing money.

### Assessing option expensiveness
- **Implied volatility percentile (IVP) over IV rank** [18:27–19:54]: Use IVP to determine if options are cheap/expensive relative to a stock's history; IV rank is prone to skew after large moves. High IVP = expensive options.
- **Multi-layer assessment** [23:12–32:31]: (1) Macro: compare IV across products; (2) Relative: check IVP for the underlying; (3) Expiration cycles: find cheaper vol in specific expirations; (4) Micro: compare same-delta options across strikes for skew anomalies.
- **Example workflow** [29:57–32:31]: SMCI showed IV 88% (high), IVP 71% (expensive). Front expiration cheaper than middle cycles; 25-delta puts at 56.8% vol cheaper than 60% average.

### Building a strategy framework
- **Define purpose** [58:23–01:02:02]: Start by specifying what you want to trade (directional up/down, volatility, income, hedging). Simplicity is key—don't build 10 million strategies; start with 2–3 core purposes.
- **Isolate profit mechanism** [01:04:08–01:07:47]: Identify *how* the trade makes money (e.g., momentum premium, post-earnings drift, mean reversion). Use academic research (SSRN) for inspiration; test signals standalone before embedding in strategy.
- **Structure list and testing** [01:11:47–01:14:27]: List candidate structures (long calls, short puts, shares, diagonals). Test simplest first (shares) to validate the profit mechanism, then overlay options. Use backtesting software, Python, or manual on-demand testing.
- **Selection and codification** [01:15:23–01:17:46]: Choose structures that work; codify rule sets (e.g., "buy when 14-day and 7-day MAs slope positive"). Evaluate signal efficacy independently before combining into strategy.

### Expected value and position selection
- **Comparing structures on same thesis** [01:38:05–01:44:31]: For a bullish VRT trade expecting 5% upside: short 30-delta put ($435 credit, $8,250 margin) vs. long 72-delta call ($1,555 cost). On 5% move: put nets $119 (1.4% ROI), call nets $336 (21.6% ROI). On stop at $855: put loses $165, call loses $325. Risk/reward and capital efficiency differ; choose based on thesis and risk tolerance.
- **Theta decay acceleration** [01:39:44–01:43:01]: Theta accelerates sharply within 60 days to expiration. Holding short-dated options requires larger moves to offset decay; longer-dated options have lower theta but require more capital upfront.
- **Probability-weighted returns** [01:59:06–02:00:55]: Calculate expected return using win probability, win amount, loss probability, and loss amount. Example: 78% prob of $95 target, 83% prob of $855 stop—use these to compare strategies quantitatively.

### Adjusting and trailing stops
- **Taking profits early** [02:21:40–02:26:16]: Don't arbitrarily exit at profit target if the trade is still working. Use trailing stops tied to moving average slopes (7-day, 14-day, 22-day) or intraday volatility (e.g., >3% daily drop). Example: TQQQ position stopped on 7-day MA turning negative, then re-entered when MA slope recovered.
- **Theta management in long options** [02:36:45–02:39:44]: Extrinsic value bleeds faster as expiration approaches. If holding long calls, plan to exit or roll before 30 days to expiration to avoid accelerating decay drag.

### Liquidity and volatility expansion
- **Bid-ask widening on big moves** [02:40:08–02:47:27]: During sharp price moves or vol spikes, market makers widen spreads to manage risk. Longer-dated options naturally have wider markets. Example: GME 7-day 80-delta calls bid 244/offered 260; 20-June 79-delta calls bid 1040/offered 1175.
- **Volatility surface trading** [02:28:03–02:29:04]: Relative value opportunities exist across expirations (e.g., 19-July vol anomaly in SMCI). These are tradable but require deeper analysis.

### Technical analysis and position management
- **Multi-timeframe alignment** [02:22:45–02:26:16]: Use moving averages (7, 14, 22, 50, 200 day) and their slopes to confirm trend. Example: TQQQ exited on 7-day MA slope turning negative despite intraday strength; re-entered when slope recovered.
- **Support/resistance for targets** [02:22:24–02:23:05]: Identify congestion zones and prior highs/lows to set profit targets. Example: TQQQ target of $75 based on prior resistance at 68 and 75 handles.

### AMD technical read (dated 2024-07-13)
- **Timeframe-dependent outlook** [02:13:16–02:19:11]: 6-month: downtrend (declining from ~$213); 3-month: uptrend (pop from ~$171); 1-month: consolidation/slight rollover. Earnings on 30 July. Near-term resistance at $186; if broken, potential run to $213–$215.

## Notable quotes

> "The name of the game at the end of the year isn't what is the percentage gain on the portfolio—would you want a 100% gain on a $1 portfolio or a 10% gain on a $100 portfolio? I would absolutely take the lower percent return on the larger principle yielding a larger dollar amount." [01:35:00]

> "What you don't want to do with options is wait too long, especially if you're buying them. You're literally holding a decaying asset." [02:37:32]

> "Delta is going to be one of the primary inputs you need to look at. Gamma is the next input that matters a lot." [01:37:31]

## Candidate wiki links

**concepts:** [[implied-volatility]], [[implied-volatility-percentile]], [[delta]], [[gamma]], [[theta]], [[theta-decay]], [[extrinsic-value]], [[expected-value]], [[probability-of-touch]], [[margin]], [[leverage]], [[profit-mechanism]], [[backtesting]], [[signal-testing]], [[moving-averages]], [[support-and-resistance]], [[technical-analysis]], [[position-sizing]], [[risk-management]], [[trading-plan]], [[process-over-outcome]]

**strategies:** [[long-call]], [[short-put]], [[covered-call]], [[covered-strangle]], [[ratio-call-diagonal]], [[momentum]], [[breakout]]

**securities:** [[spy]], [[tsla]], [[wmt]], [[smci]], [[ge]], [[amd]], [[nvda]], [[sofi]], [[hood]]

**people:** [[roaring-kitty]] (mentioned), [[nancy-pelosi]] (mentioned humorously)

## Regime / context

**Date:** 2024-07-13 (mid-July, post-earnings season, tech consolidation phase)

This is Part 6 of the "Options Trading for Beginners" series. The session is a comprehensive live workshop on strategy construction, not a market update. Timestamps reflect approximate ASR positions; numeric examples (prices, Greeks, probabilities) are illustrative and should not be treated as precise historical data. The AMD technical analysis is specific to the date of recording; longer-term uptrend remains intact despite near-term consolidation.
