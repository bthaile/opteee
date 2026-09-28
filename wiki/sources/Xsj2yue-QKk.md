---
type: source
title: "Kelly Criterion vs. Intuition: How to Actually Size Your Trades | The Options Trench"
video_id: Xsj2yue-QKk
url: https://www.youtube.com/watch?v=Xsj2yue-QKk
date: 2026-09-25
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: []
concepts: [kelly-criterion, bankroll-management, bet-sizing, position-sizing, expected-value, volatility, skew, risk-management, compounding, log-wealth, edge, portfolio-construction, correlation, volatility-risk-premium, tail-risk, probability-of-profit]
strategies: [kelly-criterion, fractional-kelly, position-sizing, risk-budgeting, portfolio-first]
saga: null
part: null
confidence: high
---

# Kelly Criterion vs. Intuition: How to Actually Size Your Trades | The Options Trench

## Summary

This episode explores the Kelly Criterion as a mathematical framework for optimal bet sizing to maximize long-term compounded wealth. Eric and Chris walk through the formula's application across binary outcomes (sports betting, insurance decisions) and continuous trading scenarios, emphasizing critical pitfalls: Kelly's sensitivity to volatility (which masks tail risk in premium-selling strategies), the danger of overestimating edge, and the practical superiority of fractional Kelly (half or quarter) for real-world trading where assumptions are uncertain.

## Key takeaways

### Foundational mechanics
- **Kelly formula (binary)** [06:06]: `(P − Q) / B`, where P = win probability, Q = loss probability, B = odds/return ratio. For even-money bets, this simplifies to `P − Q`.
- **The Haghani study** [04:51]: Educated investors given a 60/40 coin flip with real money mostly overbetted and blew up accounts; Kelly prescribes 20% of bankroll per flip.
- **Compounding principle** [03:45]: Kelly solves "how much of your bankroll to bet to maximize compounded wealth"—betting everything on any single edge destroys long-term growth if you lose once.

### Application across scenarios
- **Even-money bet (60% edge)** [07:06]: Bet 20% of bankroll per flip.
- **Getting odds (Bills Super Bowl at 13¢)** [09:22]: If you assess 18% win probability vs. market's 13%, Kelly prescribes ~5.7% of bankroll.
- **Laying odds (Bills AFC East favorite at 1.4x return)** [10:37]: If you assess 80% win probability, Kelly prescribes ~30% of bankroll—more than the underdog scenario despite equal edge, because Kelly penalizes volatility in the underdog case.
- **Insurance/self-insurance** [14:23]: A $500k home with $3k annual premium and 1-in-500 loss probability yields Kelly sizing of ~66% of home value; decision to insure depends on total net worth relative to that bet size.

### Critical pitfalls
- **Correlation blindness** [20:57]: Applying Kelly independently to each position (short put spread in SPX, strangle in QQQ) ignores correlation overlap; use portfolio-aware Kelly instead.
- **Volatility masks tail risk** [23:23]: A low-volatility asset with rare 50% crashes has lower realized vol than a 1.5% daily mover, so Kelly underestimates true risk; options skew reveals the hidden tail, but Kelly formula does not.
- **Premium sellers' trap** [25:51]: Selling far OTM options feels low-vol and "wins every week," but Kelly will massively oversize you because it only sees realized volatility, not tail probability.
- **Edge uncertainty** [27:12]: If your true edge is half what you think, full Kelly compounds at zero; even a 50% error in edge estimate is plausible in options trading (thinking 4¢ when it's 2¢).

### Fractional Kelly as practical solution
- **Half Kelly** [18:21]: Cuts growth rate by ~25% but cuts risk faster; yields 75% of optimal growth at half the risk.
- **Quarter Kelly** [29:18]: Remains healthy even if edge is 50% or 75% wrong; provides "room to maneuver" in imperfect markets.
- **Why practitioners avoid full Kelly** [28:24]: Markets shift, information is incomplete, edge estimates have wide error bars; fractional Kelly adds a "fudge factor" for unknown unknowns.

### Portfolio-level thinking
- **Three lenses** [02:25]: Individual trade, strategy, and portfolio perspectives; portfolio view accounts for correlations between positions.
- **Asymmetry in odds** [11:47]: Kelly tells you to bet more on favorites than underdogs with the same edge because it penalizes the higher volatility of the underdog scenario.

## Notable quotes

> "Kelly is a solution to the problem of what is the amount to bet to maximize your compounded wealth." [03:45]

> "If you bet everything on a coin flip and lose, even if you had an advantage on the coin flip, you're out of the game and there will be no compounding of your wealth." [04:51]

> "Kelly will completely encourage you to bet way more than you can afford to lose in that sense" (on premium selling). [25:51]

## Candidate wiki links

**concepts:** [[kelly-criterion]], [[bankroll-management]], [[bet-sizing]], [[position-sizing]], [[expected-value]], [[volatility]], [[skew]], [[risk-management]], [[compounding]], [[log-wealth]], [[edge]], [[portfolio-construction]], [[correlation]], [[volatility-risk-premium]], [[tail-risk]], [[probability-of-profit]], [[fractional-kelly]], [[volatility-term-structure]], [[implied-volatility-skew]]

**strategies:** [[kelly-criterion]], [[fractional-kelly]], [[position-sizing]], [[risk-budgeting]], [[portfolio-first]], [[premium-selling]], [[short-premium]]

**people:** [[eric]]

## Regime / context

Recorded 2026-09-25. This is a foundational education piece on bet sizing applicable across all market regimes. The examples (Bills Super Bowl odds, homeowners insurance) are illustrative; the mathematical principles are regime-independent. The emphasis on fractional Kelly and edge uncertainty reflects a post-2008 risk-management mindset and is particularly relevant for retail options traders operating with limited capital and imperfect information.
