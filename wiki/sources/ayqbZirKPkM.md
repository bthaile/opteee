---
type: source
title: "Agustin Lebron on Building a Trading Strategy | The Outlier Podcast"
video_id: ayqbZirKPkM
url: https://www.youtube.com/watch?v=ayqbZirKPkM
date: 2026-04-08
series: outlier-podcast
format: [education, interview]
experts: [agustin-lebron]
mentions: []
securities: [spy, xlb, xlc, xlk, xlv, xle, xlf, xli, xlp, xlu, xlv, xly]
concepts: [strategy-development, momentum, sector-rotation, backtesting, edge, profit-mechanism, trading-universe, lookback-period, composite-scoring, robustness, overfitting, drawdown, sharpe-ratio, compound-annual-growth-rate, leverage, data-quality, survivorship-bias, look-ahead-bias, process-over-outcome, risk-management, position-sizing]
strategies: [sector-rotation, momentum, long-only]
saga: none
part: null
confidence: high
---

# Agustin Lebron on Building a Trading Strategy | The Outlier Podcast

## Summary

Eric and Agustin Lebron walk through the practical process of building a systematic trading strategy from first principles. Using a sector rotation strategy based on momentum as a concrete example, they discuss how to research market effects via academic papers, define a trading universe, backtest with robustness in mind, and evaluate results using appropriate metrics. The session emphasizes that strategy development is iterative, that backtests reveal promising ideas rather than proven winners, and that retail traders must prioritize drawdown management and emotional discipline.

## Key takeaways

### Research & idea generation
- Start with well-researched market effects (e.g., momentum) rather than untested hunches [02:06–08:43]
- Use free resources like SSRN to find academic papers; read abstracts critically before diving into full papers [10:47–11:52]
- Recognize author credibility and institutional affiliation; papers from known researchers or asset managers carry different weight than master's theses [20:22–22:57]
- Read multiple papers (minimum ~10) to build familiarity; you'll recognize patterns and understand the landscape [24:51–26:27]
- Revisit earlier papers as you learn; if you suddenly understand something you misread before, that's a sign of progress [27:24–27:42]
- Older papers that are still cited have staying power; newer papers may reveal novel ideas but also risk being overfitted [28:09–29:20]

### Strategy definition & backtesting
- Define the profit mechanism first: why should this work? [35:47]
- Define the trading universe carefully; start simple (e.g., sector ETFs) to isolate the effect before adding complexity like options [35:47–36:31]
- Use a baseline (e.g., buy-and-hold S&P 500) and test incrementally; only add complexity if it beats the previous baseline [37:39–38:43]
- Lock one variable and iterate through others to answer key questions: how many holdings? how long to hold? what lookback period? [45:28–46:01]
- Prioritize robustness over peak returns; the best-looking result is often overfit [46:31–47:21]
- Test sensitivity to small changes (e.g., rebalance date shifted by one week); if results collapse, it's an artifact, not an edge [47:21–48:13]
- Use heat maps and segmented returns to visualize how parameters interact [59:06–59:30]

### Evaluation & metrics
- Sharpe ratio is contextual; a strategy that's in the market only 10% of the year may have poor Sharpe but excellent capital efficiency [51:27–52:06]
- For retail traders, prioritize maximum drawdown over Sharpe; losing too much money ends the game [52:50–53:46]
- Visualize drawdowns emotionally: if your portfolio drops 20% in two days, will you panic-sell or hold? [54:12–54:49]
- Normalize returns by matching drawdowns to a benchmark (e.g., S&P 500) to compare risk-adjusted performance; this reveals whether leverage could improve the strategy [56:43–58:07]
- Look for smooth, continuous relationships between parameters; big jumps or discontinuities signal overfitting or concentration risk [01:01:02–01:01:43]

### Concentration & edge
- As you concentrate holdings (top 1 vs. top 3 sectors), returns may improve but robustness often declines [55:50–56:43]
- If the strategy's outperformance depends entirely on one sector (e.g., tech), you're not exploiting a market inefficiency—you're making a secular bet [50:20–50:44]
- Test robustness by removing the best-performing sector and checking if the edge persists [50:20–50:44]
- Smooth parameter curves suggest genuine edge; jagged curves suggest you're fooling yourself [01:01:02–01:01:43]

### Data & implementation
- Data quality is critical and often overlooked; survivorship bias, look-ahead bias, corporate actions, and dividends can invalidate backtests [01:02:40–01:03:35]
- Don't trade the first promising backtest; start small and learn from real-world surprises [01:03:35–01:03:53]
- For new traders, time spent learning has zero opportunity cost; the goal must be enjoyment and curiosity, not immediate profitability [39:02–40:25]

## Notable quotes

> "A strategy is a fairly systematic process that takes information about the world and transforms it into actions that you might take in the world." — Agustin Lebron [02:06]

> "Most published finance trading research is crap because if it weren't crap, they would go trade it." — Agustin Lebron [21:05]

> "Everybody's got a plan till they get punched in the face. That's everything in trading." — Eric [55:06]

## Candidate wiki links

### Concepts
[[momentum]], [[sector-rotation]], [[backtesting]], [[edge]], [[profit-mechanism]], [[trading-universe]], [[lookback-period]], [[composite-scoring]], [[robustness]], [[overfitting]], [[drawdown]], [[sharpe-ratio]], [[compound-annual-growth-rate]], [[leverage]], [[data-quality]], [[survivorship-bias]], [[look-ahead-bias]], [[process-over-outcome]], [[risk-management]], [[position-sizing]], [[market-efficiency]], [[mean-reversion]]

### Strategies
[[sector-rotation]], [[momentum]], [[long-only]], [[buy-and-hold]]

### Securities
[[spy]], [[xlb]], [[xlc]], [[xlk]], [[xlv]], [[xle]], [[xlf]], [[xli]], [[xlp]], [[xlu]], [[xly]]

### People
[[eric]], [[agustin-lebron]]

## Regime / context

Recorded April 2026. This is a foundational education session on strategy development methodology, not a market-specific trade recommendation. The sector rotation example uses historical data from 2000 onward (the launch of sector ETFs) and is presented as a teaching framework, not a live strategy. The discussion emphasizes that backtests are idea-validation tools, not predictive guarantees, and that retail traders must account for data quality, emotional discipline, and drawdown tolerance before deploying any systematic approach.

## Proposed new slugs

- people: agustin-lebron — guest expert on systematic strategy development and quantitative research
