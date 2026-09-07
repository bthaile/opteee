---
type: source
title: "The Truth About GEX: Is It Just Noise?"
video_id: xpqkFkjYEsk
url: "https://www.youtube.com/watch?v=xpqkFkjYEsk"
date: "2026-09-06"
series: options-trench
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spx, spy, vix]
concepts: [gamma, dealer-gamma, gamma-hedging, implied-volatility, realized-volatility, volatility-regime, open-interest, market-microstructure, directional-bias, noise-vs-signal, correlation, causality, regime-dependency, volatility-clustering, vol-term-structure]
strategies: []
saga: null
part: null
confidence: high
---

# The Truth About GEX: Is It Just Noise?

## Summary

This video systematically tests four common claims about gamma exposure (GEX) as a market predictor: magnitude of moves, trending vs. chopping, directional bias, and support/resistance ("GEX walls"). Through rigorous backtesting from 2008 to present using percentile-ranked data, the analysis finds that only one claim survives scrutiny—that low gamma predicts larger subsequent moves—but even this effect is almost entirely explained by [[implied-volatility]] regime, not GEX itself. The core finding: GEX is largely noise; [[vix|VIX]] captures the same signal more cleanly.

## Key takeaways

### Evergreen mechanics

- **The assumption trap** [01:14–02:33]: GEX predictions rest on two unobservable inputs—whether customers are net long or short options, and how dealers actually hedge. Stacking assumptions compounds error; the methodology requires dealers to hedge in a specific way for GEX to work at all.

- **Data quality doesn't fix the core problem** [02:33–05:35]: Cboe's new TBT (transaction-level) dataset is expensive (~$248k for 2 years, $12k/month subscription) and covers only ~37% of volume (Cboe + ICE combined). Even with better tagging, you cannot reconstruct the entire dealer book—you have no visibility into what else dealers are holding, making any isolated GEX prediction unreliable.

- **The sign assumption is fatal** [06:55–08:13]: Standard GEX assumes dealers are long call gamma and short put gamma (implying customers sell calls and buy puts). This is empirically false; customers actively buy and sell both calls and puts in balanced volume. Switching to percentile ranking instead of sign-based assumptions improves the analysis.

- **Claim 1: Low gamma → bigger days (VIABLE, but weak)** [08:13–11:09]: Low GEX days are followed by median moves ~1.3–1.4x larger than high GEX days. This relationship is monotonic and holds across years (2008–present), not driven by a single standout period. However, this effect is almost entirely explained by [[implied-volatility]] regime.

- **Claim 2: Low gamma → trending, not chopping (VIABLE)** [11:09–12:34]: Low GEX days do tend to trend rather than chop, and this holds over multiple time horizons. This is one of the few GEX observations that survives testing.

- **Claim 3: GEX predicts direction (FALSE)** [12:34–13:51]: No reliable directional signal. SPX closes up 54.5% of days, SPY 54.7%—the market simply drifts up. GEX shows no monotonic or meaningful pattern for predicting which way the market will move.

- **Claim 4: GEX walls predict support/resistance (FALSE)** [13:51–14:00]: Gamma-weighted price levels show no edge vs. placebo. Gamma can land close to spot price by chance alone; the gap is indistinguishable from random.

- **Correlation decomposition reveals the culprit** [14:00–15:31]: Raw GEX–next-day-range correlation is 0.420 in SPX. Controlling for trailing realized vol drops it to 0.260. Controlling for implied vol drops it to 0.055. Controlling for both: 0.057. About 90% of the GEX signal vanishes once you account for [[implied-volatility]]. The strongest effect is IV, not GEX.

- **Vol echo story rejected** [15:31–17:08]: GEX is built from [[open-interest]], which reacts to volatility. The hypothesis that "low GEX predicts wide days because vol clusters" is broadly rejected by the data. [[Implied-volatility]] is the true driver.

- **VIX is simpler and stronger** [17:08–18:37]: Using identical percentile-ranked buckets, [[vix|VIX]] spreads next-day range by 2.66x (calm to stress), outperforming GEX. VIX tells you the same story faster and cleaner. GEX is not "completely noise," but it adds nothing that [[implied-volatility]] regime doesn't already capture.

- **Research corroboration** [17:08]: Analysis aligns with ~40–50 peer-reviewed studies. Six of seven common GEX claims do not survive scrutiny; only "GEX predicts volatility" persists, but [[implied-volatility]] does it better.

## Notable quotes

> "You cannot look at things like GEX in a vacuum. You can't say GEX in SPX is blank, so if price gets to whatever level in SPX, the dealers will do blank, because you have no idea what else the dealers are holding." [05:35]

> "The overwhelming majority in the simpler tool here, by far, is literally just vol regime. That's it. By far. GEX tells you literally nothing that using a base vol regime tool doesn't." [13:51]

> "It's not inherently that GEX is like completely noise, but the VIX already tells you more cleanly, faster." [18:37]

## Candidate wiki links

**concepts:**
[[gamma]], [[dealer-gamma]], [[gamma-hedging]], [[implied-volatility]], [[realized-volatility]], [[volatility-regime]], [[open-interest]], [[market-microstructure]], [[directional-bias]], [[noise-vs-signal]], [[correlation]], [[regime-dependency]], [[volatility-clustering]]

**securities:**
[[spx]], [[spy]], [[vix]]

## Regime / context

**Date:** 2026-09-06. Backtesting window: 2008–present (18 years). This is a follow-up to an earlier GEX overview video and directly addresses community questions about GEX predictive power. The analysis uses percentile-ranked GEX (not raw dollar values, which are distorted by market-size growth) and controls for [[implied-volatility]] and [[realized-volatility]] regimes to isolate true GEX signal. Key finding: GEX is a [[volatility-regime]] echo, not an independent predictor.
