---
type: source
title: "The Hidden Cost of Selling Covered Calls for Income"
video_id: "kvzQJ3wFaZs"
url: "https://www.youtube.com/watch?v=kvzQJ3wFaZs"
date: "2026-03-13"
series: outlier-podcast
format: strategy-breakdown
experts: [euan-sinclair]
securities: [hood, amzn, aapl, tsla, spx, oil, silver, natural-gas]
concepts: [opportunity-cost, capped-upside, expected-value, short-volatility, short-gamma, volatility-risk-premium, risk-premium, right-tail, mark-to-market, market-maker, straddle-price, earnings-move, implied-volatility, realized-volatility, implied-volatility-percentile, implied-volatility-rank, volatility-mean-reversion, volatility-clustering, volatility-skew, theta-decay, gamma, delta, vega]
strategies: [covered-call, covered-strangle, ratio-write, short-premium, buy-write]
confidence: high
---

# The Hidden Cost of Selling Covered Calls for Income

## Summary
A two-person Outlier Podcast discussion (host + Euan Sinclair) dismantling the popular Reddit idea that you can "sell covered calls for income." The central argument: the premium you collect is not income — it is compensation for a real liability (short volatility / capped upside), and if you sell a call for less than its true expected value you are booking *negative* income even when the trade "wins." Selling calls is only defensible when you can articulate a specific reason the call is overpriced (real edge), not as a blanket rule. The usable core: benchmark a covered call against the correct counterfactual (selling an equivalent % of shares), understand you are simply short vol, and subject every call sale to the same "why is this a sale?" analysis you'd apply to any profit-seeking trade.

## Key takeaways
- Premium is not income. If a $100 stock has a God-known 10% chance of going to $200 and you sell the $150 call for $2, that call's expected value is ~$5 (10% × $50 ITM), so selling it for $2 books ~$3 of *negative* income even though $2 of premium landed in your account. [01:19]
- It's a repeated game, not one trade. Run it 10× and you collect $2 nine times (+$18) but lose ~$48 once (−$30 net = −$3/game) — exactly the EV loss predicted. You can win five in a row, feel like a genius, and still be on the wrong side of the casino. [02:56]
- Even with a real vol-risk-premium edge (sell the $5 call for $6), only the $1 of edge is "theoretical income." The rest of the premium is a reserve held against the market-risk liability — that's how a market maker books it (P&L-to-theo). [05:24]
- Premium is not a W2 paycheck. It sits in cash-and-sweep tied to an open trade you still have to reconcile; if the call goes ITM and you must roll, the money doesn't appear from nowhere and a small account may have to add capital. [07:19]
- The correct counterfactual: selling a 25-delta call ≈ selling 25% of your position. Judge the covered call against *that* benchmark, not against zero. [10:00]
- You're just short volatility. You're sad on any large move in *either* direction (stock to 0, or called away as it rips to $200) and happy only on small moves — the payoff of a short-vol/short-gamma position, regardless of call vs. put. [11:12]
- The irony of covered calls: max profit sits above the short strike, which is exactly where the writer is unhappy (called away, unwinding inventory). People fixate on the short call and forget the trade's engine is the long equity. [11:58]
- Owning a single stock is a bet on the right tail ("for every Amazon there's 10 Pets.com"). Selling calls explicitly hands away that right tail — the whole reason to own the name instead of the index. [15:00]
- Systematic covered-call funds (e.g. S&P buy-write) tend to underperform: a good underlying spends most of its time going up, and the funds are predictable non-economic actors, so market makers front-run and bid their calls lower. [13:07]
- High IV/skew is usually high for a reason, not a free sale. Oil call skew was elevated because Polymarket implied ~62% odds of a strike on Iran before end of March; the calls only look expensive absent that information. [25:04]
- At vol extremes, implied never reaches what realized can do. Silver realized ~130% recently — there was no vol you could have sold that won, because implied never got there (same lesson he's lived in natural gas). Sinclair's joke: "buy the highest, sell the second highest" — the highest vol on the board is probably still not high enough. [30:30]
- You don't trade the IV line on a chart; your P&L comes from how much the underlying actually moves. On near-dated options he thinks in straddle prices, not IV. The "IV percentile is high so it must mean-revert" thesis ignores that P&L is driven by realized movement (and by vol clustering). [28:18]
- Sinclair's partial fix — a covered strangle held as a longer-term campaign with calls sold at a *ratio* (e.g. 500 long shares → sell only 2–3 calls, not 5) — plus doing real analysis: match vol terms (don't compare 30-day underlying vol to a 50- or 20-day option), prefer IV percentile over IV rank, and sell "meaty" ~25–30 delta rather than skinny 5-delta calls. [13:29]
- Where a genuine risk premium to *sell* calls exists: when buyers are lifting calls and the market must pay sellers (e.g. SoftBank/Masayoshi Son lifting tech calls in late 2021, sending call skew "nuclear"). Normally market makers are the natural call buyers, so there's no standing premium for retail call sellers. The hard leg is where the premium is. [34:06]

## Notable quotes
- "You have collected premium upfront, but I would not think that you collected any income." [01:19]
- "You're just short volatility. You just don't want the thing to move." [11:12]
- "Call premiums are not free money." [36:10]

## Candidate wiki links
- concepts: [[concepts/opportunity-cost]], [[concepts/capped-upside]], [[concepts/expected-value]], [[concepts/short-volatility]], [[concepts/short-gamma]], [[concepts/volatility-risk-premium]], [[concepts/risk-premium]], [[concepts/right-tail]], [[concepts/mark-to-market]], [[concepts/market-maker]], [[concepts/straddle-price]], [[concepts/earnings-move]], [[concepts/implied-volatility]], [[concepts/realized-volatility]], [[concepts/implied-volatility-percentile]], [[concepts/implied-volatility-rank]], [[concepts/volatility-mean-reversion]], [[concepts/volatility-clustering]], [[concepts/volatility-skew]], [[concepts/theta-decay]], [[concepts/gamma]], [[concepts/delta]], [[concepts/vega]]
- strategies: [[strategies/covered-call]], [[strategies/covered-strangle]], [[strategies/ratio-write]], [[strategies/short-premium]], [[strategies/buy-write]]
- securities: [[securities/hood]], [[securities/amzn]], [[securities/aapl]], [[securities/tsla]], [[securities/spx]], [[securities/oil]], [[securities/silver]], [[securities/natural-gas]]
- people: [[people/euan-sinclair]], [[people/masayoshi-son]]

## Regime / context
- As of 2026-03-13, oil call skew was elevated because Polymarket implied ~62% odds of a US strike on Iran before end of March; Sinclair treats the rich oil calls as *justified*, not a free premium. Regime-dependent.
- Silver had recently realized ~130% one-month vol — his example that at extremes, no sold vol could have won because implied never reached realized. Date/regime specific.
- "Liberation day" (the April 2025 tariff vol shock) is referenced as the tail scenario in which a one-year OTM call would explode in value — used to explain vega/mark-to-market risk of longer-dated short calls.
- The SoftBank/Masayoshi Son late-2021 tech-call buying is cited as the historical example of when a real risk premium to *sell* calls appears; not a current condition.
- The overall thesis is framed as evergreen (premium ≠ income; do the analysis), but every "is this call a sale?" judgment is explicitly regime- and underlying-specific.
