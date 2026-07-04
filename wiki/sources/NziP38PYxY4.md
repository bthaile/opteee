---
type: source
title: "Understanding How to Use Options to Get Long and Get Short | Outlier Options Trading Beginner Lab"
video_id: NziP38PYxY4
url: https://www.youtube.com/watch?v=NziP38PYxY4
date: 2026-01-17
series: beginner-lab
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy]
concepts: [profit-mechanism, time-frames, direction, expected-move, volatility, implied-volatility, delta, gamma, theta, extrinsic-value, liquidity-cycle, bid-ask-spread, order-flow, market-maker, position-sizing, risk-management, trading-plan, entry-exit-conditions, moneyness, leverage, capital-efficiency]
strategies: [long-call, short-put, covered-call, synthetic-long, vertical-spread]
saga: null
part: null
confidence: high
---

# Understanding How to Use Options to Get Long and Get Short | Outlier Options Trading Beginner Lab

## Summary

This educational session walks through a decision framework for using options to express directional trades (long or short). Starting from the assumption that you've already identified a trade idea and decided on direction, the video covers the critical questions to ask before selecting a specific option structure: profit mechanism, time frame, direction, severity of move, volatility, and liquidity. The core insight is that buying calls and selling puts both provide long delta exposure, but with fundamentally different risk profiles and Greeks—and the choice between them depends entirely on your expected profit mechanism and move size.

## Key takeaways

- **Decision framework before option selection** [04:47–05:21]: The outlier trade process assumes you've already analyzed your portfolio, determined market view, identified a trade idea, and decided direction. Only then do you ask: What is the profit mechanism? What's the time frame? What direction and severity of move do I expect? What's the volatility environment? What's the liquidity?

- **Profit mechanism drives structure choice** [12:24–13:45]: Long calls and short puts both make money as the underlying rises, but they have different Greeks and risk profiles. A breakout-upside profit mechanism typically favors long calls (uncapped upside) over short puts (defined risk but undefined downside). Compare the P&L at different move sizes to see which structure aligns with your expected move.

- **Long calls vs. short puts P&L comparison** [14:46–17:49]: In a 35-day window on a 5% up move, long calls made ~$1,400 vs. short puts ~$687. At 10% up, calls made ~$3,200 vs. puts ~$1,400. On downside, short puts cushion losses via credit received, but long calls have defined max loss while puts have undefined downside. This illustrates the trade-off: calls offer better upside capture; puts offer better downside cushion.

- **Expiration selection via liquidity and volatility** [24:58–29:46]: Don't pick expiration in isolation. First filter by open interest and bid-ask spreads to identify liquid expirations (e.g., 20 Feb, 20 March, 18 June for SPY). Then overlay implied volatility percentile and raw IV across those expirations. A 180-day expiration at 64% IV percentile may be preferable to front-month at 100% IV, depending on your account size and management plan.

- **Delta and strike selection via account constraints** [30:19–32:56]: Once you've narrowed expirations, check what strikes are liquid and what capital they require. A $25k account buying ATM calls (145 strike) at $2,230 per contract is reasonable; a $10k account is oversized. Your management plan (e.g., exit at 106 underlying = $500 loss) then determines if the position fits your risk tolerance. Never ask "what's the best option?" — ask "what fits my account, time frame, and expected move?"

- **Volatility is non-negotiable** [09:58–10:40]: Every time you touch an option, you must monitor volatility. It informs how you move through the entire decision process and can make or break a trade even if your directional view is correct.

- **Liquidity as a first-pass filter** [11:07–11:33]: Check liquidity early. If an underlying lacks sufficient liquidity, you already know you won't trade it. This is an efficient initial filter before diving into Greeks or structures.

- **Smaller, less-crowded names can offer edge** [21:53–22:38]: Retail traders often avoid illiquid names, but less competition can mean better edge for a given profit mechanism. Mega-cap options (AAPL, TSLA) have tighter spreads but higher competition; smaller names are "sloppy" but potentially less crowded.

- **Order execution: prioritize getting filled over penny-pitching** [37:42–47:31]: Don't obsess over trading at the exact midpoint. If you need to sell, look at the order book, see where liquidity sits, and be willing to give up a few cents to get a fill. Penny-pitching while the market moves can leave you worse off than accepting a slightly wider fill. Use market orders only as a last resort for risk control (e.g., hitting a stop).

- **Payment for order flow and order routing** [44:57–45:20]: Brokers using "best order routing" may batch and hold your order before sending it to the exchange, creating latency. Check your order book to see where your order was actually routed and whether it's being internalized or delayed.

- **Volatility framework applies to short volatility too** [54:28–54:51]: The same decision framework (profit mechanism → time frame → direction → severity) applies to trading volatility, not just directional moves. This is more nuanced and beyond beginner scope, but the structure is identical.

- **Synthetics and advanced structures require strategy analysis** [55:14–58:10]: Don't ask "when should I use a synthetic?" in isolation. Use the outlier strategy process: identify the profit mechanism first, then test whether a synthetic (or calendar, diagonal, etc.) is optimal for that specific mechanism versus alternatives like long ITM calls.

## Notable quotes

> "If you touch an option, you care about volatility. Period. That is all there is to it." [09:58–10:40]

> "The way that I figure out what option I'm going to end up with is by asking myself questions about what I think is going to happen." [54:09–54:28]

## Candidate wiki links

**Concepts:**
[[profit-mechanism]], [[time-frames]], [[direction]], [[expected-move]], [[implied-volatility]], [[delta]], [[gamma]], [[theta]], [[extrinsic-value]], [[liquidity-cycle]], [[bid-ask-spread]], [[order-flow]], [[market-maker]], [[position-sizing]], [[risk-management]], [[trading-plan]], [[entry-exit-conditions]], [[moneyness]], [[leverage]], [[capital-efficiency]], [[volatility]]

**Strategies:**
[[long-call]], [[short-put]], [[covered-call]], [[synthetic-long]], [[vertical-spread]]

**Securities:**
[[spy]]

**People:**
[[eric]]

## Regime / context

Recorded 2026-01-17. This is a beginner-focused educational session in the Outlier Options Trading Beginner Lab series. The framework and examples (using SPY) are evergreen; the specific option chains and prices shown are dated to early 2026 and should not be treated as current market data. The video assumes viewers have already completed the outlier trade process (portfolio analysis, market view, position sizing) and are now deciding how to express a directional trade using options.
