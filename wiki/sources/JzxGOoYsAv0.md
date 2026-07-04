---
type: source
title: "All Implied Volatility is WRONG | The Options Trench"
video_id: JzxGOoYsAv0
url: https://www.youtube.com/watch?v=JzxGOoYsAv0
date: 2026-06-13
series: options-trench
format: [education, analysis]
experts: [eric]
mentions: []
securities: []
concepts: [implied-volatility, black-scholes, days-to-expiration, volatility-term-structure, bid-ask-spread, cost-basis, delta, theta, vega, market-maker, time-frames, volatility-clustering, realized-volatility, iv-crush, weekend-effect, gap-risk, market-efficiency, technical-analysis]
strategies: [short-premium, short-straddle, short-strangle]
saga: null
part: null
confidence: high
---

# All Implied Volatility is WRONG | The Options Trench

## Summary

This episode deconstructs the Black-Scholes framework and reveals critical flaws in how implied volatility is measured and interpreted. The core insight: time does not pass uniformly across calendar days or intraday hours, yet standard IV models treat all days equally. This creates systematic artifacts in IV readings that can be mistaken for genuine volatility changes, especially near expiration and across weekends. Understanding how to properly measure "vol time" is essential for traders comparing IVs across assets or trading for small vol margins.

## Key takeaways

### Dated market read (2026-06-13)
- The "weekend effect" (VIX sawtooth pattern rising Mondays) is largely a calendar artifact, not true vol expansion [19:55]
- Natural gas American-style options historically traded at a premium to European-style near expiration due to the extra hour of optionality post-settlement [57:33]

### Evergreen mechanics

- **Black-Scholes inputs ranked by certainty** [01:02–03:43]: Strike price is known; stock price requires bid-ask midpoint judgment; cost of carry (interest + dividends) has slippage; time to expiration is the most misspecified input
- **Calendar time ≠ volatility time** [06:06–07:26]: A 72-hour option expiring Friday differs from a 72-hour option expiring Monday because business days are more volatile than weekends; the market is ~2× more volatile when open than closed
- **Weekend vol decay is ~2/3 of expected** [41:02]: Options decay approximately 2/3 of the theta you'd expect over a weekend; using a 365-day model creates false Monday vol spikes
- **DTE granularity matters** [35:14–39:07]: Rounding DTE to the nearest day (or even hour) creates false IV changes; minute-level granularity is standard in professional market-making software
- **Intraday vol is non-uniform** [53:30–54:40]: Volatility concentrates in the first 2 hours and final hours of the trading day; theta does not decay linearly across hours
- **Cross-asset IV comparison requires translation** [30:13–32:00]: Comparing IV across assets with different calendars (e.g., equities vs. commodities vs. 24/7 assets like Bitcoin) requires adjusting for the ratio of business days to calendar days; a 1-vol-point difference may be a mirage if calendars differ
- **Market makers use vol-time decay widgets** [55:03–56:06]: Professional option pricing software has built-in controls for how vol decays throughout the day; this has been standard for 20+ years
- **Practical impact scales with proximity to expiration** [27:19–27:42]: Errors from calendar misspecification range from ~0.1 vol points far from expiration to 1–3 vol points near expiration; holiday weekends amplify the effect
- **The 2/3 rule of thumb** [41:02]: Use this heuristic to filter noise: if a straddle decays only 2/3 of expected theta over a weekend, vol is unchanged; less decay = vol down; more decay = vol up
- **Retail traders can ignore this for same-calendar comparisons** [25:37–26:55]: When comparing options on the same expiration date across different stocks, calendar artifacts cancel out; the issue only matters for cross-asset or high-frequency vol trading
- **Earnings and catalyst events compress vol time** [56:33–57:13]: After earnings, options still contain significant vol that hasn't decayed; closing a short-vol position immediately post-earnings may leave money on the table or expose you to jump risk
- **American vs. European optionality near expiration** [58:04–01:01:24]: An American option's right to exercise after settlement can be worth 10–20 ticks near expiration; the EOO (exchange of options) market prices this extra hour of vol
- **24/7 trading flattens vol distribution** [17:15–18:27]: Assets trading 24/7 (Bitcoin, gold) have less lumpy vol calendars than equities; global assets spread volatility across 24 hours, while US-idiosyncratic stocks concentrate vol in US hours
- **Homework: feed articles into an LLM** [01:04:02–01:06:16]: Use a large language model to build a small module demonstrating how calendar effects scale near expiration; always ask "how much does this change my assessment?" before adopting a new concept

## Notable quotes

> "Volatility time passes faster when the market's actually open." [11:32]

> "If you specified the calendar correctly, you would say, 'Okay, I expect that the IV number in my model to be unchanged from Friday to Monday.'" [22:43]

> "The better you can specify the calendar, the more IV changes have relevance to what you think actually happened in the market." [24:24]

## Candidate wiki links

**concepts:**
[[implied-volatility]], [[black-scholes]], [[days-to-expiration]], [[theta]], [[delta]], [[vega]], [[bid-ask-spread]], [[cost-basis]], [[volatility-term-structure]], [[realized-volatility]], [[iv-crush]], [[weekend-effect]], [[gap-risk]], [[market-maker]], [[time-frames]], [[volatility-clustering]], [[market-efficiency]]

**strategies:**
[[short-premium]], [[short-straddle]], [[short-strangle]]

**securities:**
(none substantively discussed)

**people:**
(none featured or mentioned)

## Regime / context

This is a foundational education episode on a perennial topic in options trading. The concepts apply across all market regimes, though the magnitude of calendar artifacts scales with proximity to expiration and the degree of cross-asset comparison. The natural gas American/European option example is historical (pre-2010s auto-exercise rule change) but illustrates the principle. The 2/3 theta decay rule and the weekend effect are empirical observations that hold across equity markets. For traders operating at retail scale on single-asset expirations, these refinements are largely academic; for market makers, prop traders, and cross-asset vol traders, they are operational necessities.
