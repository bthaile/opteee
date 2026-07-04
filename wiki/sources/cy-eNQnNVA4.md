---
type: source
title: "Analyzing GameStop Swap Impact to Price | Meme Stock Watch Ep56"
video_id: cy-eNQnNVA4
url: https://www.youtube.com/watch?v=cy-eNQnNVA4
date: 2025-11-23
series: meme-stock-watch
format: [education, analysis, live]
experts: [eric]
mentions: [masayoshi-son]
securities: [gme, btc, mstr, spy]
concepts: [market-breadth, market-regimes, volatility-clustering, delta-neutral, covered-strangle, risk-management, backtesting, quantitative-research, correlation, sample-size, survivorship-bias, context-window-management, prompt-engineering, large-language-model, intrinsic-value, cost-basis, position-sizing, capital-efficiency, realized-vs-unrealized-pnl, pnl-attribution]
strategies: [covered-strangle, delta-neutral, short-premium]
saga: gme-saga
part: null
confidence: high
---

# Analyzing GameStop Swap Impact to Price | Meme Stock Watch Ep56

## Summary

Eric conducts a rigorous statistical analysis of GameStop equity swaps and their relationship to price behavior, using publicly available swap data and Google Sheets formulas to test whether swap expiration dates are predictive of price movement. He demonstrates the methodology for building a correlation analysis comparing pre/post-swap price performance against random control dates, and shares his current [[covered-strangle]] position (400 shares, 5 short puts, 4 short calls) which is outperforming the underlying by 56% year-to-date despite GME being down 36%.

## Key takeaways

### Dated market read (2025-11-23)

- **Broad market pullback underway** [00:00–06:00]: Market is ~5–6% off all-time highs; correction (10% drawdown) is possible but not yet confirmed. Probabilistic bias remains near-term bearish, long-term bullish pending volume stabilization and index stabilization.
- **Bitcoin 36% decline in <2 months** [07:25–10:08]: Aggressive bear market move without clear structural catalyst (no futures removal, no regulatory ban, no institutional unwinding announcement). Mirrors historical volatility patterns but remains anomalous.
- **GameStop intrinsic value near current price** [22:03]: With cash and Bitcoin holdings, intrinsic value ~$19.40/share; current price near that floor suggests limited downside but also limited margin of safety.

### Evergreen mechanics

- **Swap analysis methodology** [23:32–01:25:22]: To test swap predictiveness rigorously, collect *all* swap expiration dates and notional values, overlay price behavior 20/10/5 days before and after each expiration, calculate percent changes, then run correlation analysis. Compare against random control dates (non-swap days) to isolate swap signal from noise.
- **AI-assisted formula building** [41:41–49:27]: Use Gemini, Grok, or ChatGPT to generate WORKDAY and INDEX/MATCH formulas for date alignment and price lookup; validate outputs manually; lock cell references appropriately for copy-paste replication.
- **Handling data quality issues** [52:50–01:01:17]: Market holidays cause "date not found" errors; either manually override with nearest trading day or request AI to incorporate holiday calendars. Duplicate swap dates should be deduplicated before analysis to avoid false weighting.
- **Covered strangle execution in downtrends** [01:26:34–01:28:09]: When underlying is weak, shift to 1:0.8 or 1:0.75 call-to-put ratio (short more puts than calls) to capture premium while reducing upside cap; allows outperformance vs. buy-and-hold even in down markets.
- **Position allocation tracking** [01:30:56–01:32:26]: Allocate a fixed capital amount (e.g., $25k) to a single strategy; track utilization % (stock, cash-secured puts, cash reserve); assess returns against that full allocation, not just deployed capital, to reflect true opportunity cost.

## Notable quotes

> "I honestly think the GameStop community would do themselves a massive favor if you guys maintain awareness that swaps are a thing and they exist, but it's less of a focal point in terms of analysis and price forecasting. It's just because it's not like we can see by measuring them that it really isn't predictive." [23:32]

> "The only way to actually analyze this rigorously is not to pick the instances where this swap was due at this point and saying like, oh here look the swap made it move. It's not how you conduct an actual rigorous scientific study." [24:55]

> "Because of the coverage triangle and because of trading around it, not only am I not down, but I'm actually making a decent amount of money. And so that total allocation compared to the market this year, that position my coverage triangle in game stop something that's gone down 36% from the start of the year is outperforming the market to the upside." [01:28:09]

## Candidate wiki links

**concepts:**
[[market-breadth]], [[market-regimes]], [[volatility-clustering]], [[delta-neutral]], [[risk-management]], [[backtesting]], [[quantitative-research]], [[sample-size]], [[survivorship-bias]], [[intrinsic-value]], [[cost-basis]], [[position-sizing]], [[capital-efficiency]], [[realized-vs-unrealized-pnl]], [[pnl-attribution]], [[context-window-management]], [[prompt-engineering]], [[large-language-model]]

**strategies:**
[[covered-strangle]], [[delta-neutral]], [[short-premium]]

**securities:**
[[gme]], [[btc]], [[mstr]], [[spy]]

**people:**
[[masayoshi-son]] (mentioned re: MicroStrategy Bitcoin strategy)

## Regime / context

**Date:** 2025-11-23. Broad market in early-stage pullback; Bitcoin in aggressive bear move; GameStop near intrinsic value floor.

**Swap analysis caveat:** The swap data sample shown (~20 swaps) is incomplete; a comprehensive analysis requires *all* known GameStop swaps. The visual chart shows some anomalous periods (notably one with large pre-expiration rally followed by post-expiration contraction) but no clear systematic pattern emerges from eyeballing. Correlation analysis (homework) is required to quantify predictiveness vs. random dates.

**Position context:** Eric's $25k GME allocation (covered strangle) is ~10% of his sample portfolio and represents a deliberate long-term engagement with the GME community, not a directional bet. Year-to-date (2025) the position is +19.9% vs. GME spot −36.75%, demonstrating the power of [[delta-neutral]] premium strategies in downtrends.
