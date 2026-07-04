---
type: concept
title: "Volatility Risk Premium (VRP)"
aliases: [vrp, variance-risk-premium, short-premium-edge]
related_videos: ["AJP8M8DQ_1U", "1rqLJW1nK40", "kvzQJ3wFaZs", "Ao4evQT3dOU", "6vQeTS9cyk0", "AoHUcyVh7NY"]
related_concepts: [implied-volatility, realized-volatility, implied-volatility-percentile, mean-reversion, edge]
related_strategies: [covered-strangle, short-premium, short-put, short-strangle, covered-call]
last_updated: 2026-07-03
confidence: high
regime_dependent: true
subtype: mechanic
---

# Volatility Risk Premium (VRP)

## Definition
The volatility risk premium is the tendency for **implied volatility to be priced richer than the volatility that is ultimately realized**. Option sellers are paid this spread as compensation for carrying the risk of a large move. It is the single most-cited edge across the Outlier corpus and the engine underneath every premium-selling structure.

> "We're seeing volatility priced richer than what's ultimately happening in realized." — [[sources/AJP8M8DQ_1U]] [15:34]

## Why it is the Outlier engine
Outlier's favored structures ([[strategies/covered-strangle]], [[strategies/short-put]], [[strategies/short-strangle]]) are all ways to **harvest VRP**. The recurring teaching point is that VRP is *not* the same as high [[concepts/implied-volatility]]:

- A name can have a **low [[concepts/implied-volatility-rank]] / percentile and still have a fat VRP** — implied can sit low yet still be priced above realized. That is the ideal premium-selling condition, and it is exactly why the host sells premium on GameStop even when GME's IV percentile is ~22%. [[sources/AJP8M8DQ_1U]] [15:02]
- Conversely, **high IV is not automatically a sale** — see [[concepts/implied-volatility]]. High IV/skew is usually high *for a reason*. [[sources/kvzQJ3wFaZs]] [25:04]

## Premium ≠ income (the key reframing)
The most important correction in the corpus: the premium you collect is **compensation for a liability (short volatility / capped upside), not income**. If you sell an option for less than its true expected value you book *negative* income even on a winning trade. [[sources/kvzQJ3wFaZs]] [01:19]

- It is a repeated game: collect $2 nine times, lose ~$48 once → the EV loss shows up over many occurrences, not one trade. [[sources/kvzQJ3wFaZs]] [02:56]
- Only the portion above fair value is real edge; the rest is a reserve held against market risk — how a market maker books it (P&L-to-theo). [[sources/kvzQJ3wFaZs]] [05:24]

## When VRP fails (regime dependence)
VRP is **not a constant**. The edge fades or inverts in specific regimes:

- **At vol extremes, implied never reaches what realized can do.** Silver realized ~130%; no vol you could have sold would have won because implied never got there. [[sources/kvzQJ3wFaZs]] [30:30]
- **Premium compression:** if the GME premium compresses, the covered-strangle edge fades *even though the chart looks identical*. [[sources/AJP8M8DQ_1U]]
- **The worst earnings cycle on record** (per [[people/euan-sinclair]]) was the first since 2006 where a majority of stocks beat their implied move — a full regime where short-vol sellers lost. [[sources/Ao4evQT3dOU]] [56:41]

## Contested / open questions
- **Skewness premium vs variance premium.** Sinclair harvests a distinct *implied-skewness* premium via an unbalanced [[strategies/risk-reversal]] (short ~15Δ puts / long ~25Δ calls, net long vega) — a different premium from the plain short-vol VRP. [[sources/6vQeTS9cyk0]] [09:18]
- **Right-tail cost.** Selling calls hands away the right tail — the whole reason to own a name over the index. VRP harvest and right-tail ownership are in direct tension. [[sources/kvzQJ3wFaZs]] [15:00]

## See also
[[concepts/implied-volatility]] · [[strategies/covered-strangle]] · [[people/euan-sinclair]] · [[concepts/realized-volatility]]
