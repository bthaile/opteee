---
type: source
title: "The Wheel vs Covered Strangle Strategy Comparison"
video_id: qufmMwkEKho
url: https://www.youtube.com/watch?v=qufmMwkEKho
date: 2022-02-15
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [iwm]
concepts: [assignment, basis-reduction, capital-efficiency, covered-call, delta-selection, opportunity-cost, position-sizing, profit-taking, risk-management, theta-decay]
strategies: [covered-call, covered-strangle, short-put, the-wheel]
saga: null
part: null
confidence: high
---

# The Wheel vs Covered Strangle Strategy Comparison

## Summary

Eric compares two income-generating strategies: the wheel (sell put → get assigned → sell covered calls until assignment) and the covered strangle (sell put → get assigned → sell covered calls *and* continue selling additional puts simultaneously). Using a live backtested example on IWM from December 2015 to May 2016, he demonstrates that the covered strangle generated ~3% ROIC versus ~2.63% for the wheel, primarily because it allows more active profit-taking and basis reduction through layered short puts.

## Key takeaways

- **Primary structural difference** [00:22]: Both strategies start with a cash-secured put. The wheel then sells only covered calls against assigned shares; the covered strangle sells covered calls *and* continues deploying additional short puts, allowing more capital efficiency and activity.

- **Why Eric prefers covered strangle** [01:13]: It keeps the trader "more sensitive to price" and enables more frequent trades and profit realization. The wheel ties up capital in a single covered-call position once assigned.

- **Backtested example setup** [02:06]: IWM from December 2, 2015 to May 16, 2016. Eric deliberately chose a period with a significant drawdown to illustrate real risk management, not just upside scenarios.

- **Results comparison** [02:46]: Covered strangle: $952 P&L (~3% ROIC on $30k account). Wheel: $788 P&L (~2.63% ROIC). Note: the wheel comparison is conservative because the study ended early; it would have had additional open puts.

- **Initial trade sizing** [04:27]: Covered strangle: 1 lot of 116 puts (Jan 16 expiry, $1.38 credit). Wheel: 2 lots to match capital deployment, since the wheel doesn't plan to add more puts later.

- **First assignment and basis management** [06:44]: After assignment on Jan 9, the covered strangle side added a second short put (Feb 26 100 puts, $2.50 credit) to reduce basis from 116 to 108 if assigned again—a key advantage over the wheel.

- **Covered call timing and opportunity cost** [12:36]: On March 21, IWM at 109, the 116 calls offered only $0.51 (60 DTE). Eric declined to sell because the premium was insufficient relative to opportunity cost. The wheel would be forced to hold stock with no income; the covered strangle continues collecting put premiums.

- **Layered put management** [15:49]: By May 11, the covered strangle had realized $568 from three rounds of short puts, each lowering potential basis. The wheel had only realized $276 from two puts and was waiting for a covered-call opportunity.

- **Short call entry criteria** [17:29]: Eric sold 30-June 118 calls for $0.58 on May 9 (IWM at 117) because it offered $2 of upside room plus $58 premium—better than selling at-the-money for $0.50 with zero stock profit.

- **Bear market advantage** [20:09]: Covered strangle excels in prolonged downturns (typically ~290 days) because it allows continuous basis reduction and profit realization, whereas the wheel is passive once assigned.

- **Wheel optimization caveat** [19:49]: The wheel can be partially optimized by selling only one covered call and leaving shares unhedged for upside, but this sacrifices the income-generation edge.

## Notable quotes

> "The covered strangle allows us to remain a little more sensitive to price. It also allows us to be more active and get more trades on to realize more profits." [01:13]

> "Bear markets or when we crash tend to last for a pretty long period of time—something like 290 days. They allow me to stay more active, reduce my basis more effectively." [20:09]

## Candidate wiki links

**Strategies:**
- [[covered-call]]
- [[covered-strangle]]
- [[short-put]]
- [[the-wheel]]

**Concepts:**
- [[assignment]]
- [[basis-reduction]]
- [[capital-efficiency]]
- [[delta-selection]]
- [[opportunity-cost]]
- [[position-sizing]]
- [[profit-taking]]
- [[theta-decay]]

**Securities:**
- [[iwm]]

**People:**
- [[eric]]

## Regime / context

Backtested period: December 2, 2015 – May 16, 2016 (IWM). This was a volatile period with a significant drawdown in early January, making it a realistic test of downside management. The study was intentionally truncated to keep runtime manageable; the wheel would have had additional open puts if allowed to run to full neutralization. All numeric P&L figures are approximate and reflect the specific market conditions of that window.
