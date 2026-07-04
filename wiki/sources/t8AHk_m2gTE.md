---
type: source
title: "Short Puts Going ITM? Here's How to Manage Them!"
video_id: t8AHk_m2gTE
url: "https://www.youtube.com/watch?v=t8AHk_m2gTE"
date: "2026-05-10"
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [btc]
concepts: [assignment, early-exercise, extrinsic-value, intrinsic-value, inventory-preference, rolling-options, spot-price-sensitivity, thesis-validation, unrealized-vs-realized-pnl]
strategies: [short-put, covered-strangle, rolling-options]
saga: null
part: null
confidence: high
---

# Short Puts Going ITM? Here's How to Manage Them!

## Summary

When a short put moves in-the-money, traders face four distinct management paths: close the position, roll it forward, take assignment, or pursue unassignment (close shares and re-enter puts). The optimal choice depends on thesis validation, inventory preference, assignment risk (measured by remaining extrinsic value), spot-price sensitivity, and expiration liquidity. Rolling is a system of accounting, not a mandatory response; closing losses cleanly is often underrated.

## Key takeaways

- **Four management choices** [00:27]: Close, roll, take assignment, or pursue unassignment. Each has distinct mechanics and tax/accounting implications.
- **Start with thesis validation** [00:52]: Ask whether your original directional view is still intact. If not, closing is often the cleanest path.
- **Inventory preference matters** [02:46]: Decide upfront whether you want to take on shares at the current strike or prefer a lower entry. This shapes all downstream decisions.
- **Measure assignment risk via extrinsic value** [03:10]: Deep ITM puts with <1% extrinsic value (or <15 cents on most underlyings) face meaningful early-assignment risk. Calculate intrinsic value (spot − strike) and subtract from option price to find remaining extrinsic.
- **Counterparty slippage logic** [04:31]: Large institutional counterparties may exercise early to avoid market slippage when acquiring size, even if it costs them extrinsic value.
- **Spot-price sensitivity trade-off** [06:25]: Taking assignment at a high strike when spot has crashed leaves you far from current price and limits call-selling upside. Rolling lets you adjust basis without adding capital.
- **Expiration liquidity constraint** [09:03]: Rolling too far out (e.g., 14 days → 42 days) can trap you in longer expirations with fewer future roll windows. Prefer rolling as little in time as possible.
- **Optimal roll timing** [10:12]: Best roll opportunities occur at-the-money (maximum extrinsic, minimum intrinsic). Waiting for deeper ITM increases intrinsic value you must buy back, making rolls harder.
- **Rolling does not require a credit** [12:40]: Track cumulative cash flow in/out. A roll that closes at a loss but opens at a smaller loss can still net positive overall.
- **Unassignment mechanics** [14:35]: Accept assignment, close the shares at current spot, realize the equity loss, then re-enter short puts at a lower strike. Useful for dollar-cost-averaging into a covered strangle when you expect further downside.
- **Covered strangle context** [01:37]: Deep ITM short puts within a broader covered strangle strategy may be managed aggressively to lower basis before taking assignment on a recovery.

## Notable quotes

> "Rolling is just a system of accounting." [15:56]

> "You do not have to roll for a credit for it to make sense." [13:04]

## Candidate wiki links

**concepts:** [[assignment]], [[early-exercise]], [[extrinsic-value]], [[intrinsic-value]], [[rolling-options]], [[unrealized-vs-realized-pnl]], [[thesis-validation]], [[spot-price-sensitivity]], [[inventory-preference]], [[delta]]

**strategies:** [[short-put]], [[covered-strangle]], [[rolling-options]], [[dollar-cost-averaging]]

**securities:** [[btc]]

**people:** [[eric]]

## Regime / context

Recorded 2026-05-10. Examples reference IBIT (Bitcoin spot ETF) during a recent drawdown campaign. The framework applies to any short-put position but is especially relevant for traders running covered strangles or systematic short-premium strategies. Expiration dates mentioned (15 May, 22 May, 18 June) are specific to the recording date and serve as illustration only.
