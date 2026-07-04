---
type: source
title: "Volatility Surface & Volatility Smile Explained"
video_id: G7gf-oXptxE
url: https://www.youtube.com/watch?v=G7gf-oXptxE
date: 2022-08-10
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spy]
concepts: [implied-volatility, volatility-surface, volatility-skew, fat-tails, kurtosis, skewness-premium, moneyness, delta, log-normal-distribution]
strategies: []
saga: null
part: null
confidence: high
---

# Volatility Surface & Volatility Smile Explained

## Summary

This video explains why the Black–Scholes–Merton model's assumption of a flat implied volatility surface does not match real market behavior. The market exhibits fat tails and skew in price distributions, leading to a volatility smile: different strikes and expirations trade at different implied volatilities. Understanding the volatility surface is essential for accurate option pricing beyond textbook assumptions.

## Key takeaways

- **Black–Scholes–Merton assumptions are incomplete** [00:00–01:18]: The BSM model assumes log-normal price distributions and constant implied volatility across strikes, but real markets do not behave this way.
- **Fat tails and skew in price distributions** [03:10–05:21]: Real stock prices exhibit kurtosis (fatter tails than normal) and skew (asymmetric tail probabilities), meaning extreme moves occur more frequently than the normal distribution predicts.
- **Volatility surface replaces flat IV assumption** [06:15–07:03]: Instead of assuming the same IV across all strikes and expirations, the market prices a multidimensional surface with IV varying by moneyness (strike distance from spot) and time to expiration.
- **Volatility smile: OTM and ITM options trade higher IV** [09:43–10:32]: At-the-money options typically have lower IV; deep out-of-the-money and deep in-the-money options trade at higher IV, creating a "smile" shape when IV is plotted against strike price.
- **Real-world example in SPY options** [07:30–08:56]: A 12-delta put in SPY showed 29.23 IV, ATM puts showed ~22.8 IV, and a 12-delta call showed 18.51 IV—demonstrating that the same delta has different IV across calls vs. puts and across moneyness.
- **Market compensates for model limitations** [11:00–11:54]: Traders and market makers adjust implied volatility based on observed price behavior and tail risk, which is why the volatility surface is not flat and why a smile exists.

## Notable quotes

> "The market does not move the way that the Black Scholes model assumes that it does. We have fat tails, we have more outlier cases than we would expect to see, and that is exactly why the volatility surface is not flat and why we have a volatility smile."

## Candidate wiki links

**concepts:** [[implied-volatility]], [[volatility-surface]], [[volatility-skew]], [[fat-tails]], [[kurtosis]], [[skewness-premium]], [[moneyness]], [[delta]], [[log-normal-distribution]]

**securities:** [[spy]]

**people:** [[eric]]

## Regime / context

Recorded August 2022. This is a foundational technical explanation of how modern option markets price volatility across strikes and expirations—a concept that applies across all market regimes but is especially relevant when volatility is elevated or skewed (e.g., post-earnings, during tail-risk events).
