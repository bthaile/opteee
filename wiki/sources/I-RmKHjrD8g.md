---
type: source
title: "Project No Code - Working Session and Q&A | Options Trading for Beginners"
video_id: I-RmKHjrD8g
url: "https://www.youtube.com/watch?v=I-RmKHjrD8g"
date: "2026-06-06"
series: beginner-lab
format: [education, live, strategy-breakdown]
experts: [eric]
mentions: []
securities: [qqq, tqqq, gme, aapl, msft, nvda, spy, spx, vix]
concepts: [standard-deviation-move, market-breadth, breadth-indicators, moving-averages, portfolio-management, scaling-out, position-sizing, implied-volatility, volatility-clustering, market-regimes, backtesting, overfitting, research-depth, profit-mechanism, event-driven, earnings-move, news-sentiment, monte-carlo-simulation, no-code-tools, ai-assisted-trading, large-language-model, prompt-engineering]
strategies: [short-earnings-straddle, covered-strangle]
saga: null
part: null
confidence: high
---

# Project No Code - Working Session and Q&A | Options Trading for Beginners

## Summary

Eric walks through a live market recap following a 3.38 standard-deviation drop in the Nasdaq (QQQ down ~4.8%) driven by a stronger-than-expected jobs print, then pivots to a detailed working session on the Project No Code infrastructure—demonstrating data storage architecture, backtesting hygiene, IPO analysis automation, and the philosophy behind building a personal research platform. The session emphasizes research-first decision-making, avoiding overfitting, and using AI-assisted tools to accelerate analysis without outsourcing judgment.

## Key takeaways

### Dated market read (2026-06-06)

- **Market structure**: QQQ down 4.8% (3.38 std-dev move); non-farm payrolls +172k vs. ~88–100k estimate; unemployment steady but persistent inflation narrative reinforced [11:34–13:19]
- **Breadth divergence**: NASDAQ breadth strong but NYSE breadth weak; moving averages already trending down before today's flip; light breadth on all-time highs is a divergent signal [16:44–17:44]
- **Portfolio adjustment**: Trimmed 55–60% of capital due to confluence of red flags (weak breadth, directional positioning, anomalous put/call premium shifts); TQQQ still up ~78% from entry despite 14% daily drop [18:55–20:19]
- **Defensive rotation**: Healthcare gapped up +6% (defensive); staples weak; discretionary rolling off; VIX at 21.5 is a "really important place" for research [21:14–22:16]
- **Regime note**: Market near all-time highs but unusually mixed—not normal; futures open Sunday is a key bellwether [22:38–23:11]

### Evergreen mechanics

- **Breadth as confluence, not standalone signal**: Weak breadth alone doesn't warrant action; must stack with price action, moving averages, and positioning data [17:44–18:10]
- **Scaling capital in/out**: Overreacting to every down-tick prevents riding upside; systematic rebalancing (pulling capital for other ventures) is how wealth compounds [19:25–20:19]
- **Data infrastructure for research**: 178 TB storage (NVME + HDD tiered) enables fast parallel research; 1-hour options data back to 2015 across entire optionable universe, with 5-min and 1-min tiers for core/index names [24:47–31:53]
- **Backtesting hygiene**: Avoid overfitting by testing on in-sample window (e.g., 2005–2015), validating on out-of-sample (2016–2020), then refining and repeating; this prevents false edges [37:29–38:23]
- **Profit mechanism first**: Research starts with a hypothesis (e.g., "IPO underpricing exists"), validated via SSRN or similar; then profile by market cap, sector, time-of-IPO; only then build strategies [18:03–19:26]
- **News classification**: Organize news into buckets (standard, anomalous mentions, merger/acquisition, lawsuit, etc.); test baseline behavior vs. behavior-with-news to isolate effect [01:02:18–01:03:16]
- **AI as assistant, not oracle**: Use Claude/LLMs to generate code, alerts, and analysis scaffolds, but apply human judgment; over-reliance without domain thinking leads to wrong paths [01:10:56–01:11:34]

## Notable quotes

- "I regularly and knowingly shoot myself in the foot all the time and it's because I don't need the YouTube channel to be a million subscribers... I'm fortunate enough that I don't have to compromise my values in order to get there." [49:12–49:34]
- "A 30% plus compound annual growth rate from 2007 to present is not bad and I want to maintain that." [47:18]
- "The overwhelming majority of the time the S&P 500 is within 10% of 52-week highs and the majority of the time it's within 5% of all-time highs." [34:01–34:34]

## Candidate wiki links

**concepts:**
[[standard-deviation-move]], [[market-breadth]], [[moving-averages]], [[portfolio-management]], [[scaling-out]], [[position-sizing]], [[implied-volatility]], [[backtesting]], [[overfitting]], [[research-depth]], [[profit-mechanism]], [[event-driven]], [[earnings-move]], [[monte-carlo-simulation]], [[no-code-tools]], [[ai-assisted-trading]], [[large-language-model]], [[prompt-engineering]], [[divergent-signal]], [[confluence-of-evidence]]

**strategies:**
[[short-earnings-straddle]], [[covered-strangle]]

**securities:**
[[qqq]], [[tqqq]], [[gme]], [[spy]], [[vix]]

**people:**
[[eric]]

## Regime / context

**Date context:** 2026-06-06 (Friday). Jobs print surprise (172k vs. ~88–100k) triggered sharp reversal; market near all-time highs but showing structural weakness (breadth divergence, light volume on highs). Futures open Sunday will be a key signal for follow-through.

**Project No Code status:** Live and actively evolving. Infrastructure now includes 178 TB tiered storage (NVME + HDD), 1-hour options data back to 2015, backtesting framework with out-of-sample validation, IPO analysis automation, and current-market snapshot tools. Eric emphasizes this is overkill for most traders but necessary for his research velocity and 30%+ CAGR target.

**Philosophy note:** Eric stresses that building your own tools (rather than subscribing to a service) forces you to understand your edge, allows customization to your trading style, and avoids outsourcing judgment to black-box platforms. The Project No Code is a "lead by example" demonstration, not a prescription.
