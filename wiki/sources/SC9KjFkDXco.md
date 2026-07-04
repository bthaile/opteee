---
type: source
title: "Box Spread Trade Log"
video_id: SC9KjFkDXco
url: https://www.youtube.com/watch?v=SC9KjFkDXco
date: 2024-02-07
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spx]
concepts: [box-spread, annualized-return, risk-free-rate, yield-curve, capital-efficiency, return-on-invested-capital, transaction-costs, delta-neutral, european-style-options, cash-settled, position-sizing, trading-log]
strategies: [box-spread]
saga: null
part: null
confidence: high
---

# Box Spread Trade Log

## Summary

Eric walks through a complete spreadsheet tool for tracking long box spread positions on SPX, including annualized return calculations, yield curve integration, and fee impact analysis. The spreadsheet enables traders to compare box spread yields against the risk-free rate and monitor historical fills and P&L across multiple concurrent positions.

## Key takeaways

- **Box spread mechanics**: Long box spreads are a loan to the market; you pay a debit upfront and receive the fixed width of the strikes at expiration [00:43]
- **Strike selection**: Choose strikes with sufficient liquidity (avoid extremes with 56,000+ open interest concentration); balance width to minimize leg count while maintaining tradability [01:06–01:27]
- **European cash-settled options required**: Use SPX (not SPY) to avoid early assignment risk and forced stock delivery, which would break the fixed-profit structure [02:43–03:04]
- **Yield curve tool**: The spreadsheet includes a live yield curve to help select expiration dates; currently inverted (near-term higher yield than longer-dated) due to backwardation [03:30–04:15]
- **Risk-free rate matching**: Use the corresponding duration's risk-free rate (e.g., 5.42% for 38 DTE) to calculate net outperformance vs. lending alternatives [04:36–05:04]
- **Fee impact is critical**: At 50¢/leg × 4 legs, fees reduce annualized return from ~5.7% to ~5.68%; drag becomes severe on smaller positions [06:53–07:16]
- **Return on invested capital**: Calculate actual capital deployed (e.g., $994,000) vs. profit received ($5,880) to annualize and compare across trades [08:03–08:26]
- **Trade execution**: Work legs individually rather than as a spread to minimize slippage; track historical fills and entry strikes to optimize future entries [09:29–09:50]
- **Position tracking**: Move closed trades to a historical log to maintain clean active view and identify patterns in strike selection and timing [09:04–09:29]

## Notable quotes

> "European cash settled okay what fits that bill SPX why I typically use SPX" [03:04]

> "The reason why the fees matters so much in this case is because if we get rid of it take a look at the annual return right now it's 5681 it goes to 5701 that's a meaningful difference" [07:16]

## Candidate wiki links

**concepts:** [[box-spread]], [[annualized-return]], [[risk-free-rate]], [[yield-curve]], [[capital-efficiency]], [[return-on-invested-capital]], [[transaction-costs]], [[delta-neutral]], [[position-sizing]], [[trading-log]]

**strategies:** [[box-spread]]

**securities:** [[spx]]

**people:** [[eric]]

## Regime / context

Recorded 2024-02-07. Yield curve is noted as currently inverted (backwardated) relative to typical long-term structure—a temporary anomaly not suitable for long-term decision-making. The spreadsheet is designed for traders holding box spreads to expiration; adjustments needed if managing positions early.
