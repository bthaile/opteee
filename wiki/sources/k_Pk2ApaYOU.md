---
type: source
title: "I Tested a SPY Collar for 20 Years. Here Is What Happened."
video_id: k_Pk2ApaYOU
url: https://www.youtube.com/watch?v=k_Pk2ApaYOU
date: 2026-10-25
series: none
format: [education, analysis, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy]
concepts: [hedge, collar, downside-protection, risk-management, drawdown-management, payoff-diagram, defined-risk, risk-reward, long-put, short-call, delta, assignment, dividend, compounding, volatility, worst-year, terminal-wealth, buy-and-hold, moving-average, dollar-cost-averaging, optimization, constraint, tenor, moneyness]
strategies: [collar, protective-put, covered-call, long-put, short-call, buy-and-hold, moving-average]
saga: none
part: null
confidence: high
---

# I Tested a SPY Collar for 20 Years. Here Is What Happened.

## Summary

This video presents a 20-year backtested case study of a collar strategy applied to SPY, comparing it to buy-and-hold and a 200-day moving average approach. The collar—constructed by holding long shares, buying a 15% out-of-the-money put annually, and selling weekly 25-delta calls—reduced maximum drawdown from 46% to 17% while delivering 90% of buy-and-hold wealth (9.6% CAGR vs. 10.2%), demonstrating the risk-reward trade-off inherent in hedging. The analysis explores five families of risk reduction, evaluates hedge performance metrics, and optimizes the collar configuration within a 15% drawdown constraint.

## Key takeaways

- **Hedge definition and cost trade-off** [01:23–03:00]: A hedge reduces risk but always comes at a cost; the collar caps both downside (via long put) and upside (via short call), creating a defined-risk payoff diagram.

- **Five families of risk reduction** [04:24–05:43]: Define loss (spreads), buy a floor (protective put), fund the floor (sell calls), replace exposure (buy calls instead of shares), or hedge an entire book.

- **Collar construction rules** [10:16–11:40]: Buy ~475 DTE put at 15% OTM (member's downside tolerance); sell 25-delta calls weekly, always above purchase price, to offset put cost; rebuy shares at open if assigned.

- **Year-over-year performance** [13:31–15:18]: Collar won on drawdown in 17 of 17 out-of-sample years; won on upside in only 3 of 17 years ('07, '08, '15). Worst year: collar down 12.9% vs. buy-and-hold down 34.2% (2008).

- **Compounding and terminal wealth** [15:18–17:03]: Collar achieved 5.7× wealth vs. 6.35× for buy-and-hold over 19 years; CAGR 9.6% vs. 10.2%—90% of buy-and-hold return on a much gentler path. Outperformance during downturns matters more than annual upside.

- **P&L attribution** [18:32–20:16]: Average annual P&L: shares +10.7%, put cost −2.3%, short calls +1.0%, dividends +1.9%. Put only paid off in 2008 (+16.3% relative to account). Short calls positive in 11 of 17 years; selling above basis rule added ~2.5 points/year.

- **Optimization within constraint** [21:50–25:06]: Of 399 configurations tested, 152 stayed within 15% max drawdown. Best performer: 10% OTM put (365 DTE) + 25-delta call every 2 weeks = 9.3% return, 14.6% worst drawdown. Cheaper puts → better returns but higher drawdown; shallower call deltas → more upside but higher put cost.

- **Tenor and delta sensitivity** [23:33–25:06]: Call tenor (weekly vs. 2-week) makes ~1 point/year difference; put tenor has minimal impact; moving-average rule adds ~1 point/year but no configuration beats original return within 15% constraint.

- **Plateau principle** [25:06]: Configurations cluster around similar performance; small tweaks yield consistent results, suggesting the fundamental collar structure is robust.

- **Sleep-at-night positioning** [17:03–18:32]: Collar is for investors uncomfortable with 30%+ portfolio drawdowns; it sacrifices upside to dampen downside, making it a psychological and risk-tolerance tool, not an efficiency maximizer.

## Notable quotes

> "You do not need to outperform the market to the upside every year to do well. If you outperform the market during really bad years, notice how long it took buy and hold to catch up to the collar that had dampened this."

> "The point of a collar, especially if it's 15% below the market, the overwhelming majority of the time it's not going to get hit. That's the point of it. It's infrequent at that level."

## Candidate wiki links

**concepts:** [[hedge]], [[collar]], [[downside-protection]], [[risk-management]], [[drawdown-management]], [[payoff-diagram]], [[defined-risk]], [[risk-reward]], [[long-put]], [[short-call]], [[delta]], [[assignment]], [[dividend]], [[compounding]], [[volatility]], [[worst-year]], [[terminal-wealth]], [[buy-and-hold]], [[moving-average]], [[dollar-cost-averaging]], [[optimization]], [[constraint]], [[tenor]], [[moneyness]], [[protective-put]], [[covered-call]], [[long-premium]], [[short-premium]], [[upside-capped]], [[downside-protection]], [[drawdown-recovery]], [[max-drawdown]], [[cagr]], [[wealth-creation]]

**strategies:** [[collar]], [[protective-put]], [[covered-call]], [[long-put]], [[short-call]], [[buy-and-hold]], [[moving-average]], [[portfolio-hedging]], [[risk-first]], [[defined-risk]]

**securities:** [[spy]]

**people:** [[eric]]

## Regime / context

**Date:** 2026-10-25. **Backtest period:** 2007–2025 (19 years). **Calibration years:** 2022, 2025 (member's paper-trading period). **Out-of-sample:** remaining 17 years. The analysis uses real market data from the OTOC (Outlier Trading Operations Center) and compares collar performance to buy-and-hold and 200-day moving average strategies. The 2008 financial crisis and 2020 COVID crash are key stress-test periods where the collar's downside protection is most evident. The collar is positioned as a risk-reduction tool for investors in the later stages of wealth accumulation, prioritizing drawdown minimization over absolute returns.
