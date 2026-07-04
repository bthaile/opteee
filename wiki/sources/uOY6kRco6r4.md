---
type: source
title: "Euan Sinclair on How to Build Options Strategies That Work | The Outlier Podcast"
video_id: uOY6kRco6r4
url: https://www.youtube.com/watch?v=uOY6kRco6r4
date: 2025-03-30
series: outlier-podcast
format: [interview, education]
experts: [euan-sinclair]
mentions: [andrew-mack, warren-buffett, nassim-taleb]
securities: [spx, qqq, iwm, vix]
concepts: [edge, volatility-risk-premium, implied-volatility, mean-reversion, overfitting, backtesting, kelly-criterion, position-sizing, risk-management, market-efficiency, process-over-outcome, trading-psychology, trading-log, sample-size, confirmation-bias, volatility-forecasting, unusual-options-activity, order-flow]
strategies: [short-straddle, short-premium, zero-dte, overnight-risk-premium]
saga: null
part: null
confidence: high
---

# Euan Sinclair on How to Build Options Strategies That Work | The Outlier Podcast

## Summary

Euan Sinclair discusses the foundations of building profitable options strategies, emphasizing that edge discovery precedes all other considerations—including risk management, position sizing, and mechanics. He argues that most retail traders over-engineer their approaches, add unnecessary parameters based on small samples, and confuse descriptive market observations with predictive trading signals. The conversation covers backtesting discipline, the evolution of his thinking on volatility forecasting, and practical guidance for part-time traders.

## Key takeaways

### Dated market read (2024)

- **August 5, 2024 VIX dislocation** [01:07–02:03]: S&P VIX exceeded NASDAQ VIX (occurs ~2.5–3% of the time historically). This abnormal relationship, not the absolute VIX spike, signaled a mean-reversion opportunity. The key insight: become so familiar with normal market behavior that anomalies "punch you in the face."

### Evergreen mechanics

- **Start with edge, then ask "Can I do this?"** [55:18–56:26]: Identify trades with statistical edge first; only then filter by capital, attention, and psychological fit. Do not reverse-engineer a trade to match your lifestyle constraints.

- **Avoid overfitting via small-sample learning** [08:06–09:13]: A 1,000-observation backtest with zero free parameters is superior to a 20-observation live-trading "improvement" with three new rules. Adding parameters based on one month of trading destroys statistical robustness; you need ~1,000 observations per parameter to maintain evidence strength.

- **Handicap augmented backtests** [11:57–13:16]: If you observe a pattern (e.g., "enter 30 minutes after open") and want to test it, re-run the backtest but expect a lower Sharpe ratio (e.g., 2.0 instead of 3.0) to account for look-ahead bias. The reason must precede the test, not follow it.

- **Distinguish descriptive from predictive** [05:32–06:46]: Knowing *why* the VIX spiked (liquidation event, etc.) is interesting but not actionable. Knowing *that* a relationship is abnormal (S&P VIX > NASDAQ VIX) is actionable because it implies mean reversion, independent of future VIX direction.

- **Simplify over time, but implicitly** [33:33–35:54]: Experienced traders appear to simplify because complex knowledge becomes implicit. Hedging, for example, remains important but drops in priority as you recognize what truly drives P&L.

- **Volatility forecasting has diminishing returns** [30:46–32:15]: Sophisticated time-series models (GARCH, etc.) are largely priced in. When distortions are extreme (VIX at 30 vs. model forecast of 20), the specific model matters little; when distortions are small (forecast 20.1 vs. actual 21), no trade occurs either way. Scanners and data access have democratized edge-finding; focus on big dislocations instead.

- **Low-touch strategies for part-time traders** [52:55–54:06]: Overnight trades (close-to-open), earnings plays (buy 2 weeks prior, hold), and weekend trades require 15–20 minutes and benefit from *not* monitoring intraday. Inability to adjust during market closure prevents over-complication.

- **Kelly criterion and account structure** [43:08–46:55]: Full Kelly can reduce a $1,000 account to $0.01 before recovery. Split your account into a safe portion (e.g., 90%) and a risky portion (10%), apply full Kelly to the risky portion, and rebalance. This sets a floor without fractional Kelly's complexity.

- **Realistic return expectations** [20:22–21:36]: 1% per week implies Jim Simons–level skill. A 25 golf handicap in one year is achievable; PGA-level play is not. Expect 2–3% annual outperformance over the S&P if you're exceptional; Warren Buffett achieves this with a massive account.

- **Avoid timing the volatility risk premium** [22:43–24:01]: If you can time volatility or equity risk premiums, you're skilled enough to apply those methods to higher-predictability markets (e.g., yield-curve mean reversion). Start with easier edges; there are no bonus points for solving the hardest problem first.

- **Keep a trading log as meditation, not optimization** [28:29–29:38]: Record strategy P&L, trade count, fill quality, and average fill before market open and after close. This ritual surfaces subconscious insights and prevents reactive over-fitting. The log is a thinking tool, not a data-mining tool.

- **Recognize when knowledge hurts** [06:46–08:06]: NFL analysts with Hall of Fame credentials cannot gamble profitably despite deep football knowledge. Similarly, knowing *why* a stock moved on earnings does not predict future moves. Discretionary overlays based on narrative reasoning often destroy edge.

- **Mentor luck and implicit knowledge** [25:10–27:25]: Finding a mentor who recognizes your strengths is largely luck. Your boss may see your edge before you do. Avoid shallow networking; genuine mentorship requires mutual respect and fit.

- **Relationship-based mean reversion trades** [15:32–16:48]: Monitor ratios between index volatilities (VIX vs. VIX, Dow vs. S&P), skew indices, and yield-curve relationships. When these strong relationships break, they revert. This is more actionable than single-signal forecasting.

- **Options flow has limited predictive power** [57:38–59:09]: Volume-weighted open interest by strike (call walls, hedging flows) does show minor predictive power, especially near expiration. However, it is a small effect, often overstated by retail traders. Professional market makers already price this in; do not assume you know better than Susquehanna.

## Notable quotes

> "You should become so familiar with the normal situation that abnormal situation like leaps out and punches you in the face." [03:15]

> "The point is finding that standout situation. Um, that's where good trades come from. People get too, especially with options, they get too wound up in the mechanics and the Greeks and all this stuff." [04:20]

> "If you can do all that do it on something else like predict stuff where the predictability is higher like I don't know future spreads right really strongly mean reverting." [23:16]

## Candidate wiki links

**concepts:** [[edge]], [[volatility-risk-premium]], [[implied-volatility]], [[mean-reversion]], [[overfitting]], [[backtesting]], [[kelly-criterion]], [[position-sizing]], [[risk-management]], [[market-efficiency]], [[process-over-outcome]], [[trading-psychology]], [[trading-log]], [[sample-size]], [[confirmation-bias]], [[volatility-forecasting]], [[unusual-options-activity]], [[order-flow]], [[delta-neutral]], [[gamma]], [[theta]], [[vega]], [[volatility-term-structure]], [[skew]]

**strategies:** [[short-straddle]], [[short-premium]], [[zero-dte]], [[overnight-risk-premium]], [[mean-reversion]]

**securities:** [[spx]], [[qqq]], [[iwm]], [[vix]]

**people:** [[euan-sinclair]], [[andrew-mack]], [[warren-buffett]]

## Regime / context

Recorded March 30, 2025. Sinclair reflects on 2024 market events (August 5 VIX dislocation) and discusses his evolving views on volatility forecasting, hedging, and retail options trading growth. His latest book, *Retail Options Trading* (co-authored with Andrew Mack), was published in late 2024 and targets retail traders; earlier works (*Options as a Strategic Investment*, *Positional Options Trading*) addressed market makers and quantitative traders respectively. The conversation emphasizes timeless principles (edge discovery, sample-size discipline, simplification through experience) applicable across market regimes.
