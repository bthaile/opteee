---
type: source
title: "Deep Dive into GameStop Settlement Theory & Market Structure Analysis"
video_id: Cfs_0qgho_E
url: "https://www.youtube.com/watch?v=Cfs_0qgho_E"
date: "2024-12-21"
series: none
format: [education, analysis, live]
experts: [eric, richard-newton]
mentions: [roaring-kitty]
securities: [gme, cost, chewy]
concepts: [settlement, ftd, failed-to-deliver, etf-creation-redemption, rex-068, margin-deficiency, delayed-settlement, order-flow, market-maker, dealer-positioning, volatility-clustering, market-structure]
strategies: []
saga: gme-saga
part: null
confidence: medium
---

# Deep Dive into GameStop Settlement Theory & Market Structure Analysis

## Summary

Eric reviews a comprehensive 44-page due diligence document on GameStop settlement mechanics, examining theories about how delayed settlement cycles, ETF creation-redemption mechanics, and regulatory exemptions (particularly REX-068) may drive price movements. The analysis explores whether market makers or hedge funds are the primary short participants and questions the logical mechanics of how margin deficiencies would manifest in observable market volume. Eric emphasizes the importance of rigorous verification and identifies key gaps in the theory that require further investigation.

## Key takeaways

### Dated market read (2024-12-21)
- **Settlement framework overview** [11:38–13:27]: The document outlines three settlement formulas: T+1 (initial), T+35C (35-day calendar cycle), and T+3+2 (authorized participant return), theorizing these cycles drive GameStop runs through "kicking the can" mechanisms.
- **REX-068 extension mechanism** [13:27–15:06]: Allows firms to request 14-day extensions for margin deficiencies; document speculates this triggers observable volume spikes, though Eric questions why entities would buy openly during margin stress rather than use ETF redemption cycles.
- **ETF creation-redemption cycles** [13:27–16:58]: Theory proposes market makers use ETF baskets (holding GME, COST, Chewy) to satisfy FTDs and locates without touching the stock directly; requires validation across all holdings in those ETFs, not just the meme stocks.
- **DFV return and 2024 runs** [15:06–16:58]: Document ties DFV's return and trading activity to margin deficiencies and REX-068 extensions; emoji timeline decoded as potential catalysts for July 3–5, 2025.
- **Broader applicability** [16:58–18:13]: COST and Chewy show similar patterns, suggesting the theory applies beyond GME if robust; requires systematic evaluation of like-kind stocks within the same ETFs.

### Evergreen mechanics
- **Settlement rule hierarchy** [24:39–27:40]: SHO Rule 203 requires short sellers to close fails by T+2 (market maker exception: T+3); Rule 204 allows 35 calendar days for equity FTDs; calendar vs. trading day distinction is critical to timing predictions.
- **Market maker risk management** [01:03:00–01:07:21]: Large market makers (e.g., Citadel) manage risk across thousands of names in aggregate, not in isolation; margin calls on a single position are unlikely unless the entire book is mismanaged, making systematic short positions less probable for MMs than for hedge funds.
- **Swap mechanics and limitations** [01:14:43–01:20:56]: Swaps are non-standardized black boxes; institutions would not wait until expiry to buy underlying shares (front-running risk); they can roll swaps indefinitely or exit early, making swap-driven volume predictions unreliable.
- **Overfitting risk** [01:20:56–01:22:17]: Multiple factors (settlement cycles, options activity, sentiment, REX-068, swaps) coalesce during runs; isolating causation is difficult; even loose correlations warrant investigation but should not be treated as proof.

## Notable quotes

> "GameStop can teach you a lot about markets that you otherwise never would come across."

> "The reason why I'm so interested in that is because that's so far out from now... I'm very curious how it applies today as things sit right now because the original premise of this is that we think Moass is going to happen or might there might be another version of it that might be close to Moass, but not quite."

## Candidate wiki links

**concepts:**
[[settlement]], [[ftd]], [[failed-to-deliver]], [[etf-creation-redemption]], [[margin-deficiency]], [[delayed-settlement]], [[order-flow]], [[market-maker]], [[dealer-positioning]], [[volatility-clustering]], [[market-structure]], [[kelly-criterion]], [[risk-management]], [[position-sizing]], [[technical-analysis]], [[price-action]]

**strategies:**
[[short-squeeze]], [[short-volatility]]

**securities:**
[[gme]], [[cost]], [[chewy]]

**people:**
[[eric]], [[richard-newton]], [[roaring-kitty]]

## Regime / context

**Date:** 2024-12-21 (live stream recorded during holiday period; Eric traveling to Calgary).

**Saga context:** Part of ongoing GameStop analysis series; Eric has been reviewing DFV trades and community due diligence weekly. This document represents a synthesis of settlement-cycle theories that have circulated in the community, with particular focus on work by Richard Newton (credited as "the GameStop scribe"). 

**Key uncertainties flagged by Eric:**
- Whether primary shorts are market makers (with REX-068 margin extensions) or hedge funds (with different rule applications and motivations).
- Why margin-deficiency satisfaction would manifest as open-market volume spikes rather than ETF redemption cycles.
- Robustness of settlement-cycle predictions: Eric and Newton have observed both strong correlations and many non-correlated instances, suggesting the theory is intermittent rather than deterministic.
- Whether structural changes post-2021 have altered the mechanics (e.g., whether MOASS-like scenarios are still possible or have been "short-circuited").

**Homework items identified:**
1. Evaluate primary ETFs holding GME, COST, Chewy; observe behavior of like-kind stocks (by market cap) across move timing and severity.
2. Compile total list of expected delayed-settlement catalysts and track GME/ETF/FTD behavior against them.
3. Clarify REX-068 mechanics: why margin satisfaction would occur on open market vs. ETF cycles.
4. Determine primary short participant type and motivation.
