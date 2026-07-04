---
type: concept
title: "Implied Volatility (IV)"
aliases: [iv]
related_videos: ["sk8rQ8rfn3s", "AJP8M8DQ_1U", "kvzQJ3wFaZs", "1rqLJW1nK40", "Ao4evQT3dOU", "AoHUcyVh7NY"]
related_concepts: [volatility-risk-premium, realized-volatility, implied-volatility-rank, implied-volatility-percentile, vega, volatility-term-structure, extrinsic-value]
related_strategies: [covered-strangle, stock-replacement, short-premium]
last_updated: 2026-07-03
confidence: high
regime_dependent: true
subtype: mechanic
---

# Implied Volatility (IV)

## Definition
Implied volatility is the market's forward estimate of how much an underlying will move, backed out of option prices. In the Outlier corpus IV is treated less as a number to predict and more as an input to two questions: *is premium rich relative to what will be realized* (see [[concepts/volatility-risk-premium]]), and *am I looking at the right tenor's IV*.

## IV rank vs IV percentile
Outlier consistently **prefers [[concepts/implied-volatility-percentile]] over [[concepts/implied-volatility-rank]]** — percentile reflects how often IV has actually been lower, which is more robust than rank's high/low endpoints. [[sources/kvzQJ3wFaZs]] [13:29]

## The 30-day-metric trap (do not price LEAPS off front IV)
The most-taught IV lesson in the sample: displayed IV, IV percentile, and IV rank are all built on a **~30-day** volatility measure, so they are the **wrong tool for judging long-dated options**. [[sources/sk8rQ8rfn3s]]

- A viewer asked about buying LEAPS "because IV looks low." GME's 30-day IV was ~68.7% with IV percentile ~2% — genuinely low, *but only for the 30-day tenor*. [26:08]
- **[[concepts/volatility-term-structure]]:** front-month vol ~64% vs back-month ~77% on GME — a ~13-point spread across tenors. Near-term low ≠ long-term low. [33:27]
- 30-day and long-term vol can move in **opposite directions** over the same window (30-day fell 83→58 while long-term rose 66→81). [01:03:27]

## Why tenor matters: vega scales with time
[[concepts/vega]] (premium change per 1% IV change) **increases the further out in time you go**, because more time means a larger [[concepts/extrinsic-value]] portion. A ~566-DTE LEAP had vega ~1.05 vs ~0.22 for a 20-DTE ATM option (~5×). So a small back-end vol move can move a LEAP more than a large front-end move. [[sources/sk8rQ8rfn3s]] [47:48]

## "Don't trade the IV line"
A recurring correction: **your P&L comes from how much the underlying actually moves, not from the IV chart.** "IV percentile is high so it must mean-revert" ignores that P&L is driven by realized movement and by volatility clustering. On near-dated options, think in **straddle prices**, not IV. [[sources/kvzQJ3wFaZs]] [28:18]

## Regime / caveats
All IV/vega figures in the sources are **day-specific chain snapshots** (illustrative, not evergreen). The size of the front-vs-back term-structure spread is name- and regime-dependent — largest on high-velocity meme names like GME. [[sources/sk8rQ8rfn3s]]

## See also
[[concepts/volatility-risk-premium]] · [[concepts/vega]] · [[concepts/implied-volatility-percentile]] · [[strategies/covered-strangle]]
