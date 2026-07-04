---
type: source
title: "Ratio Put Diagonal Explained: A Powerful Bearish Option Strategy"
video_id: PVTMNm5dH6g
url: https://www.youtube.com/watch?v=PVTMNm5dH6g
date: 2024-08-03
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [o, roku]
concepts: [delta, theta, intrinsic-value, extrinsic-value, implied-volatility, gamma, liquidity, technical-analysis, support-and-resistance, risk-management, position-sizing, profit-taking, trend-following, price-action, moneyness, days-to-expiration, assignment, rolling-options, realized-vs-unrealized-pnl, volatility-clustering]
strategies: [ratio-call-diagonal, short-put, long-put, short-premium, trend-following, pullback-entry]
saga: none
part: null
confidence: high
---

# Ratio Put Diagonal Explained: A Powerful Bearish Option Strategy

## Summary

The ratio put diagonal is a directionally leveraged bearish options strategy combining long in-the-money puts (>60 DTE, typically 75–90 delta) with short out-of-the-money puts (20–40 DTE, typically 12–30 delta) to profit from downside moves while offsetting theta decay and collecting premium. The strategy is managed via technical analysis, with profit targets and stops defined at entry; position adjustments occur when short puts fall in-the-money, requiring either rolls or sales of long puts to avoid locking in losses.

## Key takeaways

- **Core structure**: Long high-delta ITM puts (>60 DTE) paired with short lower-delta OTM puts (20–40 DTE) at a ratio favoring the longs (e.g., 30 long : 5–10 short) [00:33–01:14]
- **Why ITM longs**: Limits theta decay (intrinsic value doesn't decay), provides dollar-for-dollar move in underlying (e.g., 91-delta put captures 91¢ per $1 move), and reduces need for massive price swings to profit [01:42–02:51]
- **Delta selection for longs**: Typically 60–90 delta; 80 delta is the target. Balance between liquidity (avoid odd strikes like 57½) and capital efficiency [03:56–05:02]
- **Expiration selection for longs**: >60 DTE to avoid theta acceleration; 90–180 DTE common, sometimes >1 year depending on conviction and holding period [05:48–06:33]
- **Short put mechanics**: <40 DTE (often ~20 days), OTM, designed to decay quickly and offset cost of leverage; typically 30-delta or less to preserve long-put profit potential [07:21–08:03]
- **Ratio sizing**: Heavier weighting on longs (e.g., 30:5 or 30:10) to maximize profit potential; higher short ratio collects more premium upfront but caps P&L on favorable moves [10:55–11:44]
- **Critical strike concept**: Tracks the lowest strike at which you can sell short puts without locking in a loss; calculated as (stock price − long basis − long value) / long delta [17:47–18:53]
- **Adjusted long basis**: Accounts for realized P&L from closed short puts; helps determine how many longs to sell to cover short losses [20:50–21:37]
- **Management via technicals**: Define profit target and hard stop before entry using support/resistance and near-term price action; use soft stops to trail position downside [13:42–14:06, 27:41–28:19]
- **Handling in-the-money shorts**: Either roll to defer loss or sell long puts to cover; never simply close shorts at a loss without offsetting long gains [14:27–16:56]
- **Phased entry/exit**: Often buy longs first, wait 1–2 days for confirmation, then add shorts; on exit, sell a few longs first to assess liquidity, then unwind shorts, then close remaining longs [13:07–15:12]
- **Live example (O, Jan–Mar 2024)**: Entered 30 long 60-delta puts (17 May expiry) + 10 short 55-delta puts (15 March expiry) for ~$15.75k debit; closed for 36.4% ROIC on ~3-point move via technical stops and rolling shorts [21:57–32:13]
- **Current example (Roku, June 2024)**: Long 15 of 60-delta puts (16 Aug expiry) + short 5 of 51-delta puts (5 July expiry); entered on breakdown scan after rejection at resistance [35:30–37:19]
- **Kicker options (optional)**: Cheaper OTM puts (same or closer expiry) added if expecting larger move; don't profit on small moves but compound quickly on large moves [02:51–03:56]

## Notable quotes

> "The ratio put diagonal is my hands-down favorite bearish options trading strategy."

> "The further in the money you go, the more expensive your option will be, but the less time value and the more intrinsic value will be in that option."

> "I don't want any risk in my direction. I want to have as much profit potential as possible."

## Candidate wiki links

**Concepts:**
[[delta]], [[theta]], [[intrinsic-value]], [[extrinsic-value]], [[implied-volatility]], [[gamma]], [[liquidity]], [[technical-analysis]], [[support-and-resistance]], [[risk-management]], [[position-sizing]], [[profit-taking]], [[trend-following]], [[price-action]], [[moneyness]], [[days-to-expiration]], [[rolling-options]], [[realized-vs-unrealized-pnl]], [[volatility-clustering]]

**Strategies:**
[[ratio-call-diagonal]], [[short-put]], [[long-put]], [[short-premium]], [[trend-following]], [[pullback-entry]]

**Securities:**
[[o]], [[roku]]

## Regime / context

Recorded 3 August 2024. The video walks through a completed trade in O (Realty Income) from January–March 2024 and a live position in Roku as of mid-June 2024. The strategy is evergreen but examples reflect 2024 market conditions and volatility regimes. The detailed formulas and platform mechanics (Think or Swim) are specific to the host's workflow; traders on other platforms can simplify via built-in Greeks and P&L tracking.
