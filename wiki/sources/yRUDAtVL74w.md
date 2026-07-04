---
type: source
title: "IV Rank (IVR) vs IV Percentile (IVP) | Thinkorswim (tos) is WRONG"
video_id: yRUDAtVL74w
url: https://www.youtube.com/watch?v=yRUDAtVL74w
date: 2020-08-20
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [tsla]
concepts: [implied-volatility-rank, implied-volatility-percentile, implied-volatility, outlier-strategy-process]
strategies: []
saga: null
part: null
confidence: high
---

# IV Rank (IVR) vs IV Percentile (IVP) | Thinkorswim (tos) is WRONG

## Summary

IV Rank and IV Percentile are fundamentally different calculations often conflated as synonyms, particularly in Thinkorswim's display. IV Rank uses 52-week extremes and is susceptible to outlier skew; IV Percentile counts trading days below current IV against the 252-day year and is more robust. Understanding this distinction is critical because the two metrics can diverge dramatically during market dislocations, materially changing trade approach.

## Key takeaways

- **IV Rank formula** [01:35]: (Current IV − 52-week low IV) ÷ (52-week high IV − 52-week low IV). Susceptible to outlier skew because it anchors to extremes.
- **IV Percentile formula** [02:28]: Number of trading days below current IV ÷ 252 trading days. Less susceptible to skew; uses distribution of historical levels.
- **Thinkorswim mislabeling** [01:10]: The platform displays IV Rank but labels it "IV Percentile," creating systematic confusion.
- **Practical divergence** [03:16]: In the Tesla example, IV Rank = 30%, IV Percentile = 66%—a massive discrepancy that completely changes trade selection and risk posture.
- **Normal vs. dislocation regimes** [00:21]: During calm markets the two metrics track closely; during large outlier moves (e.g., March 2020 crash), the difference becomes "super apparent."
- **Use IV Percentile for trading** [02:03]: Percentile is "way less susceptible to skew" and therefore more useful for consistent trade decision-making.

## Notable quotes

> "Think or swim is lying to you" — the platform displays IV Rank but labels it IV Percentile, creating systematic trader confusion.

> "This can completely give you a false perception of where things are right now" — IV Rank's reliance on 52-week extremes distorts context during outlier events.

## Candidate wiki links

**concepts:** [[implied-volatility-rank]], [[implied-volatility-percentile]], [[implied-volatility]], [[outlier-strategy-process]]

**securities:** [[tsla]]

## Regime / context

Recorded 20 August 2020, shortly after the March 2020 market crash. The video uses that dislocation as motivation for clarifying the IV Rank vs. Percentile distinction, which becomes most critical during high-volatility regimes. The Thinkorswim labeling error persists as a known platform quirk.
