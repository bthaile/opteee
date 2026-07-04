---
type: source
title: "Simple Guide to Hedging with Options"
video_id: lAmVmdKT85k
url: https://www.youtube.com/watch?v=lAmVmdKT85k
date: 2025-08-10
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, spx, vix]
concepts: [delta, gamma, theta, vega, risk-management, hedging, direct-hedge, indirect-hedge, implied-volatility, delta-hedging, position-sizing, portfolio-first, risk-tolerance, expected-move, moneyness, volatility-term-structure, transaction-costs, opportunity-cost]
strategies: [covered-call, long-put, collar, short-call, iron-condor, short-strangle]
saga: null
part: null
confidence: high
---

# Simple Guide to Hedging with Options

## Summary

This video deconstructs retail hedging misconceptions and presents a framework for cost-effective risk reduction. Eric distinguishes between direct hedges (positions designed to lose money to offset primary position risk) and indirect hedges (speculative trades that incidentally reduce portfolio risk), then walks through portfolio-level and trade-level hedging mechanics, Greek analysis, and concrete examples showing how perpetual hedges create drag that often outweighs their protective benefit.

## Key takeaways

### Core framework
- **Direct vs. indirect hedging** [01:12]: Direct hedges are designed to lose money to offset primary position risk; indirect hedges are speculative positions that happen to reduce portfolio risk. The preferred outcome of a direct hedge is for it to lose while the primary position wins.
- **Three hedging levels** [03:30]: Portfolio-level hedging (attacking broad portfolio Greeks), trade-level hedging (protecting individual positions), and indirect hedging (building a balanced portfolio with natural risk smoothing).
- **Define the goal first** [05:55]: Specify what risk you're hedging (e.g., "protect through earnings"), measure acceptable loss (e.g., 20% vs. 40% drawdown), and build a management plan—not a perpetual hedge.

### Portfolio-level mechanics
- **Beta-weighted delta analysis** [08:15]: Normalize positions by beta-weighting deltas against SPX/SPY to determine notional exposure and identify excess risk. A portfolio with 1,025 beta-weighted SPY deltas has ~$640k notional exposure (not at-risk capital).
- **Indirect portfolio hedging** [09:34]: Instead of direct hedges, look for speculative trades with short beta-weighted deltas (e.g., selling calls in uncorrelated sectors like healthcare) to reduce long risk naturally.
- **Avoid VIX as a direct hedge** [10:43]: VIX is the 30-day implied volatility of S&P; its correlation to individual positions and magnitude of moves are unpredictable. Buying VIX calls is "lighting your money on fire."

### Trade-level hedging
- **Define specific risk** [12:00]: For a short strangle with 20% expected move vs. 21% implied move, buy an out-of-the-money call wing to cap upside risk if you deem that the primary threat, or convert to an iron condor if bidirectional risk exists.
- **The deductible concept** [18:37]: The deductible is the difference between your basis and the long put strike, plus the cost of the put. For 100 SPY shares at $625 with a $610 put costing $642, max loss is $2,142 (21.42 per share), but this creates ~1.03% drag over 46 days (~8% annualized).
- **Drag calculation** [19:49]: A 46-day hedge with 1.03% drag annualizes to ~8%, meaning you must return >9% annually just to break even on the hedge cost.

### Bad habits to avoid
- **Blank fear of risk** [14:19]: Hedging a 15% drawdown on a "long-term hold" signals you're in the wrong position or oversized; conflating time horizon with risk tolerance.
- **No exit plan** [15:25]: Failing to specify duration, delta offset, or management triggers leads to over-hedging, reduced profitability, and closing the hedge when it's most needed.
- **Poor Greek profile** [16:24]: Buying far out-of-the-money, far-dated options for a perpetual hedge creates low gamma and a huge deductible, making the hedge ineffective.
- **Short calls as hedges** [21:08]: Short calls offset minimal risk and often cap upside at a 1:1 ratio—a poor trade-off. Use them for premium collection, not primary hedging.

### Good habits
- **Simpler hedging** [17:25]: Retail traders have better tools: position sizing, scaling in/out, and indirect hedging. Reserve direct hedges for specific, time-bound risks (e.g., earnings in 6 days).
- **Collar strategy** [22:14]: Combine a long put and short call to offset downside cost, but recognize this creates a synthetic vertical that caps both upside and downside—only use if you want zero movement.
- **Risk is part of trading** [23:21]: Clearly define acceptable risk; scrubbing away all risk also scrubs away all returns.

### Numerical example: SPY long stock hedge [18:37–21:08]
- **Setup**: 100 SPY shares at $625; buy 46-DTE $610 put for $642 (30 delta).
- **Deductible**: $15 (625 − 610) + $6.42 cost = $21.42 max loss per share.
- **Drag**: 1.03% over 46 days ≈ 8% annualized.
- **P&L at +5% SPY move** (to $656): With hedge, +$2,600; without hedge, +$3,125 (−$525 opportunity cost).
- **Risk growth**: As SPY rises, the deductible grows (now $37.42 at $656), forcing costly adjustments.

## Notable quotes

> "If you can solve that [making money on both the hedge and the primary position], you've solved the market." [01:12]

> "Risk is part of trading. You have to clearly define the risk that you are comfortable with. And then if you're trying to scrub away all your risk, you are also scrubbing away all your returns." [23:21]

## Candidate wiki links

**Concepts:**
[[delta]], [[gamma]], [[theta]], [[vega]], [[risk-management]], [[hedging]], [[implied-volatility]], [[delta-hedging]], [[position-sizing]], [[portfolio-first]], [[risk-tolerance]], [[expected-move]], [[moneyness]], [[volatility-term-structure]], [[transaction-costs]], [[opportunity-cost]]

**Strategies:**
[[covered-call]], [[long-put]], [[collar]], [[short-call]], [[iron-condor]], [[short-strangle]]

**Securities:**
[[spy]], [[spx]], [[vix]]

**People:**
[[eric]]

## Regime / context

Recorded 2025-08-10. Evergreen educational content on hedging mechanics and cost-benefit analysis. Examples use SPY at ~$625 (approximate; live prices are illustrative). The framework applies across market regimes but is most relevant for traders holding directional positions or running premium-selling strategies during elevated volatility periods (e.g., earnings).
