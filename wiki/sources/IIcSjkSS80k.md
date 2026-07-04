---
type: source
title: "Ratio Diagonal Option Strategy"
video_id: IIcSjkSS80k
url: https://www.youtube.com/watch?v=IIcSjkSS80k
date: 2023-10-10
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [rtx, aapl]
concepts: [leverage, defined-risk, delta, extrinsic-value, theta-decay, gamma, moneyness, days-to-expiration, support-and-resistance, trend-following, mean-reversion, position-sizing, profit-taking, risk-management, capital-efficiency]
strategies: [ratio-call-diagonal, trend-following, scaling-in, profit-taking]
saga: null
part: null
confidence: high
---

# Ratio Diagonal Option Strategy

## Summary

The ratio diagonal is a directional leverage strategy combining a long deep-in-the-money option (90–365 DTE) with short near-term options (within 30 DTE) at a ratio that preserves unlimited profit potential while maintaining defined risk. By controlling large notional positions with fractional capital outlay and managing theta decay through the short leg, traders can achieve capital-efficient directional exposure with built-in hedging mechanics.

## Key takeaways

- **Strategy structure** [00:26–02:41]: Long deep-ITM option (80+ delta, 6–12 months DTE) + short near-term option (2–3 weeks DTE) at a ratio (e.g., 5 long : 3 short) that eliminates upside/downside risk depending on directional bias.

- **Leverage mechanics** [01:40–02:18]: A $50k notional equity position can be controlled for ~$8,800 in options capital; leverage is "free" because options have expiration, creating opportunity for skilled traders.

- **Deep-ITM long leg rationale** [03:24–05:03]: 80+ delta moves dollar-for-dollar with underlying; reduces extrinsic value and theta decay (0.02–0.03 per day vs. higher for ATM); upfront cost acts as a "down payment" that retains value through management.

- **Critical Strike formula** [16:17–16:38]: Prevents upside/downside risk as trade evolves; calculated from adjusted long-call basis (cost of long options + closed short options + closed long options used to cover ITM shorts).

- **Ratio selection trade-off** [11:52–12:51]: Higher short ratio (e.g., 5 long : 5 short) collects more premium upfront but surrenders upside; lower ratio (5 long : 3 short) preserves more directional profit; author typically targets ~50% coverage.

- **Position sizing & allocation** [08:29–09:35]: Allocate total capital (e.g., $10k), deploy 80% or less upfront as initial outlay, reserve remainder for scaling; scale in on support/resistance breakouts or pullbacks if conviction remains high.

- **Liquidity check** [13:11–13:34]: Deep-ITM, far-dated options have reduced liquidity; test with single lot first; difficult entry = difficult exit, and these trades are not held to expiration.

- **Exit criteria** [13:53–14:48]: (1) P&L target hit; (2) short option out-of-money (can add more shorts); (3) short option in-the-money (sell long options to cover cost, realize losses, scale out); (4) if entered at 180 DTE, manage/roll when approaching 90 DTE.

- **RTX example outcome** [15:09–16:17]: Bullish trade that did not achieve expected mean-reversion move post-earnings; still returned ~7% on invested capital (~$10k allocation) by collecting short premium and managing the short ITM leg, demonstrating strategy resilience.

- **Kicker options** [05:57–06:17]: Optional far-OTM additions (30–40 DTE) to base position to maximize gamma and compound quickly; used selectively to enhance upside capture.

## Notable quotes

> "This is why we use a ratio—if we add one more view to this, using the put side right, so if we're long puts we want things to go down, but again we don't want to be wrong. If we're right, what I mean by that is if we get the down move we think is going to happen, we don't want to be penalized if it's big." [07:26–07:49]

> "The more short options you sell against the long, the more money you're going to collect upfront, the more upside potential you're going to give up if you get your move." [12:13–12:33]

## Candidate wiki links

**Concepts:**
[[leverage]], [[defined-risk]], [[delta]], [[extrinsic-value]], [[theta-decay]], [[gamma]], [[moneyness]], [[days-to-expiration]], [[support-and-resistance]], [[trend-following]], [[mean-reversion]], [[position-sizing]], [[profit-taking]], [[risk-management]], [[capital-efficiency]]

**Strategies:**
[[ratio-call-diagonal]], [[trend-following]], [[scaling-in]], [[profit-taking]]

**Securities:**
[[rtx]], [[aapl]]

**People:**
[[eric]]

## Regime / context

Recorded October 2023. The RTX example reflects a post-earnings mean-reversion setup that did not materialize as expected, yet the strategy's short-premium collection and management mechanics still delivered positive return. The Apple trade referenced (linked in video notes) is cited as a smoother, fully directional example. Ratio diagonals are evergreen directional mechanics applicable across market regimes; the specific entry signals (support/resistance, trend-following) depend on the trader's directional process.
