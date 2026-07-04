---
type: source
title: "Traps of options, Picking a strike, Selecting an expiration | Options Trading for Beginners Pt1"
video_id: LuhAOKk3rjI
url: https://www.youtube.com/watch?v=LuhAOKk3rjI
date: 2024-06-08
series: beginner-lab
format: [education, live]
experts: [eric]
mentions: []
securities: [spy, tsla, gme, spx]
concepts: [delta, theta, vega, gamma, implied-volatility, realized-volatility, moneyness, intrinsic-value, extrinsic-value, volatility-risk-premium, volatility-clustering, volatility-mean-reversion, expected-move, probability-cone, volatility-term-structure, assignment, early-exercise, settlement, leverage, risk-management, position-sizing, paper-trading, trading-psychology, process-over-outcome, edge, expected-value]
strategies: [long-call, long-put, short-call, short-put, covered-strangle, ratio-call-diagonal, ratio-write, short-straddle, short-strangle, short-volatility, zero-dte]
saga: none
part: null
confidence: high
---

# Traps of options, Picking a strike, Selecting an expiration | Options Trading for Beginners Pt1

## Summary

A foundational live workshop for beginner options traders covering the core mechanics of options contracts, the Greeks (delta, theta, vega, gamma), moneyness, and premium decomposition. The session emphasizes that options trading is not "easy money" but a learnable skill requiring discipline, proper position sizing, and paper trading before live capital deployment. Key themes include volatility as a tradable asset class, the importance of time and strike selection, and practical approaches to earnings-related volatility plays.

## Key takeaways

### Foundational mechanics
- **Options are contracts, not lottery tickets** [02:15–06:24]: Trading options is difficult but worthwhile if taken seriously. The misconception that it's "easy money" leads traders to apply insufficient effort and fail. Leverage and customizable payoff structures are the real edge, not speed or simplicity.
- **Derivatives derive value from underlying assets** [07:05–08:15]: Options are contracts whose value depends on equities, debt, or other securities. Unlike stocks (finite supply), options can be created at will provided a counterparty exists.
- **Buyer vs. seller obligations** [25:11–26:06]: Buyers of options have the *right* to exercise; sellers have the *obligation* to fulfill. This asymmetry is fundamental to pricing and risk.
- **Premium has two components: intrinsic and extrinsic** [53:50–56:08]: Intrinsic value reflects how far in-the-money an option is; extrinsic (time value + volatility) decays as expiration approaches. Understanding this split is critical for strike and expiration selection.

### Moneyness and the Greeks
- **Moneyness is determined by strike vs. underlying price alone** [55:03–56:08]: For calls, in-the-money (ITM) = strike < underlying price. For puts, ITM = strike > underlying price. Whether you are long or short does not change moneyness.
- **Delta, Theta, Vega, Gamma are the primary Greeks** [01:05:43–01:06:35]: Delta measures premium change per $1 move in underlying; Theta measures decay per day; Vega measures sensitivity to volatility; Gamma (second-order) measures delta's rate of change. These govern how positions behave under different market conditions.
- **Volatility impacts both calls and puts equally** [31:58–32:26]: Higher implied volatility increases premium for both calls and puts. Volatility is simply expected movement; higher volatility = higher risk and reward potential for both sides.

### Strike and expiration selection
- **Avoid cheap, far-OTM calls that expire worthless** [03:04], [01:32:43–01:34:09]: Retail traders often buy short-dated, far-out-of-the-money calls because they're cheap, but they require massive moves to profit. Solution: go further out in time (more extrinsic value to work with) and closer to the money (higher probability of profit). Gamma ramps faster on ATM or slightly ITM calls.
- **Time decay (Theta) is your friend or enemy depending on position** [34:10–35:03]: Longer-dated options have more extrinsic value and give the underlying more time to move in your favor. Shorter-dated options decay faster, which hurts long premium buyers but helps short premium sellers.
- **Break-even at expiration ≠ break-even today** [01:35:22–01:36:31]: For a long call, break-even at expiration = strike + debit paid. But you can profit before expiration if the underlying moves in your favor, because extrinsic value decays and intrinsic value grows.

### Volatility as an asset class
- **Implied volatility typically overstates realized volatility (variance risk premium)** [01:13:39–01:15:06]: Implied volatility (forward-looking) tends to price in larger moves than actually occur. This creates a short-volatility edge: sell premium when IV is elevated, close after IV contracts.
- **Volatility clusters and mean-reverts** [01:15:34–01:16:02]: Volatility tends to hover near recent levels (clustering) until a transitory event causes it to shift, then it clusters again at a new level. This makes short volatility strategies statistically favorable over time.
- **Earnings volatility patterns** [01:22:37–01:24:59]: ~2 weeks before earnings, implied volatility expands. Post-earnings, it typically contracts. Short straddles/strangles before earnings and close after the move can capture this contraction—but it's a numbers game; some earnings see realized vol exceed implied vol, causing losses.

### Paper trading and position management
- **Paper trade before risking real capital** [01:41:14–01:42:40]: New traders should use fake money (thinkorswim on-demand, Google Sheets, or broker simulators) to learn without drawdown risk. Paper trading will never fully replicate live trading, but it eliminates costly early mistakes.
- **Expected value, not win-rate, drives profitability** [01:30:24–01:32:05]: Scalping or any strategy must account for bid-ask spread, theta decay, commissions, and loss management. A +1% win and −2% loss requires a win-rate > 66% to be profitable. Use expected return calculations, not arbitrary profit-taking rules.
- **Settlement: trade the option, don't exercise** [01:36:56–01:37:44]: Close options by trading (selling if you bought, buying if you sold) rather than exercising. Exercising forfeits remaining extrinsic value. Trade settlement is lower-friction and more profitable.

### Practical considerations
- **Options multiplier is 100 shares per contract** [01:38:20–01:38:52]: Quoted prices are per share; multiply by 100 to get actual cost. Each contract controls 100 shares.
- **Liquidity is critical for scalping** [01:29:34–01:30:24]: Without tight bid-ask spreads, friction eats all edge. Strike selection and sizing must account for expected move, slippage, and theta decay.
- **Simplicity beats complexity** [01:16:29–01:17:34]: Multi-leg strategies (jade lizards, etc.) add friction and margin for error. Basic structures (covered strangles, ratio diagonals, ratio covered calls) are more reliable for retail traders.

## Notable quotes

> "Trading is difficult but in my opinion if you take it seriously it is entirely worth the time and effort."

> "The fact that it's not easy money is where the opportunity lies—imagine if everyone could make fast easy money; it would price the system out."

> "Simplicity is the ultimate form of sophistication."

## Candidate wiki links

### Concepts
[[delta]], [[theta]], [[vega]], [[gamma]], [[implied-volatility]], [[realized-volatility]], [[moneyness]], [[intrinsic-value]], [[extrinsic-value]], [[volatility-risk-premium]], [[volatility-clustering]], [[volatility-mean-reversion]], [[expected-move]], [[probability-cone]], [[volatility-term-structure]], [[assignment]], [[early-exercise]], [[settlement]], [[leverage]], [[risk-management]], [[position-sizing]], [[paper-trading]], [[trading-psychology]], [[process-over-outcome]], [[edge]], [[expected-value]]

### Strategies
[[long-call]], [[long-put]], [[short-call]], [[short-put]], [[covered-strangle]], [[ratio-call-diagonal]], [[ratio-write]], [[short-straddle]], [[short-strangle]], [[short-volatility]], [[zero-dte]]

### Securities
[[spy]], [[tsla]], [[gme]], [[spx]]

### People
[[eric]]

## Regime / context

Recorded 2024-06-08 (Friday live workshop). This is Part 1 of a beginner-focused series; Eric indicates plans to run two beginner sessions per month (first and third Fridays). The session assumes zero-to-minimal options experience and prioritizes foundational mechanics over advanced strategies. Volatility environment and specific price levels are approximate (ASR-garbled in places); focus on the conceptual framework rather than exact figures.
