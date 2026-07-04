---
type: source
title: "Your GEX and DEX Strategy Is Probably Wrong | The Options Trench"
video_id: GYDo30UopnI
url: https://www.youtube.com/watch?v=GYDo30UopnI
date: 2026-05-30
series: options-trench
format: [education, analysis, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, spx]
concepts: [gamma, gamma-exposure, delta, delta-hedging, delta-neutral, dealer-gamma, dealer-positioning, implied-volatility, volatility-skew, open-interest, market-maker, market-neutral, dispersion-trading, volatility-clustering, order-flow, supply-and-demand, position-sizing, risk-management, edge, market-efficiency]
strategies: [covered-call, short-strangle, short-premium]
saga: null
part: null
confidence: high
---

# Your GEX and DEX Strategy Is Probably Wrong | The Options Trench

## Summary

This episode deconstructs the assumptions underlying gamma exposure (GEX) and delta exposure (DEX) as market-prediction signals, which have gained popularity on social media. The hosts examine the foundational dealer-positioning model, identify critical assumptions that often break down in practice, and explore when these tools might have marginal utility versus when they mislead. The core message: GEX and DEX are low-resolution snapshots of dealer hedging behavior, useful only when their assumptions hold—which is far less often than practitioners assume.

## Key takeaways

### Foundational assumptions of GEX/DEX [00:24–03:08]
- **Dealer positioning model**: Market makers are assumed to be net long calls and net short puts (because retail/funds sell calls and buy puts for protection), forcing dealers to take the opposite side.
- **Delta-neutral hedging**: Dealers are assumed to hedge continuously, shorting stock against long calls and buying stock against short puts.
- **Implication**: As the market moves, option deltas change (gamma effect), forcing dealers to mechanically rebalance—selling into rallies, buying into declines.

### Gamma vs. charm mechanics [04:53–06:54]
- **Gamma**: measures delta change as the underlying price moves; dealers long gamma must sell rallies to stay hedged.
- **Charm**: measures delta change due to time decay; an OTM call losing delta over a month forces dealers to buy back short stock incrementally.
- Both effects operate simultaneously; isolating them helps understand dealer flow mechanics.

### Critical assumption #1: Dealer counterparty dominance [08:57–09:52]
- The model assumes dealers are the counterparty for most options trades.
- **Reality check**: Call skew pricing reveals whether this holds. When call skew is historically expensive (high relative to ATM), it signals investor demand to buy OTM calls—meaning dealers may be *short* calls, not long, contradicting the base assumption.
- Use relative skew pricing (e.g., 25-delta call as % of ATM) to validate or invalidate the assumption in real time.

### Critical assumption #2: Dealer book isolation [14:58–17:43]
- GEX/DEX show only the SPX leg of dealer positioning; they hide dispersion-trading hedges (dealers short index vol, long single-stock vol).
- **Example**: A dealer short SPX puts (showing negative GEX) may be long single-stock gamma elsewhere, making net gamma long—opposite the signal.
- **Consequence**: You see only half the ledger; dealers may be net buyers on declines (stabilizing) even when GEX suggests they'll sell.

### GEX vs. DEX utility [20:34–24:30]
- **DEX** (delta exposure): Largely overlaps with open interest; indicates position magnitude at a strike, useful for identifying where interest concentrates.
- **GEX** (gamma exposure): Snapshot of current gamma; only shows strikes near-the-money where gamma is material. Far OTM/ITM strikes have zero gamma but may have large open interest.
- **Complementary use**: GEX shows current flow risk; DEX reveals hidden positioning that will become gamma-relevant if the market gaps to that strike.

### Dealer hedging is not mechanical [27:51–33:29]
- Dealers do not run purely delta-neutral books; they model and lean against other dealers' anticipated hedging.
- **Poker analogy**: In liquid markets (SPX = checkers), mechanical hedging dominates. In illiquid names, dealer behavior is discretionary and depends on customer identity, profit-taking patterns, and roll behavior.
- **Implication**: The assumption that dealers will hedge predictably breaks down in less-liquid underlyings where edge actually exists.

### Research approach [25:29–27:27]
- Explore price behavior at strikes with large net positions (primary input).
- Test mid-strike behavior before reaching main strikes (0/5 convention).
- For vol-settling strategies, use GEX/DEX to inform short-strangle strike selection.
- Recognize that finding a pattern does not prove the assumption was correct; causality is hard to isolate.

## Notable quotes

"The idea is that market makers want to be market neutral, that they are going to continue to hedge as the market moves around."

"If you only look at this tool, you're only seeing part of the ledger. You're not seeing their single stock options positioning."

"There is a real impact of gamma and open interest in the marketplace. What to do with that knowledge is a very difficult problem."

## Candidate wiki links

**concepts:** [[gamma]], [[gamma-exposure]], [[delta]], [[delta-hedging]], [[delta-neutral]], [[dealer-gamma]], [[dealer-positioning]], [[implied-volatility]], [[volatility-skew]], [[open-interest]], [[market-maker]], [[market-neutral]], [[dispersion-trading]], [[order-flow]], [[supply-and-demand]], [[position-sizing]], [[risk-management]], [[edge]]

**strategies:** [[covered-call]], [[short-strangle]], [[short-premium]]

**securities:** [[spy]], [[spx]]

## Regime / context

Recorded 2026-05-30. This episode reflects a period of elevated discussion around GEX/DEX on social media as predictive tools. The hosts emphasize that while gamma and dealer hedging are real market phenomena (established since the early 2000s), the recent popularization of these metrics as standalone signals often ignores the low-resolution assumptions underlying them. The analysis is evergreen for anyone evaluating dealer-flow-based trading signals.
