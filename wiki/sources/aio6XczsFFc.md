---
type: source
title: "My Approach to Trading Earnings with Options"
video_id: aio6XczsFFc
url: https://www.youtube.com/watch?v=aio6XczsFFc
date: 2023-07-11
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [hd, aapl, lowe, mgm, ea]
concepts: [binary-events, implied-volatility, expected-move, iv-crush, earnings-move, volatility-term-structure, realized-vs-unrealized-pnl, position-sizing, liquidity-cycle, confirmation-bias, technical-analysis, market-efficiency, post-earnings-drift, delta-neutral, delta-selection, skew]
strategies: [long-straddle, short-straddle, short-strangle, covered-call, ratio-diagonal, ratio-write]
saga: none
part: null
confidence: high
---

# My Approach to Trading Earnings with Options

## Summary

Eric walks through a systematic framework for trading earnings announcements using options, focusing on implied volatility expansion (leading into the event) and contraction (after release) rather than directional bets. The core thesis is that earnings are binary events releasing significant new information; traders can exploit the volatility cycle by being long premium ~2 weeks out and short premium immediately before the announcement, with strict position sizing, liquidity filters, and defined profit/loss targets.

## Key takeaways

### Dated market read (2023-07-11)
- Home Depot (HD) earnings scheduled for May 16 before market open; Lowe's reporting May 23 before market open; Apple (AAPL) has an upcoming earnings cycle with elevated near-term IV [05:41–05:57].

### Evergreen mechanics

- **Binary event nature** [00:41–01:03]: Earnings releases are binary events because they dump large amounts of new information at once—historical performance, forward guidance, and projections—creating potential for large directional moves.

- **IV expansion timeline** [02:36–02:57]: Implied volatility typically begins expanding ~2 weeks before earnings; this is well-documented in academic literature (SSRN papers on earnings releases). The expansion is forward-looking and reflects market anticipation of volatility.

- **Expected move calculation** [03:49–04:25]: Use the at-the-money straddle price in the expiration cycle containing the earnings date to estimate expected move. For example, a $14.60 ATM straddle implies ~$14.60 up or down. Refresh this calculation close to the event, as other market moves can shift it.

- **Expiration cycle selection is critical** [04:07–04:41]: Always trade the expiration cycle that *contains* the earnings date. A cycle without the earnings event will not capture IV expansion, as the market knows that cycle is not exposed to the catalyst.

- **IV term structure anomaly** [04:58–05:41]: Look for the expiration with elevated IV relative to surrounding cycles—this signals an upcoming earnings event. Normal term structure shows IV increasing with time to expiration; an inversion (near-term IV > far-term IV) indicates an event.

- **IV contraction post-earnings** [06:16–06:34]: After earnings release, implied volatility contracts sharply because the information is now known. Both the expansion and contraction phases are tradable.

- **Long IV strategy: long straddles** [06:53–07:12]: To trade IV expansion (2 weeks to ~1 week before), use long straddles as the primary vehicle. Rarely use long single options unless there is a strong directional hypothesis, which is atypical for earnings plays.

- **Short IV strategy: short straddles/strangles** [07:12–07:46]: To trade IV contraction (right before release), use short straddles or short strangles. Can add directional skew (sell more calls than puts, or vice versa) if there is a secondary directional bias, but the primary hypothesis is IV contraction.

- **Timing for contraction trades** [09:19–10:23]: Enter short premium trades right before market close on the day before the announcement (or same day if AM release). Use the closest expiration cycle. Exit shortly after the open on the release day, once volatility has drained meaningfully—do not hold all day hoping for follow-through.

- **Position sizing** [11:36–11:53]: Size down into earnings because moves are large and frequent. Avoid trying to hit a home run on any single trade; there are many earnings events in a cycle.

- **Liquidity requirement** [11:53–12:11]: Trade mostly S&P 500 constituents or stocks with weekly options. Liquidity is critical; if a trade goes wrong and the stock gaps, illiquid positions become impossible to exit. Volatility expansion can further reduce liquidity at the worst time.

- **Defined P&L targets** [12:31–12:48]: Set clear profit targets and loss limits before entry. Do not rely solely on defined-risk strategies, but always have a plan for when to exit.

- **Exit discipline** [12:48–13:20]: After earnings release, give the market a few minutes for volatility to drain, then exit. Do not hold through the day chasing additional profit; reversals are common, and confirmation bias can trap traders.

- **Watch list and historical analysis** [13:56–14:35]: Maintain a watch list of earnings plays. Review at least 6–8 prior quarters for each stock: expected EPS, actual EPS, close before release, open after release, high/low after release. This provides context on typical move size and behavior, though outliers are common.

- **Hedging considerations** [14:54–15:36]: Hedging is expensive and can undermine the IV contraction thesis (buying expensive options to hedge short premium). Avoid downside hedges; consider capping upside risk on strong stocks that can gap up sharply post-earnings.

- **IV vs. realized volatility** [15:56–17:11]: The entire earnings trade assumes implied volatility will be elevated relative to realized (historic) volatility. Review IV/HV charts for past earnings to see if IV > HV held through the event. Occasionally realized volatility exceeds implied (a "miss"), making the trade unprofitable.

- **Limited efficacy of fundamentals and technicals** [17:29–17:52]: Fundamental multiples and technical support/resistance have limited predictive power around earnings due to the flood of new information. Do not weight these heavily.

- **Post-earnings drift (PED) weakening** [18:09–18:27]: Positive earnings announcement drift (continuation of post-earnings moves) has contracted significantly for S&P 500 stocks in the past 2 years, reducing its utility as a follow-on trade.

## Notable quotes

> "When we're trading implied volatility contraction our entire hypothesis is that implied volatility is high compared to the expected historic volatility." [14:54–15:14]

> "Remember we're trading the volatility here not the direction." [13:20]

## Candidate wiki links

**concepts:** [[binary-events]], [[implied-volatility]], [[expected-move]], [[iv-crush]], [[earnings-move]], [[volatility-term-structure]], [[realized-vs-unrealized-pnl]], [[position-sizing]], [[liquidity-cycle]], [[confirmation-bias]], [[technical-analysis]], [[market-efficiency]], [[post-earnings-drift]], [[delta-neutral]], [[delta-selection]], [[skew]]

**strategies:** [[long-straddle]], [[short-straddle]], [[short-strangle]], [[covered-call]], [[ratio-diagonal]], [[ratio-write]]

**securities:** [[hd]], [[aapl]], [[lowe]], [[mgm]], [[ea]]

**people:** [[eric]]

## Regime / context

Recorded July 11, 2023. Examples reference May 2023 earnings calendar (Home Depot, Lowe's, Apple). The framework is evergreen for any earnings cycle; the specific note on post-earnings drift contraction in S&P 500 stocks reflects market behavior as of mid-2023.
