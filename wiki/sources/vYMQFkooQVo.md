---
type: source
title: "Selling Puts vs Buy and Hold: Which Actually Wins?"
video_id: vYMQFkooQVo
url: "https://www.youtube.com/watch?v=vYMQFkooQVo"
date: "2026-10-18"
series: options-trench
format: [education, analysis, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy]
concepts: [short-put, covered-strangle, cash-secured-puts, delta, implied-volatility, time-decay, win-rate, upside-capped, downside-risk, volatility-risk-premium, put-skew, realized-volatility, compound-annual-growth-rate, drawdown, cash-management, margin-account, box-spread, variance-risk-premium, american-options, early-exercise]
strategies: [short-put, covered-strangle, cash-secured-puts, buy-and-hold, box-spread]
saga: null
part: null
confidence: high
---

# Selling Puts vs Buy and Hold: Which Actually Wins?

## Summary

This video compares the performance of selling 30-delta short puts (30 DTE to expiration) against buy-and-hold SPY from January 2007 to September 2026. While short puts exhibit an 84% win rate and smoother daily P&L volatility, they systematically underperform the index due to capped upside and asymmetric risk: the strategy captures full downside but loses delta participation on rallies. Over the full period, SPY delivered ~11% CAGR (terminal wealth $769k) versus ~4.41% CAGR for 30-delta puts ($234k), a $535k gap driven by the market's structural upward drift.

## Key takeaways

### Dated market read (2007–2026)
- **30-delta short puts: 84% win rate, but 4.41% CAGR vs. 11% for SPY** [00:00–01:23]
- **2020 COVID crash: short puts down 14% while market up 18%** [07:40] — full downside participation, but slower recovery due to delta decay on rallies
- **Terminal wealth gap: $535k difference** ($769k SPY vs. $234k 30-delta puts) [10:14]
- **Higher-delta puts (70-delta) nearly close the gap** — ~3 percentage point CAGR improvement, but with ~9 pp higher drawdown [11:29]

### Evergreen mechanics

- **Three profit vectors for short puts** [01:23]: time decay (theta), implied volatility contraction (vega), and directional upside (delta). Long equity has only two: price movement and dividends.
- **Daily P&L volatility is lower** [02:42] — smoother day-to-day returns than buy-and-hold, but this masks the long-term compounding drag.
- **Capped upside is the core trade-off** [03:56–05:13]: selling a put at 100 strike for $2 premium caps profit at $200 regardless of how far the underlying rallies; if SPY rises 20%, you forgo ~$800 of potential gain.
- **Asymmetric risk profile** [05:13–06:24]: average winning trade ~1.14% return; average losing trade ~4% — a 3.5× variance that requires consistent discipline to manage.
- **Delta decay on rallies** [06:24–07:40]: as underlying rises, put delta shrinks (30¢ → 25¢ → 22¢ per dollar move), so you underparticipate in the direction you want.
- **Volatility risk premium is insufficient** [11:29–12:41]: the rich premiums you collect (from put skew and general IV elevation) do not compensate for the directional delta drag over long periods.
- **Cash-secured puts in margin accounts should yield** [13:56–14:54]: deploying reserved capital into box spreads, ESGOV, or cash sweeps materially improves CAGR; leaving it idle is a hidden performance leak.
- **Targeting high-volatility entry windows does not solve the problem** [15:56]: selling only when IV is elevated adds liability (higher probability of downside moves) without sufficient premium uplift to close the SPY gap.

## Notable quotes

> "The markets tend to go up. That's kind of a problem for something like this because people like the margin of safety, they like the win rate, but then we don't fully appreciate the fact that things tend to go up." [03:56]

> "You get a small offset from your premium, but it doesn't compensate for what you end up experiencing from that downside move relative. It's just not a great compensation." [05:13]

> "I would not pick binarily. There's one of the reasons why I trade something called the covered strangle. It literally has a short-put component and it literally has an equity component for this exact reason." [10:14]

## Candidate wiki links

**concepts:**
[[short-put]], [[cash-secured-puts]], [[delta]], [[implied-volatility]], [[time-decay]], [[volatility-risk-premium]], [[put-skew]], [[realized-volatility]], [[compound-annual-growth-rate]], [[drawdown]], [[american-options]], [[variance-risk-premium]], [[upside-capped]], [[downside-risk]], [[win-rate]], [[margin-account]], [[box-spread]]

**strategies:**
[[short-put]], [[covered-strangle]], [[buy-and-hold]], [[cash-secured-puts]], [[box-spread]]

**securities:**
[[spy]]

**people:**
[[eric]]

## Regime / context

This analysis spans January 2007 through September 2026, encompassing the Global Financial Crisis (2008–2009), the post-GFC bull market, and the COVID-19 shock (March 2020). The 2020 drawdown is presented as a rare tail event; the presenter emphasizes not over-engineering for such scenarios, as the market's structural upward drift dominates long-term returns. The research uses SPY options (American-style, early-exercise-capable) and assumes mid-price fills and cash-secured put mechanics. Results are sensitive to delta selection, entry volatility regime, and whether reserved capital is deployed into yield-bearing instruments.
