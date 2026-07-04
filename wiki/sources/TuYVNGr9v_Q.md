---
type: source
title: "Practical Look At Rolling Options"
video_id: TuYVNGr9v_Q
url: https://www.youtube.com/watch?v=TuYVNGr9v_Q
date: 2026-05-31
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: []
concepts: [rolling-options, realized-vs-unrealized-pnl, assignment, short-put, moneyness, profit-mechanism]
strategies: [short-put, rolling-options]
saga: null
part: null
confidence: high
---

# Practical Look At Rolling Options

## Summary

This video walks through a concrete example of rolling a short put position down and out, demonstrating how to calculate realized and unrealized P&L when closing one strike and opening another. The key insight is that rolling does not require a net credit to be profitable—what matters is tracking cumulative cash flow in and out of the position.

## Key takeaways

- **Realized vs. unrealized P&L in a roll** [00:00–00:20]: When you close a losing short put (e.g., sold at $1.00, bought back at $2.00), you lock in a $100 realized loss. Opening a new short put at a lower strike (e.g., $1.50 credit) creates a new unrealized profit potential; the net cumulative flow determines whether the roll is profitable.
- **Rolling does not require a credit** [00:39–00:53]: A common misconception is that you must roll for a net credit. In the example, closing at $2.00 and opening at $1.50 is technically a debit roll, yet the cumulative cash flow (–$100 realized + $150 new credit) nets to +$50 profit. Track total money in and out, not the individual leg.
- **Cumulative cash-flow accounting** [00:53]: The discipline is to sum all credits and debits across the entire position lifecycle, not to judge each roll in isolation.

## Notable quotes

- "You do not have to roll for a credit for it to make sense. I closed this for two, I opened this for a $1.50, I opened this for less than this, but I still net out positive. What you have to do is just track the cumulative flow of money in and out."

## Candidate wiki links

**concepts:** [[rolling-options]], [[realized-vs-unrealized-pnl]], [[assignment]], [[short-put]], [[moneyness]], [[profit-mechanism]]

**strategies:** [[short-put]], [[rolling-options]]

## Regime / context

Dated 2026-05-31. This is a mechanics-focused education video with no market-specific context or dated regime assumptions. The rolling framework applies across all market conditions and volatility regimes.
