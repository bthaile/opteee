---
type: source
title: "Be Mindful Of The Service You Provide When Trading"
video_id: ckLbyp_yI88
url: https://www.youtube.com/watch?v=ckLbyp_yI88
date: 2026-02-04
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: []
concepts: [short-volatility, tail-risk, profit-mechanism, risk-management, wings, delta, moneyness]
strategies: [short-strangle, short-premium, credit-spread]
saga: null
part: null
confidence: medium
---

# Be Mindful Of The Service You Provide When Trading

## Summary

A backtested comparison of two short-premium strategies from 2020–2025 reveals the cost of adding hedges (wings) to naked short strangles. The core insight: when you sell tail risk, you are providing a service; adding a middleman (buying protective wings) compresses your profit substantially, even though both average winners and losers increase in magnitude.

## Key takeaways

- **Short strangle vs. collared strangle** [00:00–00:30]: A 30-day short strangle (10 delta, 50-point wide wings) shows higher average winners and losers than a naked short strangle, but the net profit is compressed.
- **Tail risk as a service** [00:30–00:50]: Selling tail risk (naked short premium) is a service you provide to hedgers. Once you buy wings to protect yourself, you introduce a middleman and forfeit that premium.
- **Profit compression from hedging** [00:50]: Adding protective wings forces you to widen the strikes significantly to maintain edge, but the margin is squeezed by the cost of the hedge itself.

## Notable quotes

> "If you want to buy those wings, you have to go really wide. Because when you sell those tails, think of the service you're providing. You are taking tail risk for somebody else."

> "If you add that other middleman, your profit gets absolutely compressed."

## Candidate wiki links

**concepts:** [[short-volatility]], [[tail-risk]], [[profit-mechanism]], [[risk-management]], [[delta]], [[moneyness]]

**strategies:** [[short-strangle]], [[short-premium]], [[credit-spread]]

## Regime / context

Backtest period: 2020–2025. The analysis assumes 30-day rolling entries and illustrates a fundamental trade-off in premium-selling: naked short premium captures tail-risk premium but carries unlimited downside; hedged positions reduce that premium capture but add transaction costs and complexity. The choice depends on risk tolerance and capital efficiency objectives.
