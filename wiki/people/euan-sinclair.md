---
type: person
title: "Euan Sinclair"
role: "Quant options trader, ex-market-maker, author"
related_videos: ["6vQeTS9cyk0", "Ao4evQT3dOU", "kvzQJ3wFaZs"]
related_concepts: [volatility-risk-premium, edge, dealer-gamma, fat-tails, mean-reversion, pnl-attribution, transaction-costs]
related_strategies: [short-put, short-strangle, risk-reversal, covered-strangle]
last_updated: 2026-07-03
confidence: high
---

# Euan Sinclair

Quant options trader and author, recurring guest on **The Outlier Podcast** (3 appearances in the current sample). His through-line: **edge comes from a handful of durable, well-understood risk premia plus statistical humility — not from clever, hard-to-measure effects.** He is the corpus's most rigorous skeptic and the source of most of its cross-source contradictions.

## Core positions (consistent across all 3 videos)
- **Durable edge = selling premium.** The closest thing to an always-on strategy is selling ~20Δ puts; it "should keep working over 10 years because it has for 100." There is no long-side equivalent — "you've got to pick your spots." [[sources/Ao4evQT3dOU]] [01:28]
- **Decompose your P&L.** "You can be right about volatility and still lose money — often." Every option trade has huge variance vs its edge, so P&L can't drive your theory; isolate what you *should* have made. [[sources/Ao4evQT3dOU]] [17:08]
- **Trade less; costs are termites.** Reducing [[concepts/transaction-costs]] is the single biggest improvement most retail traders can make. [[sources/6vQeTS9cyk0]] [29:45]
- **Premium ≠ income.** The covered-call "income" framing is busted — the premium is compensation for a short-vol liability. See [[concepts/volatility-risk-premium]]. [[sources/kvzQJ3wFaZs]] [01:19]

## Distinctive / contested stances (contradiction tracking)
These put Sinclair **directly at odds** with other Outlier content — exactly the kind of tension the wiki should surface, not smooth over:

- **Dealer-gamma / GEX is "absolute nonsense" for retail.** You can't infer dealer positioning from outside; even given it, you can't front-run 50 years of optimized hedging. [[sources/Ao4evQT3dOU]] [26:11]
  - ⚠️ **Contradicts** the market-update stream [[sources/FrqSC7Fbf14]], which teaches [[concepts/gamma-exposure]] / dealer delta-hedging as an actionable read. *Open tension — resolve on [[concepts/gamma-exposure]].*
- **The wings are not inferable.** His kurtosis study: proving a 0DTE strategy profitable would take ~33–4,000 years of data, so he **rejects Taleb's claim** that tail options are underpriced — while also refusing to *sell* 1-delta options. [[sources/Ao4evQT3dOU]] [58:55]
- **Buy the ATM call, sell the wings** — the opposite of the popular retail "sell 0DTE, buy the wings." [[sources/Ao4evQT3dOU]] [03:49]
- **0DTE is astonishingly hard**, not easy: real vol-terms edge but dollar [[concepts/transaction-costs]] swamp it; no advantage over weeklies/monthlies. [[sources/6vQeTS9cyk0]] [17:26]
- **Mean reversion is horizon-specific:** reversion at ~1 month, trending at ~3–6 months.
  - ⚠️ Compare [[people/tom-sosnoff]], who rejects price mean-reversion outright. *Open tension.*

## Where he agrees with the mainstream
Selling ~20Δ puts/strangles as the durable premium; separating vol P&L from directional P&L; the market-maker P&L decomposition ≡ the Black-Scholes equation. [[sources/Ao4evQT3dOU]] [18:14]

## Signature ideas to mine further
Implied-**skewness** premium via unbalanced [[strategies/risk-reversal]] (short 15Δ put / long 25Δ call, net long vega) [[sources/6vQeTS9cyk0]] [09:18]; "buy the highest, sell the second highest" vol joke; sports-betting transfer (bet relative value, size by Kelly, parlay your edge).

## See also
[[concepts/volatility-risk-premium]] · [[concepts/gamma-exposure]] · [[people/tom-sosnoff]] · [[strategies/covered-strangle]]
