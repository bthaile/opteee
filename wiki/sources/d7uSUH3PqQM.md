---
type: source
title: "SVB Collapse - Ratio Long Put"
video_id: d7uSUH3PqQM
url: https://www.youtube.com/watch?v=d7uSUH3PqQM
date: 2023-03-19
series: none
format: [education, strategy-breakdown, analysis]
experts: [eric]
mentions: []
securities: [xlf, sivb]
concepts: [delta, gamma, implied-volatility, long-volatility, event-volatility, correlation, leverage, risk-management, position-sizing, theta-decay, moneyness, gamma-scalping, expected-move]
strategies: [long-put, ratio-write]
saga: none
part: null
confidence: high
---

# SVB Collapse - Ratio Long Put

## Summary

Eric walks through a two-leg long-put strategy deployed during the SVB bank collapse (March 2023), using [[xlf|XLF]] as a proxy for the halted [[sivb|SIVB]]. He combined a higher-[[delta]] in-the-money put with a lower-[[delta]] out-of-the-money "kicker" to capture both [[theta-decay|theta]] stability and [[gamma]] acceleration, generating a 234% return on ~$11.5k deployed capital in a single week.

## Key takeaways

- **Proxy selection via correlation** [00:39–04:36]: SIVB halted on March 9; Eric validated XLF as a 0.997 three-day correlation proxy and 0.92+ five-day correlation, confirming sector-wide financial stress exposure without single-stock halt risk.

- **Two-leg put structure for event volatility** [06:44–09:56]: Bought 100 XLF March 17 $34 puts at $0.87 (high-delta, ~88 delta) + 400 March 30 $30 puts at $0.07 (low-delta, ~7 delta). The first leg provides dollar-for-dollar [[delta]] participation; the second leg is a "kicker"—cheap speculation that compounds via [[gamma]] if the move accelerates.

- **Why the kicker works** [08:50–09:56]: Out-of-the-money options are cheap to buy but offer explosive [[gamma]] payoff if the underlying moves sharply in your favor. If the move doesn't materialize, the small outlay ($2,800) is written off; if it does, the compounding [[delta]] acceleration generates outsized returns.

- **Risk control via size, not hedging** [10:17–13:04]: Eric sized the entire speculation ($11.5k) as acceptable loss, avoiding the need for complex hedges during a halted-security event. He set a mental exit at 50% loss on the kicker if conditions deteriorated, but allowed the core position to run.

- **Execution and exit** [13:25–14:28]: XLF moved from $32.93 (Friday close) to $31.37 (Monday low), generating ~$1.45 move. Eric exited Monday (March 13) after capturing [[implied-volatility]] expansion: sold the $34 puts for $2.32 (167% ROI) and the $30 puts for $0.38 (443% ROI), totaling ~$26.9k profit.

- **Flexibility over dogma** [17:21–17:42]: This event-driven structure differs from Eric's typical [[covered-strangle]] or [[ratio-call-diagonal]] playbook. He emphasizes adapting strategy to market regime—short calls would have capped upside; long puts captured velocity and [[long-volatility]].

## Notable quotes

> "I'm exposing myself to two different functions of options that I'm very interested in. I wait this trade because there's less risk involved."

> "This is where you get those huge compounding returns in options: when you buy something that's pretty far out of the money and it moves in your favor with velocity."

## Candidate wiki links

**Concepts:**
[[delta]], [[gamma]], [[implied-volatility]], [[event-volatility]], [[theta-decay]], [[moneyness]], [[leverage]], [[risk-management]], [[position-sizing]], [[correlation]], [[long-volatility]], [[gamma-scalping]]

**Strategies:**
[[long-put]], [[ratio-write]]

**Securities:**
[[xlf]], [[sivb]]

**People:**
[[eric]]

## Regime / context

**Date:** March 10–13, 2023 (SVB collapse event). SIVB halted on March 9 after a ~$150B intraday collapse; trading never resumed. This video captures a real-time opportunistic trade during a systemic financial stress event, using sector-wide correlation to bypass single-stock halt risk. The strategy is event-driven and not repeatable in normal regimes; Eric's emphasis on flexibility and risk-first sizing reflects the elevated uncertainty of a banking crisis.
