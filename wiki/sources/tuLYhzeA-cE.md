---
type: source
title: "Buying vs Selling Options — Complete Framework"
video_id: tuLYhzeA-cE
url: "https://www.youtube.com/watch?v=tuLYhzeA-cE"
date: ""
series: beginner-lab
format: [education, live]
experts: [eric]
mentions: []
securities: [sofi, nvda, qqq, spx, vix]
concepts: [mean-reversion, volatility-risk-premium, implied-volatility, implied-volatility-percentile, delta, gamma, theta, vega, rho, extrinsic-value, intrinsic-value, assignment, early-exercise, delta-neutral, leverage, capital-efficiency, risk-management, position-sizing, expected-value, profit-mechanism, portfolio-first, risk-first, process-over-outcome, trading-psychology, emotional-discipline]
strategies: [long-call, short-put, covered-strangle, ratio-call-diagonal, long-straddle, short-premium, buying-the-panic]
saga: null
part: null
confidence: high
---

# Buying vs Selling Options — Complete Framework

## Summary

This session provides a comprehensive framework for deciding when to buy versus sell options, moving beyond oversimplified heuristics like "sell when IV is high." The host walks through the mechanics of premium, the Greeks, risk profiles, and introduces a four-factor decision matrix: portfolio fit, risk preference, profit mechanism, and ancillary overlays (volatility context). The core thesis is that neither buying nor selling is inherently superior—the choice depends on alignment with your specific trade thesis and portfolio structure.

## Key takeaways

### Foundational concepts

- **Mean reversion vs. drift** [00:00–17:07]: VIX exhibits mean reversion (volatility snaps back to a band), while SPX exhibits drift (long-term upward bias). This is why volatility is a tradeable asset class and why options offer edge. Options traders gain access to mean reversion; equity traders do not.
- **Premium definition** [25:57–27:12]: Premium is simply the price of an option contract, quoted as bid–offer (e.g., $1.32 bid, $1.35 offer). It contains intrinsic value (if ITM) and extrinsic value (time + volatility).
- **Buyer vs. seller mechanics** [28:25–36:30]: Every option has two parties. Buyers pay upfront and have defined risk; sellers collect upfront and have undefined risk. Most options close before expiration (not exercised).

### Risk profiles & Greeks

- **Defined vs. undefined risk** [39:26–46:50]: Buying = defined max loss (what you paid); selling = undefined risk (theoretically unlimited, though practically capped by global value). Buying = undefined profit; selling = defined max profit.
- **Theta decay** [01:03:16–01:08:15]: Time decay erodes extrinsic value daily. Buyers lose to theta; sellers benefit. Theta is *not* an edge—it's a linear, known metric. Volatility risk premium is the actual edge for sellers.
- **Gamma** [01:10:00–01:16:06]: Rate of change of delta. Long gamma benefits from volatility expansion and price movement (either direction). Short gamma is hurt by realized volatility. Gamma is a proxy for expected volatility.
- **Vega** [01:36:16]: All options (calls and puts) increase in value when IV rises; all decrease when IV falls. Whether this helps or hurts depends on whether you're long or short the option.
- **Rho** [01:16:06–01:17:32]: Interest rate sensitivity. Higher rates make options more expensive (helps buyers, hurts sellers). Effect is small for short-dated options, larger for long-dated.

### The volatility misconception

- **Overweighting IV percentile** [01:24:36–01:39:09]: Defaulting to sell whenever IV percentile is high is a common mistake. High IV means larger expected moves, but delta (directional move) can overwhelm vega (volatility change). In the SoFi example [01:33:16–01:39:09], a long call outperformed a short put despite high IV, because the stock rallied sharply. Delta (64¢ per $1 move) dominated vega (2¢ per 1-point IV move).
- **Portfolio fit first** [01:40:33]: Before considering IV, ask: does this trade fit my portfolio structure? A portfolio heavy in short premium may need long premium to offset convexity.

### The four-factor decision framework

1. **Portfolio fit** [01:40:33]: Does the trade balance your existing positions?
2. **Risk preference** [01:42:12]: Are you comfortable with undefined risk (short) or do you prefer defined risk (long)?
3. **Profit mechanism** [01:45:14–01:46:39]: What is the primary driver? If you expect a breakout (high severity move), buying a call captures more upside than selling a put. If you expect sideways drift, selling may make sense.
4. **Ancillary overlays** [01:48:12]: Only after the above three are neutral should you consider IV percentile, theta preference, or other secondary factors.

### Expected value calculation

- **Quantifying the decision** [02:05:56–02:19:08]: Build a matrix with profit targets, loss levels, probabilities at management points and at expiration, and calculate expected return for each strategy. This removes emotion and makes the choice objective.
- **Example**: At a $142 profit target and $128 loss level, the long call may have higher expected return than the short put, even though the short put has higher probability of profit.

### Common misconceptions

- **"Selling is superior"** [01:21:58]: Neither is better; they are different. Sellers often feel superior because they collect premium and win frequently, but they cap their upside and expose themselves to tail risk.
- **"Theta is my edge"** [01:08:15]: Theta is not an edge; it's a known, linear decay. The volatility risk premium (the compensation for being short volatility) is the edge.
- **"I should always blend buying and selling"** [01:23:27]: Blending is often a concession for small accounts (cheaper spreads) or for specific risk profiles (e.g., ratio diagonals). It's not inherently better.

### Practical examples

- **Leverage via options** [22:27–23:34]: Nvidia at $1,105/share requires $110K to buy 100 shares; a call option controls the same for $15K.
- **When to use options vs. equities** [23:34–24:42]: Use options for leverage, isolating profit mechanisms (theta, volatility), or when you want to avoid days-to-expiration and vega drag. Use equities (delta-one) if you don't need leverage and want to avoid theta/vega complexity.

### Homework assignment

- **Two-stock exercise** [01:52:50–01:56:34]: Pick one bullish and one bearish stock. For each, structure both a long premium and short premium trade aligned with your thesis. Compare outcomes. Share results in Discord or comments.

## Notable quotes

- "One is not better than the other. It's just different." [01:21:58]
- "The reason why volatility itself is an interesting asset class [is that it exhibits mean reversion, unlike price]." [15:36]
- "If you're making the trade decision based solely on volatility, you make two wrong decisions, possibly." [01:39:09]

## Candidate wiki links

### Concepts
[[mean-reversion]], [[volatility-risk-premium]], [[implied-volatility]], [[implied-volatility-percentile]], [[delta]], [[gamma]], [[theta]], [[vega]], [[rho]], [[extrinsic-value]], [[intrinsic-value]], [[assignment]], [[early-exercise]], [[leverage]], [[capital-efficiency]], [[risk-management]], [[position-sizing]], [[expected-value]], [[profit-mechanism]], [[portfolio-first]], [[risk-first]], [[process-over-outcome]], [[trading-psychology]], [[emotional-discipline]]

### Strategies
[[long-call]], [[short-put]], [[covered-strangle]], [[ratio-call-diagonal]], [[long-straddle]], [[short-premium]]

### Securities
[[sofi]], [[nvda]], [[qqq]], [[spx]], [[vix]]

### People
[[eric]], [[tom-sosnoff]]

## Regime / context

This is a foundational education session with no specific market date. The examples use live option chains (SoFi, Nvidia) and historical backtests (SoFi on 8 November) to illustrate concepts, but the framework is evergreen. The session assumes familiarity with basic options terminology and is part of the Outlier Trading beginner lab series.
