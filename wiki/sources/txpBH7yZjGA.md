---
type: source
title: "Been using ChatGPT to help with options — it's kinda blowing my mind"
video_id: txpBH7yZjGA
url: https://www.youtube.com/watch?v=txpBH7yZjGA
date: 2025-05-20
series: none
format: [education, analysis]
experts: [eric]
mentions: []
securities: [spx, pltr]
concepts: [ai-assisted-trading, greeks, implied-volatility, delta, theta-decay, profit-mechanism, market-effects, price-action, technical-analysis, backtesting, statistical-significance, context-window-management, prompt-engineering, large-language-model]
strategies: []
saga: null
part: null
confidence: high
---

# Been using ChatGPT to help with options — it's kinda blowing my mind

## Summary

This video explores practical and cautionary applications of ChatGPT and large language models in retail options trading. Eric walks through real examples of how traders use AI for options math, chain analysis, and chart interpretation, then identifies critical gaps (linear Greek approximations, hallucinated data, overconfidence) and provides a structured set of prompts for learning, research, and analysis that maximize AI's utility while maintaining trader accountability.

## Key takeaways

- **AI as learning tool, not replacement** [01:16] — ChatGPT should teach you *how* to calculate Greeks and analyze setups, not replace your responsibility to do the work yourself. Leaning on it to avoid effort perpetuates a dangerous gap in trader competence.

- **Greeks are linearized in ChatGPT** [01:16] — The model applies linear movements to Greeks (delta, theta, gamma) when you describe multi-day scenarios. Real options exhibit nonlinear behavior; this simplification can mislead serious traders.

- **ChatGPT will confidently hallucinate** [03:42] — The model will read an options chain and claim "bullish accumulation" at a 95 call with 7 contracts of volume, or "heavy put volume" at a 90 strike with 1 contract. It sounds confident but is factually wrong; you must fact-check every claim.

- **Implied volatility forecasting is not AI's edge** [04:49] — ChatGPT cannot identify "overpriced premiums" because the only unknown in option pricing is IV (implied volatility). Unless the model forecasts IV better than the market consensus, it cannot help you spot mispricings. Institutional AI already prices IV; retail cannot beat that.

- **Chart analysis and technical prompts are useful** [07:05] — Feeding ChatGPT candlestick charts, Bollinger Bands, EMAs, and volume breakdowns yields practical analysis that can help you decide whether to wait or enter. You can even ask it to pull charts directly without uploading screenshots.

- **Three-bucket prompt framework** [08:05] — Organize AI queries into: (1) **Learning** (e.g., "Give me 25 questions about Greeks"), (2) **Research** (e.g., "Identify market effects and inefficiencies for an options trader"), and (3) **Analysis** (e.g., "Run a t-test on this 5-minute SPX return data").

- **Quiz generation for self-assessment** [09:03] — Ask ChatGPT to build a quiz on a concept you've learned, answer it, then request an answer key. This closes the feedback loop and validates your understanding.

- **Profit mechanisms and market effects** [11:16] — Use AI to brainstorm market inefficiencies and profit mechanisms (dealer gamma, liquidity fades, risk premia) relevant to options, then double-click into each one for deeper research.

- **Data analysis and statistical validation** [13:27] — Upload historical 5-minute price data and ask ChatGPT to compute average returns by interval, compare recent samples to historical baselines, and run t-tests to determine statistical significance. This validates anecdotal observations with rigor.

- **Fact-check all outputs** [16:42] — ChatGPT will confidently state false data (e.g., Palantir's price as $25 when it is $117). Always verify numbers, prices, and claims independently before acting on them.

- **Context and specificity matter** [12:23] — Vague prompts ("What are market effects?") yield generic, useless answers. Specifying your role ("I'm an options trader") and constraints dramatically improves output relevance.

## Notable quotes

> "It is completely cool that a model can do this, but if this is the end result, don't feel like doing this is a massive problem because your job as a trader is literally to do this." [01:16]

> "You have to fact check it. So, this is the point of you can use it as a starting point, but it is not omnipotent and it will tell you things very confidently. However, this is dead wrong, completely wrong and it won't flag that for you." [16:42]

## Candidate wiki links

**concepts:** [[ai-assisted-trading]], [[greeks]], [[delta]], [[theta-decay]], [[implied-volatility]], [[profit-mechanism]], [[market-effects]], [[technical-analysis]], [[backtesting]], [[context-window-management]], [[prompt-engineering]], [[large-language-model]]

**securities:** [[spx]], [[pltr]]

## Regime / context

Recorded 2025-05-20. This is a foundational education video on AI-assisted options trading, not a market-specific analysis. The examples (SPX tail-hour volatility, Palantir pricing) are illustrative of AI's strengths and failure modes, not actionable trade recommendations. The prompt library and framework are evergreen; the specific ChatGPT behavior observations reflect the model's state as of May 2025.
