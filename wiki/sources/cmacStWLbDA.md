---
type: source
title: "Balancing Risk and Reward in Trading | Outlier Options Trading Beginner Lab"
video_id: cmacStWLbDA
url: https://www.youtube.com/watch?v=cmacStWLbDA
date: 2026-02-07
series: beginner-lab
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [slv, spy, gld]
concepts: [risk-reward, expected-value, position-sizing, risk-tolerance, probability-of-profit, profit-mechanism, strategy-refinement, risk-management, trading-psychology, backtesting, paper-trading, trading-log, volatility-risk-premium, implied-volatility, realized-volatility, skew, put-skew, delta, moneyness, earnings-move, short-volatility]
strategies: [short-put, short-strangle, iron-condor, short-earnings-straddle, long-call, breakout]
saga: null
part: null
confidence: high
---

# Balancing Risk and Reward in Trading | Outlier Options Trading Beginner Lab

## Summary

This session deconstructs the relationship between risk and reward in trading, emphasizing that they are correlated but not linear, and that risk tolerance is deeply personal. Eric walks through foundational misconceptions (e.g., "don't be greedy," "take profits quickly"), introduces probabilistic thinking via expected value, and demonstrates how risk-to-reward profiles vary by strategy. The core lesson: understand your own tolerance, analyze your strategies empirically via paper trading and trade logs, and size positions based on realistic loss scenarios rather than aspirational return targets.

## Key takeaways

### Foundational concepts
- **Risk and reward are correlated but not linear** [05:07]. Taking 6 units of risk does not yield 1 more unit of reward than 5 units; the relationship is nonlinear and strategy-dependent.
- **Risk tolerance is deeply individualized** [08:53]. You must assess your own tolerance before trading; without this self-knowledge, you will make poor decisions. For beginners, the reward target should be "greater than zero" [12:17]—if the market returns 30% and you're up 1%, you succeeded.
- **Common bad advice includes**: "don't be greedy," "wait and give it more time," "take profits quickly," "dollar-cost average into a loser," and "roll your options" [06:20]. These are context-blind and ignore strategy-specific profit mechanics.

### Risk-reward decision-making
- **Coin-flip exercise** [14:49–23:42]. Different people have different thresholds for accepting risk. A 50/50 coin flip offering $1M or losing $250K appeals to some but not others; the threshold shifts based on financial position and personal utility. This illustrates why risk-to-reward tolerance is relative.
- **No universal "best" risk-to-reward ratio exists** [28:27]. The optimal ratio depends on the underlying strategy and market regime, not on abstract principles.
- **Probability must be added to risk-to-reward to calculate expected value** [39:24]. Probability of profit is a data point; expected value is what matters. A 48% win-rate strategy with $1,102 average win and $432 average loss can be highly profitable despite low win rate.

### Strategy-level analysis
- **Vertical spread example (SLV)** [36:01]. A $1-wide put spread at 30 delta, selling at 35¢ premium with 65¢ risk, has 36% probability of ending in-the-money and is negatively expectant (~flat). If volatility rises and you get filled at 40¢, it becomes positively expectant.
- **Volatility and skew matter** [46:43]. Implied volatility vs. realized volatility, and put skew, create opportunities. A short put credit spread in SPY may be deeply negatively expectant due to lower volatility, requiring additional edge (e.g., mean reversion, regime filters).
- **Strategy-specific expected value** [41:42]. A long call breakout strategy may have 48% win rate, $1,102 average win, and $432 average loss, yielding positive expected value despite low win rate. This cannot be replicated in a short-volatility vertical spread strategy.

### Building empirical understanding
- **Paper trade with a strategy outline** [43:19]. Document your setup, management rules, and profit mechanism. Use tools like On Demand to backtest across different regimes (e.g., 2022–2023).
- **Track trades in a log (Excel/Google Sheets)** [49:13]. Record entry, exit, P&L, and conditions. Over time, you'll identify patterns: e.g., "I win most of the time, but when I lose, I wipe out multiple winners."
- **Identify and analyze outlier losses** [50:02]. If you notice three large losses in your P&L scatter plot, investigate: When did they occur? What was common? Can you codify a filter to reduce exposure without killing profitability?
- **Position sizing based on realistic loss scenarios** [52:37]. If paper trading earnings short-straddles reveals occasional 4-sigma losses, size your live trades so that one such loss doesn't blow you up. Avoid sizing everything for the worst case (you'll make no money); instead, balance average sizing with tail-risk awareness.

### Professional vs. beginner mindset
- **At the beginner level, lean into your natural tendencies** [27:39]. If you prefer high win-rate strategies, start there; if you're drawn to low-probability, high-reward trades, test that. As a professional, you must execute what works, regardless of preference.
- **Strategy refinement requires robust testing** [51:08]. Management improvements must be validated: does cutting a tail reduce losses without cratering average wins? Does the aggregate P&L improve?

## Notable quotes

- "Risk and reward are two sides of the same coin. We already know in order to get some kind of reward, you need to put up some kind of risk. One of the first common misconceptions between these is that they are purely correlated and they are not." [05:07]
- "Your risk-to-reward tolerance is super duper individualized, insanely so. You have to understand yourself a little bit." [23:42]
- "The only way you can make good decisions is if you do the analysis on the strategies that you're trading and understand what they look like, how they behave, so that you can make logical trade decisions." [53:57]

## Candidate wiki links

**Concepts:**
[[risk-reward]], [[expected-value]], [[position-sizing]], [[risk-tolerance]], [[probability-of-profit]], [[profit-mechanism]], [[strategy-refinement]], [[risk-management]], [[trading-psychology]], [[backtesting]], [[paper-trading]], [[trading-log]], [[volatility-risk-premium]], [[implied-volatility]], [[realized-volatility]], [[skew]], [[delta]], [[moneyness]], [[earnings-move]], [[short-volatility]]

**Strategies:**
[[short-put]], [[short-strangle]], [[iron-condor]], [[short-earnings-straddle]], [[long-call]], [[breakout]]

**Securities:**
[[slv]], [[spy]], [[gld]]

**People:**
[[eric]]

## Regime / context

Recorded 2026-02-07 as part of the Outlier Options Trading Beginner Lab series. This is a foundational session on risk-reward philosophy and does not depend on current market conditions; the principles and examples (SLV, SPY, earnings) are evergreen. The session emphasizes paper trading and backtesting as the primary tools for beginners to develop empirical understanding before live trading.
