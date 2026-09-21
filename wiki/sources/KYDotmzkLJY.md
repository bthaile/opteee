---
type: source
title: "Buying vs Selling Options: Which is Better?"
video_id: KYDotmzkLJY
url: "https://www.youtube.com/watch?v=KYDotmzkLJY"
date: "2026-09-20"
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: []
concepts: [buying-premium, selling-premium, put-skew, variance-risk-premium, implied-volatility, realized-volatility, delta-neutral, directional-bias, bid-ask-spread, defined-risk, drawdown-management, regime-dependency, iv-rank, position-sizing, risk-management]
strategies: [long-call, long-put, short-put, short-call, short-put-spread, put-vertical-spread, call-vertical-spread, long-call-vertical-spread, short-strangle, covered-call, protective-put]
saga: none
part: null
confidence: high
---

# Buying vs Selling Options: Which is Better?

## Summary

This analysis examines 2.4 million options trades across 1,149 underlyings over 19 years (2007–2026) to contextualize the relationship between buying and selling options. The data reveals that neither approach is universally superior; instead, success depends on regime, structure selection, and honest accounting of directional bias and transaction costs. Bullish-biased selling strategies performed well during this uptrend-dominated period, but the variance risk premium is regime-dependent and bid-ask friction affects all traders equally.

## Key takeaways

### Dated market read (2007–2026)
- **Bullish bias dominates returns** [01:50] — Upside-favoring strategies outperformed bearish ones over the 19-year backtest, but this reflects the parabolic bull market, not an inherent superiority of selling.
- **Put skew is real and costly** [02:43] — Puts are systematically more expensive than calls due to lower price sensitivity in downside hedging; this creates a structural cost for put buyers and a potential edge for put sellers.
- **Selling wins more trades, buying wins bigger** [03:28] — Short premium strategies generate frequent small wins; long premium strategies produce rare large wins interspersed with slow account decay.

### Evergreen mechanics
- **Bid-ask spread is universal friction** [03:51] — Commission-free trading masks the real cost: bid-ask spreads on cheap options can be devastating, affecting both buyers and sellers equally.
- **Direction dominates variance** [05:22] — Across all structures tested, directional P&L outweighs variance (delta-neutral) P&L significantly; variance opportunities exist but require careful targeting.
- **Variance risk premium is not always positive** [06:25] — The difference between implied and realized volatility cycles through positive and negative regimes; selling puts to capture VRP while holding directional risk is a conflation.
- **Vertical spreads control tail risk** [07:45] — Short put verticals limit max loss compared to naked short puts, reducing per-trade drawdown, but also reduce premium collected and can lead to slow loss accumulation during losing clusters.
- **Defined risk ≠ lower drawdown** [10:20] — Defined-risk plays (verticals) produce smaller per-trade losses but still experience losing clusters; total account drawdown may not improve if premium collected is lower.
- **Popular conditions are weak predictors** [11:13] — IV rank, variance risk premium, and other common directional forecasting conditions perform near coin-flip accuracy; regime-based effects are significant.
- **Regime dependency is critical** [12:15] — Strategy rankings shift dramatically across periods (e.g., 30 DTE 30-delta puts ranked #1 in one era, #77 in another); middle-ground structures tend to perform sideways.
- **Fit your tools to your regime** [13:17] — Buying is not inherently better than selling, or vice versa; success requires understanding how each tool behaves and adapting to market regime.

## Notable quotes

> "The whole point of this video is to help you think of the relationship between buying and selling options logically, and understand where either may or may not fit into your book." [01:00]

> "Selling options, you make a lot less money per trade and you win more trades. And when you're buying options, most of the time you'll find yourself kind of in this middle ground somewhere and every once in a while you'll get huge wins and every once in a while you'll just get nothing, and your account will drain slowly." [03:28]

> "Buying is not better than selling or vice versa. It's understanding how the tools behave and then fitting them in your tool bag logically." [13:17]

## Candidate wiki links

**concepts:** [[buying-premium]], [[selling-premium]], [[put-skew]], [[variance-risk-premium]], [[implied-volatility]], [[realized-volatility]], [[delta-neutral]], [[directional-bias]], [[bid-ask-spread]], [[defined-risk]], [[drawdown-management]], [[regime-dependency]], [[iv-rank]], [[position-sizing]], [[risk-management]], [[transaction-costs]], [[tail-risk]], [[losing-clusters]], [[regime-shift]]

**strategies:** [[long-call]], [[long-put]], [[short-put]], [[short-call]], [[short-put-spread]], [[put-vertical-spread]], [[call-vertical-spread]], [[long-call-vertical-spread]], [[short-strangle]], [[covered-call]], [[protective-put]], [[vertical-spreads]]

**people:** [[eric]]

## Regime / context

This analysis spans 2007–2026, a period dominated by a parabolic bull market interrupted by three major drawdowns (2008 financial crisis, 2020 COVID crash, 2023 bear market). The bullish bias of results reflects this regime; outcomes would differ materially in a secular bear market or sideways consolidation. The 2023 bear market analysis is notable: vertical spreads performed well despite the downtrend, likely due to slow grinding declines rather than shock moves. All findings are regime-dependent and require adaptive strategy selection as market conditions evolve.
