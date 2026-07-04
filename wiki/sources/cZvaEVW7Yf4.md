---
type: source
title: "Option Leverage, Convexity, and Gamma | The Options Trench"
video_id: cZvaEVW7Yf4
url: https://www.youtube.com/watch?v=cZvaEVW7Yf4
date: 2026-05-02
series: options-trench
format: [education, strategy-breakdown]
experts: []
mentions: [euan-sinclair]
securities: [pltr]
concepts: [leverage, convexity, gamma, delta, theta, implied-volatility, volatility-term-structure, gamma-ramp, delta-hedging, realized-volatility, vega, moneyness, gamma-exposure, higher-order-greeks, price-action, position-sizing]
strategies: [gamma-scalping, delta-neutral]
saga: null
part: null
confidence: high
---

# Option Leverage, Convexity, and Gamma | The Options Trench

## Summary

This episode dissects the critical distinction between leverage and convexity in options trading. While leverage is a linear amplification of returns, convexity—driven by [[gamma]]—creates non-linear P&L that responds to the *square* of price moves rather than the move itself. The hosts use physics analogies (acceleration and distance) to explain why a 4% move produces four times the impact of a 2% move in options, and demonstrate how [[gamma]] changes across moneyness and time to expiration.

## Key takeaways

### Evergreen mechanics

- **Leverage vs. convexity** [00:28–01:59]: Leverage is linear amplification (2× leverage = 2× return); convexity is non-linear. Options embed both, but convexity is the hidden amplifier most traders underestimate.
- **The squared relationship** [07:08–09:06]: Option P&L depends on the *square* of the price move, not the move itself. A 4% move = 4× the impact of a 2% move; a 6% move = 9× the impact of a 2% move.
- **Gamma as acceleration** [16:00–17:40]: [[Delta]] is velocity (P&L change per $1 move); [[gamma]] is acceleration (change in delta per $1 move). The physics formula `distance = ½ × acceleration × time²` maps exactly to `gamma P&L = ½ × gamma × (price change)²`.
- **Gamma P&L formula** [18:04–18:32]: With 100 gamma and a $3 move: `½ × 100 × 3² = $450` (assuming delta-neutral entry). This is pure convexity gain, independent of direction.
- **Theta as the cost of gamma** [19:17–19:58]: [[Theta]] decay is not an edge; it is the cost of owning gamma. Long gamma always wins on large moves but pays theta daily.
- **Gamma profile across moneyness** [05:39–06:42]: Gamma is lowest far OTM, peaks at-the-money, and drops again ITM. This creates a "ramp" as the underlying approaches a strike.
- **Position size effect** [24:52–27:00]: As a short call moves toward ATM, its [[delta]] increases (position gets larger), so each incremental dollar move costs more. This curvature is convexity in action—your effective position size is changing without you trading.
- **Gamma and time decay** [27:27–31:16]: Gamma explodes as expiration approaches, especially ATM. A 7-day option has ~3× the ATM gamma of a 35-day option. Scaling law: gamma scales with `√(1/DTE)`, so halving DTE increases gamma by ~40%.
- **Gamma and volatility relationship** [33:53–36:35]: Linear inverse relationship: double the [[implied-volatility|IV]], halve the gamma per contract. At high vol, all strikes compress together; a $1 move means less relative to the vol regime.
- **Scaling laws** [38:34–39:13]: Greeks scale either linearly or by square root with respect to DTE and vol. [[Vega]] scales linearly with DTE; [[gamma]] scales with `√DTE`. Use this to ratio hedges: to be gamma-neutral across different expirations, you need `√(DTE ratio)` more contracts in the longer-dated option.

### Dated market read (2026-05-02)

- **Palantir (PLTR) example** [04:48–06:42]: Stock trading ~$128; 150 strike (20 OTM, ~15% OTM) has ~0.013 gamma and 25 delta. If stock rallies to $150, delta doubles to ~50, demonstrating gamma ramp in real time.

## Notable quotes

> "All leverage does is amplify the return by the leverage factor of the instrument. But there's another concept—convexity—that amplifies the return even more, and it's the thing that we're going to zoom in on today."

> "Your option results don't depend on how much the stock moves. They care about how much the stock moves squared."

> "Theta is not an edge. It's just the cost of the gamma. All theta is the cost of that gamma."

## Candidate wiki links

**concepts:** [[leverage]], [[convexity]], [[gamma]], [[delta]], [[theta]], [[implied-volatility]], [[volatility-term-structure]], [[gamma-ramp]], [[delta-hedging]], [[realized-volatility]], [[vega]], [[moneyness]], [[gamma-exposure]], [[higher-order-greeks]], [[price-action]], [[position-sizing]]

**strategies:** [[gamma-scalping]], [[delta-neutral]]

**securities:** [[pltr]]

**people:** [[euan-sinclair]]

## Regime / context

Recorded 2 May 2026. The episode uses Palantir options (35 DTE and 7 DTE) as a live example. The physics-based explanation of convexity and the squared relationship is evergreen and applies to all options across all regimes. The scaling laws (square-root relationship between gamma and DTE, linear relationship between gamma and IV) are fundamental and regime-independent.
