---
type: source
title: "Inside Vertical Spreads | Outlier Options Trading Beginner Lab"
video_id: ELLig97y0io
url: https://www.youtube.com/watch?v=ELLig97y0io
date: 2026-01-10
series: beginner-lab
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, qqq, tsm, ktos]
concepts: [vertical-spreads, delta, gamma, theta, vega, greeks, defined-risk, directional-bets, implied-volatility, expected-value, probability-of-touch, transaction-costs, capital-efficiency, risk-to-reward, profit-mechanism, volatility-term-structure, horizontal-spreads, calendar-spreads, diagonals, ratio-call-diagonal, leverage, margin]
strategies: [long-call-spread, long-put-spread, short-call-spread, short-put-spread, covered-call, ratio-call-diagonal, calendar-spreads]
saga: null
part: null
confidence: high
---

# Inside Vertical Spreads | Outlier Options Trading Beginner Lab

## Summary

Vertical spreads are a commonly misunderstood options strategy that traders often approach incorrectly. While they offer defined risk and capital efficiency, they are fundamentally directional bets—not volatility plays—and carry inherent negative expected value due to their structure and transaction costs. The session walks through the mechanics, P&L profiles, and practical scenarios where verticals can make sense, emphasizing that success requires a strong directional thesis rather than blind probability-based entry.

## Key takeaways

### Mechanics & Greeks
- **Vertical spreads flatten Greeks** [12:25]: When you buy and sell two options close in strike, you neutralize delta, gamma, theta, and vega relative to a naked short. A short 680 put (29 delta, −1 gamma, +12 theta, −81 vega) becomes a spread with 0.9 delta, −0.026 gamma, +0.025 theta, −1.163 vega.
- **Width matters** [13:35]: Narrow spreads (1–10 points) behave like traditional verticals; wider spreads behave increasingly like single options and expose more of the underlying move.
- **Verticals are directional, not volatility bets** [10:10]: High IV does not automatically favor selling; low IV does not automatically favor buying. The Greeks are flattened, so IV sensitivity is minimal.

### Expected Value & Probability
- **Verticals are negatively expectant by default** [22:47]: A typical 1-point-wide short put spread at 30 delta has 68% win probability (making $0.22) and 32% loss probability (losing $0.78). Expected value = (0.68 × 0.22) − (0.32 × 0.78) = **negative**.
- **Breakeven requires ~78% win rate** [27:24]: To achieve neutral expected value on this structure, you need a 78% probability of profit—a 10-point swing from the market-implied 68%.
- **Transaction costs are devastating** [31:11]: At $0.50 per leg, a 4-leg round trip (open 2 legs, close 2 legs) costs $2.00. On a $33 max profit, this is 6% drag, pushing the trade back into negative expectancy.

### Profit Mechanism & Directional Thesis
- **You must be directionally correct** [20:16]: Verticals require a strong directional hypothesis. Trading them purely on IV percentile or probability without directional conviction leads to losses.
- **Capped upside is the core weakness** [28:35]: Even if you are right and the underlying moves 4% (25 points in QQQ), a tight vertical captures only $22 of that move. Shares would capture the full move; a wider spread captures more but costs more.
- **One leg always drags** [37:36]: Even if you are right directionally, the long leg (if buying) or short leg (if selling) acts as a hedge and reduces profit. This is structural drag.

### When Verticals Make Sense
- **Earnings plays with margin constraints** [33:38]: If you want to sell an at-the-money straddle but lack margin, capping one or both sides with a vertical reduces capital requirement while accepting defined risk.
- **Explosive growth names** [34:38]: Buying a call-side wing (vertical) while selling naked puts can work if you have conviction that puts are overpriced and you want to cap tail risk on the upside.
- **Probability density analysis** [35:48]: Verticals of different widths can reveal where probability mass concentrates in the options chain—useful for market analysis, not necessarily for trading.

### Horizontal Spreads (Calendars & Diagonals)
- **Ratio call diagonals subsidize holding costs** [55:27]: Buy longer-dated calls; sell shorter-dated calls at a ratio that makes theta positive. This funds the long position while capping upside if the underlying rallies hard.
- **Trade relative volatility across terms** [58:47]: Buy options in one expiration, sell in another, to exploit term-structure kinks or relative mispricing.

### Account Size & Alternatives
- **Small accounts should avoid verticals** [38:36]: Instead of trading verticals, paper trade extensively and save capital. Once you have $25–50K, explore other methodologies that avoid the structural downsides.
- **Options are more capital-efficient than shares** [47:55]: Four 25-delta calls ($13,400) give the same 100-delta exposure as 100 shares ($32,500), but without the theta/vega drag of verticals.
- **Margin vs. trading with margin** [48:59]: Options provide baked-in leverage (trading *with* margin); shares on margin require borrowing (trading *on* margin) and incur daily borrow costs.

## Notable quotes

"Verticals are something that look really good. They make a lot of intuitive sense and in general, they absolutely suck." [06:26]

"The problem with vertical spreads is the way that they are understood. Most options traders think verticals are something that they are not." [06:26]

"If you do that, you lose." [26:28] (on trading verticals based purely on probability without directional conviction)

## Candidate wiki links

**concepts:** [[vertical-spreads]], [[delta]], [[gamma]], [[theta]], [[vega]], [[greeks]], [[defined-risk]], [[directional-bets]], [[implied-volatility]], [[expected-value]], [[probability-of-touch]], [[transaction-costs]], [[capital-efficiency]], [[risk-to-reward]], [[profit-mechanism]], [[volatility-term-structure]], [[horizontal-spreads]], [[calendar-spreads]], [[leverage]], [[margin]]

**strategies:** [[long-call-spread]], [[long-put-spread]], [[short-call-spread]], [[short-put-spread]], [[covered-call]], [[ratio-call-diagonal]], [[calendar-spreads]]

**securities:** [[spy]], [[qqq]], [[tsm]], [[ktos]]

## Regime / context

Recorded 2026-01-10 in a live beginner-focused education session. Market conditions (IV, underlying prices) are approximate and illustrative; the structural critique of verticals applies across regimes. The session emphasizes that vertical spreads are a tool with specific use cases, not a default strategy for small accounts or probability-based trading.
