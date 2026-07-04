---
type: source
title: "The ULTIMATE Covered Strangle Option Strategy Masterclass"
video_id: wS7sjV_UOMw
url: https://www.youtube.com/watch?v=wS7sjV_UOMw
date: 2023-08-15
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [iwm, spy, spx]
concepts: [covered-strangle, cash-secured-put, covered-call, delta, theta-decay, implied-volatility, volatility-risk-premium, support-and-resistance, linear-regression-channels, moving-averages, position-sizing, scaling-in, basis-management, risk-management, capital-efficiency, profit-taking, rolling-options, assignment, technical-analysis, fundamental-analysis, market-regimes, days-to-expiration, probability-of-touch]
strategies: [covered-strangle, short-put, covered-call, ratio-write, box-spread]
saga: null
part: null
confidence: high
---

# The ULTIMATE Covered Strangle Option Strategy Masterclass

## Summary

The covered strangle is a three-legged strategy combining a short cash-secured put, long equity, and a ratio-covered call (typically short fewer calls than shares held to preserve upside). It is designed to maintain market exposure while enhancing buy-and-hold returns through premium collection and careful basis management across multiple market conditions. The strategy relies on disciplined scaling protocols, technical/fundamental analysis, and rolling mechanics to manage risk and optimize profitability.

## Key takeaways

### Strategy structure
- **Three legs**: short cash-secured put + long stock + ratio covered call (not 1:1) [01:43]
- **Cash-secured put**: defined profit, undefined risk down to zero [02:00]
- **Covered call ratio**: sell fewer calls than shares held to maintain uncapped upside (e.g., 6 calls against 800 shares leaves 200 shares uncapped) [02:37]
- **Why ratio matters**: avoids the capped-upside drawback of traditional 1:1 covered calls [03:06]

### Position management
- **Cash-secured put P&L**: target ~65% max profit; use IV-adjusted sliding scale [04:21]
- **Long stock management**: use support/resistance, moving averages, linear regression channels; take profit when unwinding [04:46]
- **Covered call management**: let expire at short strike; rarely roll unless significantly more profitable [05:23]
- **Loss management**: structure allows holding unrealized losses if basis is managed correctly; only applies to broad market indices with history of new highs [06:26]

### Entry and scaling process
- **Entry**: sell cash-secured put first [06:44]
- **Put outcomes**: out-of-money (sell again) or in-the-money (close for loss, roll, or take assignment) [07:01]
- **Assignment flow**: if assigned, sell covered calls at ratio + simultaneously sell more cash-secured puts [07:21]
- **Scaling on decline**: carefully manipulate basis downward by adding risk on the way down; only viable for broad indices [07:46]
- **Capital allocation**: split into total allocation, initial outlay, and scaling protocol [16:11]

### Product selection
- **Liquidity first**: prefer very liquid products with weekly options; avoid illiquid names [10:23]
- **Dividend**: optional; prefer ≥2% if included [10:44]
- **IWM vs SPY**: IWM preferred for slightly higher volatility and better diversification (Russell 2000 vs S&P 500 concentration) [11:06]
- **Implied volatility**: prefer IV trending above realized volatility (positive variance risk premium); more aggressive when IV percentile >20 [12:08]

### Technical and fundamental analysis
- **Technical**: apply moving averages, linear regression channels; use to inform initial size and scaling, not as hard entry/exit [13:30]
- **Fundamental** (individual stocks): check solvency, quick ratio >1, revenue/sales growth, trading above 50/20 EMAs, cash flow, PE ratios [14:08]
- **Index ETFs**: less critical; focus on liquidity and volatility [14:50]

### Delta and strike selection
- **Cash-secured put delta**: 0.15–0.50 (higher delta = more credit but higher probability of assignment) [15:12]
- **Distance from highs**: favor lower delta (20–25) when near all-time highs [15:50]
- **Short call delta**: prefer above basis of shares to avoid locking in losses [20:18]

### Sizing and scaling mechanics
- **Total allocation**: generous; core portfolio allocation [16:36]
- **Initial outlay**: 20–30% if near highs and IV low; allows room to scale [17:19]
- **Scaling protocol**: deploy on each 5% decline; use remaining capital to improve basis [18:42]
- **Basis improvement**: each doubling of position size requires doubling of new capital for same basis improvement [19:20]
- **Scaling patience**: average bear market ~298 days; scale meaningfully up front, then slow down [20:00]

### Days to expiration and rolling
- **DTE range**: 0–50 days [21:45]
- **High IV, grinding higher**: favor longer duration to collect enough premium [22:05]
- **Current low-IV environment**: favor shorter DTE for better theta decay and sensitivity [22:23]
- **Weekly expirations**: critical for flexibility; allows rolling in 2–4 day increments vs 20–30 day jumps [22:43]
- **Best roll timing**: when stock equals strike (most choices) [23:41]
- **Roll mechanics**: buy back time value, manage basis, prefer credit; sometimes small debit acceptable if position profitable [24:00]

### Capital efficiency
- **Unused capital**: deploy into box spreads expiring before put assignment dates to capture risk-free rate (>5% currently) [25:47]
- **Deconflict timing**: ensure box spread expiration before cash-secured put expiration [26:25]

## Notable quotes

> "The covered strangle is designed to maintain market exposure so I trade the covered strangle in almost every single market condition." [01:00]

> "I do not sell short calls to long stock at a one-to-one ratio typically... if I'm long 800 shares at 181.94 and I'm short six short calls at 182 which is above my basis I have 200 shares that are uncapped." [03:06]

> "There's no other scenario that I would feel comfortable adding risk on the way down but in this scenario I do feel comfortable you just have to be patient." [08:49]

## Candidate wiki links

### Concepts
[[covered-strangle]], [[cash-secured-put]], [[covered-call]], [[delta]], [[theta-decay]], [[implied-volatility]], [[volatility-risk-premium]], [[support-and-resistance]], [[linear-regression-channels]], [[moving-averages]], [[position-sizing]], [[scaling-in]], [[basis-management]], [[risk-management]], [[capital-efficiency]], [[profit-taking]], [[rolling-options]], [[assignment]], [[technical-analysis]], [[fundamental-analysis]], [[market-regimes]], [[days-to-expiration]], [[probability-of-touch]], [[box-spread]], [[risk-free-rate]]

### Strategies
[[covered-strangle]], [[short-put]], [[covered-call]], [[ratio-write]], [[box-spread]]

### Securities
[[iwm]], [[spy]], [[spx]]

### People
[[eric]]

## Regime / context

Recorded August 2023. The strategy is presented as evergreen and applicable across market conditions, though the video emphasizes its particular strength in broad-market indices (IWM, SPY, SPX) with long histories of making new highs. The discussion of risk-free rates >5% and box spreads reflects the 2023 interest-rate environment. The COVID-era example (March 2020) illustrates the strategy's scaling mechanics during a sharp drawdown and V-shaped recovery.
