---
type: source
title: "The Outlier Research Process: How I Maintained a 30% CAGR over 19 Years of Trading"
video_id: 7lb6sXnN-ak
url: https://www.youtube.com/watch?v=7lb6sXnN-ak
date: 2026-06-21
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spx, spy, vix]
concepts: [research-depth, backtesting, confirmation-bias, edge, profit-mechanism, hypothesis-testing, survivorship-bias, overfitting, data-mining, monte-carlo-simulation, walk-forward-analysis, parameter-sweep, stress-testing, regime-switching, volatility-risk-premium, post-earnings-drift, transaction-costs, process-over-outcome, risk-management, quantitative-research]
strategies: [short-volatility, short-premium]
saga: null
part: null
confidence: high
---

# The Outlier Research Process: How I Maintained a 30% CAGR over 19 Years of Trading

## Summary

This is a comprehensive end-to-end guide to the research lifecycle for developing and validating trading edges. Eric walks through six core phases—sourcing, profiling, signal overlay, testing (backtest/forward/live), evaluation, and iteration—emphasizing that rigorous research requires attempting to disprove ideas rather than confirm them. The core thesis is that maintaining a 30% compound annual growth rate over nearly 20 years depends entirely on process discipline, not outcome luck.

## Key takeaways

### Research lifecycle phases
- **Sourcing** [01:42]: Brainstorm and identify what you want to research; start with primary literature (SSRN, NBER) rather than YouTube to establish a known baseline.
- **Profiling** [02:03]: Conduct an eyeball test to identify instances and patterns; understand the underlying profit mechanism, not just the surface effect.
- **Signal overlay** [02:29]: Find relationships between indicators and the source; moving averages are a canonical example for momentum strategies.
- **Testing gauntlet** [02:49]: Three phases—backtest (historical), forward test (rule-based projection with synthetic data), live test (paper or minimal real capital).
- **Evaluation** [22:37]: Use trends, parameter sweeps, and Monte Carlo to assess viability; avoid Goldilocks analysis and rose-colored glasses.
- **Iteration** [35:54]: Perpetual observation at trade, strategy, and portfolio levels; edge decays over time and requires continuous adaptation.

### Mindset and bias management
- **Strong convictions loosely held** [03:42]: Do rigorous research, then immediately reshape your view when better data arrives; avoid identity attachment.
- **Guilty until proven innocent** [12:50]: Enter testing to break ideas, not validate them; pre-commit to parameters before testing to avoid overfitting.
- **Avoid confirmation bias** [01:15]: Most research is confirmation bias wrapped in fancy language; the gap between effort and rigor is massive.
- **Key biases to watch** [04:33]: Anchoring, availability, clustering, confirmation, curve fitting, disposition, hindsight, loss aversion, recency, p-hacking, overconfidence, survivorship.

### Profit mechanisms and edge definition
- **Edge requires positive expectancy** [05:38]: Not inherent to options or premium-selling; must contain a causal reason for existence.
- **Variance risk premium example** [08:53]: Exists because crash protection is in high demand; observable across regimes but ebbs and flows; very robust starting point.
- **Structural alpha** [09:52]: Window dressing near month-end creates defined relationships between equities and bonds; observable and testable.
- **Hypothesis vs. thesis** [10:20]: Hypothesis is what you think will happen; thesis explains why it might happen and adds causal connections.

### Testing rigor and common pitfalls
- **Avoid data mining** [12:23]: Don't beat data to death; there is a time for overfitting to understand relationships, but only with rigorous follow-up testing.
- **Non-negotiables** [13:15]: Log everything; make aggressive assumptions (adverse fills, not mid); pre-commit before testing; consider why the other side of the trade exists.
- **Survivorship bias** [15:32]: Test across multiple securities, not just one; check sequence of returns; account for delisted stocks that would have qualified historically.
- **Transaction costs** [17:19]: Assume crossing the spread every time; if strategy breaks under adverse fills, it's weak or requires liquid-only securities.
- **Walk-forward and k-folding** [30:54]: Split data into training and testing windows; rotate windows; use purging and embargoes to prevent label leakage.

### Stress testing and robustness
- **Look for plateaus, not peaks** [32:05]: Peaky results indicate terrible overfitting; robust strategies show similar performance across parameter variations.
- **Shock through regimes** [19:08]: For bearish strategies, test in bullish conditions; for bullish, test in bearish; cherry-pick stress periods deliberately.
- **Fat tails and leptokurtic distributions** [25:43]: Real market data has fatter tails than normal distribution; bake this into analysis or you're looking at lopsided data.
- **Regime classification** [26:39]: Conditioning variables tell you how the universe looks, not a direct signal to do X; understand regime-dependent vs. cross-regime viability.
- **Block resampling** [27:44]: Standard t-tests don't account for autocorrelated data; use block bootstraps or rolling blocks to preserve dependence.

### Evaluation metrics and forward testing
- **Don't trust Sharpe ratios from backtests** [28:47]: Deflate all metrics; they're inflated by multiple hypothesis testing; only trust live sample data.
- **Vectorized vs. event-driven backtesting** [29:11]: Vectorized is fast for scoping; event-driven is slower but more robust and controlled.
- **Sample size and distribution width** [33:45]: Whatever you test is unlikely the median; it's skewed one direction; need enough iterations to identify what's representative.
- **Capacity as a future problem** [34:15]: Even large liquid markets like VRP in indices will reprice if you apply too much volume; edge moves away over time.
- **Edge decay** [35:29]: Post-earnings drift is a canonical example; edge becomes more competitive and decays; you must adapt continuously.

### Forward and live testing
- **Purpose of forward testing** [19:32]: Expose yourself to out-of-sample, novel data your backtest hasn't seen; confirm if edge actually holds.
- **Live testing duration** [20:03]: Paper trade or minimal viable size; duration depends on the strategy and your confidence level.
- **Data quality and corporate actions** [21:19]: Keep raw data untouched; handle splits, dividends, and price adjustments correctly; match data granularity to what you're testing (e.g., intraday for zero-DTE).

### Research tools and data management
- **Primary literature as baseline** [07:19]: SSRN, NBER give you a known plan to test against; if you can reproduce results, you know you have good research discipline.
- **Oat Talk and project-no-code** [11:40]: Market analysis tools and playlists available for building your own research infrastructure.
- **Observation-driven edge discovery** [08:04]: Over time, identify things that look weird against historic precedent stored in your context window; iterate from there.

## Notable quotes

> "It's the only way I've maintained a 30% compound annual growth rate over nearly 20 years. It's because of doing stuff like this." [06:27]

> "Every idea is guilty until proven innocent. The point here is you should be going into testing, attempting to break everything, not validate." [12:50]

> "You want to look for plateaus. You do not want peaks. If you look at a peak in your results, it almost immediately means all the time that you are terribly overfit." [32:05]

## Candidate wiki links

### Concepts
[[research-depth]], [[backtesting]], [[confirmation-bias]], [[edge]], [[profit-mechanism]], [[hypothesis-testing]], [[survivorship-bias]], [[overfitting]], [[data-mining]], [[monte-carlo-simulation]], [[walk-forward-analysis]], [[parameter-sweep]], [[stress-testing]], [[regime-switching]], [[volatility-risk-premium]], [[post-earnings-drift]], [[transaction-costs]], [[process-over-outcome]], [[risk-management]], [[quantitative-research]], [[kelly-criterion]], [[expected-value]], [[fat-tails]], [[market-efficiency]], [[mean-reversion]]

### Strategies
[[short-volatility]], [[short-premium]], [[momentum]], [[trend-following]]

### Securities
[[spx]], [[spy]], [[vix]]

### People
[[eric]]

## Regime / context

Recorded June 21, 2026. This is a foundational education piece on the Outlier research methodology, designed as an end-to-end guide for developing and validating trading edges. Eric notes this is part one of a multi-part series; a follow-up for pro members will include specific worked examples. The methodology is presented as timeless process doctrine rather than market-specific analysis, though examples reference variance risk premium in equity indices and post-earnings drift as canonical edge cases.
