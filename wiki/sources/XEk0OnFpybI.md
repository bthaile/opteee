---
type: source
title: "GameStop Earnings Vol Trade & DD Library Review"
video_id: XEk0OnFpybI
url: "https://www.youtube.com/watch?v=XEk0OnFpybI"
date: "2024-03-18"
series: none
format: [education, analysis, live]
experts: [eric]
mentions: [roaring-kitty]
securities: [gme, aapl, spy]
concepts: [covered-strangle, implied-volatility, earnings-vol-play, bid-ask-spread, theta-decay, delta, gamma, position-sizing, risk-management, naked-short-selling, ftd, dark-pools, order-internalization, volume-analysis, technical-analysis, market-maker, trading-psychology]
strategies: [covered-strangle, short-premium, earnings-vol-play]
saga: gme
part: null
confidence: medium
---

# GameStop Earnings Vol Trade & DD Library Review

## Summary

Eric reviews GameStop's elevated implied volatility (123%) ahead of earnings on 28 March and demonstrates how he's adjusting his [[covered-strangle]] position to capitalize on the vol spike. He then conducts a detailed critique of community DD posts on naked shorting, dark pools, and FTD cycles, emphasizing the importance of objective analysis and correcting common misconceptions about market mechanics. A viewer's short-dated call position is dissected to illustrate the dangers of trading illiquid weekly options with wide [[bid-ask-spread]]s and steep [[theta-decay]].

## Key takeaways

### Dated market read (2024-03-18)

- **GameStop vol elevated at 123% on 28 March expiration** [00:00] — heavy on a comparative basis; Eric plans to adjust his [[covered-strangle]] to trade the earnings vol spike.
- **Call/put skew not anomalous** [18:22] — positioning data (571 vs 175 calls vs puts in 17 April; 41 vs 10 in 28 March) shows no heavy directional bias into earnings; suggests standard release, not a squeeze setup.
- **Community positioning has cooled** [19:33] — fewer emails about GameStop cycles and theories; longer-term holders "hunkering down"; transient traders falling away.
- **Coverage strangle P&L: +7.5% while underlying down 5.2%** [30:08–31:37] — demonstrates the strategy's resilience in sideways/down markets; realized premium of ~$2,540 on $25k allocation; sustainable but not "sexy."

### Evergreen mechanics

- **Covered strangle adjustment process** [20:53–23:31] — roll short puts from 17 April (23s, 21s) into 28 March (22s, 26s); size up slightly; take call side (28s) down near scratch after vol siphons to front expiration.
- **Delta selection based on risk tolerance** [26:05] — delta chosen to match desired position risk; ATM options near earnings have extreme [[gamma]], so delta changes rapidly; naked earnings trades on volatile stocks like GameStop require either spreads or minimal sizing.
- **Bid-ask spread as a hidden cost** [34:37–38:05] — compare GME weekly (82¢ spread, 3.42% of strike) vs AAPL same expiration (10¢ spread, ~0.1% of strike); illiquidity is a direct transfer to market makers.
- **Theta decay accelerates within 60 DTE** [39:27–48:04] — theta as % of premium rises sharply; at 48 DTE, theta is 1.25% daily; by 17 April, it becomes parabolic; breakeven moves up as time passes without directional move.
- **Long option breakeven drift** [41:18–45:08] — purple line (today's P&L curve) vs blue line (expiration); as time advances, breakeven shifts right; a week forward, stock must hit 2390 instead of 2334 to break even.
- **Weekly options are a trap for retail** [45:08–49:19] — wide spreads + parabolic decay = "giving market makers an egregious amount of money"; solution: go 125 DTE, 68 delta (deeper ITM), accept higher premium but get 2¢ theta instead of 3¢.

### DD library critique

- **FTD cycle overfitting** [01:18:08] — broad statistical analysis of GameStop (pre/post ATM) shows T+33/T+35 cycles are not reliably correlated with price moves; classic overfitting to historical data.
- **Dark pool misconceptions** [01:05:42–01:09:14] — dark pool transactions hit consolidated tape within seconds; do not suppress buying pressure; volume spikes at market open/close are normal liquidity events, not evidence of fuckery; same pattern in AAPL, SPY.
- **Naked shorting is real, but conclusions are speculative** [01:11:52–01:13:24] — FTDs and >100% float short are provable; Citadel's dual MM/HF arms are a conflict; but the leap to "uncontrolled squeeze will happen" contradicts the premise that manipulation is pervasive and would be stopped again.
- **Broker share lending is standard** [56:11–57:03] — shares in your account are not physically parked; brokers lend them out (like banks lend deposits); you retain rights but not custody unless you opt out (e.g., DRS).
- **GameStop's abnormality is the real takeaway** [01:19:46] — the one solid conclusion: GameStop's performance is not normal; this is the easiest and most defensible observation.

## Notable quotes

> "The covered strangle isn't going to look super sexy when the market's going straight up. That's when you have to increase your shares. But with the market doing what it is now, that's why I've pivoted so hard where the stock requirement is so very light and the cash secured put requirement is much heavier."

> "It literally pains me to see so many new options traders trading something as nuanced as GameStop and just losing money. I really hate to see that because I know the people that are losing the money are the people that don't really have the money to lose."

> "My entire lens, generally of the world, but particularly markets is the best attempt I can possibly conjure up at objective analysis. That is literally my goal standard. It's because it's how I trade. It's the only way to make money in markets."

## Candidate wiki links

**concepts:** [[covered-strangle]], [[implied-volatility]], [[bid-ask-spread]], [[theta-decay]], [[delta]], [[gamma]], [[position-sizing]], [[risk-management]], [[naked-short-selling]], [[ftd]], [[dark-pools]], [[order-internalization]], [[volume-analysis]], [[technical-analysis]], [[market-maker]], [[trading-psychology]], [[earnings-vol-play]], [[moneyness]], [[days-to-expiration]], [[expected-move]]

**strategies:** [[covered-strangle]], [[short-premium]], [[earnings-vol-play]], [[weekly-options]]

**securities:** [[gme]], [[aapl]], [[spy]]

**people:** [[eric]], [[roaring-kitty]]

## Regime / context

**Date:** 18 March 2024 (pre-earnings, 28 March expiration live).

**GameStop saga context:** This is a live trading update and community education stream. Eric is running a real $25k [[covered-strangle]] allocation on GME to demonstrate sustainable options income; the position is +7.5% YTD despite the underlying down 5.2%, illustrating the strategy's resilience in choppy markets. The DD library segment critiques popular community theories (FTD cycles, dark pool suppression, naked shorting) with emphasis on statistical rigor and market mechanics; Eric's stance is that while naked shorting and FTDs are real, many community conclusions overfit historical data or misunderstand how dark pools and market-making work.
