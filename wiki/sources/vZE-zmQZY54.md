---
type: source
title: "Don't Trade Until You Master This Sizing Formula"
video_id: vZE-zmQZY54
url: https://www.youtube.com/watch?v=vZE-zmQZY54
date: 2026-11-01
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, spx, amazon]
concepts: [position-sizing, risk-management, structural-risk, managed-risk, portfolio-management, strategy-level-sizing, trade-level-sizing, kelly-criterion, stress-testing, margin-requirement, gap-risk, heat-analysis, correlation, drawdown, circuit-breaker, clustering, variance-premium, trend-following, undefined-risk, defined-risk]
strategies: [covered-call, short-strangle, short-put, premium-selling, trend-following, position-sizing, risk-budgeting]
saga: null
part: null
confidence: high
---

# Don't Trade Until You Master This Sizing Formula

## Summary

Position sizing is the only fully controllable lever in options trading and has a massive impact on strategy performance. This video breaks down a three-level framework—portfolio, strategy, and trade—for managing risk through structural vs. managed risk, stress testing, and capital allocation. The same edge can produce vastly different outcomes depending on how positions are sized across these nested levels.

## Key takeaways

- **Why sizing matters** [00:00–01:05]: The same strategy with identical edge produces dramatically different equity curves when sized at 1×, 2×, and 4× base levels; sizing is the primary performance lever you control.

- **Structural vs. managed risk** [02:30–04:58]: Structural risk is the full cost to put on a trade (e.g., $1 for a put); managed risk is what you actually expect to lose before exiting (e.g., $0.48 if you manage at 2× credit). Knowing both lets you trade larger sizes while staying within capital constraints.

- **Gap risk and hedging** [06:07–07:22]: Naked strategies (short strangles) can gap past your management level; size conservatively for high-gap instruments, or hedge with correlated instruments (e.g., E-minis for SPX) to offset gap risk.

- **Margin requirements are not risk** [08:42–09:51]: Broker margin calls reflect capital set-aside, not actual loss potential. You must survive margin expansion when volatility rises and the underlying moves against you; don't base sizing solely on worst-case scenarios.

- **Portfolio-level risk adjustment** [11:08–12:20]: Covered calls and short strangles have vastly different stress profiles; a naive 50/50 split is actually ~77% covered call / 23% short strangle when risk-adjusted. Correlation matters: bonds and equities are now ~0.4–0.5 correlated, breaking traditional hedges.

- **Independent bets and correlation** [12:20–13:26]: Selling puts in SPY and Amazon looks like two trades but is highly correlated; use "heat" analysis to stress-test the entire book in a bad scenario (all positions underwater simultaneously) to verify your size is survivable.

- **Strategy-level clustering** [14:41–15:59]: Premium sellers win frequently with small wins but suffer large losses; trend followers have many small losses and infrequent large wins. Plan for loss clustering, not just average loss size. A 95% confidence interval on clustered losses guides your budget.

- **Kelly criterion and fractional Kelly** [15:59–17:18]: Kelly gives optimal growth per trade but is a ceiling, not a target. Half-Kelly or quarter-Kelly preserves most growth while cutting variance significantly. Calm samples overstate edge; rare events (COVID) happen rarely but must be accounted for.

- **Trade-level execution** [17:18–20:00]: Risk per trade is dynamic—adjustments change your risk profile. Calculate contracts from risk budget (e.g., $5,814 budget ÷ $1,820 per contract = 3.19 → 3 contracts). Verify fit within strategy heat cap and portfolio heat cap before entry.

- **Worked example: $500k account** [18:34–20:00]: 25% max drawdown tolerance split into premium seller (75k, 12.9% bad-run loss) and trend follower (50k, 23.2% bad-run loss). Each strategy gets a capital allocation; each trade gets a contract count derived from stress loss and risk budget. Use AI/API tools to automate broker data ingestion and sizing verification.

- **Common mistakes** [20:00–21:11]: Portfolio level—trades go on randomly without tracking correlation; strategy level—sizing off average loss ignores streaks; trade level—ignoring stress loss for undefined-risk positions and not accounting for dynamic risk from adjustments.

## Notable quotes

> "The way that you size it has a massive impact on your performance. That's why sizing is so important."

> "Risk management and sizing is really the only thing you can fully control as an options trader."

> "If you size your option positions off of the worst-case scenario in every single one of them, you'll never put any risk on."

## Candidate wiki links

**concepts:** [[position-sizing]], [[risk-management]], [[structural-risk]], [[managed-risk]], [[portfolio-management]], [[kelly-criterion]], [[stress-testing]], [[margin-requirement]], [[gap-risk]], [[heat-analysis]], [[correlation]], [[drawdown]], [[circuit-breaker]], [[clustering]], [[variance-premium]], [[undefined-risk]], [[defined-risk]], [[capital-allocation]], [[portfolio-hedging]], [[dynamic-risk]]

**strategies:** [[covered-call]], [[short-strangle]], [[short-put]], [[premium-selling]], [[trend-following]], [[risk-budgeting]], [[position-sizing]]

**securities:** [[spy]], [[spx]], [[amazon]]

**people:** [[eric]]

## Regime / context

Recorded November 2026. Reflects current market conditions (bonds–equities correlation ~0.4–0.5). Framework is regime-agnostic and applies across bull/bear/sideways markets. Emphasis on stress-testing and clustering is particularly relevant in high-volatility regimes where gap risk and margin expansion are material.
