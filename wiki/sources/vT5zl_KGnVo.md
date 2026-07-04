---
type: source
title: "Iran War Impact on Oil Volatility and Inflation"
video_id: vT5zl_KGnVo
url: https://www.youtube.com/watch?v=vT5zl_KGnVo
date: 2026-03-28
series: options-trench
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spy, qqq, iwm, usl, gld, slv, tlt, ief, rbob, wti, oxy, crude-oil]
concepts: [volatility-risk-premium, implied-volatility, volatility-skew, risk-reversal, delta-hedging, position-sizing, realized-volatility, momentum, technical-analysis, market-regimes, inflation, interest-rates, duration, equity-risk-premium, expected-move, probability-of-touch, delta, vega, gamma, price-action, relative-value, correlation, risk-management, kelly-criterion, expected-value]
strategies: [call-credit-spread, put-spread, long-call, short-premium, pairs-trade, momentum]
saga: null
part: null
confidence: high
---

# Iran War Impact on Oil Volatility and Inflation

## Summary

In a volatile geopolitical environment driven by Iran tensions, oil prices have spiked dramatically, creating a cascading effect across asset classes. The hosts analyze how elevated oil futures curves, combined with rising inflation expectations, create pricing discrepancies between equity and bond markets. They demonstrate a systematic approach to finding relative-value trades by comparing implied probabilities across different assets and using vertical spreads to isolate directional bets from volatility exposure.

## Key takeaways

### Dated market read (2026-03-28)

- **Oil curve inversion signals inflation risk** [03:05–06:36]: RBOB (gasoline) front-month futures are 25–30% higher than 1-year contracts. If spot prices hold, rolling futures could force CPI up 1%+ directly from gasoline alone, with second-order effects potentially pushing inflation to 4–5% annually.
- **Gold and bonds showing downside skew** [03:44–04:50]: Gold down ~15% in one month (a 1-year standard-deviation move); put skew and risk reversals in both gold (GLD) and long bonds (TLT, IEF) are making 1-year highs, signaling market concern about inflation and rising rates despite only ~25 bps move in 10-year yields.
- **Fed rate expectations have shifted** [08:55–09:27]: Previous probability of two additional rate cuts has evaporated; now 25% probability of 25 bps *raises* priced in for September through April, a complete reversal from zero probability before.
- **VIX and realized vol elevated** [24:37–25:48]: VIX above 24–25 handle since March 6; average name in watchlist at 85th percentile of 1-year vol; realized vols also high, but implied even higher—substantial vol risk premium in the market.

### Evergreen mechanics

- **Vertical spreads isolate probability** [19:39–20:54]: A $10 call spread with defined risk/reward (e.g., pay $2.50 to make $7.50 = 3:1 odds) cleanly expresses a probability bet, unlike single options which conflate probability with distance-through-strike. Vega cancellation across strikes removes vol sensitivity.
- **Payoff visualizer for strike selection** [21:42–22:41]: Grid-search tool showing every strike pair and odds for a target price reveals intuition: wider strikes pay more (lower win probability); tighter strikes pay less (higher win probability).
- **Cross-asset relative-value framework** [11:07–16:12]: Identify contradictions in implied probabilities across markets. Example: if oil call spread pays 3:1 for spot staying flat, and S&P put spread pays 6:1 for 20% decline, compare those odds to your own scenario probabilities to find mispricings.
- **Scenario analysis through duration math** [13:34–15:27]: If 10-year yields rise 100 bps, bond prices drop ~7% (duration ≈ 7); if CPI rises 100 bps and equity risk premium stays constant, S&P PE compresses from 20× to 16×, implying ~20% equity decline. Compare payoffs on both to find relative value.
- **Momentum vs. implied vol** [33:02–38:32]: Annualize recent 1-month returns and compare to implied vol term structure. Oxy up 32% in 27 trading days (≈90% annualized vol) but 90-day IV only 42—not expensive in context. Prevents blindly selling "high vol" without checking realized moves.
- **Directional conviction + sizing** [40:15–48:51]: Options enable asymmetric risk/reward when you have directional edge. Buying "expensive" puts as a hedge/stop-loss allows you to size into a larger directional bet (long deltas) with defined downside. The put's cost is the insurance premium for the right to take the bet you want.
- **Net short vol = longer delta than you think** [26:41–28:33]: Selling options in high-vol environments implicitly adds delta exposure. If market drops 20% and you're short premium, you're longer than your notional suggests. Awareness of this hidden leverage is critical.

## Notable quotes

> "I just look at prices, and I look at option surfaces. That's my blanket."

> "The way I thought about buying those puts was they gave me the option to buy all the deltas that I actually wanted to buy. Like I could never have made that bet if that put didn't exist."

> "Size is the gigantic variable. If you're right about things all the time but you're not big when you're right and you're not small when you're wrong, that's the problem."

## Candidate wiki links

**concepts:** [[volatility-risk-premium]], [[implied-volatility]], [[volatility-skew]], [[risk-reversal]], [[delta-hedging]], [[position-sizing]], [[realized-volatility]], [[momentum]], [[inflation]], [[interest-rates]], [[duration]], [[equity-risk-premium]], [[expected-move]], [[delta]], [[vega]], [[relative-value]], [[risk-management]], [[expected-value]]

**strategies:** [[call-credit-spread]], [[put-spread]], [[long-call]], [[short-premium]], [[pairs-trade]]

**securities:** [[spy]], [[qqq]], [[iwm]], [[crude-oil]], [[gld]], [[tlt]], [[oxy]]

**people:** [[eric]]

## Regime / context

Recorded March 28, 2026, during active Iran–US tensions with elevated geopolitical risk premium. Oil futures curve steep (contango), VIX sustained above 24 for ~3 weeks. Fed pivot from rate-cut expectations to potential hikes has repriced bond and equity risk premiums. This is a high-vol, high-realized-move environment where relative-value and scenario-based hedging strategies are particularly relevant. The analysis applies to any regime where multiple asset classes are repricing simultaneously due to a common shock (inflation, rates, geopolitical event).
