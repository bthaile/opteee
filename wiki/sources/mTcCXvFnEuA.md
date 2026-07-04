---
type: source
title: "Ratio Covered Call Option Strategy"
video_id: mTcCXvFnEuA
url: https://www.youtube.com/watch?v=mTcCXvFnEuA
date: 2023-04-12
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [tsla]
concepts: [covered-call, delta, delta-neutral, capped-upside, unlimited-upside, premium, capital-efficiency, risk-management, position-sizing, cost-basis, profit-taking, assignment, rolling-options, trading-plan]
strategies: [covered-call, ratio-call-diagonal, covered-strangle]
saga: null
part: null
confidence: high
---

# Ratio Covered Call Option Strategy

## Summary

The ratio covered call is a modified covered call that maintains uncapped upside potential by selling fewer calls than the number of shares held, creating a net long delta position. While it collects less premium upfront than a standard covered call, it allows traders to participate in significant rallies while still generating income, making it superior for bullish scenarios where large moves are expected.

## Key takeaways

- **Standard covered call mechanics** [00:22–01:03]: Long 200 shares + short 2 calls = 200 long deltas vs. 200 short deltas = capped profit at strike + premium.
- **Ratio covered call structure** [01:32–02:29]: Long 200 shares + short 1 call = 200 long deltas vs. 100 short deltas = 100 uncovered deltas = unlimited upside potential.
- **Core tradeoff** [02:29–02:54]: Ratio covered calls collect less premium upfront (less hedge if the move doesn't materialize) but unlock significantly greater profit potential on rallies.
- **Management flow** [03:14–04:47]: After assignment of short calls, you can roll the position, allow assignment (losing 100 shares), or flatten entirely depending on your original trade hypothesis.
- **Strike selection process** [10:12–11:41]: Balance between collecting premium upfront and preserving capital gains potential; selling closer to cost basis collects more premium but caps upside; selling further OTM preserves upside but collects less.
- **Expiration and ratio laddering** [09:09–09:49]: Prefer selling calls week-over-week rather than all at once to avoid concentration risk; maintain at least 100 shares uncovered to preserve the ratio structure.
- **Live example comparison** [06:23–12:35]: Standard covered call on 500 shares of Tesla (5 short calls) yielded ~$10,950 P&L in a strong rally; ratio covered call (4 short calls) yielded ~$17,125 P&L on the same move, demonstrating the upside capture advantage.

## Notable quotes

> "This is the scenario I'm attempting to expose myself to" — on why the ratio covered call is preferred in bullish environments [12:16].

## Candidate wiki links

**Concepts:** [[covered-call]], [[delta]], [[delta-neutral]], [[capped-upside]], [[premium]], [[capital-efficiency]], [[cost-basis]], [[assignment]], [[rolling-options]], [[position-sizing]], [[profit-taking]]

**Strategies:** [[covered-call]], [[covered-strangle]], [[ratio-call-diagonal]]

**Securities:** [[tsla]]

## Regime / context

Recorded January 2023 in a bullish market environment. The example uses historical backtesting on thinkorswim to compare covered call vs. ratio covered call performance during a strong rally. This strategy is presented as a component of the broader [[covered-strangle]] framework and is most advantageous when traders expect significant upside moves.
