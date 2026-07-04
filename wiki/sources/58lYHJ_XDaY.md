---
type: source
title: "Why I HATE Vertical Spreads and When to ACTUALLY Use Them"
video_id: 58lYHJ_XDaY
url: https://www.youtube.com/watch?v=58lYHJ_XDaY
date: 2026-05-20
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [aapl]
concepts: [profit-mechanism, implied-volatility-percentile, vega, delta, gamma, theta, expected-return, risk-defined, return-on-invested-capital, expected-move, volatility-skew, risk-management, position-sizing, trading-psychology]
strategies: [long-call, short-call, short-put, long-put, short-straddle, iron-condor, short-strangle, vertical-spreads]
saga: null
part: null
confidence: high
---

# Why I HATE Vertical Spreads and When to ACTUALLY Use Them

## Summary

Vertical spreads are structurally neutral on Greeks and capital-efficient, but retail traders commonly misuse them by starting with capital constraints rather than profit mechanisms. The host argues that while verticals have legitimate use cases—risk mitigation around earnings, targeting specific distribution zones, and reducing shakeouts—they should never be chosen simply because a trader cannot afford naked options. High probability of profit, defined risk, and attractive risk-to-reward ratios are market-competitive features that do not guarantee profitability.

## Key takeaways

- **Vertical spreads flatten Greeks** [12:28]: Long call spreads and short put spreads are structurally equivalent; both create defined profit and loss zones by offsetting delta, gamma, vega, and theta across the strikes.

- **Capital constraint is not a valid reason** [02:47]: The market is indifferent to account size. Starting with "I can't afford a naked option, so I'll use a vertical" inverts the proper decision tree: identify the profit mechanism first, then choose structures that attack it.

- **High IV percentile + vertical = no vol exposure** [04:07]: A trader seeing 86% IV percentile and selling a put spread to capture vol contraction actually hedges away vega (e.g., short 17¢ vega, long 16¢ vega = 1¢ residual). The structure defeats the stated thesis.

- **High probability of profit ≠ profitable** [05:31]: A simulated system with 90% win rate (avg win $20, avg loss $200) loses money overall. The market prices in high-probability outcomes; there is no free edge.

- **Risk-defined ≠ safe** [06:22]: Defined risk prevents catastrophic single-trade blowups but enables "death by a thousand paper cuts"—slow capital erosion if the underlying profit mechanism is negative expected value.

- **Return on invested capital can mislead** [08:43]: A $1 profit on $0.01 risk = 10,000% ROIC, but it is still $1. Optimizing for efficiency over absolute profit can lead to suboptimal decisions.

- **Legitimate use case: earnings risk mitigation** [10:00]: When trading short vol through earnings (e.g., AAOI expected move 16%, actual 57%), an iron condor caps loss at max spread width while a naked short straddle loses multiples of credit received.

- **Legitimate use case: targeting distribution zones** [13:21]: If conviction is that a stock will rally to a specific level (e.g., 190) but not far beyond, a vertical isolates that zone and eliminates unwanted Greek exposure (vol, theta, gamma).

- **Legitimate use case: reducing shakeouts** [14:21]: A vertical can keep a trader in a position through normal intraday reversals that would trigger a hard stop on a naked short, allowing the trade to resolve per plan.

- **Legitimate use case: skew targeting** [14:40]: When call spreads are cheap relative to put spreads due to skew (e.g., GameStop), verticals allow tactical entry into that relative value.

- **Operational friction matters** [11:35]: Additional legs increase fill difficulty, slippage, and execution risk. Over-hedging risk can erode returns more than the risk reduction is worth.

## Notable quotes

> "The market doesn't care if you have a small account, it is completely indifferent to you."

> "Risk defined equals safe. It's literally the same thing I just showed you... it's kind of like death by a thousand paper cuts."

> "I don't actually hate verticals. I really dislike how misused, misunderstood, and misapplied they are."

## Candidate wiki links

**concepts:** [[profit-mechanism]], [[implied-volatility-percentile]], [[vega]], [[delta]], [[gamma]], [[theta]], [[expected-return]], [[risk-defined]], [[return-on-invested-capital]], [[expected-move]], [[volatility-skew]], [[risk-management]], [[position-sizing]], [[trading-psychology]]

**strategies:** [[long-call]], [[short-call]], [[short-put]], [[long-put]], [[short-straddle]], [[iron-condor]], [[short-strangle]]

**securities:** [[aapl]]

## Regime / context

Recorded 2026-05-20. The AAOI earnings example (26 Feb, expected move 16%, realized 57%) and GameStop skew reference anchor the discussion to recent market conditions, but the core critique of vertical-spread misuse is evergreen. This is a foundational education piece on structure selection and the primacy of profit mechanism over capital efficiency.
