---
type: source
title: "How to Build Options Trades That Actually Make Sense"
video_id: 3L6XRJq0IUo
url: https://www.youtube.com/watch?v=3L6XRJq0IUo
date: 2026-08-30
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [micron]
concepts: [profit-mechanism, volatility-risk-premium, implied-volatility, realized-volatility, distribution, location, width, shape, term, put-skew, volatility-surface, implied-volatility-percentile, expected-move, time-decay, greeks, gamma, theta, vega, directional-bias, volatility-claim, term-structure, variance-premium, risk-premium, greek-attribution, greek-profile, pnl-attribution]
strategies: [long-call, synthetic-long, stock-replacement, short-put, vertical-spread, long-volatility, short-volatility, straddle, long-straddle, put-spread, call-credit-spread]
saga: null
part: null
confidence: high
---

# How to Build Options Trades That Actually Make Sense

## Summary

This video teaches traders to reverse their approach to trade construction: instead of learning a strategy first and then finding something to trade it in, start with a **profit mechanism** (an edge or market inefficiency), then work through four filtering questions about location, width, shape, and term to determine which structure best captures that edge. The core insight is that the same directional idea can be expressed through multiple structures with vastly different Greeks, P&L curves, and risk profiles—and choosing the wrong expression can cause you to lose money even when your directional thesis is correct.

## Key takeaways

- **Start with profit mechanism, not strategy** [00:34–01:27]: Begin by identifying a real market inefficiency (e.g., implied vol is rich relative to realized vol), then work backward to find the structure that captures it. Never start by learning a strategy and hunting for something to trade it in.

- **Four market dimensions priced into every option** [02:00–04:04]: The market prices location (directional claim), width (volatility/distribution spread), shape (skew/asymmetry), and term (expiration relationships). Every trade speculates on at least one of these; understand which one(s) you're actually trading.

- **Location claim is just one of four** [04:30–05:25]: A directional view ("it's going up") immediately eliminates half the structure universe, but it's not the only tradeable claim. Width, shape, and term claims are equally valid.

- **Implied vol surface is not uniform** [06:37–07:34]: Each strike and each expiration has its own implied vol. A common mistake is measuring IV percentile on 30-day vol but then trading a 60-day short put—you're expressing your idea in a different vol regime than you analyzed.

- **Target relative to bracket (expected move)** [08:33–09:48]: Check whether your directional target falls within the market's implied move (one standard deviation). If it's outside, you're making two claims: directional AND that implied vol is too cheap.

- **Expected move scales by square root of time** [10:13–10:40]: The same 25% implied vol produces different expected move ranges across different expirations. A 7-day move is much smaller than a 90-day move, even with identical vol.

- **Distribution width matters for trade selection** [11:16–11:41]: If you're selling premium and think vol is overpriced, you can trade things inside the distribution. If you're directional, you might target something more likely within it. Wider distributions (higher vol) change the entire picture.

- **Same idea, different term = different Greeks and P&L shape** [12:58–13:51]: A bullish trade expressed in near-term options is gamma and theta sensitive but not vega sensitive; far-term is the opposite. Choosing near-term for more gamma means accepting high theta decay and a narrow window to be right.

- **You can be directionally correct and still lose money** [13:51–14:17]: If the stock goes up but implied vol was overpriced relative to realized vol, or if time decay outpaces your move, you lose despite being right on direction.

- **Vertical spreads neutralize most Greeks** [15:19–15:45]: Narrow verticals isolate a specific zone and eliminate gamma, vega, and theta exposure. This is why selling a put spread when vol is high doesn't capture much vol edge—the structure itself neutralizes it.

- **Straddles are not pure volatility trades unless hedged** [16:35–17:05]: Over the life cycle, straddles develop directional tilts and Greek imbalances. A point-in-time vol claim is reasonable, but the trade shape changes as it evolves.

- **Use structure as a tool to isolate your edge** [17:26–17:52]: Match your market view (location, width, shape, term) to a structure that isolates those factors. This is the inverse of "I know spreads, so I'll trade spreads."

## Notable quotes

> "You shouldn't literally never place a trade like that ever again." (referring to learning a strategy first, then finding something to trade it in)

> "You can be completely correct and still lose money." (the core risk of mismatched structure to thesis)

## Candidate wiki links

**concepts:** [[profit-mechanism]], [[volatility-risk-premium]], [[implied-volatility]], [[realized-volatility]], [[distribution]], [[location]], [[width]], [[shape]], [[term]], [[put-skew]], [[volatility-surface]], [[implied-volatility-percentile]], [[expected-move]], [[time-decay]], [[greeks]], [[gamma]], [[theta]], [[vega]], [[directional-bias]], [[volatility-claim]], [[term-structure]], [[variance-premium]], [[risk-premium]], [[greek-attribution]], [[greek-profile]], [[pnl-attribution]]

**strategies:** [[long-call]], [[synthetic-long]], [[stock-replacement]], [[short-put]], [[vertical-spread]], [[long-volatility]], [[short-volatility]], [[straddle]], [[put-spread]], [[call-credit-spread]]

**securities:** [[micron]]

**people:** [[eric]]

## Regime / context

Dated 2026-08-30. This is a foundational education video on options trade construction methodology, not a market-specific or time-sensitive analysis. The principles (profit mechanism first, structure second, Greeks as expression tools) are evergreen. The Micron example is illustrative only and does not constitute a trade recommendation.
