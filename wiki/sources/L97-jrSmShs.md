---
type: source
title: "Live Strategy Testing | Options Trading for Beginners"
video_id: L97-jrSmShs
url: https://www.youtube.com/watch?v=L97-jrSmShs
date: 2026-05-16
series: beginner-lab
format: [education, live, strategy-breakdown]
experts: [eric]
mentions: []
securities: [vrtx, onpl, tr, wgs, fly, wmb, crs, prig, evn, lumn, mstr, tem, lit, ala, ba, ana, cpng, ea, lc, id, sm, ci, ups, ta, ae, s, oxy, duo, aapl, pfe, shop, ccj, rig]
concepts: [profit-mechanism, outlier-strategy-process, signal-identification, structure-selection, hypothesis-testing, universe-filtering, rule-set-definition, backtesting, paper-trading, position-sizing, volatility-risk-premium, implied-volatility, realized-volatility, delta, theta-decay, iv-crush, earnings-move, expected-move, trading-log, pnl-attribution]
strategies: [short-straddle, short-volatility, earnings-vol-play]
saga: none
part: null
confidence: high
---

# Live Strategy Testing | Options Trading for Beginners

## Summary

Eric walks through the foundational framework for testing options trading strategies, using a short-volatility earnings play as a live case study. The session covers the Outlier Strategy Process—identifying profit mechanisms, designing signals, selecting structures, and building rules—before executing a manual paper-trading test across eight earnings positions to validate the concept.

## Key takeaways

- **Start with profit mechanism, not structure** [07:17] — Most new traders jump directly to choosing option structures (spreads, calendars) before understanding *why* they'd profit. Reverse this: identify the edge first (e.g., volatility risk premium), then select the vehicle.

- **The Outlier Strategy Process has four layers** [05:31–08:13]:
  1. Identify the profit mechanism (e.g., implied vol trending over realized vol through earnings)
  2. Design signals to measure and capture it
  3. Explore different structures (straddles, strangles, etc.)
  4. Build the complete strategy with rules

- **Source profit mechanisms from research or observation** [08:51–09:44] — Beginners should anchor to peer-reviewed research (SSRN) rather than untested hunches, to avoid confusing a broken testing process with a non-existent edge.

- **Define your universe before testing** [14:59–15:56] — Filter for stocks with upcoming earnings, liquid options (at least 5,000 OI ideally), and sufficient underlying volume (250k+ daily). This prevents wasting time on illiquid names.

- **Write explicit rules before you trade** [16:19–18:42] — Entry: 10–15 min before close, sell nearest-DTE short straddle at-the-money. Hold through earnings. Exit: next trading day, last 30–60 min. Specificity prevents discretion creep.

- **Track delta, premium, and IV on entry and exit** [31:27–32:03] — Log short call delta, premium, IV; short put delta, premium, IV. This reveals whether you're actually capturing the intended effect (IV crush, theta decay) or just getting lucky.

- **Normalize position size by underlying price** [37:26–37:52] — Avoid defaulting to one lot per trade; size so that each position represents roughly equal notional risk. Use the highest-priced underlying as a reference.

- **One day of results is not a sample** [01:00:35–01:03:46] — The manual test showed 6 wins, 2 losses, +$4,224 net on eight trades. This is a *first pass*, not validation. Test at least 8–12 quarters of earnings (ideally 20–24) before drawing conclusions.

- **Use APIs and data tools to scale testing** [01:01:43–01:02:27] — Manual hand-jamming is educational but inefficient. Leverage ORATS or similar for bulk options data; Python/R for automation. Stock data is free; options data requires a subscription.

- **Ask filtering questions as you test** [01:04:54] — While reviewing results, pose hypotheses: "Can I filter by IV rank, earnings surprise, sector, or time-to-expiration to improve win rate or average profit?"

## Notable quotes

> "The trick here is to learn how to identify and isolate the profit mechanism first and then do the other stuff." [07:45]

> "If you don't learn to find some type of joy in this then this trading in general will be really hard work." [53:22]

## Candidate wiki links

**concepts:** [[profit-mechanism]], [[outlier-strategy-process]], [[hypothesis-testing]], [[backtesting]], [[paper-trading]], [[position-sizing]], [[volatility-risk-premium]], [[implied-volatility]], [[realized-volatility]], [[delta]], [[theta-decay]], [[iv-crush]], [[earnings-move]], [[trading-log]], [[pnl-attribution]], [[signal-identification]], [[structure-selection]], [[rule-set-definition]], [[universe-filtering]]

**strategies:** [[short-straddle]], [[short-volatility]], [[earnings-vol-play]]

**securities:** [[vrtx]], [[onpl]], [[duo]], [[pfe]], [[shop]], [[ccj]], [[rig]], [[spy]]

**people:** [[eric]]

## Regime / context

Recorded 2026-05-16 during live earnings season (late April–early May). The manual test covers one trading day (May 4–5, 2026) across eight earnings positions. Eric notes this is the first installment of a multi-part series; a follow-up covering a full earnings week is planned for the next day. Future videos will extend the framework into Python/R-based backtesting using ORATS API.
