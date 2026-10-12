---
type: source
title: "Most Online Trading Strategies Are Garbage: Here's What Actually Works"
video_id: oZs0I5TYgeA
url: https://www.youtube.com/watch?v=oZs0I5TYgeA
date: 2026-10-11
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, spx]
concepts: [profit-mechanism, strategy-design, strategy-development, defined-risk, win-rate, delta, implied-volatility, variance-risk-premium, risk-premium, put-skew, positive-drift, trend-following, position-sizing, liquidity, delta-hedging, tail-risk, left-skew, drawdown, clustering, measured-facts, quantitative-analysis, rule-set-definition, edge, structural-effects, mispricings, information-asymmetry, risk-management, portfolio-construction, trend-indicators, regime-dependency]
strategies: [put-credit-spread, short-put-spread, covered-call, short-strangle, long-call-spread, iron-condor, short-straddle, variance-risk-premium, volatility-trading]
saga: null
part: null
confidence: high
---

# Most Online Trading Strategies Are Garbage: Here's What Actually Works

## Summary

This video deconstructs three common online trading strategies to expose the difference between rules that sound reasonable and strategies with genuine profit mechanisms. Eric demonstrates why convenience-based rules and outcome descriptions fail to constitute real strategies, then walks through a live variance-risk-premium put-credit-spread example that illustrates how measured facts, quantitative analysis, and understanding *why* an edge exists separate working strategies from gambling disguised as systems.

## Key takeaways

- **Rules ≠ Strategy** [00:00–02:50]: A strategy requires a profit mechanism—the underlying reason someone would pay you. Rules alone provide certainty but not positive expectancy. The "$5 wide spreads" example has clear rules but no explanation for why it should make money.

- **Fixed-width spreads hide risk** [04:07–05:27]: Selling a $5 wide spread on a $50 stock (10% of price) creates a completely different risk profile than the same $5 width on a $500 stock (1% of price). Delta-based sizing normalizes across price levels; fixed dollar widths do not.

- **Win rate is a lever, not a guarantee** [05:27–06:37]: Higher win rates (achieved by selling further OTM) come with asymmetric payoff ratios—you make less per win but can lose multiples of that on a single loss. This relationship is not linear and requires explicit modeling.

- **Identify the profit mechanism first** [06:37–08:48]: Before building rules, ask: *Why should this make money? Who pays me?* The "long-dated call spreads after pullback" strategy assumes indices recover but never justifies *why*. The "6-month strangles on earnings IV spikes" misses the fact that earnings premium concentrates in the front wall, not 6+ months out.

- **Earnings IV premium is front-wall concentrated** [08:48–11:13]: Selling 6-month strangles to capture earnings volatility is a category error—the variance risk premium around earnings is priced into near-term options, not far-dated ones. You're selling tail risk instead of the actual effect.

- **The Outlier Strategy Process** [12:32–13:50]: (1) Identify a profit mechanism (risk premium, structural flows, mispricings, liquidity functions, information edge). (2) Measure and test signals that target that mechanism. (3) Build rules and structures that fit the measured profile.

- **Live example: SPY/SPX put-credit spread** [15:00–20:09]: Sell 30-delta or 20-delta puts, buy 10-delta or 5-delta puts, ~30 DTE, hold to expiration, size by 50/200-day trend. Profit mechanism: index options are overpriced ~84% of days (funds buy protection regardless of price); puts are skewed expensive; markets drift up. Long put protects against left-tail clustering (9 major drawdown periods since 2009).

- **Measure, don't guess** [20:09–24:07]: Every rule must attach to a quantitative fact, not opinion. Delta-based sizing works across price levels; arbitrary widths do not. Trend sizing cuts losing trades more than winning ones (by design). Returns ~36% on capital at risk, ~83% win rate, ~4.5% average return per trade over 129 instances.

- **Know when the edge breaks** [22:48–24:07]: Monitor whether the profit mechanism still exists (e.g., does variance risk premium flip negative for multiple months?). Data-driven decision-making prevents waiting years to realize a strategy no longer works.

## Notable quotes

> "You can make rules. You can make all sorts of rules, and they give you certainty, but they don't give you positive expectancy." [12:32]

> "The overwhelming majority of earnings premium and the variance risk premium around earnings is around the term with earnings. If you're 6 plus months out, you're not even trading that earnings at all." [10:01]

## Candidate wiki links

**concepts:**
[[profit-mechanism]], [[strategy-design]], [[defined-risk]], [[win-rate]], [[delta]], [[implied-volatility]], [[variance-risk-premium]], [[risk-premium]], [[put-skew]], [[positive-drift]], [[tail-risk]], [[left-skew]], [[position-sizing]], [[trend-following]], [[quantitative-analysis]], [[rule-set-definition]], [[edge]], [[measured-facts]], [[regime-dependency]]

**strategies:**
[[put-credit-spread]], [[short-put-spread]], [[variance-risk-premium]], [[volatility-trading]], [[covered-call]], [[short-strangle]], [[long-call-spread]]

**securities:**
[[spy]], [[spx]]

## Regime / context

Recorded 2026-10-11. This is a foundational education piece on strategy construction applicable across market regimes. The live SPY/SPX put-credit-spread example is presented as a teaching tool to illustrate the Outlier Strategy Process; Eric explicitly disclaims it as personalized financial advice. The variance-risk-premium effect cited (index options overpriced ~84% of days since 2010) is regime-dependent and should be re-validated before deployment in new market conditions.
