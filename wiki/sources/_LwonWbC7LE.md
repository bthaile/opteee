---
type: source
title: "Portfolio Management Fundamentals — Goal Setting & Risk Framework"
video_id: _LwonWbC7LE
url: https://www.youtube.com/watch?v=_LwonWbC7LE
date: null
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, xlv, xlc, xlk, xlb, xlv, exc, exc, lmt, noc, pltr]
concepts: [portfolio-first, risk-management, position-sizing, expected-value, max-drawdown, delta, theta, vega, beta, market-regimes, disposition-effect, process-over-outcome, trading-plan, expected-return, annualized-return, compound-annual-growth-rate, volatility-risk-premium, delta-hedging, delta-neutral, sector-rotation, tariffs, market-breadth, trend-identification]
strategies: [covered-strangle, short-premium, vertical-spread, ratio-call-diagonal, short-put]
saga: null
part: null
confidence: high
---

# Portfolio Management Fundamentals — Goal Setting & Risk Framework

## Summary

This video walks through the foundational process of portfolio management: defining clear portfolio-level goals (return target, volatility tolerance, consistency requirement), then building and sizing individual trades to align with those goals. The host demonstrates a live example using a $25,000 account targeting 15% annual return, showing how to construct a multi-strategy portfolio using beta-weighted delta analysis, position sizing within risk tolerance, and trade-level expected-value calculations to hit monthly dollar targets while respecting portfolio circuit breakers.

## Key takeaways

### Portfolio goal-setting (foundational)
- **Define three core metrics** [16:52–21:14]: percent return target, volatility measure (max drawdown), and consistency (monthly vs. average over time). These three buckets inform every downstream decision.
- **Reconcile trade-offs explicitly** [24:07]: higher return requires higher involvement, lower consistency, and higher volatility. Identify which you're willing to sacrifice.
- **Avoid the "5% per month" trap** [18:30–29:29]: a $300K portfolio targeting $5K/month requires ~48% annualized return—industry-leading and inconsistent. Clarify whether you want that return *every* month or *on average* over 36 months; the answer changes everything.
- **Capital efficiency matters more than you think** [29:29–34:55]: a smaller account with a realistic 15% annual return, combined with consistent monthly savings, compounds to $1M+ over 20 years. Chasing 30% returns on $25K yields only $7.5K/year—not worth the risk.

### Disposition stage (macro context)
- **Start with economy, not individual tickers** [11:35–15:33]: understand tariff landscape, GDP growth/contraction, and sector trends before picking trades. This creates a disposition (bias) that informs all subsequent decisions.
- **You don't need to be an economist** [11:35]: know enough to recognize impact (e.g., tariffs → automotive risk) without mastering all details.

### Portfolio construction & sizing
- **Use a simple tracker** [57:22–01:17:45]: list each trade with risk (dollars and % of portfolio), return target, win probability, and expected value. Sum portfolio-level delta, theta, vega, and beta-weighted delta to ensure alignment with goals.
- **Cap individual trade risk** [55:50–57:22]: for a $25K account, keep single-trade risk under 2–3% of portfolio. This example uses 1.36% per trade, capping total portfolio risk at 3%.
- **Beta-weight against SPY** [01:10:27–01:20:19]: calculate how each position's delta behaves relative to the broad market. If you want to be net long, ensure your delta-weighted portfolio reflects that; avoid delta-neutral "fence-sitting" unless it serves your goal.
- **Manage duration** [01:18:50–01:20:19]: avoid clustering all positions in one expiration; use diagonals or longer-dated calls to spread risk across time.

### Trade-level analysis
- **Calculate expected value** [01:03:36–01:08:59]: win probability × win amount − loss probability × loss amount. A 88% win rate on $100 profit vs. 12% loss on $5,200 is deeply unprofitable (negative EV). Reject it, even if it "feels" high-probability.
- **Theta decay erodes high-probability trades fast** [01:07:05]: a zero-DTE long strangle with 88% win probability loses that edge within hours as theta bleeds; the breakeven expands, flipping the trade negative.
- **Manage jump risk via avoidance and sizing** [01:24:17–01:25:43]: avoid earnings or geopolitical events; use historical worst-case moves (e.g., 20-point jump in PLTR) to set hard stops and confirm position size is tolerable.

### Real example walkthrough
- **$25K account, 15% annual goal = $313/month target** [47:41–51:57]: break the annual goal into monthly dollars to make it concrete.
- **EXC vertical spread** [53:13–57:22]: $1-wide call spread, 34 DTE, 65% probability of expiring OTM, risking $340 (1.36% of portfolio), targeting $160 profit.
- **LMT call spread** [01:12:57–01:15:58]: $5-wide spread, 75% win probability, risking $295 (1.1% of portfolio), targeting $205 profit. Positive expected value.
- **PLTR diagonal** [01:18:50–01:22:48]: 90-day call diagonal, max risk ~$800 (3.2% of portfolio), max profit $912 at expiration. Manage downside at 63 strike.
- **Portfolio summary** [01:17:45–01:20:19]: three trades, ~$635 total capital deployed (2.5% of portfolio), net short ~0.5 delta, long theta, short vega. Healthy alignment with goal.

## Notable quotes

> "The entire purpose of the disposition stage is to give you context around different things because when we click down one level to the portfolio, now we're looking at based on my current analysis of the landscape, what am I holding and does it align with my current analysis of the landscape." [15:33]

> "The difference between a 10% and a 15% return over a 20 year time frame is the difference between $168,000 versus $409,000." [49:12]

> "If you're okay with a little more volatility in your returns, then sure, it definitely becomes possible. But the other thing people don't account for is unfortunately, tax man." [33:23]

## Candidate wiki links

### Concepts
[[portfolio-first]], [[risk-management]], [[position-sizing]], [[expected-value]], [[max-drawdown]], [[delta]], [[theta]], [[vega]], [[beta]], [[market-regimes]], [[disposition-effect]], [[process-over-outcome]], [[trading-plan]], [[expected-return]], [[annualized-return]], [[compound-annual-growth-rate]], [[delta-hedging]], [[delta-neutral]], [[sector-rotation]], [[tariffs]], [[trend-identification]]

### Strategies
[[covered-strangle]], [[short-premium]], [[vertical-spread]], [[ratio-call-diagonal]], [[short-put]]

### Securities
[[spy]], [[exc]], [[lmt]], [[noc]], [[pltr]]

### People
[[eric]]

## Regime / context

This is a foundational education video on portfolio architecture and goal-setting, not a market-specific analysis. The live example uses current market conditions (tariff discussion, sector rotation themes) as context, but the framework is evergreen. The video assumes familiarity with options Greeks and basic strategies; it is intermediate-to-advanced in scope.
