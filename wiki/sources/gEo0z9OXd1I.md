---
type: source
title: "Why You're Probably Lighting Money on Fire with 0DTEs | Options Trading for Beginners Ep5"
video_id: gEo0z9OXd1I
url: "https://www.youtube.com/watch?v=gEo0z9OXd1I"
date: "2026-07-11"
series: beginner-lab
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spx]
concepts: [zero-dte, gamma, theta, delta, implied-volatility, time-decay, gamma-scalping, tail-risk, path-dependence, negative-skew, liquidity, extrinsic-value, moneyness, delta-hedging, gamma-hedging, volatility-risk-premium, defined-risk, position-sizing, risk-management, greek-attribution]
strategies: [zero-dte, long-call, short-put, put-spread, defined-risk, delta-hedging, gamma-scalping]
saga: none
part: null
confidence: high
---

# Why You're Probably Lighting Money on Fire with 0DTEs | Options Trading for Beginners Ep5

## Summary

This episode explores the structural mechanics and pitfalls of zero-days-to-expiration (0DTE) options trading. While 0DTEs are not inherently unprofitable, they amplify Greeks dramatically—especially gamma and theta—creating velocity and path-dependency that trap retail traders into blind premium-selling or cheap long-option strategies. The core lesson: 0DTEs require active management, tail-risk awareness, and a tested system; buying cheap options or selling naked spreads without a plan is a reliable way to lose money.

## Key takeaways

### Dated market read (2026-07-11)

- **0DTE gamma dominance** [13:17–14:45]: At-the-money 0DTE options exhibit extreme gamma (0.086 vs. 0.05 at 3DTE), creating hyperbolic delta sensitivity. This makes small underlying moves devastating for long buyers and forces constant rehedging for short sellers.
- **Liquidity evaporation** [33:58]: As 0DTE options approach expiration, liquidity disappears entirely. SPX is preferred over SPY because of size efficiency, European-style exercise, and Section 1256 tax treatment.
- **Real path-dependent example** [42:34–45:19]: A 7550 call bought at open for $16.70 swung to −$6.70, then +$23, then decayed to near-zero. Delta ranged from ~30 to 75 to near-zero; gamma peaked mid-day then collapsed. This illustrates why 0DTEs are "super duper path dependent."

### Evergreen mechanics

- **Theta decay is non-linear** [11:46–13:17]: Gross theta on 0DTE far-OTM options is often lower than 3DTE, but relative to remaining premium it is extremely high. The ratio of theta to remaining time is what matters.
- **Gamma ramps parabolic** [31:14–32:39]: Gamma begins climbing meaningfully at 5DTE (over 2× the 30DTE level) and becomes hyperbolic as expiration approaches. Everything amplifies.
- **Negative skew kills short premium** [33:58–34:45]: The distribution of 0DTE short-premium trades is narrow around small profits but has fat tails of catastrophic losses. One losing trade erases many small winners.
- **Out-of-the-money options expire worthless** [48:20–49:39]: 94–98% of low-delta 0DTE calls expire worthless. Buying cheap OTM calls is a "many small losses, hope for one big winner" game with poor odds.
- **Defined-risk spreads require balance** [51:08–52:42]: Spreads that are too tight (5 points) collect almost nothing and have poor risk-reward; spreads that are too wide (100 points) have tail risk that erases many small credits. Strike a balance based on your system.
- **Blind selling is unsustainable** [52:42–54:07]: Selling 0DTE spreads every day without a plan is luck-based, not skill-based. You must have an adaptive sizing system, tail-risk controls, and entry/exit rules.
- **Emotional discipline requires a tested plan** [57:29]: Emotional difficulty with 0DTEs stems from lack of confidence in your system. Once you have a robust, backtested plan you trust, emotional reaction dissipates.

## Notable quotes

- "The defining risk of a zero DTE long option versus a 30 DTE option is higher theta and nothing else" — *incorrect; the real risk is extreme gamma and path-dependency.*
- "One losing trade will erase a shit ton of winning trades. That's why if you do stuff like this you kind of have an adaptive sizing system based on different market variables."
- "Everything becomes hyperbolic. That's the important piece here."

## Candidate wiki links

**concepts:**
[[zero-dte]], [[gamma]], [[theta]], [[delta]], [[time-decay]], [[implied-volatility]], [[tail-risk]], [[path-dependence]], [[negative-skew]], [[liquidity]], [[extrinsic-value]], [[moneyness]], [[delta-hedging]], [[gamma-hedging]], [[volatility-risk-premium]], [[defined-risk]], [[position-sizing]], [[risk-management]], [[greek-attribution]], [[charm]]

**strategies:**
[[zero-dte]], [[long-call]], [[short-put]], [[put-spread]], [[defined-risk]], [[delta-hedging]], [[gamma-scalping]]

**securities:**
[[spx]]

**people:**
[[eric]]

## Regime / context

Recorded 2026-07-11 during live market hours. This is Episode 5 of the *Beginner Lab* series (8 episodes total). The analysis uses live SPX option chains and historical 0DTE data from January–July 2026. All numeric figures (Greeks, prices, expiration times) are approximate due to ASR transcription and market volatility. The core mechanics (gamma ramp, theta acceleration, path-dependency, negative skew) are regime-independent and apply across all 0DTE markets.
