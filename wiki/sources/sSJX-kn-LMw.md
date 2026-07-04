---
type: source
title: "Which SPX Strategy Works Best? 0 DTE vs 1 DTE (Detailed Analysis)"
video_id: sSJX-kn-LMw
url: https://www.youtube.com/watch?v=sSJX-kn-LMw
date: 2025-04-06
series: none
format: [education, analysis, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spx]
concepts: [zero-dte, days-to-expiration, delta, implied-volatility, volatility-term-structure, volatility-clustering, market-regimes, risk-management, compound-annual-growth-rate, max-draw-down, overnight-risk-premium, vega, short-volatility]
strategies: [zero-dte, short-premium, short-strangle, short-straddle, iron-condor, naked-short-selling]
saga: null
part: null
confidence: high
---

# Which SPX Strategy Works Best? 0 DTE vs 1 DTE (Detailed Analysis)

## Summary

A detailed backtested comparison of zero-DTE and one-DTE short-premium strategies on SPX from May 2022 through March 2025, revealing that naked short options outperform capped-risk spreads but underperform during volatility-expansion regimes. The analysis demonstrates that overnight volatility is mispriced in favor of sellers during declining-volatility periods, and that regime identification via VIX term structure is critical for strategy selection.

## Key takeaways

- **Zero-DTE naked strategies vastly outperform spread variants** [02:29–03:51]: Naked short strangles and straddles deliver higher compound annual growth rates than iron condors or ratio spreads, but with significantly higher max drawdown. Spread strategies cap upside by design.

- **2023 vs. 2024 regime split reveals volatility sensitivity** [03:51–05:16]: 2023 showed positive performance across all strategies during a broad volatility downtrend; 2024 turned negative as volatility expanded and spiked, demonstrating that zero-DTE strategies are regime-dependent and struggle when IV is rising.

- **Overnight volatility (1 DTE) is systematically underpriced except during expansion phases** [06:26–07:51]: One-DTE strategies underperformed zero-DTE across the full sample, but in 2024 (volatility-expansion period), overnight volatility actually outperformed intraday zero-DTE for naked strategies—a critical reversal.

- **VIX term structure monitoring is essential for regime detection** [05:16–06:26]: Compare VIX 1-day against VIX 3-month to identify transitory volatility phases. When volatility is steadily climbing (as in 2024), zero-DTE strategies deteriorate; when volatility is declining, they excel.

- **Entry time and delta selection matter for robustness** [01:11–02:29]: 15:00 ET entry (12:00 PT) was chosen for lower month-over-month variance, not optimization. Five-delta wings on spreads balance liquidity with risk capping; 50-delta / 15-delta iron condors offset enough risk to avoid mirroring naked positions.

- **A third, superior strategy exists but is teased for follow-up** [07:51]: The host hints at an undisclosed strategy that "grossly outperforms all of these across the board" and has been traded live for years.

## Notable quotes

> "If you're going to attempt to try and trade this kind of strategy from just an always do it perspective, you're going to underperform. There are periods where this works better than other periods." [05:16]

## Candidate wiki links

**concepts:** [[zero-dte]], [[days-to-expiration]], [[delta]], [[implied-volatility]], [[volatility-term-structure]], [[volatility-clustering]], [[market-regimes]], [[risk-management]], [[compound-annual-growth-rate]], [[overnight-risk-premium]], [[short-volatility]], [[vega]]

**strategies:** [[zero-dte]], [[short-premium]], [[short-strangle]], [[short-straddle]], [[iron-condor]], [[naked-short-selling]]

**securities:** [[spx]]

## Regime / context

This analysis spans May 2022 through March 2025, capturing two distinct volatility regimes: a declining-IV environment in 2023 (favorable for zero-DTE sellers) and a volatile, expanding-IV environment in 2024 (where overnight volatility became relatively attractive). The data is a hybrid of purchased SIBO data and backtesting. The host emphasizes that strategy selection must be regime-aware and that VIX term-structure monitoring is a prerequisite for live trading of these tactics.
