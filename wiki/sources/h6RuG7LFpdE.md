---
type: source
title: "Option Volatility Overview — Implied, Historical, Realized & Forecast"
video_id: h6RuG7LFpdE
url: "https://www.youtube.com/watch?v=h6RuG7LFpdE"
date: "2025-02-07"
series: beginner-lab
format: [education, live]
experts: [eric]
mentions: []
securities: [aapl, wmt, pltr, spy, spx, vix]
concepts: [implied-volatility, historical-volatility, realized-volatility, volatility-clustering, volatility-mean-reversion, volatility-skew, volatility-surface, volatility-term-structure, delta, vega, theta, greeks, expected-move, standard-deviation-move, implied-volatility-percentile, implied-volatility-rank, volatility-risk-premium, trading-plan, trading-log, position-sizing, risk-management, process-over-outcome, emotional-discipline, right-tail]
strategies: [long-call, long-dated-calls, short-premium]
saga: null
part: null
confidence: high
---

# Option Volatility Overview — Implied, Historical, Realized & Forecast

## Summary

This comprehensive session covers the foundational mechanics of volatility in options trading, distinguishing between implied volatility (forward-looking market expectation), historical volatility (backward-looking realized movement), and forecast volatility (institutional pricing models). The host demonstrates how volatility exhibits mean-reversion and clustering behavior, how to visualize it via skew and term structure, and critically, how to integrate volatility analysis into trade construction to avoid being "right but wrong"—directionally correct but unprofitable due to vega and theta decay.

## Key takeaways

### Dated market read (2025-02-07)
- Walmart IV at ~32%, 96th percentile; GameStop IV at ~72%, 1st percentile—same move magnitude, vastly different relative context [56:16]
- Palantir earnings expected move ~20–30% based on historical gaps; average daily range ~5.5% insufficient for earnings fade planning [39:18]

### Evergreen mechanics

- **Volatility definition & types** [20:47]
  - Volatility = time-bound measurement of variance; expected dispersion from mean
  - Four types: implied (forward-looking), historical/statistical (backward-looking), realized (can be either), forecast (institutional models)
  - Implied volatility is annualized one standard deviation move; ~68% of data falls within 1σ, ~95% within 2σ, ~99.7% within 3σ

- **Implied vs. Historical volatility** [23:27]
  - IV uses calendar days; HV uses trading days—critical for period comparison
  - IV always forward-looking; HV always rear-view
  - Both are primary metrics for retail traders

- **Volatility visualization** [32:03]
  - **Smile/skew**: plot strike price vs. IV across an options chain; shows relative pricing of calls vs. puts at same delta
  - Puts typically skewed higher (more expensive) due to downside hedging demand [36:54]
  - **Volatility surface**: 2D or 3D visualization across strikes and expirations; reveals relative value opportunities and event-driven anomalies (e.g., earnings spikes)

- **Mean reversion & clustering** [44:34]
  - Volatility is a true mean-reverting asset (unlike price, which exhibits drift)
  - VIX over 10 years: midline ~16, range ~12–21; Walmart price over same period: ~15 to ~67
  - Volatility spikes but always reverts; clustering = tendency to hang at current level until catalyst triggers transition, then new cluster forms

- **Volatility–price correlation misconception** [50:26]
  - Common myth: price up → vol down; price down → vol up
  - **False**: no causal relationship; both can move in same direction
  - Vol is expectation of movement magnitude, independent of direction
  - General tendency: downside moves increase vol more than upside (hedging demand), but not prescriptive

- **IV percentile vs. IV rank** [56:16]
  - **IV percentile (IVP)**: count of days with lower IV than today ÷ period (typically 252); contextual, nuanced
  - **IV rank (IVR)**: (current IV − 52-week low) ÷ (52-week high − 52-week low); anchors to extremes, prone to stale data
  - Prefer IVP for relative context; Walmart 32% IV = 96% IVP (very high) vs. GameStop 72% IV = 1% IVP (very low)

- **Historical volatility calculation** [01:01:34]
  - Gather price data → calculate log returns → compute mean → calculate variance (average squared deviation) → take square root
  - Different models (Yang–Zhang, Parkinson, Garman–Klass, Rogers–Satchell) use different inputs (close-to-close, high–low, open–high–low–close, overnight moves)
  - GKYZ (combined Garman–Klass + Yang–Zhang) recommended for retail; includes overnight returns

- **Expected move calculations** [01:12:37]
  - One-day move: stock price × IV ÷ 16 (since √252 ≈ 16)
  - One-week move: stock price × IV × √(7/252)
  - One-month move: stock price × IV × √(1/12)
  - Two/three standard deviation: multiply expected move by 2 or 3

- **Variance risk premium (IV bias)** [01:13:52]
  - Ratio: (IV − HV) ÷ HV; positive = vol expensive, negative = vol cheap
  - Difference: IV − HV; simpler but less normalized
  - Institutions use this to identify short-vol or long-vol opportunities

- **Being "right but wrong"** [01:17:50]
  - Example: buy 21-Mar 115 call (10 delta, 0.06 vega) at $0.42; stock +$1, vol −2%, theta −1 day
    - Delta gain: +$0.10; vega loss: −$0.12; theta loss: −$0.02 → net −$0.04 (loss despite directional win)
  - Solution: buy longer-dated options (>60 days) with higher delta (60+) to reduce vega/theta drag
  - Example: 20-Jun 71-delta call; same +$1 move, −2% vol, −1 day → net +$0.23 (profitable)
  - **Key insight**: Greeks optimization is non-negotiable; directional correctness ≠ trade profitability

- **Risk management via sizing & stops** [01:33:09]
  - Mental stop + hard stop: set two price levels; size so loss at each level is acceptable (e.g., $1,000 on $100k account)
  - Can size up (e.g., 3-lot) if comfortable with both levels
  - Stop-market orders acceptable but expect poor fills; stop-limit orders dangerous (may not fill, leaving you in unwanted trade)
  - Account for expected move magnitude (use earnings move, not just average daily range) when setting stops

- **Dispersion trading concept** [01:43:02]
  - Index vol built from constituents, not inverse; individual stock vol driven by idiosyncratic risk
  - Institutions trade dispersion: calculate expected vol for each stock relative to index, trade the gap
  - Keeps pricing efficient

## Notable quotes

> "Volatility is a true mean reverting asset, unlike stocks, stocks exhibit drift." [46:04]

> "You can be right, but wrong at the same time. And that's typically a result of honestly being stupid. You don't have to do that. You just have to make trades that are designed smarter." [01:23:49]

> "If you don't have a clear understanding of what the effect is that you're trying to trade, the probability of you magically just picking the correct options to capture it is about zero." [01:25:29]

## Candidate wiki links

**concepts:**
[[implied-volatility]], [[historical-volatility]], [[realized-volatility]], [[volatility-clustering]], [[volatility-mean-reversion]], [[volatility-skew]], [[volatility-surface]], [[volatility-term-structure]], [[delta]], [[vega]], [[theta]], [[greeks]], [[expected-move]], [[standard-deviation-move]], [[implied-volatility-percentile]], [[implied-volatility-rank]], [[volatility-risk-premium]], [[trading-plan]], [[trading-log]], [[position-sizing]], [[risk-management]], [[process-over-outcome]], [[emotional-discipline]], [[right-tail]]

**strategies:**
[[long-call]], [[long-dated-calls]], [[short-premium]]

**securities:**
[[aapl]], [[wmt]], [[pltr]], [[spy]], [[spx]], [[vix]]

**people:**
[[eric]]

## Regime / context

Recorded 2025-02-07 (Friday live session). Market conditions: Walmart IV 32% (elevated), Palantir pre-earnings (20–30% expected move). Content is evergreen mechanics; specific IV levels and earnings dates are dated. Next session: Greeks overview and practical application.
