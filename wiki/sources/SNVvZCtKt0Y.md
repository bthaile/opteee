---
type: source
title: "Andrew Mack on Retail Options Trading | The Outlier Podcast"
video_id: SNVvZCtKt0Y
url: https://www.youtube.com/watch?v=SNVvZCtKt0Y
date: 2025-11-26
series: outlier-podcast
format: [interview, education]
experts: [andrew-mack]
mentions: []
securities: [spx, qqq, tqqq]
concepts: [market-on-close, zero-dte, implied-volatility, volatility-risk-premium, volatility-clustering, mean-reversion, volatility-term-structure, bid-ask-spread, delta, straddle-price, realized-volatility, expected-move, edge, backtesting, confirmation-bias, disposition-effect, social-consensus-bias, market-efficiency, seasonality, gap-risk, process-over-outcome, risk-management, position-sizing, trading-psychology, emotional-discipline, model-building, quantitative-research]
strategies: [short-volatility, long-volatility, short-straddle, gamma-scalping, momentum, trend-following]
saga: null
part: null
confidence: high
---

# Andrew Mack on Retail Options Trading | The Outlier Podcast

## Summary

Andrew Mack returns to discuss the evolution of retail options trading in 2025, focusing on the decline of market-on-close (MOC) effects, the mechanics of volatility trading, and the critical balance between research and execution. The conversation emphasizes observation-driven edge discovery, behavioral bias management, and the importance of understanding market mechanics before deploying capital.

## Key takeaways

### Dated market read (2025-11-26)

- **MOC effect fade**: The market-on-close rebalancing opportunity that produced 5–12× returns on zero-DTE options has largely disappeared over the past six months; occasional bursts now require additional catalysts (month-end, all-time highs) rather than pure mechanical rebalancing [01:02–02:22]
- **Long volatility performance**: Long vol has worked well recently as the VIX elevated above 20; when straddle implied break-evens break, markets trend toward the second standard deviation rather than reverting [02:22–03:36]
- **Volatility clustering vs. mean reversion**: Volatility clusters in the short term (days to weeks) even though it mean-reverts over longer horizons; selling vol at VIX 22–27 is riskier than at VIX 14–16 due to clustering dynamics [31:58–32:58]

### Evergreen mechanics

- **Observation-first edge discovery**: The best trading effects are found by noticing something genuinely weird in real-time, then investigating with data—not by mining data hoping to find an effect [04:51–05:55]
- **Spread widening as a signal**: Market makers widen bid-ask spreads to discourage trading; when realized moves exceed the widened spread, it signals a potential opportunity worth tracking [05:55–07:02]
- **Contextual validation**: After noticing an effect, analyze whether spreads were wide enough to negate the opportunity; brainstorm contextual clues (day of week, economic calendar, catalyst type) that might predict recurrence [07:57–09:05]
- **Risk-premium vs. transient effects**: Risk-premium effects (volatility selling, equity risk premium) can be analyzed extensively because they persist; transient effects (news catalysts, flow events) require faster execution with incomplete information [10:02–12:19]
- **Incomplete information is acceptable**: Retail traders must operate with imperfect information; waiting for perfect data before acting on transient effects guarantees missing them [12:19–13:35]
- **Baseline observation builds intuition**: Watch a single zero-DTE contract's bid-ask spread for hours; notice the normal range (~$2), then flag when it widens to $4—this trains pattern recognition without requiring formal analysis [19:01–21:25]
- **Repeatability as validation**: An effect observed once is noise; look for it to occur multiple times across different contexts before committing capital [19:01–20:17]
- **Understanding market mechanics is prerequisite**: Know how the VIX is calculated, its relationship to the options chain, and how dealer gamma affects price action before searching for edges; this prevents false positives [15:55–16:51]
- **Relaxed observation beats motivated search**: Avoid pre-committing to finding an effect in a specific place (e.g., "I will find something in verticals today"); instead, observe broadly without agenda and let patterns emerge naturally [16:51–18:02]
- **Volatility level context matters**: VIX at 14–16 favors short-vol traders (premium is fair, moves are muted, reversion likely); VIX at 25+ favors long-vol traders (premium is overpriced, clustering likely, tail risk real) [28:27–30:52]
- **Seasonality patterns exist but require caution**: July tends to have low realized volatility (good for short vol); September–November see volatility pickup (harder for short vol); Thursday gap fills occur ~80% of the time but lack clear theoretical explanation [01:03:31–01:05:45]
- **Model building requires an effect first**: Don't build models hoping to find an effect; identify an effect (e.g., "FOMC fades the first move, reverses in the second half"), then use a model to parameterize risk and win rate [39:19–40:17]
- **Avoid over-modeling**: A rolling ridge regression on 25 risk-on/risk-off variables performed only marginally better than a simple 200-day moving average; most randomly-built models are beaten by existing solutions [37:58–39:19]
- **AI as a regurgitation tool**: Use LLMs to brainstorm model types and related approaches, not to find the "magic solution"; ask "what other ways could I simulate this effect?" rather than "what model should I use?" [43:50–44:56]

### Behavioral and psychological

- **P&L-driven trading is lethal**: Allowing current screen color (red/green) to influence the next trade destroys payoff ratios; winners become risk-averse (taking profits too early), losers become risk-seeking (holding bad trades) [55:38–57:54]
- **Social consensus bias is the most dangerous**: Obsessing over Twitter, CNBC, and consensus narratives introduces second-guessing and prevents focus on your specific effect; tune out noise and trade what is happening, not what you think should happen [46:05–49:57]
- **Two phases of trader development**: Early phase: absorb all ideas to map the puzzle corners; mature phase: exclude noise and focus on your identified effects [52:25–53:29]
- **Contextual factors explain losing streaks**: If you start shorting vol at VIX 26–27 and lose immediately, check whether you're violating your own rules (e.g., you should only short vol at VIX 14–16); losing doesn't mean the edge is gone, it may mean context is wrong [01:00:09–01:02:21]
- **Stress tolerance from other domains transfers**: Combat sports, military service, and high-stakes activities build resilience that makes trading losses feel manageable by comparison; trading is not uniquely stressful [01:09:14–01:10:33]

## Notable quotes

> "The best effects start by noticing something weird as you just alluded to rather than diving into the data and hoping to find the effect that way." [04:51]

> "You're going to have to operate with imperfect and incomplete information. And that's true of a lot of things in life that have, you know, positive skew payoff profiles." [12:19]

> "Trading is not a uniquely stressful job." [01:09:14]

## Candidate wiki links

### Concepts
[[market-on-close]], [[zero-dte]], [[implied-volatility]], [[volatility-risk-premium]], [[volatility-clustering]], [[mean-reversion]], [[volatility-term-structure]], [[bid-ask-spread]], [[delta]], [[straddle-price]], [[realized-volatility]], [[expected-move]], [[edge]], [[backtesting]], [[confirmation-bias]], [[disposition-effect]], [[social-consensus-bias]], [[market-efficiency]], [[process-over-outcome]], [[risk-management]], [[position-sizing]], [[trading-psychology]], [[emotional-discipline]], [[quantitative-research]], [[seasonality]]

### Strategies
[[short-volatility]], [[long-volatility]], [[short-straddle]], [[gamma-scalping]], [[momentum]], [[trend-following]]

### Securities
[[spx]], [[qqq]], [[tqqq]]

### People
[[eric]]

## Regime / context

Recorded late November 2025. Market-on-close effects have faded significantly from their peak in 2024–early 2025; volatility clustering and mean-reversion dynamics are discussed in the context of elevated VIX (above 20) and recent realized moves. Seasonality observations (July calm, fall volatility pickup) reflect historical patterns but are treated with appropriate skepticism. Andrew Mack is preparing for a heavyweight MMA fight scheduled for fall 2026.
