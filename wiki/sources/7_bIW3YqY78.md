---
type: source
title: "Picking a Strategy & Placing a Trade | Options Trading for Beginners Pt3"
video_id: 7_bIW3YqY78
url: https://www.youtube.com/watch?v=7_bIW3YqY78
date: 2024-06-22
series: beginner-lab
format: [education, live]
experts: [eric]
mentions: []
securities: [smci, gme, amc, tsm, spy]
concepts: [days-to-expiration, theta, theta-decay, delta, gamma, implied-volatility, implied-volatility-percentile, extrinsic-value, intrinsic-value, linear-regression-channels, volatility-term-structure, realized-volatility, paper-trading, trading-plan, trading-log, position-sizing, profit-mechanism, price-action, delta-hedging, moneyness, expected-move]
strategies: [ratio-call-diagonal, covered-call, long-call, buying-the-panic]
saga: none
part: null
confidence: high
---

# Picking a Strategy & Placing a Trade | Options Trading for Beginners Pt3

## Summary

Part 3 of the beginner options series transitions from theory to practical application, focusing on how to select appropriate expiration cycles, understand the Greeks (particularly theta, delta, and gamma), and structure trades using real examples. The session emphasizes the critical tradeoffs between days-to-expiration, theta decay, delta exposure, and gamma acceleration, demonstrating how these factors interact to determine position profitability and risk management.

## Key takeaways

### Dated market read (2024-06-22)

- **SMCI consolidation setup** [05:41]: After a 30–60% run, SMCI is consolidating sideways with elevated IV percentile (65%+), setting up as a momentum breakout candidate to the upside.
- **IV percentile vs. IV rank distinction** [07:10]: SMCI has 82% absolute IV but lower IV percentile; GE has 30% IV but 70% percentile—relative volatility matters more than absolute figures for strategy selection.

### Evergreen mechanics

- **Days-to-expiration tradeoffs** [20:34–21:15]: Shorter DTE options expire faster and decay more rapidly as a percentage of premium; longer DTE options have more extrinsic value but require longer for thesis to play out. The right DTE depends on your expected move timeline.
- **Theta decay is perpetual, not discrete** [29:12]: Theta decay happens continuously 24/7, not in daily chunks. Market makers accelerate weekly theta into weekends to account for lower volatility, so weekend premium decay is already priced in.
- **Theta decay accelerates within 60 DTE** [22:37]: Extrinsic value bleeds precipitously once you cross 60 days to expiration; a 7 DTE option loses ~21% of premium per day, while a 90 DTE option loses ~1.8% per day.
- **Theta is highest for at-the-money options** [34:54]: ATM options have the most extrinsic value to decay; deep ITM calls have less extrinsic value at entry but can suffer large losses if they fall OTM.
- **Delta increases as you go in-the-money** [59:36]: Delta rises toward 1.0 as an option moves deeper ITM; higher delta = more dollar-for-dollar move with the underlying, but options are more expensive.
- **Gamma is low for far OTM, long-dated options** [55:11]: A 32 delta far OTM call gains only 6 cents of delta per $1 move; a 30 delta call 56 DTE gains 11 cents per $1 move. Low gamma means slow delta acceleration and poor compounding on big moves.
- **In-the-money calls outperform far OTM calls on absolute returns** [57:39]: If AMC moves to $50, a 50-strike call returns ~$4,400 vs. ~$3,500 for a 20-strike call, despite higher cost, because of superior delta exposure per dollar move.
- **Rolling options realizes P&L immediately** [26:17]: Every roll closes the existing position and opens a new one; you lock in losses or gains on the short calls being rolled. Buying back at $0.710 after selling at $0.157 realizes a $0.553 loss per contract.
- **Rolling out and up improves basis** [28:08]: When rolling short calls, move out in time as little as possible and up in strike to improve your cost basis and preserve upside potential. If you roll too far out, you lose expiration liquidity and flexibility.
- **Far ITM options become difficult to roll** [35:31]: Once options are so far ITM that extrinsic value is minimal, rolling out and up becomes impossible; you may be forced to roll out much further in time, losing liquidity and trapping yourself.
- **Paper trading is essential before real money** [01:16]: Start with paper trading, not real capital. Most retail traders make avoidable mistakes; a trade checklist and disciplined process prevent costly errors.
- **Define profit and loss targets before entering** [15:42]: For every trade, define your profit target and stop-loss level before placing it. This single discipline dramatically improves long-term results.
- **Profit mechanism drives strategy selection** [17:11]: Understand *why* you're trading (e.g., expecting a big parabolic move vs. collecting premium). Once you define the profit mechanism, the right strategy naturally follows.
- **Ratio call diagonals are a core beginner strategy** [01:05:48]: Buy longer-dated, slightly ITM calls; sell shorter-dated calls against them. This structure balances time decay, delta exposure, and compounding potential.
- **Covered strangles and straddles are foundational** [01:45:34]: Along with ratio diagonals, these are the core strategies to master as a beginner; most advanced structures layer variations on these.
- **Trading plan and trading log are non-negotiable** [01:46:24]: A documented trading plan (400+ pages over 16 years) and consistent trading log are the primary drivers of long-term success, not short-term wins.

## Notable quotes

> "The hallmark of a trader is somebody who stands the test of time—it's not a one-year thing, a five-year thing, a ten-year thing. It's literally 20, 40 years of long runs of time."

> "Once you define the profit mechanism, it naturally backs you into the exact thing that you're trying to do more often than not."

> "I never got too hung up on the theoretical side; I learned it in parallel with everything else. The transition from theory to practical application is one of the reasons I've been able to create success with trading."

## Candidate wiki links

### Concepts
[[days-to-expiration]], [[theta]], [[theta-decay]], [[delta]], [[gamma]], [[implied-volatility]], [[implied-volatility-percentile]], [[extrinsic-value]], [[intrinsic-value]], [[linear-regression-channels]], [[volatility-term-structure]], [[realized-volatility]], [[paper-trading]], [[trading-plan]], [[trading-log]], [[position-sizing]], [[profit-mechanism]], [[price-action]], [[moneyness]], [[expected-move]], [[emotional-discipline]], [[process-over-outcome]]

### Strategies
[[ratio-call-diagonal]], [[covered-call]], [[long-call]], [[short-strangle]], [[short-straddle]], [[buying-the-panic]]

### Securities
[[smci]], [[gme]], [[amc]], [[tsm]], [[spy]]

### People
[[eric]]

## Regime / context

Recorded 2024-06-22 during a live educational session. Market conditions reflect mid-June 2024 volatility environment. SMCI consolidation and GME/AMC option examples are illustrative of the period's meme-stock and AI-chip volatility. The session is part 3 of a planned 6-week beginner options series; part 4 will focus on analyzing options chains in depth.
