---
type: source
title: "0DTE Option Strategy Comparison"
video_id: z9YbIRtXbrg
url: https://www.youtube.com/watch?v=z9YbIRtXbrg
date: 2024-01-13
series: none
format: [education, analysis, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spx]
concepts: [zero-dte, volatility-risk-premium, implied-volatility, realized-volatility, short-volatility, delta, moneyness, overfitting, market-regimes, theta-decay]
strategies: [short-straddle, short-strangle, short-iron-condor, iron-fly, zero-dte]
saga: null
part: null
confidence: high
---

# 0DTE Option Strategy Comparison

## Summary

Eric compares five years of backtested zero-DTE option structures (short straddle, short strangle, short iron condor, and iron fly) on SPX, analyzing profitability across different delta strikes and wing widths. The analysis reveals that the 15–20 delta strangle without wings performed best overall, but results vary significantly by volatility regime; he emphasizes the critical risk of overfitting to historical data and the importance of adapting to changing market conditions.

## Key takeaways

- **Why trade zero-DTE:** The goal is to capture variance risk premium—the tendency for implied volatility to overshoot realized volatility—not to "get rich quick" [01:00–01:40].
- **Core structures tested:** Short straddle (same strike, unlimited loss both sides), short strangle (wider OTM, lower win rate but higher average win), short iron condor (defined loss via wings), and iron fly (defined loss on straddle) [02:39–04:31].
- **5-year backtest winner (2018–2023, 10 a.m. entry, no profit/loss management, SPX):** The 20 delta strangle with no wings generated ~$37,000 profit; the 15 delta strangle was close behind with lower max loss (~$11,000 vs. $9,400) [05:17–05:37].
- **Volatility regime matters:** In high-volatility periods (e.g., 2019–early 2020), further OTM strikes (15–20 delta) outperformed closer-to-money strikes (30–40 delta) because realized volatility frequently exceeded implied volatility [05:37–06:38].
- **With wings:** The 15 delta short / 10 delta long strangle and 20 delta short / 10 delta long strangle both yielded ~$36–37k profit, but the latter had lower max loss (9,400 vs. 11,000) and higher average loss per trade (2,700 vs. 2,200)—choose based on risk tolerance [07:48–08:15].
- **Iron fly caution:** Only the 5-delta-wide iron fly was profitable, indicating IV was still tracking below realized volatility too often; the wings reduced outsized losses but capped upside [09:28–09:54].
- **Overfitting risk:** Cherry-picking the best historical combination and expecting it to persist forward is dangerous; Eric pivoted mid-year when 50-delta straddles stopped outperforming in lower-volatility regimes [08:31–09:08].
- **Next steps:** Viewer feedback will drive follow-up videos on year-over-year performance, optimal entry times, and alternative timeframes (not just zero-DTE) [09:54–10:39].

## Notable quotes

> "Most people lose money doing these—that's what it comes down to." [01:21]

> "The goal at least for me is to make money, so I will flow between things as I need to make the most money." [03:54]

> "You have to be careful when you look at back tests for overfitting—when you just cherry-pick the best possible things and then expect that to be the outcome going forward." [09:08]

## Candidate wiki links

**concepts:** [[zero-dte]], [[volatility-risk-premium]], [[implied-volatility]], [[realized-volatility]], [[short-volatility]], [[delta]], [[moneyness]], [[theta-decay]], [[overfitting]], [[market-regimes]], [[variance-risk-premium]]

**strategies:** [[short-straddle]], [[short-strangle]], [[short-iron-condor]], [[iron-fly]]

**securities:** [[spx]]

**people:** [[eric]]

## Regime / context

Backtest period: 2018–2023 (SPX, cash-settled European-style options, 10 a.m. entry, held to expiration, no active profit/loss management). Results are sensitive to volatility regime; the high-volatility 2019–early 2020 period (COVID crash) shows outsized moves that favor wider OTM strikes. Eric notes mid-2024 pivot away from 50-delta straddles due to regime shift into lower volatility, illustrating the importance of live monitoring and avoiding overfitting to historical backtests.
