---
type: source
title: "Software and Tools I Use to Trade Options - Skill Development | Outlier Pro"
video_id: mO3gU9NeusA
url: https://www.youtube.com/watch?v=mO3gU9NeusA
date: 2025-12-12
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [aapl, spx]
concepts: [trading-plan, trading-log, market-breadth, implied-volatility, realized-volatility, volatility-risk-premium, delta, gamma, vega, earnings-move, zero-dte, expected-move, iv-rank, implied-volatility-percentile, volume-profile, technical-analysis, backtesting, quantitative-research, market-maker, dealer-gamma, position-sizing, risk-management, process-over-outcome, pnl-attribution, market-regimes, sector-rotation, economic-data, volatility-term-structure, skew, order-flow, unusual-options-activity]
strategies: [covered-strangle, short-premium, zero-dte, earnings-vol-play, box-spread, momentum, short-straddle]
saga: none
part: null
confidence: high
---

# Software and Tools I Use to Trade Options - Skill Development | Outlier Pro

## Summary

Eric walks through the complete ecosystem of platforms, tools, and workflows he uses for options trading research, analysis, and execution. The video covers market research platforms (SSRN, Thinker Swim, O-Rats, Unusual Whales, BarChart), modeling environments (Python, R, Jupiter, Excel, Google Sheets), and execution infrastructure, emphasizing that the research and feedback loop—via trading plans and trade logs—is where the real work happens. He stresses that expensive platforms like Bloomberg terminals don't materially improve retail edge, and that consistent process matters more than tool proliferation.

## Key takeaways

### Research & Documentation
- **Trading plan and trade log are foundational** [00:00]. Documentation can be as simple as Word, Google Sheets, or Excel; the structure matters more than the platform.
- **SSRN is essential for foundational research** [11:27]. Most retail traders skip the scientific approach and lose money as a result; SSRN teaches analytical rigor.
- **Economic data sources (FRED, Edgar, NBER)** [09:56] provide regime context but should not drive portfolio positioning directly; macro-primed portfolios underperform momentum-based approaches.

### Market Research Platforms
- **BarChart** [16:16] excels at market breadth analysis, economic calendars, breadth indicators, and stock screeners; used for high-level market analysis and daily scan alerts.
- **Unusual Whales** [21:57] is superior for options flow research, volatility tools, net premiums, and positioning; best for active, short-term, flow-based trading but not recommended as a starting point for most traders.
- **O-Rats** [26:09] provides the most convenient earnings analysis, options chain visualization across the vol curve, and trade-level data; pairs well with API integration.
- **BarChart and Unusual Whales open automatically** [17:24] in Eric's Chrome workflow; O-Rats opens only for specific use cases.
- **Bloomberg terminals (~$20k/month)** [12:35] offer no material edge for retail traders despite rich data; Eric plans to access one for community research via Patreon.

### Modeling & Analysis
- **Python (Jupiter notebooks) and R** [40:35] are the workhorses for backtesting, strategy codification, and statistical analysis; no excuse to avoid them with AI assistance available.
- **Excel and Google Sheets** [43:12] are perfect starting points for basic modeling (term structure, delta skew, vega changes); Google Sheets preferred for portability.
- **Historical options data from CBOE** [20:09] is expensive but the purest source; intraday-level data costs scale significantly.

### Execution & Portfolio Tracking
- **Trading plan is consulted post-trade, not pre-trade** [44:35] for most experienced traders; newer traders should use it to slow down and catch mistakes (e.g., missing earnings dates).
- **Portfolio-level dashboard (C2C: Command & Control)** [48:22] bubbles up strategy-level statistics into a single view; tracks core vs. speculative allocation performance separately.
- **End-of-month after-action review (AAR)** [50:00] reveals which profit mechanisms are working in the current regime; directs capital reallocation (e.g., away from speculative futures toward speculative vol if vol is outperforming).
- **Thinker Swim remains the execution platform** [51:21]; desktop, laptop (ASUS ROG G14), and mobile workstation used depending on travel and workload.

### Indicators & Chart Setup
- **Start zoomed out, zoom in** [01:02:05] to understand long-term context before trading near-term moves; prevents false confidence in short-term rallies.
- **Six-month and three-month timeframes** [01:02:05] are primary; six-month tests momentum factor, three-month aligns with typical trading windows (2–6 weeks).
- **Custom indicators** [01:04:28] include implied/realized vol stats, ADR/ATR, custom volume split (buy/sell), moving averages (10, 20, 50, longer-term), volume profile, price spike plot (sigma moves), RSI with EMA, autocorrelation stats, and breadth histogram (NASDAQ + NYSE net highs/lows).
- **Spot gamma, dealer gamma, delta exposure** [32:03] are "fun party tricks" but effectively meaningless without understanding the limiting assumptions (counterparty is not always a market maker; portfolio is not just SPX; hedging is imperfect).

### Zero-DTE Setup
- **Zero-DTE dashboard** [01:11:43] sits front-and-center in the trade log; contains day-specific statistics and performance data for zero-DTE trades.
- **Short-term vol charts** [01:15:01] on upper screen track vol, price spikes, recent price moves, ADR, specific ranges, expected moves; price charts used only for data extraction (sample periods, positioning), not directional bias.

### Portfolio Allocation Philosophy
- **Core allocation first** [01:08:14], then speculative; core provides dampening and consistency even if speculative fails.
- **Last three years anomalously strong** [01:00:54]; majority of returns from speculative bucket, but core still delivering strong returns despite two-thirds of covered strangles struggling.
- **Box spreads double-dip capital** [01:13:25]; cash securing puts is placed into box spreads timed to de-conflict from expiration; box spread premium over risk-free rate averages 0.75–1.0 point.

### Affiliate Relationships & Tool Selection
- **No editorial mandate** [14:00] with O-Rats, Unusual Whales, BarChart; relationships built on affiliate links and discounts, not revenue-sharing.
- **Options Omega** [14:00] is siloed to zero-DTE SPX trading; not included in general workflow.
- **Moonpower** [15:07] recently added; too early to assess after ~1 week of testing.

## Notable quotes

- "Most people skip all that. Most people lose money because they skip all that. Don't skip." [11:27] — on SSRN research.
- "It's a fun party trick. It's fun to be aware of. But it's effectively meaningless." [32:03] — on spot gamma and dealer gamma.
- "The cost of doing business" [29:00] — on professional-level trading infrastructure investment.

## Candidate wiki links

**concepts:** [[trading-plan]], [[trading-log]], [[market-breadth]], [[implied-volatility]], [[realized-volatility]], [[volatility-risk-premium]], [[delta]], [[gamma]], [[vega]], [[earnings-move]], [[zero-dte]], [[expected-move]], [[iv-rank]], [[implied-volatility-percentile]], [[volume-profile]], [[technical-analysis]], [[backtesting]], [[quantitative-research]], [[market-maker]], [[dealer-gamma]], [[position-sizing]], [[risk-management]], [[process-over-outcome]], [[pnl-attribution]], [[market-regimes]], [[sector-rotation]], [[volatility-term-structure]], [[skew]], [[order-flow]], [[unusual-options-activity]]

**strategies:** [[covered-strangle]], [[short-premium]], [[zero-dte]], [[earnings-vol-play]], [[box-spread]], [[momentum]], [[short-straddle]]

**securities:** [[aapl]], [[spx]]

**people:** [[eric]]

## Regime / context

Recorded December 2025. Eric reflects on three anomalously strong trading years (2023–2025) driven primarily by speculative allocation outperformance, with core allocation providing consistent dampening. The video is educational and platform-agnostic; tool recommendations reflect his personal workflow and affiliate relationships, not universal prescriptions. Emphasis on process, feedback loops, and regime-aware capital reallocation over tool proliferation.
