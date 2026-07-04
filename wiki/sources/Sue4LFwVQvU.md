---
type: source
title: "GME Livestream with @RichardNewton - GameStop Analysis"
video_id: Sue4LFwVQvU
url: https://www.youtube.com/watch?v=Sue4LFwVQvU
date: 2024-07-14
series: none
format: [live, education, interview]
experts: [richard-newton]
mentions: [roaring-kitty, ryan-cohen, masayoshi-son]
securities: [gme, chewy]
concepts: [settlement, regulation-sho, delta, gamma, implied-volatility, theta, extrinsic-value, intrinsic-value, market-maker, order-flow, bid-ask-spread, volatility-term-structure, options-pricing, dealer-positioning, gamma-ramp, unusual-options-activity]
strategies: [long-call, short-put, covered-call]
saga: gme-saga
part: null
confidence: high
---

# GME Livestream with @RichardNewton - GameStop Analysis

## Summary

Eric and Richard Newton conduct a deep-dive analysis of GameStop's options market structure, settlement mechanics, and the implications of roaring Kitty's recent $170M position accumulation. The discussion covers Regulation SHO settlement rules (T+1, T+3, T+6, C+35), options Greeks and pricing dynamics, and forensic examination of order flow to assess whether a $3–5M starting capital could have been leveraged into the capital needed for the June position. The stream explores the mechanics of gamma squeezes, market maker hedging behavior, and the role of informed order flow detection in options markets.

## Key takeaways

### Dated market read (2024-07-14)

- **Settlement window analysis** [02:12–08:41]: Regulation SHO Rules 203 and 204 allow market makers to fail to deliver for T+3, T+6, and C+35 (calendar days, excluding weekends and holidays). Roaring Kitty's June 13 share purchase triggers a C+35 settlement deadline around July 18–22, coinciding with heavy July 19 options expiration interest.
- **July 19 options concentration** [12:12–13:41]: ~40% of open interest concentrated in July 19 expiration; 139.5% implied volatility on that cycle vs. 127% on August 16. This is standard for GameStop but noteworthy given settlement timing.
- **Chewy position mystery** [01:17:28–01:25:44]: Between June 13 and June 24, roaring Kitty accumulated ~9.1M Chewy shares (~$225M notional at ~$25/share). With only ~$6M cash on hand post-GameStop options conversion, the capital source remains unclear; options activity insufficient to explain the position.
- **Cash position snapshot** [02:11:16–02:14:48]: End-of-May cash balance ~$29.2M; interest earned suggests ~$90M was in the account during May, consistent with a pre-loaded war chest rather than options-generated capital.

### Evergreen mechanics

- **Delta and leverage** [26:14–27:06]: Delta measures premium change per $1 move in underlying; a 64-delta option moves ~64¢ for every $1 stock move. Deeper ITM options (higher delta) provide more dollar exposure per contract; OTM options (lower delta) offer higher percentage returns but require larger moves.
- **Theta decay acceleration** [24:21–25:03]: Theta decay is exponential near expiration; minimal decay 60+ days out, accelerating sharply within 30 days and becoming highly nonlinear within 7 days. Longer-dated positions (60+ DTE) reduce decay drag but cost more upfront.
- **Extrinsic value and bid-ask spreads** [22:22–23:46]: Extrinsic value = option price − intrinsic value. For a $26 stock, $25 call at $5.25 has $1 intrinsic and $4.25 extrinsic (all subject to theta decay). GameStop options trade at ~1.4% bid-ask spread vs. SPY at ~0.014%, reflecting volatility and liquidity differences.
- **Market maker order-flow detection** [51:31–53:07]: Market makers flag orders as informed vs. uninformed based on size, persistence, and structure. Large block orders (e.g., $3M+ positions) at specific strikes signal conviction; MMs hedge or run with such orders depending on risk appetite.
- **Gamma and compounding** [38:45–39:10]: Gamma is the rate of change of delta; higher gamma (near-term, ATM options) means delta changes faster, enabling rapid compounding on favorable moves but accelerating losses on adverse moves.
- **Volatility surface and pricing** [42:54–44:36]: Implied volatility is market-derived; forecast volatility (proprietary MM models) determines option pricing. MMs maintain volatility surfaces to price options; if mispriced, speculators and HFT firms arbitrage the gap.
- **Position construction** [38:23–38:45]: Typical approach: base position 60+ DTE, slightly ITM or ATM (high delta, ~64+) for dollar exposure; shorter-dated "kicker" options 2–3 weeks out, slightly OTM (30–40 delta) for gamma compounding on large moves.

## Notable quotes

> "Standard technical analysis in my opinion doesn't translate well to something like GameStop and a lot of that has to do with the fact that there are all these other injects that absolutely have a dominating effect on price and volume."

> "The fundamental problem here is liquidity with so many shares being dominated by household especially um in periods like right now you can see tremendous volume but where are the market makers and the broker dealers going to go to get shares."

> "This is an insane amount of conviction right like insane amount of conviction because you can see what the standard premiums are for positions that are being built and then you start seeing blocks come in the two millions five millions and there's a bunch of them at the same time it's so."

## Candidate wiki links

**concepts:** [[settlement]], [[regulation-sho]], [[delta]], [[gamma]], [[theta]], [[implied-volatility]], [[extrinsic-value]], [[intrinsic-value]], [[market-maker]], [[order-flow]], [[bid-ask-spread]], [[volatility-term-structure]], [[options-pricing]], [[dealer-positioning]], [[gamma-ramp]], [[unusual-options-activity]], [[moneyness]], [[days-to-expiration]], [[volatility-clustering]]

**strategies:** [[long-call]], [[short-put]], [[covered-call]], [[gamma-scalping]]

**securities:** [[gme]], [[chewy]]

**people:** [[roaring-kitty]], [[ryan-cohen]], [[masayoshi-son]]

## Regime / context

**Date:** July 14, 2024. This stream occurs during a quiet consolidation period for GameStop following the May–June volatility spike (May 3 high ~$48, June 7 high ~$80, June 14 decline to ~$17). Roaring Kitty's June 13 share purchase and subsequent June 24 Chewy 13G filing are the primary catalysts under discussion. The July 19 options expiration and C+35 settlement deadline (approximately July 18–22) are key technical levels being monitored.

**Settlement context:** T+1 settlement for equities and options (as of May 28, 2024) shortens the window for market maker inventory management. Regulation SHO Rules 203/204 and C+35 calendar-day deadlines create predictable pressure points for forced covering or hedging.

**Volatility regime:** Implied volatility on July 19 expiration at 139.5% is elevated but substantially lower than May–June peaks (200–300%+), suggesting market has priced in some normalization while maintaining elevated expectations for the settlement window.
