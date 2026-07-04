---
type: source
title: "Complete Ratio Call Diagonal Option Strategy Guide"
video_id: JJv88Q2HbNM
url: https://www.youtube.com/watch?v=JJv88Q2HbNM
date: 2024-08-31
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [nvda, russell-2000]
concepts: [delta, theta, gamma, extrinsic-value, intrinsic-value, implied-volatility, moneyness, days-to-expiration, leverage, capital-efficiency, position-sizing, risk-management, technical-analysis, support-and-resistance, trend-following, profit-mechanism, expected-return, probability-cone]
strategies: [ratio-call-diagonal, long-call, short-premium, scaling-in, scaling-out]
saga: null
part: null
confidence: high
---

# Complete Ratio Call Diagonal Option Strategy Guide

## Summary

The ratio call diagonal is a bullish, directional options strategy designed as an equity replacement. It combines long deep in-the-money calls (60+ DTE, 60+ delta) with short out-of-the-money calls (under 40 DTE, ~30 delta) in a ratio that preserves upside exposure, optionally layering in high-gamma kicker options for convexity. The strategy manages theta decay through time and moneyness selection while using technical analysis to size positions and define exit levels.

## Key takeaways

- **Core structure** [00:25–02:16]: Long deep ITM calls (60+ DTE, 60+ delta) form the base; short OTM calls (under 40 DTE, ~30 delta) offset theta; optional kicker calls add gamma exposure. Ratio is typically 10 long to 3–5 short to avoid capping upside.

- **Why deep ITM long calls** [01:25–06:37]: Higher delta (70–80) means better dollar-for-dollar movement with the underlying; deeper ITM reduces extrinsic value and theta bleed. Trade-off: higher upfront cost, but managed via position sizing and technical stops.

- **Theta decay optimization** [03:45–07:46]: 60+ DTE minimizes theta decay rate; further OTM short calls (under 40 DTE) collect credit to offset long-call theta. At 65 DTE, theta decays ~9¢/day; at 190 DTE, ~5¢/day; at 37 DTE, ~13¢/day.

- **Leverage and capital efficiency** [11:22–12:41]: Controlling ~710 shares via 10 long calls (71 delta each) costs ~$21,000 vs. $117,000 for 1,000 shares; delta-adjusted exposure is lower but capital requirement is a fraction.

- **Kicker options (high-gamma add-on)** [13:32–15:07]: Sold at 20–37 DTE with 30–32 delta; theta decay is steep (12–22¢/day on $2–4 options), so only add with strong conviction. Gamma compounds massively but requires active management.

- **Short call management** [15:46–24:36]: Collect credit to offset theta (e.g., $385 per contract covers ~5 days of long-call theta). Roll out and up if they fall ITM; alternatively, sell long calls to cover the cost of closing short calls. Never let short deltas exceed long deltas (critical strike formula prevents upside loss-lock).

- **Critical strike formula** [28:34–31:16]: `(Long basis − Current long value) / Long delta + Current stock price` ensures short calls don't lock in losses. Number of short lots = (Long lots × Long delta) / Short delta, capped to preserve upside.

- **Product selection** [20:47–22:22]: Requires liquid underlyings (S&P 500 stocks, ETFs, sector ETFs) with strong option chains. Avoid bottom-fishing; trade things showing strength and moving in your direction.

- **Position management via technical analysis** [25:15–28:02]: Define support (floor) and resistance (targets) using volume nodes, trend lines, or other TA. Size position so downside loss and upside gain align with portfolio risk/reward. Use probability cone to assess likelihood of hitting targets.

- **Real trade example: Russell 2000** [34:29–40:13]: Bought 10 Sep 2050 calls (70+ delta) on 11 July breakout; sold 5 Aug 2350 calls (30 delta) on 17 July when momentum slowed; scaled in 3 more calls on 22 July after pullback; unwound in tranches as support broke. Final result: $76K profit (63% ROIC) on $121K initial outlay.

## Notable quotes

> "The goal of this video is to refresh what you've heard, maybe integrate some new data points, and then walk you through holistically how the strategy works." [00:00]

> "I do not want to lose money if I'm too right." [20:00]

> "The short calls are secondary to the long calls. So you don't have to automatically put them on at the same time." [35:40]

## Candidate wiki links

**Concepts:**
[[delta]], [[theta]], [[gamma]], [[extrinsic-value]], [[intrinsic-value]], [[implied-volatility]], [[moneyness]], [[days-to-expiration]], [[leverage]], [[capital-efficiency]], [[position-sizing]], [[risk-management]], [[technical-analysis]], [[support-and-resistance]], [[trend-following]], [[profit-mechanism]], [[expected-return]], [[probability-cone]]

**Strategies:**
[[ratio-call-diagonal]], [[long-call]], [[short-premium]], [[scaling-in]], [[scaling-out]]

**Securities:**
[[nvda]], [[russell-2000]]

**People:**
[[eric]]

## Regime / context

Recorded 31 August 2024. The strategy is evergreen and regime-agnostic, though the Russell 2000 example (11 July – 1 August 2024) reflects a breakout-and-pullback environment typical of summer consolidation. The video emphasizes that ratio call diagonals are designed for trending markets where the underlying shows strength; they are not suitable for choppy, range-bound conditions or bottom-fishing scenarios.
