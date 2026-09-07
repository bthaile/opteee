---
type: source
title: "Euan Sinclair: The Low VIX Is a Trap - Here's Why | The Outlier Podcast"
video_id: SLD5bc43lAg
url: "https://www.youtube.com/watch?v=SLD5bc43lAg"
date: "2026-08-20"
series: outlier-podcast
format: [interview, education]
experts: [euan-sinclair]
mentions: [aaron-brown, ken-griffin, blair-hull]
securities: [spy, iwm, qqq, spx]
concepts: [implied-volatility, volatility-term-structure, variance-risk-premium, volatility-of-volatility, mean-reversion, regime-dependency, risk-management, position-sizing, kelly-criterion, volatility-crush, zero-dte, market-microstructure, systemic-risk, leverage, financial-crisis]
strategies: [short-volatility, calendar-spread, short-straddle, short-strangle, covered-strangle, ratio-spread, delta-hedging, risk-reversal]
saga: null
part: null
confidence: high
---

# Euan Sinclair: The Low VIX Is a Trap - Here's Why | The Outlier Podcast

## Summary

Euan Sinclair discusses why current low VIX levels mask dangerous structural imbalances in the options market, particularly in zero-DTE products. He emphasizes that trading volatility is fundamentally about the variance risk premium rather than absolute IV levels, and that proper position sizing and risk-reward evaluation must precede any trade structure. Sinclair warns of pre-disaster conditions in financial markets driven by retail flow, zero-DTE proliferation, and concentration of market-making power among a handful of firms.

## Key takeaways

### Dated market read (2026-08-20)

- **VIX at ~16 is low but not extreme** [05:54] — approximately 40th percentile historically; median is ~19 over 35 years. The real concern is zero-DTE and one-DTE volatility, which is severely depressed (one-day variance swap strike under 8, ATM vol under 7).
- **Steep curve collapse after 3-month** [05:54] — the VIX term structure shows normal relationship between VIX and 3-month IV, but falls off a cliff in zero-DTE, suggesting flow-driven mispricing rather than fundamental repricing.
- **NASDAQ IV relative to S&P at extreme levels** [10:50] — NASDAQ VIX is at ~5th percentile relative to S&P VIX, but this does not automatically signal a profitable trade because realized volatility in NASDAQ is proportionally higher; variance premium may not be mispriced.

### Evergreen mechanics

- **Volatility is sticky; regimes persist** [01:10] — volatility tomorrow is a good predictor of volatility today; variance premium paid yesterday is likely to pay tomorrow. This is why options are easier to trade than stocks (easier forecasting problem, harder monetization problem).
- **Daily monitoring framework** [02:19] — track VIX ratios across products (IWM VIX, Diamond VIX), term structure relationships, volatility of volatility, and VIX futures vs. spot VIX. Patterns emerge when z-scores deviate significantly.
- **Distinguish between implied and realized volatility** [11:56] — when trading multi-leg spreads, you are always trading the implied-to-realized spread, not just implied. A trade can be "right" on implied but lose money if realized volatility moves unfavorably.
- **Risk premium varies by time horizon** [21:40] — measure variance premium at 30-day, 60-day, 90-day horizons separately. Edge exists at different expirations; don't assume one rule applies across all durations.
- **Mean reversion is unreliable for timing** [16:53] — when VIX is below 5th percentile, average reversion to median takes ~120 days, but one historical period lasted 5.5 years. Insufficient data to build predictive models; use formal time-series methods (GARCH) instead.
- **Structure is secondary to edge** [26:10] — if volatility is overpriced, the primary way to profit is to sell it. Overthinking structure (strangles, condors, spreads) often obscures the core short-volatility bet. Simplicity often wins.
- **Risk-to-reward must be evaluated before entry** [28:43] — use portfolio software to model worst-case scenarios. Example: selling a zero-DTE SPY straddle for $300 max profit against $15,000 margin requirement and potential $2,000+ loss is unfavorable for most traders. Hedge cost often erodes edge.
- **Position sizing depends on risk tolerance and portfolio context** [33:16] — no universal rule for strike width or position size. Euan targets maximum daily loss ≤ one week of average P&L. Others may accept 1:250 risk-reward. Decision must be made in advance, not during drawdown.
- **Monte Carlo simulation reveals hidden scenarios** [37:59] — run simulations to find paths where the "can't lose" trade actually loses. Identify which market conditions hurt you most; understand the distribution of outcomes, not just expected value.
- **Hedging increases position size capacity** [43:51] — undefined downside risk requires smaller position size (larger denominator in Kelly criterion). Hedging reduces that denominator, allowing larger notional exposure while maintaining acceptable loss.
- **Calendars are now granular; old rules don't apply** [07:06] — with daily expirations available up to 3–4 weeks, calendar spreads can be constructed with precise duration matching. This changes the risk profile vs. monthly-only expirations.
- **Percentiles vs. z-scores** [13:30] — use z-scores for mean-reverting processes (expect reversion to mean); use percentiles for non-mean-reverting ratios (e.g., NASDAQ/S&P IV ratio). Both are nonparametric; choose based on the question.
- **Fiduciary responsibility shapes risk framework** [49:49] — personal account, prop account, and institutional (ETF/SMA) accounts require different risk profiles. Euan trades prop account looser than ETF account (grandmothers' and doctors' money); personal account loosest. Framework is identical; risk levels differ.
- **Pre-disaster conditions: retail flow, zero-DTE, concentration** [54:26] — every major financial crisis has been preceded by instrument proliferation (portfolio insurance '87, credit derivatives '08, now retail + zero-DTE). Market-making is now 90% concentrated in ~5 firms; systemic risk is high.
- **24-hour trading will concentrate volume further** [57:43] — small market makers cannot staff 24/7 desks; volume will flow to mega-firms (Citadel, Susquehanna, Jane Street). If one blows up, all are exposed to similar positions; risk of cascading failure.

## Notable quotes

- "Options, they're not deep like quantum gravity is deep, right? You can get to that level reasonably quickly. And then you've got to kind of actually just go and put that into practice." [01:10]
- "If you're trading V with options, you're never just trading implied. You're always trading that implied to realize spread." [13:00]
- "The edge is being short V and then they put something together which really kind of isn't short V... whereas like you know you think V's overpriced well go ahead sell a straddle see how that works." [27:34]

## Candidate wiki links

**concepts:**
[[implied-volatility]], [[volatility-term-structure]], [[variance-risk-premium]], [[volatility-of-volatility]], [[mean-reversion]], [[regime-dependency]], [[risk-management]], [[position-sizing]], [[kelly-criterion]], [[volatility-crush]], [[zero-dte]], [[market-microstructure]], [[systemic-risk]], [[leverage]], [[financial-crisis]], [[realized-volatility]], [[implied-to-realized-spread]], [[monte-carlo-simulation]], [[garch]], [[percentile]], [[z-score]], [[fiduciary-responsibility]], [[market-concentration]], [[retail-trading-behavior]]

**strategies:**
[[short-volatility]], [[calendar-spread]], [[short-straddle]], [[short-strangle]], [[covered-strangle]], [[ratio-spread]], [[delta-hedging]], [[risk-reversal]], [[hedging]]

**securities:**
[[spy]], [[iwm]], [[qqq]], [[spx]], [[vix]]

**people:**
[[aaron-brown]], [[ken-griffin]], [[blair-hull]], [[nassim-taleb]]

## Regime / context

Recorded 2026-08-20. VIX environment is historically low-to-moderate (16, ~40th percentile), but zero-DTE and one-DTE volatility is severely depressed, creating a steep term-structure cliff. This is a pre-crisis regime characterized by retail flow proliferation, zero-DTE instrument explosion, and concentration of market-making among five mega-firms. Euan warns this mirrors conditions preceding '87 (portfolio insurance), 2000 (tech bubble), and 2008 (credit derivatives). The conversation emphasizes that low absolute VIX masks structural fragility and that proper risk-reward evaluation and position sizing are non-negotiable before entry.
