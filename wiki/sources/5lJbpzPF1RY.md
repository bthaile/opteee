---
type: source
title: "Early Exercise Strategy Most Options Traders Never Learn | The Options Trench"
video_id: 5lJbpzPF1RY
url: https://www.youtube.com/watch?v=5lJbpzPF1RY
date: 2026-06-27
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [ibit, btc]
concepts: [early-exercise, assignment, intrinsic-value, extrinsic-value, put-call-parity, optimal-stopping-problem, theta, delta, vega, implied-volatility, risk-free-rate, financing-costs, american-options, european-options, dividend-capture, cost-benefit-analysis]
strategies: [short-put]
saga: null
part: null
confidence: high
---

# Early Exercise Strategy Most Options Traders Never Learn | The Options Trench

## Summary

Eric and Chris work through a live early assignment scenario on IBIT short puts to explain the two-stage test for evaluating whether early exercise makes economic sense. The first test compares interest earned on short proceeds against the extrinsic value of the forgone call; the second test—often overlooked—determines whether the current moment is *optimal* for exercise using marginal benefit/cost analysis via theta and daily interest. The session covers American vs. European option mechanics, dividend-capture logic for calls, and practical liquidity considerations when trading deep in-the-money options.

## Key takeaways

### Dated market read (2026-06-27)

- **IBIT assignment scenario** [00:27–02:34]: Eric held short 41-strike puts ~22 days to expiration (DTE) when assigned early; stock at ~$33.50, out-of-the-money calls trading 5–6 cents, ~91 delta.
- **Implied volatility context** [28:28]: IBIT IV at 50%, IV percentile at 62% as of the session date.

### Evergreen mechanics

- **Two-stage early-exercise test for puts** [03:11–08:07]:
  - **Stage 1**: Is the interest earned on short proceeds greater than the extrinsic value of the call you're giving up? If yes, exercise *could* be justified.
  - **Stage 2**: Is *now* the optimal time to exercise, or would waiting one more day yield better marginal benefit? Compare daily interest (~0.5 cents in the example) against theta decay of the forgone call (~0.7 cents). When theta > daily interest, hold; when they cross, optimal exercise window approaches.
  
- **Why Stage 2 matters** [08:32–09:47]: American options lack closed-form pricing solutions precisely because of the optimal stopping problem—early exercise is irreversible, so timing matters. Most retail traders only run Stage 1, leading to suboptimal early exercises.

- **Practical example walkthrough** [04:03–07:41]: 
  - 22 DTE, $41 strike, stock $33.50, risk-free rate 4.3%.
  - Interest earned: ~10.6 cents over 22 days.
  - Call value: 5.5 cents.
  - Stage 1 passes (10.6 > 5.5).
  - Stage 2 analysis: optimal exercise ~17 DTE; counterparty exercised 5 days early.

- **Historical comparison** [19:08–21:08]: On June 5, stock was $34 (50 cents higher), out-of-the-money call was 43 cents, total interest to expiration only 20 cents—Stage 1 *fails*. On June 24 (23 DTE), call was 8 cents, interest 11 cents—Stage 1 passes, but optimal exercise still ~15 DTE.

- **Why someone might exercise suboptimally** [26:33–28:28]:
  - **Volatility belief**: If counterparty believes realized vol will be near zero, theta value collapses; they may view the 0.7-cent theta as overstated and prefer to lock in the 10.6-cent interest.
  - **Spread width & execution**: 41-strike puts trading 20 cents wide; bid may be below intrinsic. Exercising at intrinsic may be preferable to selling at a wide bid.
  - **Margin/portfolio rebalancing**: Desire for cash, margin requirements, or position reconfiguration (though less likely to explain this specific case).

- **American vs. European options** [34:42–35:32]:
  - American puts can be exercised early to capture financing; European puts cannot, so they trade at a discount and can trade *below* intrinsic value due to financing costs.
  - American calls are exercised early only to capture dividends; European calls cannot, so they also trade below intrinsic if a dividend is imminent.

- **Early call exercise (dividend capture)** [35:56–39:06]:
  - Exercise a call early only if the upcoming dividend exceeds the put value you're giving up.
  - Unlike puts, there is no Stage 2 optimization for calls—if you're going to exercise, always wait until the day before ex-dividend.
  - Cost-benefit: dividend value vs. put value on the same strike.

- **Deep in-the-money liquidity workaround** [40:34–42:49]:
  - When a deep ITM call market is wide (e.g., 20 cents), consider buying the out-of-the-money put + 100 shares instead; use put-call parity to infer the call's fair value from the tighter put market.
  - This avoids slippage on the wide call bid-ask and may be cheaper than paying financing embedded in the call price.

- **Rate sensitivity** [22:42–24:39]:
  - The risk-free rate (or margin loan rate) is critical to the Stage 1 calculation. IBKR Light vs. Pro accounts have different margin rates (~4.63% for this trade size on Pro). Each trader should use their own borrowing rate, not a generic benchmark.

## Notable quotes

> "The first test you want to run is, is the benefit greater than what the thing I'm giving up? Is the interest greater than the call that I'm giving up if I'm exercising a put?"

> "Exercising is irreversible. Once I exercise, I can't unexercise. So this is part of a larger class of problem called the optimal stopping problem."

> "An American style option can never trade below intrinsic value because you always have the right to sell it at intrinsic. A European option can definitely trade way below intrinsic because of the financing costs."

## Candidate wiki links

**Concepts:**
[[early-exercise]], [[assignment]], [[intrinsic-value]], [[extrinsic-value]], [[put-call-parity]], [[optimal-stopping-problem]], [[theta]], [[delta]], [[vega]], [[implied-volatility]], [[risk-free-rate]], [[financing-costs]], [[american-options]], [[european-options]], [[dividend-capture]], [[cost-benefit-analysis]], [[bid-ask-spread]], [[moneyness]]

**Strategies:**
[[short-put]], [[covered-call]]

**Securities:**
[[ibit]], [[btc]]

**People:**
[[eric]]

## Regime / context

Recorded 2026-06-27 in the immediate aftermath of an early assignment on IBIT short puts. The session uses this live scenario to teach the two-stage framework for evaluating early exercise decisions on American-style options. IBIT had been in a downtrend since October 2025, creating elevated premiums that attracted the short-put position. The analysis is evergreen but grounded in June 2026 market conditions (IBIT IV ~50%, SOFR ~4.3%).
