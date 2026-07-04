---
type: source
title: "Vega, Volga, Vomma | The Options Trench"
video_id: U0u1rT_3Q6U
url: https://www.youtube.com/watch?v=U0u1rT_3Q6U
date: 2026-05-16
series: options-trench
format: [education, strategy-breakdown]
experts: []
mentions: [euan-sinclair]
securities: [spy, gme]
concepts: [vega, gamma, convexity, implied-volatility, volatility-skew, delta, moneyness, greeks, higher-order-greeks, mark-to-market, volatility-surface, ratio-call-diagonal, vega-neutral, position-sizing, risk-management, trading-psychology]
strategies: [ratio-call-diagonal, short-strangle, short-straddle, covered-strangle]
saga: null
part: null
confidence: high
---

# Vega, Volga, Vomma | The Options Trench

## Summary

This episode explores higher-order Greeks—specifically vega, volga (or vamma), and vomma—and how volatility changes reshape option Greeks across the strike surface in ways that can surprise traders. The hosts demonstrate how a position that appears vega-neutral at one volatility level can become dramatically short vega when implied volatility spikes, using ratio spreads and far-out-of-the-money short options as practical examples. The key insight: Greeks are snapshots in time, and convexity in the volatility dimension can turn seemingly safe trades into margin-draining disasters.

## Key takeaways

- **Vega peaks at-the-money and decays out-of-the-money** [06:25–07:13]. At-the-money options have maximum vega (~$1.26 per point for 79 DTE SPY); far OTM options have minimal vega initially but explosive sensitivity to volatility changes (volga).

- **At-the-money vega is insensitive to volatility level itself** [23:25–24:12]. The vega of an ATM option depends only on time to expiration and strike price, not on the current IV level. This is a direct output of Black-Scholes.

- **Ratio spreads (1×2) can appear vega-neutral but become short vega when IV spikes** [12:59–13:46]. A trader might construct a 1×2 call spread with zero net vega, but when volatility increases, the short OTM calls gain vega faster than the long ATM call, flipping the position to short vega.

- **Volga (vega gamma) is highest far out-of-the-money** [44:33–45:18]. Out-of-the-money options have minimal vega but enormous volga—their vega sensitivity to IV changes is convex. This creates the "U-shaped" volga profile (inverse of the vega curve).

- **Extreme IV moves can cause mark-to-market losses on margin** [42:12–43:23]. A 20–30% IV shock on a seemingly safe 1×2 or far-OTM short strangle can generate $2,600+ unrealized losses per contract, forcing liquidation at the worst time.

- **Far-OTM short options are "nitroglycerin"** [51:18–52:08]. Selling 5-delta options may have 90%+ probability of profit, but when they move, delta can explode from 5 to 90, and vega sensitivity becomes non-linear. Professional traders avoid this because the juice isn't worth the squeeze.

- **Vega is non-uniform across the volatility surface** [08:02–08:29]. IV percentile or IV rank being high doesn't mean all strikes are equally rich; skew means puts trade higher IV than calls, and vega per strike varies accordingly.

- **Why longer-dated straddles are always more expensive than shorter-dated ones** [16:13–17:18]. Expected move scales with √time; a longer straddle must be more expensive, or arbitrage is available (buy calendar spread).

- **At extreme IV levels, all strikes converge in Greeks** [36:16–37:23]. When IV is very high (e.g., 200%), a 20% OTM strike is "a sneeze" away from ATM; all options behave similarly. A 1×2 position collapses to net short 1 option.

- **Structured products and ratio trades exploit volga** [48:35–49:40]. Banks sell attractive-looking payoff diagrams (e.g., 1×2 put spreads) that are short volga; they hedge by buying volga elsewhere, profiting when IV spikes.

- **Platforms don't display volga, but it's calculable** [50:19–50:40]. Most retail brokers (IB, Think or Swim) don't show volga per strike, making it invisible to retail traders despite being as easy to compute as delta or gamma.

- **Professional sellers focus on ATM/straddles, not wings** [51:43–53:26]. Euan Sinclair and other pros avoid selling far-OTM options because the convexity risk is unquantifiable and the premium doesn't compensate for tail risk.

## Notable quotes

> "If you sell really far out of the money options, there can be a really ugly part in the holding of your position that makes you question just about everything." [01:42–02:05]

> "At extreme levels of volatility, all that matters is what your inventory is... I'm just short one option." [37:23–37:41]

> "The Greeks on those out-of-the-money options are like nitroglycerin. They operate completely differently than the way at-the-money options do." [51:18–51:43]

## Candidate wiki links

**concepts:** [[vega]], [[gamma]], [[convexity]], [[implied-volatility]], [[volatility-skew]], [[delta]], [[moneyness]], [[greeks]], [[higher-order-greeks]], [[mark-to-market]], [[volatility-surface]], [[vega-neutral]], [[position-sizing]], [[risk-management]], [[trading-psychology]]

**strategies:** [[ratio-call-diagonal]], [[short-strangle]], [[short-straddle]], [[covered-strangle]]

**securities:** [[spy]], [[gme]]

**people:** [[euan-sinclair]]

## Regime / context

Recorded May 16, 2026. The discussion is evergreen—volga and higher-order Greeks apply across all market regimes, though the impact is most visible during volatility shocks (e.g., geopolitical events, earnings surprises). Single-stock volatility can reach extreme levels (GameStop mentioned at 400–500 IV); index volatility (SPX) typically ranges 15–45 but can spike to 45+ in stress scenarios. The 79 DTE SPY example is chosen for clarity; the mechanics hold at any expiration, though vega per contract is larger further out in time.
