---
type: source
title: "Building an Options Portfolio | Options Trading for Beginners Pt10"
video_id: vDyL0Aff0gk
url: "https://www.youtube.com/watch?v=vDyL0Aff0gk"
date: "2024-08-17"
series: beginner-lab
format: [education, live]
experts: [eric]
mentions: []
securities: [spy, sso, hyg, xlu, xle, upstart, tgtx]
concepts: [reverse-planning, portfolio-first, position-sizing, risk-management, expected-value, probability-of-touch, delta-hedging, volatility-risk-premium, dollar-cost-averaging, capital-efficiency, disposition-effect, market-regimes, trend-identification, support-and-resistance, volume-profile]
strategies: [covered-strangle, short-premium, short-put, short-call, long-call, ratio-write]
saga: null
part: null
confidence: high
---

# Building an Options Portfolio | Options Trading for Beginners Pt10

## Summary

This session covers the foundational framework for constructing an options trading portfolio aligned with long-term financial goals. Eric walks through reverse planning (begin with the end in mind), portfolio allocation splits between core and speculative positions, and practical trade construction using expected-value analysis. The core thesis: define your annual return target, break it into monthly milestones, allocate capital to strategies that can hit those targets, and size individual trades to fit within portfolio risk constraints.

## Key takeaways

### Reverse planning & goal-setting
- **Begin with the end in mind** [02:39–03:02]: Start by defining your long-term financial target (e.g., $5M by age 50), then work backward to calculate required monthly savings and return rates.
- **Dollar-cost averaging as baseline** [17:33–18:55]: A $100/month savings into an S&P 500 index fund over 30 years roughly doubles your money; this is your "do nothing" benchmark.
- **Three wealth levers** [20:24–20:40]: (1) savings rate, (2) investment returns, (3) income growth. You cannot save your way to wealth alone; your money must work for you.

### Portfolio structure: core vs. speculative
- **80/20 split example** [44:02–44:54]: Allocate 80% to a systematic core strategy (e.g., covered strangle on SSO using 50-day moving average momentum) that targets ~20% annual return; reserve 20% (~$20K on a $100K account) for speculative trades to amplify returns.
- **Core allocation rationale** [44:25–44:54]: If your core alone hits 20% annually, you've already met a 15% portfolio target; the speculative 20% is pure upside.
- **Risk per trade** [45:22–45:44]: Cap individual trade risk at ~5% of total account value (e.g., $5K max loss on a $100K account) to ensure you can take multiple iterations.

### Trade construction & expected-value analysis
- **Surrogate option method** [13:34–14:50]: Mentally simulate how your options would look if the underlying moved $1 against you; use the options chain to estimate unrealized loss at that price level.
- **Probability of touch vs. in-the-money** [33:28–33:51]: Use probability of touch (not probability of in-the-money) to calculate expected value; this matters when you have hard stops.
- **Expected-value calculation** [01:02:19–01:03:14]: Multiply (probability of win × profit) + (probability of loss × loss) to determine if a trade is positively or negatively expectant before entry.
- **Analyze tab in thinkorswim** [01:32:02–01:33:51]: The y-axis is P&L, x-axis is underlying price; purple line = today's value, blue line = value at expiration; use probability analysis to see odds of hitting different price targets.

### Disposition & market context
- **Top-down approach** [37:34–37:54]: Start with your market view (bullish, bearish, neutral), then build positions that align with that disposition.
- **Avoid myopic single-stock focus** [26:24–27:27]: Trading only one stock (e.g., GME) limits agility; as a trader, your edge is the ability to pivot to what's working. Investors can buy what they like; traders must be flexible.
- **Sector weakness as opportunity** [01:06:23–01:06:47]: When broad indices are weak, scan for underperforming sectors (e.g., XLU, XLE) to find short-premium opportunities.

### Practical portfolio example (2016 backtest)
- **SSO + 50-day MA strategy** [43:18–43:40]: A simple momentum strategy (long SSO above 50-day MA, exit below) averaged ~20% annually over 10 years but had a rough 2022 (−40% drawdown).
- **Speculative allocation deployment** [49:14–01:05:08]: With $20K speculative capital, build multiple small positions (e.g., ratio put diagonals, iron condors, short premium spreads) that each target $200–$400 profit, stacking them to hit the $1,250/month goal.
- **Position management** [01:23:14–01:23:53]: Define position size and margin upfront; do not try to adjust or roll a losing trade to defend it. Either it hits your target or your stop; if stopped, move to the next trade.

## Notable quotes

> "The whole point of trading is agility. You can pivot to things that are working, that are not working, that have strength, that have weakness." [27:27–27:48]

> "If you don't know what you're aiming for, how on Earth are you going to hit it?" [24:16–24:20]

> "The portfolio is very individual to the trader." [03:58–04:19] (via the dog's non-verbal communication)

## Candidate wiki links

**concepts:**
[[reverse-planning]], [[portfolio-first]], [[position-sizing]], [[risk-management]], [[expected-value]], [[probability-of-touch]], [[dollar-cost-averaging]], [[capital-efficiency]], [[disposition-effect]], [[market-regimes]], [[trend-identification]], [[support-and-resistance]], [[volume-profile]], [[delta-hedging]], [[volatility-risk-premium]]

**strategies:**
[[covered-strangle]], [[short-premium]], [[short-put]], [[short-call]], [[long-call]], [[ratio-write]]

**securities:**
[[spy]], [[sso]], [[hyg]], [[xlu]], [[xle]], [[upstart]], [[tgtx]]

**people:**
[[eric]]

## Regime / context

Recorded 2024-08-17 (live session). The portfolio examples use 2016 as a hypothetical backtest year to avoid hindsight bias; the core concepts (reverse planning, allocation splits, expected-value trade sizing) are evergreen. This is Part 10 of the beginner-lab series; future sessions will shift to ad-hoc Q&A format based on viewer feedback rather than prescribed curriculum.
