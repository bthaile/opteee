---
type: source
title: "GameStop, eBay, Options, and Volatility | Ep61"
video_id: NV_N1zDszZI
url: https://www.youtube.com/watch?v=NV_N1zDszZI
date: 2026-05-10
series: options-trench
format: [education, analysis, market-note]
experts: [eric]
mentions: [roaring-kitty]
securities: [gme, ebay]
concepts: [covered-strangle, delta, implied-volatility, volatility-term-structure, right-tail, cash-value-per-share, open-interest, skew, volatility-risk-premium, realized-vs-unrealized-pnl, leverage, price-action]
strategies: [covered-strangle, short-premium, covered-call, ratio-write]
saga: gme-saga
part: null
confidence: high
---

# GameStop, eBay, Options, and Volatility | Ep61

## Summary

Eric analyzes the GameStop–eBay acquisition proposal through both fundamental and options-market lenses, examining deal probability (~17–30%), financing structure, and RC Cohen's strategic vision. He demonstrates how to use options chains to gauge market conviction in the deal, illustrates the natural right-tail skew in GameStop's distribution due to its cash floor, and showcases a live [[covered-strangle]] position generating 30% annualized return—outpacing the underlying's 19.8% YTD move.

## Key takeaways

### Dated market read (2026-05-10)

- **Deal probability assessment** [09:46–12:50]: GameStop–eBay deal faces structural financing gaps; even full GameStop dilution leaves ~$16B shortfall. TD's "highly confident" letter is not locked financing. Market prices deal at ~17% on Polymarket (justified); started at 37% on May 4 due to liquidity, not true conviction.
- **eBay up, GameStop up anomaly** [39:07–40:34]: Unusual that both acquirer and target rallied on announcement day (May 1). Normally acquirer stock declines near-term due to risk/expense; eBay's 125 offer price creates a ceiling for GME in the interim.
- **June earnings catalyst** [46:46–48:04]: GameStop earnings June 9; June options chain shows elevated IV (58% wall on calls/puts) partly due to deal probability, partly due to GME's structural right-tail skew from cash floor (~$10–11/share).
- **Open interest anomaly** [58:41–01:02:37]: June 30-strike calls show 3:1 call-to-put ratio (very elevated); most OI built mid-April and post-announcement (May 1). Transactions predominantly on offer side = net long positioning. 2.3M notional calls vs. 174K puts in June term.

### Evergreen mechanics

- **Using options chains to price deal conviction** [43:21–45:19]: Compare delta/probability of 125-strike across time. Pre-announcement (April 30): 24δ, 19δ, 15δ. Post-announcement: 30δ, 22δ, 16δ. Slight premium at 125; larger drop-offs above = market skeptical of deal closing.
- **Right-tail distribution from cash floor** [49:23–52:47]: GME's net cash (~$4.65B, ~$10–11/share) removes left-tail risk, concentrating probability rightward. This creates natural call skew and justifies [[covered-strangle]] as superior to naked short-call strategies in GME.
- **Covered-strangle construction in GME** [52:47–54:16]: Sell 18-June 22-strike puts (28δ, 87¢ = 32% annualized); sell 29-strike calls (29δ, $1.00 = 36.7% annualized). Call premium exceeds put premium (4-point inversion) due to right-tail skew. YTD return: 30% vs. GME's 19.8% (10% alpha).
- **Volatility risk premium harvesting** [57:21–58:41]: GME's bullish and bearish premium magnitudes are similar across terms, indicating heavy premium-selling activity. Consolidation in 25s, 30s, 32s, 35s, 50s; largest open interest in June (unusual; typically front-month dominates).
- **Realized vs. implied move divergence** [55:39–57:21]: GME can experience sharp realized moves exceeding implied moves during deal-related surges. Prefer [[short-premium]] on eBay side (higher risk premiums, put skew, reduced severity if deal fails) over directional GME plays.

## Notable quotes

> "Cohen strikes me as the kind of person that's like a serial entrepreneur and a CEO… he's constantly looking to grow and work on increasingly complex projects and businesses."

> "The fact that you're seeing progress but it's not like this insane progress coming through" — on GameStop's operational improvements and the rationale for the eBay pivot.

> "There's a lot of right tail opportunity in game stop because of this kind of function" — on the cash-floor-driven skew enabling covered-strangle outperformance.

## Candidate wiki links

**concepts:** [[covered-strangle]], [[delta]], [[implied-volatility]], [[volatility-term-structure]], [[right-tail]], [[open-interest]], [[skew]], [[volatility-risk-premium]], [[realized-vs-unrealized-pnl]], [[leverage]], [[price-action]], [[moneyness]], [[probability-of-touch]]

**strategies:** [[covered-strangle]], [[short-premium]], [[covered-call]], [[ratio-write]], [[short-put]]

**securities:** [[gme]], [[ebay]]

**people:** [[roaring-kitty]]

## Regime / context

Recorded May 10, 2026, during the active GameStop–eBay acquisition proposal phase (announced ~May 1). Deal probability remains low (~17–30%) pending eBay board response and TD financing confirmation. GameStop earnings scheduled June 9, 2026. This episode is part of the broader [[gme-saga]] but does not constitute a numbered part; it is a market-update analysis of the acquisition's options-market implications and Eric's live covered-strangle position.
