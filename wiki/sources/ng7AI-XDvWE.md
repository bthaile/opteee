---
type: source
title: "Beginner Lab: Option Pricing Explained (Session 8)"
video_id: ng7AI-XDvWE
url: "https://www.youtube.com/watch?v=ng7AI-XDvWE"
date: "2024-01-16"
series: beginner-lab
format: [education, live]
experts: [eric]
mentions: []
securities: [cisco, meta, gme, nne]
concepts: [implied-volatility, intrinsic-value, extrinsic-value, premium, bid-ask-spread, delta, gamma, theta, vega, pricing-models, black-scholes-merton, volatility-clustering, moneyness, early-exercise, risk-free-rate, dividend-yield, market-maker, order-flow, implied-volatility-percentile, implied-volatility-rank, volatility-term-structure, support-and-resistance, consolidation, breakout]
strategies: []
saga: none
part: null
confidence: high
---

# Beginner Lab: Option Pricing Explained (Session 8)

## Summary

This session covers the fundamental mechanics of option pricing, including the components of an options contract, the distinction between intrinsic and extrinsic value, pricing model inputs, and the role of implied volatility in determining option premiums. Eric emphasizes that retail traders cannot reliably identify mispriced options due to institutional dominance of the market, and that profitability comes from risk assumption and directional conviction rather than exploiting pricing inefficiencies.

## Key takeaways

### Dated market read (2024-01-16)
- Cisco (CSCO) trading ~$60; 28-DTE ATM 62.5 call priced $1.73/$1.90 [21:16]
- Meta (META) trading ~$647; 28-DTE ATM 650 call priced $29.85/$30.10 [22:31]
- GameStop (GME) showing 78.25% IV but only 8% IV percentile, indicating elevated vol relative to its own history [01:03:31]

### Evergreen mechanics

- **Components of an options contract** [19:45–23:57]: underlying symbol, days to expiration, strike price, premium, option type (call/put), and American vs. European style all impact pricing.

- **Pricing model inputs** [21:16–28:09]: underlying price, option type, contract style, strike price, days to expiration, risk-free rate, dividend yield, and implied volatility. All inputs except IV are known definitively; IV is the only unknown because it reflects future price movement.

- **Premium decomposition** [31:46–35:14]: premium = intrinsic value + extrinsic value. Intrinsic value is the strike's relationship to current price; extrinsic value comprises time decay and implied volatility. Implied volatility requires time to exist—at expiration (time = 0), IV collapses to zero.

- **Moneyness and intrinsic value** [35:14–36:47]: for calls, ITM = stock price > strike; for puts, ITM = stock price < strike. ITM options have intrinsic value and are worth more than OTM options.

- **Retail traders cannot identify mispriced options** [47:26–48:50]: if you identify a mispricing, every other active market participant has already missed it. Institutional HFT firms and market makers compete on microsecond-scale vol discrepancies (to six decimal places) with lower transaction costs and hedging capabilities that retail cannot match.

- **Implied volatility vs. forecast volatility** [40:15–51:35]: implied volatility is extracted from market prices (what the market is pricing); forecast volatility is what you predict it should be. Retail traders derive IV from the market and accept it as accurate; competing on vol forecasting is not a viable edge.

- **Put-call parity enforcement** [50:16]: violations of put-call parity are hunted by HFT algorithms in microseconds, maintaining efficient pricing relationships between puts and calls.

- **Bid-ask spreads** [01:10:43–01:17:24]: the bid is the highest price a buyer will pay; the ask is the lowest price a seller will accept. Liquid options (high volume/open interest) have narrower spreads. Market makers set these prices and typically allow fills near the midpoint. Whole-number strikes (e.g., 20, 25, 30) have significantly more open interest than half-strikes or odd numbers.

- **Volatility skew and moneyness** [01:06:32]: implied volatility varies by strike. ATM options typically have lower IV; deep ITM and OTM options (the "tails") have higher IV, reflecting tail-risk pricing.

- **Implied volatility percentile vs. rank** [01:00:24–01:03:31]: IV percentile and IV rank normalize IV relative to the underlying's own history, making them comparable across different securities. IV percentile is less prone to skew. Example: Meta 43% IV with 73% IV percentile; GME 78% IV with 8% IV percentile shows GME is elevated but still historically low for itself.

- **Order book vs. tape** [01:22:50]: the order book shows resting (unfilled) orders; the tape (time & sales) shows executed transactions. Order books provide limited edge for retail traders despite marketing claims.

- **Consolidation is time-frame relative** [01:31:33–01:34:23]: consolidation is sideways, range-bound price action. What appears as consolidation on a 5-minute chart may be an uptrend on a daily chart. Breakouts require specific underlying conditions beyond consolidation alone.

- **Profitability does not require mispricing** [56:44–57:54]: even if options are priced correctly, you can profit through directional conviction and risk assumption. The difference between a correctly priced and mispriced option is the profit mechanism, not the ability to make money.

- **Retirement accounts and options trading** [01:24:18–01:28:23]: Roth and traditional IRAs allow options trading (subject to account restrictions). Naked strategies typically prohibited in IRAs. Some 401(k) plans restrict options trading; check your plan provider.

## Notable quotes

> "The biggest difference to be aware of here is the risk side of the equation and the reward side of the equation." [14:58]

> "Implied volatility is just an expectation of price movement. That's all it is." [29:58]

> "You fucking don't [identify mispriced options as a retail trader]. You absolutely do not." [47:26]

## Candidate wiki links

**concepts:** [[implied-volatility]], [[intrinsic-value]], [[extrinsic-value]], [[premium]], [[bid-ask-spread]], [[moneyness]], [[delta]], [[gamma]], [[theta]], [[vega]], [[volatility-clustering]], [[early-exercise]], [[risk-free-rate]], [[dividend-yield]], [[market-maker]], [[order-flow]], [[implied-volatility-percentile]], [[implied-volatility-rank]], [[volatility-skew]], [[support-and-resistance]], [[consolidation]], [[breakout]], [[put-call-parity]]

**strategies:** (none substantively discussed)

**securities:** [[cisco]], [[meta]], [[gme]]

**people:** [[eric]]

## Regime / context

Recorded 2024-01-16 during live Beginner Lab session (Session 8 of options-trading curriculum). Market conditions: Meta ~$647, Cisco ~$60, GameStop elevated IV (78%) but low IV percentile (8%). This is an educational session; all numeric examples are approximate and illustrative. The session emphasizes conceptual understanding of pricing mechanics over tactical trading decisions. Homework assignment: build a Black-Scholes-Merton model in Excel or Google Sheets using ChatGPT for guidance, post results in Discord learning lab.
