---
type: source
title: "Can You Beat The Market With The Wheel? 20 Years of Proof"
video_id: wKIxZ9Z9mSE
url: https://www.youtube.com/watch?v=wKIxZ9Z9mSE
date: 2026-10-04
series: none
format: [education, analysis, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy]
concepts: [capped-upside, cash-secured-puts, covered-call, covered-strangle, delta, delta-bands, drawdown, drawdown-management, expiration, gamma, implied-volatility, long-beta, max-drawdown, moving-averages, premium-selling, realized-volatility, risk-reward, short-call, short-put, theta-decay, timing, upside-management, volatility-skew]
strategies: [the-wheel, covered-strangle, covered-call, cash-secured-puts, short-call, short-put, delta-hedging, position-management, timing]
saga: null
part: null
confidence: high
---

# Can You Beat The Market With The Wheel? 20 Years of Proof

## Summary

This video analyzes 20 years of historical performance (2007–2026) of the wheel strategy applied to SPY, revealing that while the base wheel generates ~8% annualized returns versus SPY's ~11%, it significantly underperforms due to capped upside on both the short-put and short-call legs. The analysis demonstrates that strategic modifications—including partial call coverage, selective put entry based on moving averages and IV/RV conditions, and shorter time-to-expiration (20 DTE vs. 30 DTE)—can reduce maximum drawdown from 55% to 31% while maintaining competitive returns, ultimately converging toward a covered-strangle structure.

## Key takeaways

### Dated market read (2007–2026)
- Base wheel (30 DTE, 30 delta) delivered ~8% CAGR vs. SPY's ~11% over the full period [06:39]
- Wheel outperformed SPY in bear markets (2008, 2022) due to premium dampening effect [04:00]
- Wheel outperformed in sideways markets (2011, 2015) when premium collection added value [03:37]
- Wheel significantly lagged during recovery periods (2020) due to capped upside [04:41]

### Evergreen mechanics

**Core wheel structure and its limitations:**
- The wheel is a series of trades, not a unified strategy; in SPY context, it is effectively long-beta exposure [00:00]
- Short cash-secured put creates capped upside / unlimited downside asymmetry [01:06]
- Short call against assigned shares further caps upside, negating the primary return driver (market appreciation) [02:31]
- Common marketing ("get paid to buy," "get paid to sell") obscures the cost of capped upside and changing market conditions [02:31]

**Delta and time-to-expiration optimization:**
- Sweet spot for delta selection: high 20s to mid-30s delta balances return and drawdown [08:39]
- Shorter DTE (20 DTE vs. 30 DTE) can outperform because gamma risk is irrelevant when assignment is predetermined; allows access to richer premium on the curve [11:27]
- Exit timing: holding to expiration yields slightly higher returns but higher drawdown; exiting at 25% DTE reduces drawdown with modest return sacrifice [10:08]

**Call-side management:**
- Selling calls against 100% of shares caps upside; covering only 50% of shares maintains upside while reducing credit [12:34]
- Timing call sales (only above 200-period MA, or when IV > RV) improves total return in most cases but does not reliably reduce drawdown [13:58]
- Closing at 50% profit and rolling new options performs similarly to holding to expiration [15:25]
- Delta-band rebalancing is ineffective due to insufficient time decay between adjustments [15:25]

**Put-side management:**
- Selling additional cash-secured puts only when above 200-period MA or IV > RV improves overall position [16:50]
- Trend-gating put entry (requiring bullish conditions) helps capture premium in favorable regimes [16:50]

**Covered strangle as optimized wheel:**
- Combines 30-delta short options at ~20 DTE, 50% call coverage, selective put entry (200-period MA + IV > RV filter), and long equity from inception [16:50]
- Reduces max drawdown from 55% to 31% while sacrificing only ~1% annualized return [16:50]
- Addresses core wheel defects: maintains upside exposure, reduces gamma/assignment friction, and improves risk-adjusted returns [16:50]

**Cost and tax considerations:**
- Friction costs (commissions, slippage, bid-ask) and tax implications are material; cannot ignore them when comparing to buy-and-hold [05:59]
- Active trading creates multiple occurrences per year, compounding friction and tax drag [05:59]

## Notable quotes

> "The wheel itself is not a strategy. It's just a series of trades." [00:00]

> "You're missing a lot of upside profit potential." [03:37]

> "It doesn't matter how bumpy your P&L is coming into that window, if you already know your resolution at the end of the thing." [11:27]

## Candidate wiki links

**concepts:**
[[capped-upside]], [[cash-secured-puts]], [[covered-call]], [[covered-strangle]], [[delta]], [[delta-bands]], [[drawdown]], [[drawdown-management]], [[expiration]], [[gamma]], [[implied-volatility]], [[long-beta]], [[max-drawdown]], [[moving-averages]], [[premium-selling]], [[realized-volatility]], [[risk-reward]], [[short-call]], [[short-put]], [[theta-decay]], [[timing]], [[upside-management]], [[volatility-skew]]

**strategies:**
[[the-wheel]], [[covered-strangle]], [[covered-call]], [[cash-secured-puts]], [[short-call]], [[short-put]], [[delta-hedging]], [[position-management]]

**securities:**
[[spy]]

**people:**
[[eric]]

## Regime / context

This analysis spans 20 years of historical backtesting (2007–2026) across multiple market regimes: the 2008 financial crisis, the 2011–2015 sideways consolidation, the 2020 COVID recovery, and the 2022 bear market. The wheel's performance is regime-dependent: it excels in low-volatility and bear-market environments but lags during strong bull rallies. The covered-strangle variant is presented as a structural improvement that addresses the wheel's core defect (capped upside) while maintaining its premium-collection benefits. All results are approximate and subject to backtesting assumptions (slippage, commissions, tax treatment not fully detailed).
