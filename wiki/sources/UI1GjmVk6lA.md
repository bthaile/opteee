---
type: source
title: "Trade Execution and Strategy Review | Outlier Pro Skill Development"
video_id: UI1GjmVk6lA
url: https://www.youtube.com/watch?v=UI1GjmVk6lA
date: 2026-10-16
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [mos, pg, pm, tcom, hims, mci, mrvl, amd, spy, spx, iwm, qqq]
concepts: [range-breakout, trade-execution, profit-mechanism, position-sizing, portfolio-fit, delta-selection, liquidity-analysis, time-decay, volatility-management, kelly-criterion, risk-management, stress-testing, distribution-analysis, trade-expression, discretionary-trading, quantitative-analysis, performance-analysis, drawdown-management, tail-risk, win-rate]
strategies: [short-put-spread, long-call, synthetic-short, directional-trading, range-breakout, premium-selling, vertical-spread, position-management]
saga: none
part: null
confidence: high
---

# Trade Execution and Strategy Review | Outlier Pro Skill Development

## Summary

Eric walks through recent discretionary range-breakout trades (Mosaic, PG, PM, TCOM) and earnings-driven positions (Hims, Mastercard, Marvell, AMD), detailing the outlier trade process from market scanning through position management. He then provides detailed feedback on a community member's one-day short put spread strategy, emphasizing the need for broader testing across delta, DTE, and trade expressions before committing to a specific structure.

## Key takeaways

### Trade Execution & Discretionary Positions

- **Range-breakout scan methodology** [14:52]: Identifies securities trading within defined ranges (using trailing highs/lows) that break out on elevated volume relative to 20-day average; filters for liquidity and catalyst confirmation.
- **Mosaic (MOS) entry** [23:24]: Bought 20 Nov 75 calls at ~135–136 after range breakout; 5–6 day expected hold; soft target near 72–73 volume node; hard stops below 67.80 (volume support) and initial soft stop below open.
- **Position sizing discipline** [25:48]: Speculative positions sized at ~0.25% of portfolio; tight stops (2.1% average daily range) create high probability of being stopped out; asymmetric payoff structure prioritizes fast losses over slow gains.
- **Earnings as time constraint** [28:19]: Mosaic earnings on 29th creates hard deadline; no earnings perspective in options chain, so position management via price action and time catalyst only.
- **PG and PM trades** [29:37]: Same range-breakout logic as Mosaic; PM has earnings on 21st (closer constraint); both locked in at scratch/near-breakeven after recent pullbacks.
- **TCOM downside synthetic short** [31:57]: Illiquid options (30–60 cent spreads) managed via synthetic shorts (short call + long put) to balance liquidity across strikes; stopped out 9th on strong rally; ~0.25% portfolio risk.
- **Hims premium anomaly trade** [34:36]: Sold expensive 20 Nov puts at ~120; exited next day at 65 after 8.7% underlying move (50% loss on option despite directional correctness); illustrates leverage nonlinearity.
- **Mastercard range breakout + premium anomaly** [35:44]: Long shares on range breakout; up ~7.5%; earnings constraint forces shorter hold duration due to earnings season overlap.
- **Marvell long-dated calls** [38:06]: Bought Jan 2028 300 calls at 54, sold at 72 on 12th Oct (50% return); longer duration allowed to avoid earnings; exited on close below 10-period MA.
- **AMD short put spread** [39:25]: 16 Oct 55/540 short put spread sold at 145; now trading at 183 (profitable but volatile); underlying down 7.12%, IV up 7.3%; expires tomorrow; sit-and-wait management.

### Strategy Review Feedback (Lost Hiker's One-Day Short Put Spread)

- **Trade in SPX, not SPY** [42:12]: SPX offers better tax treatment (Section 1256, cash-settled) and no partial assignment risk; equally liquid.
- **Profit mechanism is sound** [43:23]: Dominantly long delta (bullish drift); narrow spread captures index upside with minimal vega exposure; completely viable.
- **Trade expression too narrow** [46:05]: Testing only 20-delta put and 16.5-delta put spread is premature; should grid across multiple delta widths (5, 10, 11 deltas) and multiple DTE to understand surface before optimizing.
- **Missing distribution analysis** [50:19]: Need streak data (avg winning/losing streaks, max streaks, frequency of near-max-drawdown events) to distinguish between one-off extremes and recurring tail risk; informs sizing decisions.
- **Kelly sizing guidance** [51:42]: Do not use full Kelly; build grid across full Kelly, 3/4 Kelly, 1/2 Kelly, 1/4 Kelly; final sizing likely 3–6 Kelly depending on tail frequency (intuitive estimate, not precise).
- **Performance reporting expansion** [50:19]: Add distribution of returns, win/loss streaks, and frequency of near-drawdown events; current summary (CAGR, max DD, Sharpe) lacks fidelity for risk decisions.
- **Stress testing is strong** [55:49]: Injecting full losses at 2× observed frequency and expanding worst periods is good; validate frequency assumptions against actual distribution before finalizing multiplier.
- **Avoid SPY comparison** [57:29]: Comparing to buy-and-hold SPY is common but unhelpful; compare instead to risk-free rate and multiples thereof; SPY and strategy are different instruments.
- **Forward testing across ETFs** [01:02:45]: Testing on SPY, IWM, QQQ is reasonable for robustness check, but recognize high correlation; max drawdown may be understated if combined; profile profit mechanism separately on each before combining.

## Notable quotes

- "The profit mechanism here is a range breakout and then thus the expectation of a continuation over some duration." [17:19]
- "Leverage giveth and leverage taketh. That's why you have to plan very carefully." [34:36]
- "Kelly is always a ceiling. It's not a target." [51:42]

## Candidate wiki links

**concepts:** [[range-breakout]], [[trade-execution]], [[profit-mechanism]], [[position-sizing]], [[portfolio-fit]], [[delta-selection]], [[liquidity-analysis]], [[time-decay]], [[volatility-management]], [[kelly-criterion]], [[risk-management]], [[stress-testing]], [[distribution-analysis]], [[trade-expression]], [[discretionary-trading]], [[quantitative-analysis]], [[performance-analysis]], [[drawdown-management]], [[tail-risk]], [[win-rate]], [[earnings-catalyst]], [[support-and-resistance]], [[volume-analysis]], [[options-chain]], [[synthetic-short]], [[assignment]], [[section-1256]]

**strategies:** [[short-put-spread]], [[long-call]], [[synthetic-short]], [[directional-trading]], [[range-breakout]], [[premium-selling]], [[vertical-spread]], [[position-management]], [[earnings-vol-play]]

**securities:** [[mos]], [[pg]], [[pm]], [[tcom]], [[hims]], [[mci]], [[mrvl]], [[amd]], [[spy]], [[spx]], [[iwm]], [[qqq]]

**people:** [[eric]]

## Regime / context

**Date:** 16 October 2026 (trades reviewed from 8–15 October; AMD spread expires 16 October).

**Market context:** Mid-earnings season; breadth constraints and shorter-duration positioning preference due to market regime; index drift bias (long delta favorable).

**Caveats:** All live numeric figures (prices, Greeks, P&L percentages) are approximate from ASR transcript; exact fills and current marks should be verified in live systems. Discretionary trade examples reflect one trader's process and risk tolerance; not prescriptive. Strategy review feedback is pedagogical critique, not endorsement of specific sizing or execution.
