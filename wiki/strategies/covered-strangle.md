---
type: strategy
title: "Covered Strangle (a.k.a. the \"Coverage Triangle\")"
aliases: [coverage-triangle, covered-triangle]
related_videos: ["AJP8M8DQ_1U", "1rqLJW1nK40", "kvzQJ3wFaZs"]
related_concepts: [volatility-risk-premium, implied-volatility-percentile, position-sizing, scaling-in, theta-decay, delta]
related_strategies: [covered-call, cash-secured-put, short-put, the-wheel, ratio-write]
last_updated: 2026-07-03
confidence: high
regime_dependent: true
---

# Covered Strangle (a.k.a. the "Coverage Triangle")

## Structure
Long stock **+** short puts **+** *ratio* short calls. The host brands his version the **"coverage triangle" / "covered triangle"** — it is the same position as a covered strangle. [[sources/1rqLJW1nK40]] Both legs sell premium against a long-equity core, so the trade is fundamentally a way to harvest [[concepts/volatility-risk-premium]] on a name you want to own.

## Why Outlier favors it (on GME especially)
- It monetizes **sideways chop** that would bleed a long-call holder and strand a 100%-equity holder who lacks a sell rule. [[sources/1rqLJW1nK40]] [17:30]
- It works even at **low [[concepts/implied-volatility-rank]]** as long as the [[concepts/volatility-risk-premium]] stays fat — the defining GME condition. [[sources/AJP8M8DQ_1U]] [15:02]
- **Live evidence:** +13.5% vs. a −25.86% buy-and-hold from a $29 GME entry (~39% outperformance, same ticker/window); a separate campaign ran ~+28.8% while spot was down ~8.9%. [[sources/1rqLJW1nK40]] · [[sources/AJP8M8DQ_1U]] [16:43]

## Management playbook (the details that matter)
- **Ratio the calls.** Sell fewer calls than shares (e.g. 500 shares → 2–3 calls, not 5) so you keep upside and stay net-long the name. [[sources/kvzQJ3wFaZs]] [13:29]
- **Never sell a call below your basis** — it risks locking in a loss. Drive basis down first via disciplined [[concepts/scaling-in]]. [[sources/1rqLJW1nK40]] [33:21]
- **Delta selection is inventory-first, price-second:** downtrend ~20–30Δ (don't want more shares), rally 35–50Δ, sideways ~35Δ. [[sources/1rqLJW1nK40]] [1:42:58]
- **~20–21 DTE, not 45.** "45 DTE is a tastytrade artifact." Shorter tenors annualize to a higher return, and the defined roll/assignment playbook means gamma isn't the concern. [[sources/1rqLJW1nK40]] [1:33:53]
- **Roll the short call rather than use a [[strategies/call-credit-spread]].** A covered call can be rolled to defer/avoid a realized loss; a credit spread must be closed and re-established for tiny credit and skewed risk/reward. [[sources/1rqLJW1nK40]] [1:44:14]
- **Reserve capital.** Target ~80% utilization; keep dry powder to scale in on dips and adjust basis. [[sources/1rqLJW1nK40]] [13:14]

## Regime dependence & risks
- The edge lives on the [[concepts/volatility-risk-premium]] staying fat; **if premium compresses, the edge fades even though the chart looks the same.** [[sources/AJP8M8DQ_1U]]
- Sinclair's caveat on the short-call leg: selling calls is **short volatility / short the right tail** — only defensible when you can name a reason the call is overpriced, not as a blanket "income" rule. See [[people/euan-sinclair]] and [[sources/kvzQJ3wFaZs]] [11:12].
- Most-dangerous case = insolvency/delisting on the equity core (low probability, size for it); most-likely bad case = drift to intrinsic value, managed by allocation + basis-adjustable short puts. [[sources/1rqLJW1nK40]] [1:16:15]

## See also
[[concepts/volatility-risk-premium]] · [[strategies/covered-call]] · [[strategies/the-wheel]] · [[securities/gme-saga]] · [[people/euan-sinclair]]
