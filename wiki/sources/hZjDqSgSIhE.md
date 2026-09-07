---
type: source
title: "Why Options Liquidity Matters (More Than You Think) | The Options Trench"
video_id: hZjDqSgSIhE
url: https://www.youtube.com/watch?v=hZjDqSgSIhE
date: 2026-08-29
series: options-trench
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spy, xhb, ibm, xom, ko, jnj]
concepts: [liquidity, bid-ask-spread, implied-volatility, moneyness, open-interest, volume, market-microstructure, phantom-liquidity, order-flow, market-maker, designated-primary-market-maker, payment-for-order-flow, order-routing, execution, spread-cost, volatility-normalization, liquidity-measurement, market-structure, institutional-trading, retail-trading, dark-pool-trading]
strategies: [vertical-spread, covered-call, protective-put]
saga: null
part: null
confidence: high
---

# Why Options Liquidity Matters (More Than You Think) | The Options Trench

## Summary

This episode provides a comprehensive overview of options liquidity: how to measure it, common misconceptions, and the mechanics of market structure that affect traders at different scales. The hosts discuss bid-ask spreads normalized by volatility, phantom liquidity on pro-rata exchanges, and how payment for order flow and order routing impact retail versus institutional traders differently.

## Key takeaways

### Measuring liquidity
- **Bid-ask spread as % of strike** [01:53]: Normalize spreads by dividing by the strike price to compare across different securities. SPY typically trades at ~0.01% spread; less liquid names like XHB may be 3.4% or wider.
- **Volatility-normalized spreads** [04:14]: On a 20% IV name, spreads <1 vega point = high liquidity; 1–2 vega points = medium; >2 vega points = low. Higher IV names require proportionally wider spreads to maintain equivalent liquidity.
- **Volume and open interest** [13:34]: A soft floor of ~30,000 contracts of open interest is a practical threshold; volume turnover relative to OI indicates trading activity and market health.

### Liquidity patterns
- **Moneyness effect** [09:29]: In-the-money options are wider than out-of-the-money because market makers care about delta risk (stock replication) rather than vega; deep ITM options have minimal vega.
- **Time decay and vega** [10:14]: Longer-dated options are wider because they carry more vega; a 12-month option's vega is a multiple of a 3-month option's, so spreads scale accordingly.
- **Round strikes and demand** [11:26]: Liquidity attracts liquidity—round strikes (e.g., 120) accumulate order flow and become tighter as traders prefer to trade where execution is certain.
- **Volatility regime shifts** [15:46]: Liquidity can cycle dramatically; GME exemplifies "trades by appointment" behavior—dormant until a catalyst floods the market with interest.

### Phantom liquidity and market structure
- **Pro-rata allocation** [34:58]: On pro-rata exchanges (CBOE, NASDAQ, NYSE), size allocation is proportional to posted size, not time priority. A trader posting 1,000 contracts gets 2/3 of incoming flow vs. one posting 500, regardless of arrival order.
- **Phantom illiquidity** [36:11]: Traders post oversized orders to secure allocation on small fills, but the full size is not actually available at that price. Attempting to "chip away" causes the market to move.
- **Designated primary market maker privilege** [39:24]: The DPPM (e.g., Citadel on CBOE) receives 40% allocation of all trades on their listed options after customer orders are filled—a huge structural advantage.

### Institutional vs. retail execution
- **Shopping orders** [28:37]: Institutional traders shopping large orders (e.g., 3,000 contracts) discover that screen prices (e.g., $3.20 for 20 contracts) do not hold at size; actual offers may be $3.50 or worse.
- **Information leakage** [29:42]: Once an order is shown to the broker market, counterparties know a buyer exists; lifting the screen price signals remaining size, causing other traders to widen or bid ahead.
- **Size and cost scaling** [26:31]: Smaller accounts can trade less-liquid names with less competition; larger accounts face exponential spread costs as they consume available size.

### Payment for order flow and order routing
- **Retail fills improve, institutional fills worsen** [41:46]: PFOF likely improves retail execution but worsens fills for institutional hedgers (e.g., funds buying puts to hedge), whose costs are ultimately borne by pension beneficiaries.
- **Counterfactual uncertainty** [46:26]: Technology, algorithmic pricing, and asset-class correlation improvements happened simultaneously with PFOF; disentangling causation is difficult.
- **Order routing control** [49:05]: High-volume traders should negotiate commissions and consider direct routing or algorithmic execution vendors to reduce execution costs; low-volume traders are indifferent to PFOF.
- **Broker fill quality disclosures** [50:09]: Brokers publish annual fill-quality reports (aggregate level) that can inform routing decisions.

### Practical considerations
- **Vertical spreads and spread cost** [22:03]: Vertical spreads have limited risk, so a wide market is particularly painful; cost per unit of risk becomes unfavorable for retail end-users.
- **Biotech opportunities** [27:20]: Biotech options are illiquid and incestuous, but smaller accounts can find clean ideas with less competition in that pool.
- **Commission negotiation** [25:32]: Retail traders paying 65–75 cents per contract should negotiate with brokers; rates can be reduced significantly, especially with volume.

## Notable quotes

> "Liquidity attracts liquidity. I mean, this is like a saying that in the markets, right? It's like liquidity begets liquidity." [11:48]

> "If you don't want to be the best offer, you can be the best bid." [38:22]

> "It's a poker game at that point." [31:13]

## Candidate wiki links

**concepts:** [[liquidity]], [[bid-ask-spread]], [[implied-volatility]], [[moneyness]], [[open-interest]], [[volume]], [[market-microstructure]], [[phantom-liquidity]], [[order-flow]], [[market-maker]], [[payment-for-order-flow]], [[order-routing]], [[execution]], [[spread-cost]], [[volatility-normalization]], [[market-structure]], [[institutional-trading]], [[retail-trading]], [[vega]], [[delta]], [[time-decay]]

**strategies:** [[vertical-spread]], [[covered-call]], [[protective-put]]

**securities:** [[spy]], [[xhb]], [[ibm]], [[xom]], [[ko]], [[jnj]]

**people:** [[eric]]

## Regime / context

Recorded 2026-08-29. Discussion reflects current U.S. options market structure (pro-rata exchanges, PFOF, designated primary market makers). Liquidity metrics and spread examples are approximate and time-sensitive; actual spreads vary by underlying, IV regime, and market conditions. The analysis applies broadly to equity options but does not address index options, futures options, or international markets.
