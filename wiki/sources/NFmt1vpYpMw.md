---
type: source
title: "Avoid This 0DTE Option Strategy"
video_id: NFmt1vpYpMw
url: https://www.youtube.com/watch?v=NFmt1vpYpMw
date: 2024-03-23
series: options-trench
format: [education, analysis, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spx]
concepts: [zero-dte, variance-risk-premium, defined-risk, undefined-risk, iron-condor, short-strangle, short-premium, delta, max-loss, position-sizing, risk-tolerance, transaction-costs, compound-annual-growth-rate, drawdown, expected-return, risk-management]
strategies: [iron-condor, short-strangle, short-call, short-put]
saga: null
part: null
confidence: high
---

# Avoid This 0DTE Option Strategy

## Summary

This video compares defined-risk (iron condor) versus undefined-risk (short strangle) zero-DTE strategies on SPX, using backtested data from 2022–2023 to quantify the cost of buying protective wings. The core finding: while wings reduce max loss, they drag returns significantly; naked short premium with max-loss management often outperforms, but requires proper position sizing and risk tolerance alignment.

## Key takeaways

- **Defined vs. undefined risk trade-off [01:08–02:23]**: Iron condors cap loss both directions but narrow the profit zone; short strangles widen profit zone but expose you to unlimited loss. Both capture variance risk premium, but the cost of wings is material.

- **Variance risk premium is real [03:03–03:54]**: A January 2024 study confirms zero-DTE options offer substantial variance risk premium (implied variance consistently higher than realized variance until settlement), validating the short-premium thesis—but success is not guaranteed and returns are skewed.

- **Backtesting setup: 2022–2023 [05:10–05:53]**: Two-year sample chosen deliberately: 2022 down ~20%, 2023 up ~23%, net still negative. Tested short 20-delta strangles vs. iron condors with 5/10/15-delta long wings, entered 1 hour before close.

- **Tight wings kill returns [06:15–07:01]**: 20-delta short / 15-delta long iron condor: max loss only $775, but CAGR 4.7%, max drawdown 9.8%. Naked 20-delta strangle: $26,995 P&L, CAGR 12.3%, but max loss $5,657. Wings are expensive.

- **Max-loss management on strangles [08:12–08:55]**: Capping max loss at 200% or 300% of max profit cuts off only ~14 unprofitable tail trades while improving CAGR from 12.3% to higher, reducing max loss from $5,657 to $2,200. Fewer transactions = lower drag.

- **Wings + management on iron condors underperforms [09:21–09:44]**: Even with tighter wings (5-delta long), iron condors with max-loss management yield only $9,600–$177,000 P&L vs. naked strangles at $26,995+. The cost of buying protection compounds.

- **Naked options + max-loss caps preferred [10:35–10:54]**: Eric's lean: use naked short options with max-loss management (not max-profit caps, which add transactions and reduce efficacy). Avoid over-managing; interaction costs are a killer.

- **Actionable rule-set [12:04–12:29]**: Can optimize entry/exit using VIX levels, SPX levels, or trend filters without cherry-picking. Even unoptimized naked-strangle strategies achieved double-digit CAGR through 2022 drawdown and 2023 rally.

## Notable quotes

> "If you want to exist as a trader for any meaningful duration of time you need to be thoughtful about risk."

> "Implied variance is higher on average than realized variance—that's why there's a market here."

> "You have to determine what function you're providing the market. If you think you just get to sell options and make money because you're selling, but then you want to buy wings to protect your position, you're placing a premium on your risk aversion and that's going to negatively impact profitability."

## Candidate wiki links

**concepts:** [[zero-dte]], [[variance-risk-premium]], [[defined-risk]], [[undefined-risk]], [[delta]], [[max-loss]], [[position-sizing]], [[risk-tolerance]], [[transaction-costs]], [[compound-annual-growth-rate]], [[drawdown]], [[expected-return]], [[risk-management]], [[short-premium]]

**strategies:** [[iron-condor]], [[short-strangle]], [[short-call]], [[short-put]]

**securities:** [[spx]]

**people:** [[eric]]

## Regime / context

Backtested on SPX 2022–2023, a period spanning severe drawdown (2022: ~−20%) and partial recovery (2023: +23%). Results are in-sample; the video notes that optimization using VIX/SPX/trend filters can improve entry timing without overfitting. No commissions included. All trades entered 1 hour before close (3 p.m. ET) and held to expiration (zero overnight gap risk).
