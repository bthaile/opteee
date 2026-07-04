---
type: source
title: "0 DTE SPX Option Strategy"
video_id: hPcJPFpJ_lM
url: https://www.youtube.com/watch?v=hPcJPFpJ_lM
date: 2020-10-14
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spx]
concepts: [zero-dte, delta, implied-volatility, probability-cone, expected-value, risk-management, position-sizing, stop-loss, margin, buying-power, spread-mechanics, expectancy, standard-deviation-move, bull-market, volatility-clustering]
strategies: [zero-dte, short-put, credit-spread]
saga: null
part: null
confidence: high
---

# 0 DTE SPX Option Strategy

## Summary

Eric analyzes zero days-to-expiration (0 DTE) SPX put spreads, a popular short-premium strategy that appears attractive but carries hidden risks. While he personally tested this approach, he found a 7–9 DTE variant significantly outperforms it. The core issue: despite perceived limited risk via spreads, most traders add stops that create ~40% probability of loss realization, making the risk–reward ratio unfavorable for consistent profitability.

## Key takeaways

- **The appeal and the trap** [00:47–01:37]: 0 DTE trades promise quick daily profits, but this exploits impatience. Eric tested the strategy and found it underperforms a 7–9 DTE hybrid version.

- **Typical setup** [02:01–03:07]: Traders sell low-delta (5–10 delta) put spreads on large indices (SPX, NDX) to reduce contract count. A 50-wide spread at 5 delta collects ~$1.55 per spread, requiring ~$4,800 margin per contract.

- **Limited risk is an illusion** [03:35–04:47]: The spread itself provides max loss protection, but most traders add a stop loss (typically 2–3× credit received) to match their risk tolerance. This negates the spread's protective benefit and increases actual loss probability.

- **Expectancy math** [05:37–06:42]: Max profit $155 vs. max loss $4,845 per spread = poor risk–reward. Scaling to 5–10 lots ($775 profit vs. $24,225 max loss) tests psychological pain tolerance. The spread is primarily a buying-power reduction tool, not true risk mitigation.

- **Stop-loss probability** [07:57–10:59]: With a 2.5× credit stop (~$5.43 on a $1.55 credit), there's approximately 40% probability of being stopped out on a 0 DTE trade. This means 60% win rate but 40% loss rate, creating unfavorable long-term expectancy.

- **Market regime dependency** [11:23–12:34]: The strategy works well in perpetual bull markets with low volatility, but fails in two-sided or choppy markets. It is not a "set and forget" trade; it requires strict entry criteria and environmental conditions.

- **Why 7–9 DTE is superior** [12:11–13:18]: Longer duration allows more buffer for underlying movement, reducing whipsaw exits. Better expectancy and more utilitarian than 0 DTE, though still conditional on market regime.

- **Skepticism on marketing claims** [13:43–14:29]: Anyone selling 0 DTE as a "one-trick pony" strategy is likely omitting other edge sources. Eric's personal testing confirms the strategy is statistically insufficient on its own.

## Notable quotes

> "It's not as good as it sounds and like I said I tried it. I found a hybrid of this strategy to be far more effective where instead of doing zero days to expiration I will do something closer to seven or nine days with slightly different mechanics and that performed significantly better for me."

> "The spread serves as 'oh shit if things go really sideways that's my max loss' but then most folks will also set a stop on top of that so that they can have something returning a little closer to their profile."

> "Sixty percent of the time you'll make something close to your max profit of 155 dollars and then somewhere close to 40 percent of the time you're gonna lose that 543 on that zero days expiration trade."

## Candidate wiki links

**concepts:** [[zero-dte]], [[delta]], [[implied-volatility]], [[probability-cone]], [[expected-value]], [[risk-management]], [[position-sizing]], [[stop-loss]], [[margin]], [[spread-mechanics]], [[expectancy]], [[standard-deviation-move]], [[volatility-clustering]]

**strategies:** [[zero-dte]], [[short-put]], [[credit-spread]]

**securities:** [[spx]]

**people:** [[eric]]

## Regime / context

Recorded October 2020, during a bull-market environment. The analysis reflects market conditions favorable to short-premium strategies. Eric's recommendation to use 7–9 DTE instead of 0 DTE is based on personal backtesting and live trading experience. The strategy's viability is highly dependent on market regime (bull vs. two-sided) and volatility environment; it is not universally applicable.
