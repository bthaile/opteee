---
type: source
title: "Delta as Probability"
video_id: mRnYJOmu_BM
url: https://www.youtube.com/watch?v=mRnYJOmu_BM
date: 2025-06-03
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spy, tsla]
concepts: [delta, probability-of-touch, implied-volatility, moneyness, days-to-expiration]
strategies: []
saga: null
part: null
confidence: high
---

# Delta as Probability

## Summary

Delta is commonly used as a rough proxy for probability of finishing in the money at expiration, but this approximation breaks down under two key conditions: longer time to expiration and higher implied volatility. The video demonstrates this breakdown using SPY and Tesla options, showing that actual calculated probability can diverge significantly from delta, especially in volatile underlyings.

## Key takeaways

- **Delta ≠ probability of ITM**: A 30-delta option does not always have a 30% probability of finishing ITM; the relationship is approximate and degrades under specific conditions. [00:00]
- **Liquidity and volatility matter**: SPY (highly liquid, lower volatility) shows delta as a reasonable approximation at 39 DTE (30 delta → 28.14% actual probability), but the gap widens with duration. [00:00]
- **Duration effect**: At 249 DTE on SPY, a 30-delta option shows only 25% actual probability vs. the 29–30% delta suggests—a 4–5 point divergence. [00:24]
- **Volatility amplifies the error**: Tesla, with higher implied volatility, shows much larger discrepancies: 30 delta at 39 DTE yields only 23.7% actual probability (6.3 point gap). [01:12]
- **Extreme divergence at longer dates**: Tesla at 249 DTE (Jan 2026) shows a 30-delta option with ~15% actual probability—roughly half the delta value. [01:37]
- **Two drivers of breakdown**: Volatility and duration are the primary factors that cause delta to diverge from true probability of touch. [01:37]
- **Use separate calculation**: A dedicated probability-of-ITM calculation is more accurate than relying on delta as a proxy. [01:59]

## Notable quotes

> "If you go further out in time, the relationship starts to break down more." [00:48]

> "There are two things that skew using delta as the probability. Volatility is one. Second is duration." [01:37]

## Candidate wiki links

**Concepts:**
- [[delta]]
- [[probability-of-touch]]
- [[implied-volatility]]
- [[moneyness]]
- [[days-to-expiration]]

**Securities:**
- [[spy]]
- [[tsla]]

## Regime / context

Recorded 2025-06-03. The analysis uses current option chains and is evergreen in its mechanics, though specific option prices and probabilities are dated to the recording. The video references a separate educational resource on the dedicated probability-of-ITM calculation (not included in this transcript).
