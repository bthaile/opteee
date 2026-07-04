---
type: source
title: "Analyzing Roaring Kitty's Trades Pt6 | GameStop Analysis Live Ep14"
video_id: "IsiLvT-L3vk"
url: "https://www.youtube.com/watch?v=IsiLvT-L3vk"
date: "2024-10-13"
series: none
format: live
experts: [roaring-kitty, richard-newton]
securities: [gme, spy]
concepts: [days-to-expiration, delta, gamma, gamma-ramp, leverage, out-of-the-money, cost-basis, stock-split, early-exercise, deep-itm-calls, position-sizing, order-internalization, payment-for-order-flow, bid-ask-spread, dollar-cost-averaging, buy-and-hold, risk-tolerance, asset-allocation, naked-short-selling, short-squeeze, meme-stock, confirmation-bias]
strategies: [long-call, leaps, event-driven]
confidence: high
---

# Analyzing Roaring Kitty's Trades Pt6 | GameStop Analysis Live Ep14

## Summary
A 3+ hour GameStop live stream (Pt6 of an ongoing series) in which the host reconstructs Roaring Kitty's (DFV / Keith Gill) full option-trade history from his posted "YOLO" update screenshots, building a spreadsheet that tracks every position's strike, size, basis and days-to-expiration (DTE). The analytical payoff is a profile of DFV's tendencies: he almost always buys far-out-of-the-money, long-dated calls to get cheap leveraged directional exposure (not a gamma ramp), holds with long DTE, and never sells options. The one exception — a single very short-dated (3 DTE) trade — lined up with a GameStop event, supporting the inference that near-dated buys signal event plays. Threaded throughout are evergreen lessons on cost-basis reconstruction, stock-split adjustment, "at the bid" vs mid fills, order internalization, and general risk/allocation advice from chat Q&A.

## Key takeaways

### Evergreen options mechanics
- DTE tendencies: across his entire 2019–2020 history, DFV's option entries cluster at long DTE — 495, 458, 229, 198, 168, 138, 137, 107, 94, 52 days — overwhelmingly >90 DTE, with only one short-dated (3 DTE) outlier. This is presented as a stable, identifiable behavioral fingerprint. [03:07][03:08]
- Far-OTM long-dated calls are leveraged directional exposure, NOT a gamma ramp. Because they're so far out in time their gamma is tiny; going far OTM just lets you buy a larger gross number of cheap contracts for a leveraged Delta play on a stock you think goes up. [03:03][03:06][03:07]
- "Building units" (a real gamma-ramp play) requires near-term OTM options where gamma is large and compounds on a move; DFV's positions are too far out in time for that. Illustrated live: at ~49 DTE a ~10–13 delta option shows gamma ~16 vs ~8 at 168 DTE. [03:07]
- Near-dated option purchases = event plays. The lone 3 DTE departure (14 Jan 2020) coincided with a GameStop holiday-sales readout — so when he buys near-dated options it "probably infers he thinks an event is happening," versus his usual longer-term leveraged-directional style. [03:09][03:10]
- "At the bid" vs "mid": a large order (e.g. 5,000 contracts, ~$2.75M premium) is essentially next-to-impossible to fill at the bid; a print tagged at the bid for that size looks like a data/coding error, not a real execution (bid/ask 5.45×5.65, transacted 5.50 = mid). [00:57][00:58]
- Cost-basis reconstruction & the 2022 4-to-1 stock split: to compare his April 2021 basis to June 2024 you must divide old strikes/prices by 4 (or multiply share counts by 4). Reported June-2024 basis on the 20-strike calls ≈ 5.6754, total premium ≈ $68.1M, tracked cost ≈ $65.7M; the ~$314K variance is commissions/fees. [01:04][01:14][01:16]
- Finding large trades via block/volume screens: total option volume (e.g. 8,460 on the 29th) is not his trade — most is small retail flow. He isolates his activity by screening for unusual blocks (~5K+, then min 1K contracts) across dates. [51:38][52:45][53:34]
- He only ever bought calls — never sold options. Across all reconstructed history he never sold a call; selling calls would be contrary to his long-biased thesis. [03:12][03:13]

### General investing / discipline
- Dip-timing trap: "people spend too much time waiting and not enough time investing." If you can't stomach a $1,000 unrealized loss on $10K, the market isn't for you — that's the nature of buy-and-hold, and waiting for a dip that may never come is an unwinnable setup. [05:26][05:54][09:39]
- Holistic approach to wealth: hold multiple asset classes; real estate gets far better tax treatment than trading, where "you are destroyed on taxes." [26:46][27:36]
- Order internalization / PFOF: firms like Citadel internalize flow because it's legal and advantageous — "playing the game as it's laid out for them." Fines (~$1M against ~$2.9B quarterly trading revenue) are too small to create any incentive to comply. [21:09][23:19][24:12]

### GME-saga narrative
- Position reconstruction (June 2024 20-strike calls, June 21 2024 expiry): the bulk (~60,000 contracts) was built 20–22 May 2024, with the 22nd the big day, plus additional blocks on later dates (e.g. one on 31 May). Chat regulars (off Putin, Vladimir, Dr Z) collaborate live to reconcile counts and a stray "at the bid" print. [29:22][31:12][40:57]
- Share position: on his return he held ~5 million shares (~4.8M net add after split adjustment) with a cash/cost basis reconstruction in progress. [01:08][01:13][01:22]
- Exercise-to-force-shorts theory: chat cites Newton's video that DFV exercised calls to force naked shorts to buy; host flags an exercise of the 16 April calls in the historical record for later study. [01:22][03:13]
- "Is he a plant?" theories dismissed: no evidence DFV has special information; his tweets come after moves, not before ("that would get caught instantly"). Host proposes a minute-level study of randomly-sampled tweet dates vs GME price to test it objectively. [02:03][02:07][02:08]
- MOASS skepticism: doubts an infinite squeeze — regulators turned off the buy button before to prevent systemic collapse; markets are supply/demand measurements, not perfect valuation machines, and won't let GME run to infinity (though they could let it run further). [02:30][02:31]

## Notable quotes
- "People spend too much time waiting and not enough time investing." [05:26]
- "He's not building units — he's creating leveraged directional exposure." [03:03]
- "If we see him play near-dated options, that probably infers he thinks an event is happening." [03:10]

## Candidate wiki links
- concepts: [[concepts/days-to-expiration]], [[concepts/delta]], [[concepts/gamma]], [[concepts/gamma-ramp]], [[concepts/leverage]], [[concepts/out-of-the-money]], [[concepts/cost-basis]], [[concepts/stock-split]], [[concepts/early-exercise]], [[concepts/deep-itm-calls]], [[concepts/position-sizing]], [[concepts/order-internalization]], [[concepts/payment-for-order-flow]], [[concepts/bid-ask-spread]], [[concepts/dollar-cost-averaging]], [[concepts/buy-and-hold]], [[concepts/risk-tolerance]], [[concepts/asset-allocation]], [[concepts/naked-short-selling]], [[concepts/short-squeeze]], [[concepts/meme-stock]], [[concepts/confirmation-bias]]
- strategies: [[strategies/long-call]], [[strategies/leaps]], [[strategies/event-driven]]
- securities: [[securities/gme]], [[securities/spy]]
- people: [[people/roaring-kitty]], [[people/richard-newton]]

## Regime / context
- This is Pt6 of the "Analyzing Roaring Kitty's Trades" series (branded "GameStop Analysis Live Ep14"), aired 2024-10-13 — roughly four months after DFV's June 2024 return and the June-expiry 20-call position that earlier parts reconstructed.
- Timeline position: prior parts reconstructed the June 2024 position; this session works backward through DFV's full posted history (Sept 2019 → 2 June 2024) to establish baseline tendencies. Host explicitly ends by saying the next session picks up at "the 2 June 24 comeback."
- Heavily community-collaborative and live: much of the runtime is real-time spreadsheet reconciliation with chat (off Putin, Vladimir, Dr Z, Newton via text). Granular figures are read aloud from auto-caption and should be treated as low-confidence; the behavioral conclusions are the durable output.
- Sits well before the later Meme Stock Watch Ep51 (2025-09-28) source, which reaches the same core finding (DFV only bought long calls, no evidence of sold options).
