---
type: source
title: "Measuring Risk Adjusted Returns for Short Puts"
video_id: KlHlEa4t-fU
url: https://www.youtube.com/watch?v=KlHlEa4t-fU
date: 2025-10-19
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, qqq, upro, sso]
concepts: [return-on-invested-capital, implied-volatility, risk-management, position-sizing, volatility-risk-premium, margin-requirement, capital-efficiency]
strategies: [short-put]
saga: null
part: null
confidence: high
---

# Measuring Risk Adjusted Returns for Short Puts

## Summary

This video teaches traders how to compare short-put opportunities across different underlyings by calculating risk-adjusted returns normalized for implied volatility, rather than simply chasing the highest nominal premium. The core metric divides return on invested capital (or return on risk) by the option's implied volatility to produce a comparable unit of return per unit of volatility exposure, enabling better position selection and sizing decisions.

## Key takeaways

- **The habit to break** [00:00]: Most traders select short puts based solely on which credit is largest; this ignores the risk profile and volatility environment of each underlying.

- **Return on invested capital (ROIC)** [01:16]: Premium ÷ margin requirement. For a $856 premium on $6,859 margin (portfolio margin), this yields ~12.5% return over the trade duration, or ~105% annualized—but this is not repeatable and depends on favorable margin treatment.

- **Cash-secured return** [03:51]: Premium ÷ cash requirement. The same $856 premium on $64,900 cash requirement yields 1.3% return over duration, or ~5.6% annualized—a more realistic baseline for most traders.

- **Implied-volatility-adjusted return** [05:06]: Divide your return metric by the option's implied volatility (expressed as a decimal, annualized by multiplying duration ÷ 252 trading days). This produces a dimensionless ratio: return per unit of volatility. Use this to compare across underlyings.

- **Comparison: SPY vs. QQQ** [06:20]: Even though QQQ shows higher volatility (20.78% vs. lower) and higher premium, when normalized for IV, both offer nearly identical risk-adjusted returns—requiring a third decimal place to distinguish them.

- **Comparison: UPRO vs. SSO** [07:34]: UPRO (3× levered S&P) has 26.7% higher IV than SSO (2× levered), yet offers 30.77% higher premium—indicating a slight excess risk premium that may justify a smaller position in UPRO over SSO.

- **Building the calculator** [06:20]: Create a simple Google Sheets template with green-shaded input cells (premium, IV, duration, margin/cash requirement) and formula cells below. Compare as many underlyings as needed in parallel columns.

- **Normalization matters** [05:06]: Use 252 trading days (or 365 calendar days consistently) to annualize volatility; use the option's implied volatility rather than underlying or term volatility for precision.

## Notable quotes

> "Most people that are selling short puts are really just focusing on which one gives them the highest credit, the largest number that fits in their account."

> "This number literally just means those are the units of return that you're getting per unit of volatility, of implied volatility in the option. So this number itself doesn't really mean anything. It's not like some of these are good, some of them are bad. This is more used as a comparison metric."

## Candidate wiki links

**concepts:** [[return-on-invested-capital]], [[implied-volatility]], [[risk-management]], [[position-sizing]], [[volatility-risk-premium]], [[margin-requirement]], [[capital-efficiency]], [[annualized-return]]

**strategies:** [[short-put]]

**securities:** [[spy]], [[qqq]], [[upro]], [[sso]]

## Regime / context

Recorded 2025-10-19. The examples use current market conditions (SPY, QQQ, UPRO, SSO pricing and IV levels as of that date). The methodology is evergreen and applies across market regimes; the specific numeric outputs will vary with volatility environment and margin availability. Portfolio margin treatment (6.8% requirement) is not available to all traders; cash-secured returns provide a more universal baseline.
