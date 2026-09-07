---
type: source
title: "What Are FLEX Options? | The Mechanics Explained | The Options Trench"
video_id: cSG1UVDcO6A
url: "https://www.youtube.com/watch?v=cSG1UVDcO6A"
date: "2026-08-22"
series: options-trench
format: [education, analysis]
experts: []
mentions: [michael-burry, roaring-kitty]
securities: [tsla, gld, spy, spx]
concepts: [flex-options, custom-options, counterparty-risk, liquidity, options-chain-analysis, derivatives, 13f-reporting, notional-value, execution, market-microstructure, information-asymmetry, broker-duty, best-execution, order-flow, dark-pool-trading, delta-hedging, market-maker-positioning, bid-ask-spread, option-pricing, regulatory-framework]
strategies: [options-trading, market-making, execution-optimization]
saga: null
part: null
confidence: high
---

# What Are FLEX Options? | The Mechanics Explained | The Options Trench

## Summary

FLEX options are customizable, exchange-cleared options contracts that allow traders to specify strike price, expiration date (including AM/PM settlement), and European vs. American exercise style. While they sacrifice liquidity and transparency compared to standard listed options, they eliminate counterparty risk through exchange clearing and are increasingly used by option-based ETFs to construct precise buffer strategies. Understanding FLEX mechanics is critical for interpreting 13F filings and avoiding execution-related mispricing.

## Key takeaways

### Mechanics & structure
- **Custom terms**: FLEX options allow specification of exact strike (including half-strikes), expiration date, AM/PM settlement, and European/American style [02:28–03:40]
- **Exchange clearing**: Despite being custom, FLEX options are cleared by the exchange, eliminating counterparty risk entirely [03:40]
- **No order book**: FLEX trades require broker-mediated RFQ (request for quote) to find counterparties; no screen or automated matching [02:28]
- **Liquidity trade-off**: Narrower universe of potential sellers means wider spreads and less edge for buyers, but precise hedge matching [03:40]

### Primary use cases
- **Buffer ETFs**: Most common application; ETFs use FLEX to construct exact cap/floor levels matching their mandate on specific dates [05:57–07:10]
- **Highly liquid underlyings**: FLEX on GLD, SPY, and other liquid assets carry minimal hedging risk for market makers; often priced near fair value [08:12–09:15]
- **Loss-leader pricing**: Market makers often price low-risk FLEX packages competitively to build broker relationships for higher-edge business [09:15–10:15]

### 13F reporting pitfalls
- **Options are useless on 13F**: Short option positions are not reported at all; only long notional value appears [17:10–18:29]
- **No strike/expiry detail**: 13F lists only notional value of underlying, not delta, strike, or expiration—making spreads invisible [18:29]
- **FLEX not distinguished**: FLEX options are reported identically to listed options if the underlier is 13F-eligible (e.g., SPY but not SPX) [19:39]
- **Reporting threshold**: Positions below $200,000 aggregate value need not be reported, even for reporting entities [20:42]
- **Useful only for holder composition**: 13F can confirm whether arbitrage-oriented firms (Citadel, Jane Street, Sig) hold a security, suggesting potential inefficiency [22:00]

### Execution & pricing dynamics
- **Dark printing advantage**: FLEX trades print end-of-day (not real-time), allowing market makers to hedge delta without racing algorithmic front-runners [28:47–29:46]
- **Broker incentive misalignment**: Brokers may avoid shopping orders to large trading firms (who have sales desks) to prevent order theft; instead route to smaller, discreet market makers [41:22–43:49]
- **Egregious prints**: Large FLEX crosses sometimes print at extreme prices (e.g., 50¢ through screen offer) when brokers fail to put market makers in competition [34:16–35:39]
- **Floor coverage arms race**: Large firms (Citadel) stationing traders on option floors to intercept crosses and prevent brokers from capturing full commissions [37:52–39:07]
- **Customer attention matters**: Brokers exploit inattentive clients who don't monitor execution quality; detail-oriented customers force competitive pricing [39:07–40:13]

### Future outlook
- **ETF-driven growth**: FLEX volume growing dramatically as option-based ETF issuance accelerates; M&A in ETF provider space signals sustained gold rush [46:01–47:08]
- **No peak in sight**: Incentives point to continued FLEX proliferation alongside new ETF launches [47:08]

## Notable quotes

> "The exchange is clearing the trade, but there's no screen or order book for it because it's custom." [02:28]

> "The 13F is useless for options... you don't have to report any short option positions at all. So if you even saw an option position, a large option position, you would have no idea if it was part of a spread." [17:10]

> "If you're the kind of customer that does not realize that you're being ripped off, if you're not really paying that much attention to the option prices, don't really understand how execution and competition work, you might not realize that you got ripped off on the price." [39:07]

## Candidate wiki links

**concepts:**
[[flex-options]], [[custom-options]], [[counterparty-risk]], [[liquidity]], [[options-chain-analysis]], [[derivatives]], [[13f-reporting]], [[notional-value]], [[execution]], [[market-microstructure]], [[information-asymmetry]], [[broker-duty]], [[best-execution]], [[order-flow]], [[dark-pool-trading]], [[delta-hedging]], [[market-maker-positioning]], [[bid-ask-spread]], [[option-pricing]], [[regulatory-framework]], [[buffer-etf]], [[spread]], [[front-running]], [[incentive-alignment]]

**strategies:**
[[options-trading]], [[market-making]], [[execution-optimization]], [[delta-hedging]]

**securities:**
[[tsla]], [[gld]], [[spy]], [[spx]]

**people:**
[[michael-burry]], [[roaring-kitty]]

## Regime / context

Recorded August 2026. This is part one of a three-part series on FLEX options; subsequent parts address 13F misreporting and structural inefficiency detection. The discussion reflects market structure as of mid-2020s, with emphasis on the rapid growth of option-based ETFs and their reliance on FLEX mechanics for precise hedging. Execution dynamics and broker incentive structures described are endemic to OTC and semi-OTC derivatives markets and remain relevant across market regimes.
