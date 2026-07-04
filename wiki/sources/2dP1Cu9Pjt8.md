---
type: source
title: "The Myth of the 'Best' Options Strategy (Here's What Actually Works)"
video_id: 2dP1Cu9Pjt8
url: https://www.youtube.com/watch?v=2dP1Cu9Pjt8
date: 2025-05-18
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [nvda, spx]
concepts: [profit-mechanism, market-regimes, convexity, theta-decay, gamma, win-rate-vs-profitability, risk-management, expected-value, outlier-strategy-process, overfitting, position-sizing]
strategies: [short-put, long-call, directional-breakout]
saga: null
part: null
confidence: high
---

# The Myth of the 'Best' Options Strategy (Here's What Actually Works)

## Summary

There is no universally "best" options strategy—the concept itself is a trap. Instead, traders should identify specific profit mechanisms and market conditions, then select or build strategies optimized for those contexts. The video walks through seven traits of an ideal strategy (multi-regime adaptability, reliability, favorable win/loss ratios, defined risk, theta benefit, gamma benefit, undefined upside) and demonstrates why no single strategy satisfies all criteria simultaneously. The solution is the [[outlier-strategy-process]]: isolate the profit mechanism, then construct a relative best strategy for that specific edge.

## Key takeaways

- **No universal best strategy exists** [04:15] — Seeking a single strategy that always works optimally is lazy thinking; the market doesn't reward one-size-fits-all approaches.

- **Seven traits of an ideal strategy** [00:00–04:15]:
  - Trades multiple [[market-regimes]] (bullish, bearish, sideways)
  - Produces consistent, positively expectant results
  - Larger winners relative to losers (convexity)
  - Undefined profit potential (uncapped upside)
  - Capped losses (defined risk)
  - Benefits from [[theta-decay]]
  - Benefits from [[gamma]]

- **High win rate ≠ high profitability** [01:27] — Selling far out-of-the-money puts (e.g., 2-delta) wins 95%+ of the time but collects small premiums; one rare large move wipes out dozens of winners. This is "selling the tails."

- **Undefined losses are catastrophic** [02:50–04:15] — A 5% decline in [[spx]] can turn a $90 premium win into a $7,600 loss; the math shows how quickly one loser erases 80+ winners.

- **Theta and gamma typically conflict** [04:15] — Short premium strategies benefit from theta decay but suffer from gamma (short gamma = losses accelerate on big moves). Long gamma strategies benefit from gamma but bleed theta.

- **The Outlier Strategy Process** [05:51] — Build strategies relative to specific profit mechanisms and market effects, not in isolation. Isolate the edge first, then optimize the structure.

- **Nvidia DeepSeek example** [07:17–11:18] — When [[nvda]] crashed on DeepSeek R1 news, two strategies modeled the expected recovery differently:
  - Short 26-delta put (21 March): $545 premium, 1,500 margin, but loses $3,700–$6,800 on 10–15% further decline
  - Long call (16 May 120 strike): $1,590 cost, loses only $270–$865 on same declines, profits $952 by recovery
  - The long call was better suited to the profit mechanism (price reversion after overextension).

- **Portfolio context matters** [12:33] — The best strategy is relative to both the profit mechanism *and* your broader portfolio objectives; size and risk tolerance must align.

## Notable quotes

> "There is no option strategy that does all of this. It doesn't exist. And this is the problem when we try to frame things like what is the best option strategy—we're trying to be lazy."

> "The best option strategy is going to be relative and built first around the profit mechanism you're trying to trade and then the second something that fits in with your broader portfolio objectives."

## Candidate wiki links

**Concepts:**
[[profit-mechanism]], [[market-regimes]], [[convexity]], [[theta-decay]], [[gamma]], [[win-rate-vs-profitability]], [[risk-management]], [[expected-value]], [[outlier-strategy-process]], [[overfitting]], [[position-sizing]], [[short-gamma]], [[undefined-losses]]

**Strategies:**
[[short-put]], [[long-call]], [[directional-breakout]]

**Securities:**
[[nvda]], [[spx]]

**People:**
[[eric]]

## Regime / context

Recorded May 18, 2025. The Nvidia example references the DeepSeek R1 announcement (late 2024) and subsequent recovery; timestamps and P&L figures are illustrative and approximate. The video is evergreen in its framework: the Outlier Strategy Process and the seven-trait checklist apply across all market regimes and time horizons.
