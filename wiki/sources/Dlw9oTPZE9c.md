---
type: source
title: "Options Trading for Beginners"
video_id: Dlw9oTPZE9c
url: https://www.youtube.com/watch?v=Dlw9oTPZE9c
date: 2023-03-14
series: beginner-lab
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, aapl, iwm, spx, ndx]
concepts: [assignment, bid-ask-spread, call-credit-spread, delta, delta-hedging, delta-neutral, days-to-expiration, extrinsic-value, gamma, greeks, implied-volatility, intrinsic-value, iv-crush, leverage, moneyness, out-of-the-money, premium, risk-management, theta, vega, volatility-term-structure]
strategies: [covered-call, covered-strangle, long-call, long-put, ratio-call-diagonal, short-call, short-put]
saga: none
part: null
confidence: high
---

# Options Trading for Beginners

## Summary

A comprehensive introduction to options contracts for new traders, covering the fundamental mechanics of calls and puts, the structure of options chains, intrinsic and extrinsic value, implied volatility, and the Greeks (delta, gamma, theta, vega, rho). The video emphasizes that options are derivatives whose value is derived from an underlying security, offering leverage, hedging capability, and non-directional trading opportunities unavailable in equities alone.

## Key takeaways

- **What options are**: Derivatives—contracts tied to an underlying security (stock, ETF, index) that give the buyer a right and the seller an obligation [00:42–01:24]
- **Two types of options**: Calls (right to buy at strike price) and puts (right to sell at strike price); you can buy or sell either [08:43–09:11]
- **Long call**: Buyer has the right to purchase the underlying at the strike price; profits when underlying appreciates [14:50–15:47]
- **Short call**: Seller has the obligation to deliver the underlying at the strike price if exercised; profits when underlying stays flat or declines [16:53–17:19]
- **Long put**: Buyer has the right to sell the underlying at the strike price; profits when underlying depreciates [17:44–18:39]
- **Short put**: Seller has the obligation to buy the underlying at the strike price if exercised; profits when underlying stays flat or rises [18:39–19:01]
- **Contract multiplier**: Each options contract controls 100 shares of the underlying; quoted prices must be multiplied by 100 [27:33–28:57]
- **Intrinsic value**: How far an option is in the money (for calls: security price minus strike; for puts: strike price minus security price) [40:31–41:10]
- **Extrinsic value (time value)**: The portion of premium attributable to time remaining until expiration; decays to zero at expiration [37:44–45:26]
- **Moneyness for calls**: In the money when strike < security price; out of the money when strike > security price [38:32–40:00]
- **Moneyness for puts**: In the money when strike > security price; out of the money when strike < security price [42:52–43:27]
- **Implied volatility (IV)**: Forward-looking forecast of expected volatility; higher IV increases option premiums for both calls and puts [53:33–55:49]
- **Realized/historic volatility**: Observed past volatility; used as a reference but not directly for pricing [56:20–56:46]
- **Delta**: Rate of premium change per $1 move in underlying; also approximates probability of expiring in the money [01:05:59–01:10:37]
- **Gamma**: Rate of change of delta; highest at the money, increases as expiration approaches [01:11:01–01:13:06]
- **Theta (time decay)**: Rate of extrinsic value decay per day; highest for at-the-money options, accelerates near expiration [01:13:29–01:15:11]
- **Vega**: Rate of premium change per 1% change in implied volatility [01:15:34–01:15:51]
- **Rho**: Rate of premium change per 1% change in risk-free rate; more relevant for longer-dated options [01:15:51–01:16:16]
- **American vs. European options**: American can be exercised anytime; European only at expiration [25:42–26:03]
- **Exercise vs. trading the contract**: Most traders close positions by trading the contract rather than exercising, as profit is already baked into premium [23:46–24:34]
- **Buy to open (BTO) / Sell to close (STC)**: Inverse transactions to establish and exit long positions [30:25–30:51]
- **Sell to open (STO) / Buy to close (BTC)**: Inverse transactions to establish and exit short positions [30:25–30:51]
- **Leverage in options**: Control larger notional exposure with smaller capital outlay; amplifies both gains and losses [02:53–03:11]
- **Non-directional strategies**: Options enable profit from sideways markets or volatility changes, not just directional moves [03:34–04:47]
- **Income generation**: Selling options can generate income on principal without drawing down the position [04:19–04:47]
- **Bid-ask spread and mid pricing**: Market makers quote bid (lower) and ask (higher); traders typically target the mid for fills [49:27–49:45]
- **Volatility surface**: Implied volatility varies by strike and expiration; not uniform across the options chain [57:56–58:53]
- **Recommended homework**: Create a Greeks table (delta, gamma, theta, vega, rho) across multiple expirations and moneyness levels for a single underlying [01:04:31–01:05:14]
- **Paper trading first**: Commit to at least six months of paper trading before risking real capital [01:17:25–01:17:43]

## Notable quotes

> "Options are a little more accessible to people, a little bit smaller of a product, and there's some rules that tie to options that make them kind of advantageous for a lot of scenarios, specifically beginner strategies." [01:04]

> "The beauty in that scenario is you can come up with non-directional returns—you can make money if something doesn't really go in your favor but doesn't go against you too far, or if something doesn't move a whole lot." [03:57]

> "Volatility is the heart and blood of derivatives. It's why options have any outstanding value—because the future is unknown." [59:18]

## Candidate wiki links

**concepts:**
[[assignment]], [[bid-ask-spread]], [[delta]], [[delta-hedging]], [[delta-neutral]], [[days-to-expiration]], [[extrinsic-value]], [[gamma]], [[greeks]], [[implied-volatility]], [[intrinsic-value]], [[iv-crush]], [[leverage]], [[moneyness]], [[out-of-the-money]], [[premium]], [[risk-management]], [[theta]], [[vega]], [[volatility-term-structure]]

**strategies:**
[[covered-call]], [[covered-strangle]], [[long-call]], [[long-put]], [[ratio-call-diagonal]], [[short-call]], [[short-put]]

**securities:**
[[spy]], [[aapl]], [[iwm]], [[spx]], [[ndx]]

**people:**
[[eric]]

## Regime / context

Recorded March 2023. This is a foundational educational video with no time-sensitive market commentary; all concepts and mechanics remain evergreen. The video is the longest in Eric's 2023 output to date and serves as a comprehensive onboarding resource for retail traders new to options. Emphasis on paper trading for at least six months before live trading reflects a conservative risk-management stance appropriate for beginners.
