---
type: source
title: "Black Scholes Merton Inputs Decoded | The Options Trench"
video_id: Jfq38jbTtzE
url: https://www.youtube.com/watch?v=Jfq38jbTtzE
date: 2026-07-11
series: options-trench
format: [education, analysis]
experts: []
mentions: [merton, samuelson]
securities: [spy, ung]
concepts: [black-scholes, black-scholes-merton, implied-volatility, volatility, time-to-expiration, moneyness, vega, bid-ask-spread, volatility-smile, volatility-skew, delta, option-pricing, market-microstructure, liquidity, arbitrage, risk-premium, volatility-risk-premium, samuelson-effect, continuous-hedging, replication, american-vs-european-options, gap-risk, stock-price, etf-mechanics, etf-premium-discount, nav, market-making, fair-value, information-asymmetry, limit-to-arbitrage, statistical-arbitrage]
strategies: [delta-hedging, market-making]
saga: null
part: null
confidence: high
---

# Black Scholes Merton Inputs Decoded | The Options Trench

## Summary

This episode decodes the five primary inputs to the Black-Scholes-Merton (BSM) option pricing model: underlying price, strike, time to expiration, risk-free rate, and volatility. While the first four inputs are relatively knowable, volatility remains the true unknown—a forecast of future realized volatility. The hosts explore how each input contains hidden complexity and ambiguity in real market application, from how time is measured to which stock price to use for hedging.

## Key takeaways

- **BSM as a measuring stick, not truth** [02:28–02:48]: BSM is best used to compare options across strikes and expirations, not to derive absolute fair value. Its assumptions (continuous markets, frictionless hedging, log-normal returns) don't reflect reality, but they cancel out when comparing relative values.

- **Time input is a fraction of the year** [06:31–07:39]: Days to expiration must be divided by 365 (or the model's year convention) to get the T variable. If 22 calendar days remain, input 22/365, not 22. This prevents confusion across different time horizons.

- **Volatility scales with the square root of time** [12:20–13:05]: To convert annualized volatility to daily volatility, divide by √256 ≈ 16. For monthly, divide by √12. This scaling is built into the model; always input annualized volatility regardless of option duration.

- **Implied vol is not a single number** [13:57–15:07]: Every strike has its own implied volatility (the "vol smile"). Calls and puts each have bid and ask vols. Deep in-the-money options show noisy vol curves due to low vega; use out-of-the-money strikes for cleaner IV readings.

- **Vega drives vol noise in bid-ask spreads** [15:30–16:36]: A 20-cent wide market on a deep ITM call with 0.5 vega becomes a 40 vol-point wide market. The same dollar width translates to more vol points as vega shrinks, creating apparent "opportunities" that are just bid-ask artifacts.

- **Short-dated options have noisier vol curves** [22:39–24:11]: Near-expiration options (especially over weekends) show parabolic vol spikes and sawtooth patterns due to low vega and discrete strike liquidity. Longer-dated options have smoother curves because vega is larger.

- **Samuelson effect in commodities** [28:33–30:32]: In commodity markets, implied volatility increases as expiration approaches (e.g., crude oil front-month vol > back-month vol). This reflects that near-term supply shocks matter more than long-term equilibrium; equities don't always show this pattern.

- **Stock price is ambiguous** [35:39–41:48]: Which stock price to input depends on context. Market makers use bid for call bids (to hedge by selling stock at bid), ask for put bids (to hedge by buying stock at ask). For ETFs trading at a premium/discount to NAV, the "right" price depends on your hedging intent and arbitrage constraints.

- **Liquidity and strike divisibility create sawtooth patterns** [20:22–21:48]: SPY options are tighter on strikes divisible by 5 (705, 710, 715) due to higher market-maker interest. In-between strikes (706, 707, 708) are wider, creating apparent vol spikes that vanish when you filter by liquidity.

- **Market makers converge on fair value** [42:37–45:51]: Absent information asymmetry or size constraints, market makers have similar views of fair value. Deviations become risk-premium games (e.g., UNG trading at a premium when share creation is capped) rather than true arbitrage opportunities.

## Notable quotes

> "Merton gets no respect around here. What is that? Like a Rodney Dangerfield thing?"

> "Volatility is truly the unknown, right? That's a forecast, something that we are legit trying to predict the future."

> "Black-Scholes is resting on these assumptions, but we don't necessarily take it seriously. But those assumptions being true or false, if we're just comparing options to one another, a lot of those assumptions cancel out with each other."

## Candidate wiki links

**concepts:** [[black-scholes]], [[black-scholes-merton]], [[implied-volatility]], [[volatility]], [[time-to-expiration]], [[moneyness]], [[vega]], [[bid-ask-spread]], [[volatility-smile]], [[delta]], [[option-pricing]], [[market-microstructure]], [[liquidity]], [[arbitrage]], [[risk-premium]], [[volatility-risk-premium]], [[continuous-hedging]], [[replication]], [[american-vs-european-options]], [[gap-risk]], [[etf-mechanics]], [[nav]], [[fair-value]], [[information-asymmetry]], [[limit-to-arbitrage]], [[statistical-arbitrage]]

**strategies:** [[delta-hedging]], [[market-making]]

**securities:** [[spy]], [[ung]]

**people:** [[merton]], [[samuelson]]

## Regime / context

Recorded 2026-07-11. This is a foundational education episode on BSM mechanics and real-world input ambiguity. The discussion assumes familiarity with basic options terminology (calls, puts, ITM/OTM) but is accessible to intermediate traders. The examples (SPY, UNG) and market-making context reflect 2026 market structure; some institutional practices may differ by venue or regulatory regime.
