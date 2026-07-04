---
type: source
title: "Revenge Trading, Strategy Analysis, Managing Deep ITM Short Calls - Skill Development"
video_id: iFxhd-PYW1Q
url: https://www.youtube.com/watch?v=iFxhd-PYW1Q
date: 2025-08-08
series: none
format: [education, live, strategy-breakdown]
experts: [eric]
mentions: []
securities: [pltr, hims]
concepts: [earnings-vol-play, implied-volatility, theta-decay, delta, vega, position-sizing, loss-aversion, process-over-outcome, trading-psychology, emotional-discipline, expected-move, volatility-term-structure, opportunity-cost, capital-efficiency, mark-to-market, tax-efficiency]
strategies: [short-straddle, covered-call, leaps, short-premium]
saga: null
part: null
confidence: high
---

# Revenge Trading, Strategy Analysis, Managing Deep ITM Short Calls - Skill Development

## Summary

A skill-development stream addressing two core trader challenges: exiting earnings straddles too early due to loss aversion and revenge trading, and managing deeply in-the-money short calls that have become uncapped liabilities. The session uses live volatility tracking on HIMS earnings to quantify how fast IV contracts post-earnings, then pivots to a real case study of a Palantir position with 11 tranches of short calls spanning 165–210 strikes, demonstrating how to make quantitative decisions about unwinding via rolling averages, tax-aware position restructuring, and LEAPS reallocation.

## Key takeaways

### Dated market read (2025-08-08)

- **HIMS earnings volatility decay** [09:00–45:00]: Tracked a short straddle entry at ~10.82 (sold at close on Aug 4) through the Aug 5 open. Within 2 minutes post-open, IV crush was ~19%; by 1 hour, ~47% of premium had evaporated despite the stock moving only ~$2. This demonstrates that early exits sacrifice significant theta decay—the profit mechanism itself.
- **Palantir position snapshot** [01:08:00–02:00:00]: Long 5,000 shares at avg basis $38; short calls across 11 tranches (165–210 strikes, mostly 2026–2027 expiry) with weighted avg strike ~$178. Current spot ~$182.20 = $721k position value, $200k residual profit if held to max. Probability of touching $210 over next 70 days: 79.4%; $250: 56%.

### Evergreen mechanics

- **Earnings straddle exit timing** [03:42–06:25]: The core issue is not knowing the optimal exit window. Solution: backtest your earnings plays across a large sample, track straddle price decay minute-by-minute for the first 30–60 min post-open, and build a profile. This removes guesswork and prevents loss-aversion-driven early exits.
- **Loss aversion and revenge trading** [04:07–06:49]: Early exits and attempts to "erase losses" signal incomplete detachment from trading capital. Prescription: (1) research the strategy deeply to know what's optimal; (2) emphasize process over outcome; (3) mentally penalize deviations from the researched plan.
- **Outlier losses cannot be disregarded** [05:02–07:23]: Do not exclude bad trades from analysis. Instead, use rolling-average P&L plots (e.g., 10-trade and 20-trade moving averages) to visualize whether strategy changes are working. Accept the ugly patches; contextualize them with a change log.
- **Managing deep ITM short calls** [01:08:00–02:00:00]: Start with "if no position, what do I want?" Then quantify the opportunity cost: current position value vs. residual profit vs. time locked up. Compare to alternative deployments (e.g., LEAPS). Use probability of touch and delta equivalence to make logical decisions. Example: 133 LEAPS at $185 strike (Jan 2027) cost $617k vs. $721k locked in covered calls; LEAPS offer 79% prob of $210 touch and uncapped upside.
- **Tax-aware unwinding** [01:58:00–02:00:00]: Selling a small tranche of shares (e.g., 700 shares = ~$100k) can neutralize the short-call liability while preserving the bulk of the position. Wash-sale rules allow this as long as no substantially identical position is re-established within 30 days. Mark-to-market election (for full-time traders) eliminates wash-sale constraints.

## Notable quotes

- "If we know what's optimal, then we know that the decision that we're making inherently will automatically get us back closer to where we want to be faster, no matter what." [48:25]
- "We don't get to get rid of the outliers. We simply get to take them in context." [51:44]
- "Options are fucking cool. Be an outlier." [02:00:55]

## Candidate wiki links

**concepts:** [[earnings-vol-play]], [[implied-volatility]], [[theta-decay]], [[delta]], [[vega]], [[position-sizing]], [[loss-aversion]], [[process-over-outcome]], [[trading-psychology]], [[emotional-discipline]], [[expected-move]], [[volatility-term-structure]], [[opportunity-cost]], [[capital-efficiency]], [[mark-to-market]]

**strategies:** [[short-straddle]], [[covered-call]], [[leaps]], [[short-premium]]

**securities:** [[pltr]], [[hims]]

**people:** [[eric]]

## Regime / context

Recorded 2025-08-08 during a Thursday skill-development stream (normally Patreon-only, opened to public due to community questions). Market context: strong rally in PLTR and broad equities; HIMS earnings on Aug 4–5 used as live case study. All numeric figures (share counts, P&L, prices, probabilities) are approximate due to ASR transcription; treat as illustrative rather than exact. Tax calculations assume second-highest federal bracket + state tax; individual results vary by jurisdiction and trader status (mark-to-market election status affects wash-sale applicability).
