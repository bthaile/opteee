---
type: source
title: "Gamma Exposure (GEX) Is Misleading You: Here's What the Research Actually Says"
video_id: shoxAlBc974
url: https://www.youtube.com/watch?v=shoxAlBc974
date: 2026-08-23
series: options-trench
format: [education, analysis]
experts: [eric]
mentions: [chris]
securities: [spy, spx, spxw]
concepts: [gamma, gamma-exposure, gamma-hedging, delta-hedging, open-interest, implied-volatility, market-maker, order-flow, confirmation-bias, cherry-picking, volatility-modeling, market-microstructure, zero-dte, inventory-management, hedging-intensity, volatility-skew, expected-move, distribution, position-sizing]
strategies: [delta-hedging, gamma-scalping]
saga: null
part: null
confidence: high
---

# Gamma Exposure (GEX) Is Misleading You: Here's What the Research Actually Says

## Summary

This video deconstructs the widespread retail narrative around gamma exposure (GEX) as a predictive market signal, using peer-reviewed research to show that GEX is built on unverifiable assumptions, incomplete data, and misclassified trade direction. The speaker demonstrates that dealer gamma is typically *positive* (not short, as commonly assumed), that customer flow is flat across expirations, and that gamma's actual market impact is rare and modest—contradicting the "gamma wall" prediction framework. GEX is better used as a volatility or sizing input than as directional forecasting.

## Key takeaways

- **Cherry-picking and confirmation bias dominate GEX commentary** [00:00–01:18]: Posts claiming "gamma walls" predict moves appear only *after* the move occurs; no commentary tracks failed predictions, creating a false signal.

- **Gamma is a model output, not an objective fact** [02:53–07:09]: Gamma varies based on volatility assumptions, DTE interpretation, and pricing model choice. Even "objective" inputs like time-to-expiration are debatable (1 DTE ≠ 24 hours).

- **Trade direction classification is 59–83% accurate at best** [08:32–10:15]: The quote rule (83%), Lee-Ready (80%), EMO (77%), and tick rule (59%) all fail on index spreads and combinations (~15% of volume), making dealer-side inference unreliable.

- **Open interest is stale for zero-DTE options** [11:53–13:22]: Zero-DTE positions open and close intraday; they don't appear in published OI. By mid-session, cumulative zero-DTE volume can exceed prior-day OI, rendering GEX calculations "effectively fatal."

- **Most market makers do NOT delta-hedge continuously** [13:22–15:04]: Only 4 of 43 market makers in one study consistently delta-hedge; most rebalance inventory within minutes and quote to attract offsetting flow. Daily volume exceeds net position change by 32×.

- **Dealer gamma is typically positive, not short** [16:32–17:59]: Using 440M+ Cboe SPX/SPXW trade records at 1-minute frequency, Amaya et al. found mean daily gamma of ~$341B positive; gamma is positive ~90% of days. The standard "dealers are short gamma" assumption is backwards most of the time.

- **Customer flow is flat, not systematically long puts / short calls** [17:59–19:30]: Zero-DTE customers sold 17% of volume and bought 16%—nearly flat. The convention that customers are net buyers of puts and sellers of calls is not supported by actual trade data.

- **Gamma's market impact is rare and modest** [19:30–20:40]: GARCH and linear models show gamma-driven variance effects are real but occur in tails; the impact is "not that profound" and doesn't behave as commonly assumed.

- **GEX works better as a volatility/sizing signal than directional predictor** [20:40–22:11]: Use GEX to inform position sizing or expected range in extreme regimes, not to forecast direction. Test any GEX-based strategy using the Outlier research process.

- **Research itself lacks consensus** [20:40]: Even peer-reviewed studies with access to detailed trade data disagree on gamma's effects, undermining confidence in any GEX-based signal.

## Notable quotes

> "For every instance where there is this massive gamma wall that leads to this obvious move, it's funny how those comments come out after the move."

> "Gamma is the rate of change of delta" and "gamma itself is a model output, and there's different gammas that you can logically arrive at based on different input conditions."

> "Nobody outside of a clearing firm can tell you any of this. There are observable facts we can pull. There are things that we can infer, and then there are things that are literally not available."

## Candidate wiki links

**concepts:**
[[gamma]], [[gamma-exposure]], [[gamma-hedging]], [[delta-hedging]], [[open-interest]], [[market-maker]], [[order-flow]], [[confirmation-bias]], [[cherry-picking]], [[volatility-modeling]], [[market-microstructure]], [[zero-dte]], [[inventory-management]], [[hedging-intensity]], [[expected-move]], [[distribution]], [[position-sizing]]

**strategies:**
[[delta-hedging]], [[gamma-scalping]]

**securities:**
[[spy]], [[spx]], [[spxw]]

**people:**
[[eric]], [[chris]]

## Regime / context

**Date:** 2026-08-23. This analysis reflects the post-zero-DTE era (Tuesday/Thursday expirations added to the standard Monday/Wednesday/Friday cycle), which has fundamentally altered dealer positioning and customer flow patterns relative to pre-2020 research. The speaker emphasizes that much GEX commentary relies on pre-2000 trade-classification data and outdated assumptions about customer behavior. Retail traders should be aware that published open-interest data is stale for zero-DTE products and that the "gamma wall" narrative is primarily a post-hoc rationalization rather than a predictive framework.
