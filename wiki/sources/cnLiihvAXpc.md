---
type: source
title: "Market Making Tricks for Non Market Makers | The Options Trench"
video_id: cnLiihvAXpc
url: https://www.youtube.com/watch?v=cnLiihvAXpc
date: 2026-04-18
series: options-trench
format: [education, interview, analysis]
experts: [eric]
mentions: []
securities: [spy, ibm, uso, gme]
concepts: [market-maker, market-efficiency, edge, execution, liquidity-cycle, order-flow, risk-premium, position-sizing, trading-psychology, business-model, economies-of-scale, regulatory-framework, volatility-surface, strike-vol, profit-mechanism]
strategies: [market-making, short-premium, execution-optimization]
saga: null
part: null
confidence: high
---

# Market Making Tricks for Non Market Makers | The Options Trench

## Summary

This episode explores the structural differences between market makers, professional fund managers, and retail traders—and which market-making principles can be profitably adapted by non-market-makers. The hosts clarify that retail traders cannot legally replicate market-maker strategies due to regulatory privileges (short-locate exemptions, position-limit exemptions, order-rate exemptions), but can adopt execution discipline, liquidity-provision thinking, and strike-vol monitoring to improve their own trading. The core insight: understand your place in the market ecosystem and optimize for the constraints you actually face.

## Key takeaways

### Market-maker regulatory advantages (cannot be replicated by retail)
- **Short-locate exemption** [05:21]: Market makers don't need pre-trade locate approval when hedging; retail and funds must secure locates beforehand via prime brokers.
- **Position-limit exemption** [06:48]: Market makers have no caps on options positions; retail is capped at 250,000 contracts per side. In low-volume markets (e.g., USO options), this can severely constrain trading volume.
- **Order-rate exemption** [09:19]: Market makers can send unlimited orders; retail is capped at ~390 orders per day on average (the "390 order rule").
- **Designated market maker (DMM) allocation** [08:36]: Specialists receive guaranteed participation (e.g., 40%) on bid/offer trades in their assigned names.

### Why these privileges exist [10:35]
Market-maker privileges are the "ante" that incentivizes continuous liquidity provision. Without them, no one would post bids/offers (they'd only trade when certain to win). The bargain: privileges in exchange for **mandatory quoting obligations**—maintaining tight spreads, minimum size, and continuous presence, subject to regulatory review and probation for violations.

### Money-manager perspective: warehouse risk, not flip [16:38]
- **Differentiate from market makers** [19:13]: Don't compete on speed. Instead, offer to warehouse larger size without "ruining the picture" (bidding up the assets the broker is trying to buy).
- **Pitch to brokers** [21:33]: "I can't be as fast as a market maker, but I'll take your risk off your hands and not immediately flip it against you."
- **Economies of scale** [24:08]: Institutional advantages include better funding rates, portfolio margining, and lower per-contract costs. Retail paying $1/contract cannot run a viable options business at scale.
- **Sharpe ratio trade-off** [22:39]: A fund can accept 1–1.5 Sharpe after fees if it warehouses risk; market makers need 5+ Sharpe because they're just flipping.

### Retail execution: strike-vol scanner and market-making around your axe [28:14]
- **Build a strike-vol monitor** [29:01]: Track how individual strike vols (not ATM vol) are changing across a cross-section of names. Strike vol is what drives P&L, not headline vol.
- **Distinguish strike-vol from ATM vol** [29:48]: If SPX rallies and vol falls, the higher strike naturally trades lower vol than yesterday's strike—but the strike vol itself may not have moved.
- **Identify relative outperformance/underperformance** [30:27]: On days when IBM vol outperforms (rises faster than peers), that's a good day to sell IBM options if you want to be short IBM vol.
- **Scale in/out around your signal** [31:33]: Sell 3,000 vega on outperformance days; buy back 1,000 vega on underperformance days. You're "market making around your axe"—executing intelligently over time rather than all at once.
- **Detect flow** [31:11]: Abnormal strike-vol moves often signal options flow pushing the surface; dig deeper to confirm before executing.

### Retail advantages over market makers [34:43]
- **Infinite patience**: No obligation to trade; can wait for optimal entry/exit.
- **Liquidity flexibility**: Small position sizes (10–30k) mean you can flip from long to short in minutes without market impact.
- **Post-earnings drift (PEAD) arbitrage** [36:05]: Big money takes time to position; retail can ride the flow and exit before the dinosaur steps off.
- **Leech strategy** [36:05]: Detect large order flow, ride it briefly, exit cleanly—no need to hold the full position.

### Should you want to be a market maker? [37:49]
- **No**: Market-maker P&Ls are large, but traders are evaluated on "value over replacement"—the boss credits 90% of the P&L to the firm's technology, not the trader.
- **Capex burden**: Becoming a market maker requires hundreds of millions in annual tech capex and maintenance.
- **Survivorship**: ~1,000 market makers existed 25 years ago; now ~10 remain. Most failed.
- **Retail freedom**: As a sole prop, you avoid corporate politics, customer calls, and board meetings. The trade-off (lower absolute P&L) is worth it for autonomy and learning.

### Community and growth [45:54]
- **What's missed from institutional seats**: Collaboration, sparring, peer feedback, shared incentives.
- **Modern compensation**: Discord, group chats, and social media now enable community-building that was impossible in 1985. You can approximate institutional collaboration without the golden handcuffs.

### Know your place on the reef [50:17]
- **Market makers provide liquidity** and get paid for it. Understand what risk premium you're offering and how you're accessing it.
- **Minimize execution cost** subject to your constraints. If your edge pencils out despite imperfect execution, the edge is real.
- **Avoid low-edge markets**: SPY is too liquid; market makers don't make money there. Edge lives in sparse liquidity (e.g., energy options, low-volume names).
- **Be honest about your advantages and disadvantages.** Play to your strengths.

## Notable quotes

> "You cannot trade like a market maker. You cannot from a regulatory point of view—this is a regulatory designation to be a market maker. It is not just a status and a job. It's literally got all kinds of legal infrastructure around it." [04:31]

> "It's like the ante in poker. If there were no ante, you should never play. You would only play when you knew you were going to win. So there has to be an incentive." [11:29]

> "Know your place and play into your strengths." [52:29]

## Candidate wiki links

**concepts:**
- [[market-maker]]
- [[liquidity-cycle]]
- [[order-flow]]
- [[risk-premium]]
- [[execution]]
- [[edge]]
- [[volatility-surface]]
- [[profit-mechanism]]
- [[trading-psychology]]
- [[position-sizing]]
- [[economies-of-scale]]

**strategies:**
- [[short-premium]]
- [[market-making]]

**securities:**
- [[spy]]
- [[ibm]]
- [[uso]]
- [[gme]]

**people:**
- [[eric]]

## Regime / context

Recorded 2026-04-18. This is a follow-up to a previous episode on "what a market maker actually does." The discussion is evergreen—regulatory structure and incentive alignment are stable—but references to specific market-maker firms and survivor counts reflect the state of the industry as of early 2026. The retail execution techniques (strike-vol scanning, market-making around your axe) are applicable to any options market with sufficient depth and flow.
