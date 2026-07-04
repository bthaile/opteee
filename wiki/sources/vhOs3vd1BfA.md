---
type: source
title: "The Problem with Trading the Wheel for Income"
video_id: vhOs3vd1BfA
url: https://www.youtube.com/watch?v=vhOs3vd1BfA
date: 2025-03-09
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy]
concepts: [cash-secured-put, assignment, covered-call, premium, basis, position-sizing, risk-management, mark-to-market, realized-vs-unrealized-pnl, capital-efficiency, emotional-discipline, market-regimes]
strategies: [the-wheel, covered-strangle, short-put, covered-call]
saga: null
part: null
confidence: high
---

# The Problem with Trading the Wheel for Income

## Summary

The wheel strategy—selling cash-secured puts, taking assignment, and selling covered calls—sounds attractive but has critical limitations when used for income generation, especially during prolonged downtrends. This walkthrough demonstrates a live backtest on SPY from January–June 2022, showing how premium collection dries up as the underlying falls, leaving traders with minimal income and significant unrealized losses. The key insight: income traders must buffer 12–24 months of required income and avoid relying on current-period premium to meet expenses.

## Key takeaways

- **The wheel's appeal vs. reality** [00:00–01:00]: The strategy sounds like a win-win (premium on entry, premium on exit, appreciation), but requires eyes-wide-open risk management during downturns.

- **Live backtest setup** [02:03–03:17]: Starting with $100k on SPY at ~4575, sell 2× 30-delta puts at 443 strike, collect $1,428 premium (1.6% ROIC for 30 days, ~19% annualized).

- **First cycle: assignment and call sale** [04:35–05:47]: Puts assigned at 443; stock falls to 435 by expiration. Sell 2× 30-delta calls at 449 strike, collect $455 premium. Position now underwater ~$1,600 on shares but profitable overall due to premium.

- **Subsequent cycles show premium collapse** [07:05–10:43]: As market falls from 435 → 397 → 387, premium available on calls shrinks dramatically. By May, selling at-the-money calls yields only 14 cents per contract; selling above basis yields near-zero premium.

- **The income problem in downtrends** [12:05–14:09]: When stock is down 15%, available premium is insufficient for meaningful income. Trader must choose: sell below basis (risky), accept minimal premium, or extend duration (reduces flexibility).

- **Scaling in to reduce basis** [15:22–16:34]: Adding 30 shares at 364 reduces basis from 443 to 432, but premium on 432-strike calls is still only ~10 cents—not viable for income.

- **Year-to-date performance** [16:34–17:44]: By mid-June 2022 (6 months in), position is down ~12% despite wheel activity. Premium collected ($26 on last calls) is negligible relative to unrealized loss.

- **Critical rule for income traders** [17:44–18:50]: Do not use current-month or current-year premium for living expenses. Buffer at least 12 months of required income (preferably 24 months) so you can absorb prolonged downturns without forced liquidation or bad decisions.

- **Alternative: covered strangle** [00:57]: Eric prefers covered strangles (selling both puts and calls as satellites around the underlying) because they offer better adjustment mechanics and capital efficiency than the wheel in sideways/down markets.

## Notable quotes

> "If you go into this with such a skewed perception and then you start seeing things going awry, that's typically when our strategies unravel and we make bad decisions."

> "The biggest favor to yourself is don't use the income for the same month or even the same year. Pad at least one full year of your required income—that's padded, meaning you give it a buffer."

## Candidate wiki links

**concepts:** [[cash-secured-put]], [[assignment]], [[covered-call]], [[premium]], [[basis]], [[position-sizing]], [[risk-management]], [[mark-to-market]], [[realized-vs-unrealized-pnl]], [[capital-efficiency]], [[emotional-discipline]], [[market-regimes]]

**strategies:** [[the-wheel]], [[covered-strangle]], [[short-put]], [[covered-call]]

**securities:** [[spy]]

## Regime / context

This backtest spans January–June 2022, a period of significant market decline (SPY fell ~20% from ~4575 to ~3640). The analysis is historically grounded and illustrates how the wheel's income-generation capacity collapses in bear markets. The key lesson applies across all market regimes: income strategies require a multi-year buffer to survive drawdowns without forced liquidation.
