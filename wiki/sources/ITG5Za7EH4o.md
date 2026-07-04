---
type: source
title: "SIMPLIFIED Covered Strangle Option Strategy"
video_id: ITG5Za7EH4o
url: https://www.youtube.com/watch?v=ITG5Za7EH4o
date: 2023-06-21
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [iwm, tsla, amzn, pfe]
concepts: [covered-strangle, delta, theta-decay, days-to-expiration, moving-averages, linear-regression-channels, scaling-in, risk-management, position-sizing, capital-efficiency, assignment, profit-mechanism, technical-analysis, trend-identification]
strategies: [covered-strangle, short-put, scaling-in, rolling-options]
saga: null
part: null
confidence: high
---

# SIMPLIFIED Covered Strangle Option Strategy

## Summary

A hands-off covered strangle strategy designed for busy traders who lack constant market access. The approach prioritizes simplicity over optimization: set up the trade after hours, deploy within 60 seconds, and return only after expiration to assess and adjust. The strategy uses short puts (15–35 delta) and uncovered short calls (above cost basis) on liquid underlyings, typically within 45–60 days to expiration, with optional scaling and technical filters to enhance profitability.

## Key takeaways

- **Core trade structure** [00:39–01:24]: Sacrifice optimization for simplicity; flexible time frame (weeklies to 680+ days, but ideally 45–60 DTE); covered strangle is the chosen vehicle.
- **Ticker selection** [02:01–02:40]: Pick anything you already like for buy-and-hold (e.g., index ETFs like IWM, or individual stocks like TSLA, AMZN, PFE); liquidity matters less if you hold to expiration.
- **Days to expiration & delta** [03:19–04:46]: Ideally 45–60 days out; short puts 15–35 delta; short calls selected by strike price relative to cost basis, not delta. Theta decay accelerates within the 60-day window.
- **Strike selection for short calls** [05:25–05:46]: Avoid selling calls below your cost basis to prevent upside cap; use uncovered calls (not covered calls) to preserve unlimited upside potential.
- **Management flow** [09:16–11:06]: If assigned on the put, buy shares; if assigned on the call, sell shares. If stock stays between strikes, reload. No mid-month adjustments required.
- **Scaling & capital allocation** [11:22–12:36]: Use 70% of account capital if >20 away from all-time highs; 50% if near highs. Example: $100k account, buy 200 shares at $100 (20k), sell 2× $95 puts (collect $200), sell 1× $105 call (collect $100); total outlay ~$39k, ~2% return in one month.
- **Optional enhancements** [06:25–08:43]: Layer in 50/150-day moving averages and linear regression channels to pause or scale risk; rolling options to increase profit potential. These add complexity but are not required.
- **Remaining capital** [13:47–14:05]: Deploy unused capital in box spreads or additional covered strangles; or hold for scaling opportunities on down moves.

## Notable quotes

> "Once you set up this strategy which does take time after hours you could literally deploy it within 60 seconds of having access to a computer."

> "The main thing is I don't want to have upside risk so I'm going to avoid selling short calls below my basis because they just turn into a problem more often than not."

> "If you're smart about it covered calls can keep pace with the market—this is one of those details that makes a big difference."

## Candidate wiki links

**Concepts:**
[[covered-strangle]], [[delta]], [[theta-decay]], [[days-to-expiration]], [[moving-averages]], [[linear-regression-channels]], [[scaling-in]], [[risk-management]], [[position-sizing]], [[capital-efficiency]], [[assignment]], [[profit-mechanism]], [[technical-analysis]], [[trend-identification]], [[buy-and-hold]]

**Strategies:**
[[covered-strangle]], [[short-put]], [[scaling-in]], [[rolling-options]]

**Securities:**
[[iwm]], [[tsla]], [[amzn]], [[pfe]]

**People:**
[[eric]]

## Regime / context

Recorded June 2023. The strategy is regime-agnostic and designed for any market environment; the example uses historical IWM data from March 2019 for illustration. Suitable for buy-and-hold portfolio enhancement with minimal time commitment (60 seconds per deployment, review only at expiration). Scaling and technical filters are optional and can be added based on available time and market conditions.
