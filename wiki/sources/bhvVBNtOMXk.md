---
type: source
title: "Option Structures and Strike Selection | Options Trading for Beginners Pt2"
video_id: bhvVBNtOMXk
url: https://www.youtube.com/watch?v=bhvVBNtOMXk
date: 2024-06-15
series: beginner-lab
format: [education, live]
experts: [eric]
mentions: [roaring-kitty, nassim-taleb, euan-sinclair]
securities: [gme, iwm, aapl, nvda, spy, hood]
concepts: [delta, gamma, theta, vega, implied-volatility, volatility-term-structure, volatility-skew, greeks, moneyness, days-to-expiration, extrinsic-value, intrinsic-value, theta-decay, probability-of-touch, expected-move, market-maker, bid-ask-spread, assignment, early-exercise, risk-management, position-sizing, portfolio-first, process-over-outcome, edge, profit-mechanism, expected-return, trading-psychology, emotional-discipline]
strategies: [long-call, short-call, long-put, short-put, call-credit-spread, put-credit-spread, long-straddle, short-straddle, long-strangle, short-strangle, iron-condor, iron-butterfly, ratio-call-diagonal, covered-call, protective-put, synthetic-long]
saga: none
part: null
confidence: high
---

# Option Structures and Strike Selection | Options Trading for Beginners Pt2

## Summary

This workshop covers option structures, strike selection mechanics, and the Greeks—the foundational tools for understanding how options behave across time, price movement, and volatility. Eric walks through single-leg options (calls and puts), multi-leg spreads (verticals, straddles, strangles, iron condors), and emphasizes that options are tools to implement a profit mechanism, not an edge in themselves. The session stresses portfolio-first thinking, risk management via sizing, and the critical importance of defining rules ahead of time rather than discretionary trade-by-trade decisions.

## Key takeaways

### Dated market read (2024-06-15)
- GameStop volatility and structure complexity remain a live teaching example; broader market participants (HFTs, prop traders, market makers, retail) operate in fundamentally different competitive spaces [02:11–02:27]
- Implied volatility skew visible across expirations and strikes; relative value opportunities exist in kinks and term-structure departures (e.g., 28 June vs. 19 July call/put skew on SPX) [21:16–30:43]

### Evergreen mechanics

**Options pricing & volatility:**
- Options are priced by market consensus via supply and demand; retail should use implied volatility (IV) from current prices rather than attempt to forecast volatility unless sophisticated [18:30–20:07]
- Volatility increases as you move further out in time (more can happen); near-term volatility often contracts as expiration approaches [01:02:10–01:03:28]
- Volatility skew and term-structure kinks reveal relative value plays; compare IV across strikes and expirations to identify mispricings [21:16–30:43]

**Strike selection & Greeks:**
- When buying calls/puts, go beyond 60 DTE and consider slightly in-the-money (higher Delta) to reduce time decay risk; further OTM options have higher gamma and theta bleed [37:18–42:07]
- Delta represents directional exposure; Gamma measures Delta's rate of change (accelerates near expiration); Theta is daily extrinsic value decay; Vega is sensitivity to IV changes [01:06:28–01:08:43]
- Theta decay accelerates within 60 DTE; buying options beyond 60 DTE reduces time risk but increases capital outlay [37:18–42:07]
- Deeper ITM options (higher Delta) have lower theta decay on a dollar basis but cost more upfront; further OTM options (lower Delta) have higher percentage returns on smaller capital if a big move occurs [48:09–55:41]

**Single-leg options:**
- Long call: break-even = strike + premium; you profit if underlying moves up enough to cover premium, but don't need to reach strike to start profiting [01:10:27–01:15:13]
- Short call: break-even = strike + credit received; you have a buffer against upward moves equal to the credit [01:15:36–01:17:35]
- Long put: break-even = strike − premium; profit if underlying falls enough [01:19:19–01:22:47]
- Short put: break-even = strike − credit; you have a buffer against downward moves [01:19:19–01:22:47]

**Multi-leg structures:**
- Vertical spreads (call/put spreads): add a short leg to define risk and reduce capital requirement; similar profit zone to single options but with capped risk [01:24:15–01:24:36]
- Long straddle/strangle: bet on volatility expansion (big move in either direction); short straddle/strangle: bet on volatility contraction (stay in range) [01:25:58–01:28:16]
- Iron condor / iron butterfly: defined-risk versions of straddles/strangles; short versions profit if underlying stays within range [01:28:16–01:28:59]
- Ratio call diagonal: buy longer-dated, deeper ITM calls; sell shorter-dated, further OTM calls ("kicker options") for leverage and compounding potential [46:40–52:48]

**Position management & psychology:**
- Exercise options only if you intend to hold shares; exercising a losing long call/put forfeits remaining extrinsic value and ties up capital inefficiently [42:24–45:00]
- Don't make trade-by-trade discretionary decisions (e.g., "take profits" or "cut losses" ad hoc); define rules ahead of time and measure strategy performance over a long-term system [56:04–58:34]
- Avoid obsessing over what the other side of your trade is thinking; focus on your own profit mechanism and system [14:13–16:43]
- Position sizing is directly correlated with risk; portfolio-first approach (core allocation + speculative allocation) beats position-first approach [01:35:50–01:40:39]

**Quantifying probability:**
- Use probability of touch (not just probability of expiration ITM) to inform early management rules [01:43:04–01:44:11]
- Options chains embed probability; a 30 Delta call has ~30% probability of being ITM at expiration, but higher probability of being touched intraday [01:43:27–01:44:11]

**Practical exercises:**
- Build a Google Sheet with Delta, Gamma, Theta, Vega across 3–4 expirations and multiple strikes to internalize Greek behavior [01:21:18–01:22:08]
- Study relative volatility plays by comparing IV across strikes and expirations; identify kinks and term-structure anomalies [21:16–30:43]

## Notable quotes

> "There's always a trade. The issue is whether you have a diverse enough skill set to find it, or whether you're willing to size down enough to be comfortable putting it on." [05:18–05:36]

> "Volatility is the one part that we're using to price options. That's really what we're trading as options traders, whether or not you fully recognize it." [58:59–59:21]

> "Don't get too wrapped up in the outcome of an individual trade. Everything you do as a trader should be viewed in the performance of a long-term system." [57:48–58:09]

## Candidate wiki links

**concepts:**
[[delta]], [[gamma]], [[theta]], [[vega]], [[greeks]], [[implied-volatility]], [[volatility-term-structure]], [[volatility-skew]], [[moneyness]], [[days-to-expiration]], [[extrinsic-value]], [[intrinsic-value]], [[theta-decay]], [[probability-of-touch]], [[expected-move]], [[market-maker]], [[bid-ask-spread]], [[assignment]], [[early-exercise]], [[risk-management]], [[position-sizing]], [[portfolio-first]], [[process-over-outcome]], [[edge]], [[profit-mechanism]], [[expected-return]], [[trading-psychology]], [[emotional-discipline]]

**strategies:**
[[long-call]], [[short-call]], [[long-put]], [[short-put]], [[call-credit-spread]], [[put-credit-spread]], [[long-straddle]], [[short-straddle]], [[long-strangle]], [[short-strangle]], [[iron-condor]], [[iron-butterfly]], [[ratio-call-diagonal]], [[covered-call]], [[protective-put]], [[synthetic-long]]

**securities:**
[[gme]], [[iwm]], [[aapl]], [[nvda]], [[spy]], [[hood]]

**people:**
[[roaring-kitty]], [[nassim-taleb]], [[euan-sinclair]]

## Regime / context

Recorded 2024-06-15 (Friday afternoon, US market hours). This is Part 2 of the beginner-lab series; Part 1 covered options fundamentals (calls, puts, buyers, sellers, Greeks intro). The session is live and interactive, with chat participation shaping the flow. GameStop volatility is a live teaching example but not the focus. Volatility environment and term-structure observations are specific to the date; relative value mechanics are evergreen. Next session planned to focus on profit-mechanism analysis and capital allocation.
