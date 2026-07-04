---
type: source
title: "The Wheel Strategy: How to Maximize Returns"
video_id: FRbKRktUDzA
url: https://www.youtube.com/watch?v=FRbKRktUDzA
date: 2025-10-12
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy]
concepts: [capped-upside, delta, delta-hedging, profit-mechanism, risk-management, theta-decay, trend-following]
strategies: [the-wheel, covered-call, short-put, ratio-write, covered-strangle]
saga: null
part: null
confidence: high
---

# The Wheel Strategy: How to Maximize Returns

## Summary

The wheel strategy—selling cash-secured puts, taking assignment, then selling covered calls—is mechanically sound but systematically caps upside and misleads traders into underperformance. Two concrete improvements: manage short puts via delta bands (rather than arbitrary profit targets) to capture directional moves, and sell calls at a ratio (e.g., 2-to-3 or 1-to-3 against long shares) to preserve upside participation. A superior variant, the covered triangle, combines long shares with short puts and ratio calls simultaneously, enabling dynamic scaling and trend-following exits.

## Key takeaways

- **The wheel's core weakness: capped upside.** Selling puts gives you defined profit but undefined loss; selling calls against assigned shares caps gains. If the underlying rallies, you capture only 20–30 cents per dollar of move, missing 70–80 cents of profit [02:50–05:35].

- **Delta-band management beats arbitrary targets.** Instead of closing at "50% profit in X days," set a delta floor (e.g., 25 delta) and roll back to your starting delta (e.g., 30 delta) whenever breached. This keeps you in the trade during rallies and captures directional moves [04:15–05:35].

- **Sell calls at a ratio, not 1:1.** If assigned 300 shares, sell 2 calls instead of 3. Calculate the breakeven: if max profit is $5,136 on a 3-lot, a 2-lot needs only ~5% upside to match it. In strong rallies, go to a 1-lot [06:51–08:21].

- **The covered triangle: simultaneous long shares + short puts + ratio calls.** Buy 200 shares, sell 1 put, sell 1 call. This distributes the same ~300-share exposure without capping upside. Add trend-following stops and scale in/out based on market regime [08:21–11:02].

- **Rolling is more flexible with ratio calls.** If a short call is breached massively, you can add more size (more long shares) rather than rolling out-and-up, which ties up capital and preserves the ceiling [11:02].

## Notable quotes

> "If the stock goes up by a dollar, your option, your short put to be specific is only increasing by 30 cents. So you're missing 70 cents that the underlying made." [04:15]

> "Rather than using these arbitrary x% profits and y% time, we can literally just say whenever my option falls below a set delta, I'm going to move myself back to a 30 delta." [05:35]

## Candidate wiki links

**Concepts:**
[[capped-upside]], [[delta]], [[delta-hedging]], [[profit-mechanism]], [[risk-management]], [[theta-decay]], [[trend-following]], [[position-sizing]]

**Strategies:**
[[the-wheel]], [[covered-call]], [[short-put]], [[ratio-write]], [[covered-strangle]], [[rolling-options]]

**Securities:**
[[spy]]

## Regime / context

Recorded 2025-10-12. Applies to any bullish-to-neutral regime where the wheel is deployed. The delta-band and ratio-call improvements are evergreen mechanics; the covered-triangle variant is a natural progression for traders seeking to reduce upside cap without abandoning the wheel's simplicity.
