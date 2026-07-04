---
type: source
title: "GameStop Coverage Triangle & Options Strategy Deep Dive"
video_id: WQrRww-DKiE
url: "https://www.youtube.com/watch?v=WQrRww-DKiE"
date: "2023-04-17"
series: none
format: [education, analysis, live]
experts: [eric]
mentions: []
securities: [gme, spy]
concepts: [covered-strangle, cost-basis, delta, delta-hedging, delta-neutral, expected-move, gamma, implied-volatility, moneyness, position-sizing, probability-cone, realized-vs-unrealized-pnl, risk-management, short-put, theta, theta-decay, trading-plan, volume-analysis]
strategies: [covered-strangle, short-put, scaling-in, scaling-out]
saga: gme-saga
part: null
confidence: medium
---

# GameStop Coverage Triangle & Options Strategy Deep Dive

## Summary

Eric walks through a live GameStop position management case study, demonstrating how he rotated out of equity into short puts to reduce cost basis, then explores options buying mechanics—specifically how to structure call spreads when targeting a price move. The session covers theta decay on far-OTM units, delta accumulation, and the trade-off between conviction timing and position sizing.

## Key takeaways

- **Position rotation (April 7)** [13:20–24:12]: Exited 400 shares at $23 (basis $25.75, realizing ~$1,070 loss) and simultaneously sold 4 short puts at the $23 strike to recover the loss via premium. This reduced effective basis by $2.75 per share (~10% improvement) without requiring the stock to recover to original entry.

- **Volume as a leading indicator** [27:47–29:02]: GameStop has never had a major move without preceding volume expansion. Eric uses 5-day vs. 20-day average volume and slope to confirm risk-off before exiting; waits for volume confirmation before scaling back in.

- **Units and convexity in call buying** [41:22–48:16]: When targeting a specific price (e.g., $34 by June), buying far-OTM calls (e.g., $50 strike at $0.32) allows accumulation of many contracts for the same capital, yielding higher aggregate delta (~1,890 delta on 475 contracts vs. 876 delta on 26 at-the-money calls). However, theta decay is severe on a percentage basis (~2¢ daily on a $0.12 purchase = 17% daily decay).

- **Timing cost of units** [50:50–53:41]: A 10% move in GameStop yields $7,118 profit today but only $443 in two weeks (94% decay) if the move is delayed. This illustrates why far-OTM units require precise timing; holding them is expensive.

- **Balancing conviction and decay** [54:58–58:39]: If expecting a move over three expiration cycles, split capital equally across front-week, near-term, and further-out expirations. Front-week units (at $0.03) allow 555 contracts per $1,667 allocation; you can afford to lose all three tranches and still profit if the move hits in any cycle.

- **Vertical spreads mute theta** [01:20:18–01:21:49]: Selling a $25 call and buying a $24 call reduces theta from $2.71 to $0.32, making spreads more directional bets than pure theta plays. Time-frame selection matters less for spreads than for naked units.

- **Current GameStop positioning** [33:59–35:14]: Using ~60% of allocation in short puts ($25 strike, May 30 expiry; $26 strike, May 16 expiry). Realized + unrealized P&L is 22% vs. 13% buy-and-hold equivalent, achieved with <90% capital utilization.

## Notable quotes

> "There has literally never been a random crazy move in GameStop that was not preceded by volume." [27:47]

> "The short answer is if I think this thing is going to go to 34 and let's just say it's sometimes soon, what I would do is I would go out far out of the money... because you can buy so many of them that you can eventually brute force your delta." [40:19–41:22]

## Candidate wiki links

**concepts:** [[delta]], [[theta]], [[theta-decay]], [[implied-volatility]], [[moneyness]], [[gamma]], [[cost-basis]], [[position-sizing]], [[volume-analysis]], [[realized-vs-unrealized-pnl]], [[risk-management]], [[delta-hedging]], [[expected-move]]

**strategies:** [[short-put]], [[covered-strangle]], [[scaling-in]], [[scaling-out]]

**securities:** [[gme]], [[spy]]

**people:** [[eric]]

## Regime / context

Recorded April 17, 2023. GameStop trading in the $24–$27 range; no major catalyst visible at time of recording. Eric notes he will produce a deeper fundamental deep-dive video separately. The position management case study is part of his ongoing GameStop saga documentation (sample trade, not the full portfolio). Numeric figures (share prices, P&L percentages, option premiums) are approximate due to ASR transcription quality and live market data.
