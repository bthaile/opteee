---
type: source
title: "How I Use AI to Trade Options (Beginners Watch This) | Project No Code"
video_id: "AoHUcyVh7NY"
url: "https://www.youtube.com/watch?v=AoHUcyVh7NY"
date: "2026-05-30"
series: project-no-code
format: education
experts: []
securities: [spx]
concepts: [ai-assisted-trading, no-code-tools, large-language-model, context-window-management, prompt-engineering, backtesting, overfitting, monte-carlo-simulation, survivorship-bias, quantitative-research, edge, profit-mechanism, variance-risk-premium, implied-volatility, realized-volatility, volatility-skew, term-structure, outlier-strategy-process]
strategies: [opening-range-breakout, short-premium, credit-spread, short-straddle, trend-following]
confidence: high
---

# How I Use AI to Trade Options (Beginners Watch This) | Project No Code

## Summary
A live primer ahead of the "Project No Code" launch, where the host (Eric of Outlier Trading) walks through how a non-engineer can use frontier AI coding agents to build a personal options quantitative-research database with zero lines of code. The usable core is a concrete, reproducible workflow: pick paid AI models (he uses Claude Code + ChatGPT via Codex), manage the context window with a CLAUDE.md + SOP + roadmap documentation system, and use AI to run backtests/grid searches (opening-range breakout, variance-risk-premium by tenor) that used to take weeks. He stresses that AI is a force multiplier, not an edge generator — the trader still has to know what questions to ask, guard against overfitting/survivorship bias, and never start from a preferred option structure.

## Key takeaways
- Project No Code = a "no-code" quant research database built entirely with AI; he wrote zero lines of code despite building a >1B-row options dataset, and has shelved his personal DB to trade off this public framework. [05:55] [08:34] [52:34]
- Cost model: real money upfront on data (APIs ~a few hundred $/month, turn off once downloaded; he spent six figures over his career on data), but no recurring cost afterward except storage/compute + a paid AI subscription. Free AI models aren't viable for this in reasonable time. [07:06] [07:53]
- The workflow accelerates the "outlier strategy process": AI compresses the build-strategy and testing steps (opening thousands of charts, Excel churn) that are the real time sink. A trader's primary job is researcher; ~95%+ of what you test won't work ("digging for gold" is edge). [09:31] [11:57] [12:58]
- Worked example: test an opening-range breakout across ~2,000 names over 10 years in ~5 minutes, then grid-search minute-level from the open to find the optimal window. [14:15] [14:55]
- Backtesting is a hard requirement (he links a "basics of backtesting" video): overfitting is the core danger; defend with bootstrapping, segmentation, randomized-order checks, and Monte Carlo simulations trained on your own data — all now doable in one AI session. [15:45] [16:38] [16:56]
- Context-window management is the single most important skill. Compacting a chat summarizes and loses detail ("context rot"); huge context also slows the model down. Don't wait until you hit the 1M-token limit to compact or start a new chat. [25:13] [26:19] [33:32]
- His documentation system: a CLAUDE.md at repo root (internal turnover, ~40,000-char cap) + a larger "no-code SOP" (kitchen-sink log with a table of contents so AI can jump to the relevant section) + a roadmap; update the SOP daily, and have AI write a markdown turnover file at each chat's end capturing key decisions, open action items, and in-flight work for the next agent. [27:51] [28:55] [33:57]
- Chat models vs coding agents are different tools (Claude ≠ Claude Code): use the chat model for big planning/architecture/brainstorming, then hand off to the coding agent to operationalize. He coordinates everything in VS Code (Python, Jupyter, terminals). Built mostly on Claude 4.7; 4.8 just launched. [19:18] [35:12] [37:53]
- Prompting: give AI a role/lens ("you are an options strategist / a full-stack engineer building an options research database"); the quick-start prompt he provides is ~17 pages split into phases. Ask AI to brainstorm and produce courses of action with pros/cons rather than dictating. [39:05] [40:01]
- Force AI to be non-agreeable: he instructs CLAUDE.md to be objective and actively "punch holes" in his thinking. AI is sycophantic — it accelerates judgment but doesn't replace it; cross-validate with a second/third model, which matters more the less expert you are. [24:09] [41:25] [42:16] [01:04:24]
- Data hygiene best practices: go slow and plan before acting; smoke-test (pull 25 tickers before 4,000); point AI to the correct API docs; keep it on one task (build the DB first); and capture delisted names to avoid survivorship bias. [55:48] [01:06:42] [01:08:02]
- Use gating to avoid babysitting: have AI build a plan with gates, execute to gate X, request review, then continue; "bypass permissions" in Claude Code reduces confirmation friction. [01:14:20] [01:16:29]
- Library convention: separate "workshop" (temporary exploration) from "research" (maintained); archive rather than delete; a README instructs the AI how to run/organize studies; each test gets its own folder with a spec sheet (strategy outline) + a Jupyter script + documented visuals. [01:19:04] [01:20:22]
- Live options examples run with Claude: SPX skew and term structure, and variance-risk-premium across tenors (implied runs richer than realized, ~0.96 avg pts on 30-day); you can grid-search which tenor carries the richest/most-consistent risk premium and best max-drawdown, then combine into a CAGR objective. [01:13:08] [01:17:35] [01:18:38]
- Never start from a structure ("I want to sell credit spreads"): the market doesn't care about your preferred structure and it isn't edge. Better posed: "capture variance risk premium — brainstorm ways." Perpetual premium-selling is flawed because only ~68% of days (2007–present) carry risk premium, so ~32% of the time you'd be selling at bad points; the research question is how to find the rich (2+ pt) periods. [01:22:13] [01:23:23] [01:23:59]
- AI won't hand you edge ("yo AI, find me edge" won't work): you must build your own domain context to ask good questions. A model returning an answer means nothing — it just wants to complete the task. [01:10:10] [01:25:22]
- Hardware: Windows-based (Mac/Linux workable); RAM is the biggest lever (he runs 96GB DDR5, calls 32GB a minimum); use parquet compression and keep data triplicated for redundancy; a ~$2,000 machine is sufficient. [55:05] [56:38] [01:00:03]

## Notable quotes
- "I have written literally zero lines of code." [08:34]
- "AI is a force multiplier. You still need to be the thinking, planning, oversight on the entire thing." [24:09]
- "The market doesn't care what structure you prefer to trade. That doesn't equal edge." [01:22:43]

## Candidate wiki links
- concepts: [[concepts/ai-assisted-trading]], [[concepts/no-code-tools]], [[concepts/large-language-model]], [[concepts/context-window-management]], [[concepts/prompt-engineering]], [[concepts/backtesting]], [[concepts/overfitting]], [[concepts/monte-carlo-simulation]], [[concepts/survivorship-bias]], [[concepts/quantitative-research]], [[concepts/edge]], [[concepts/profit-mechanism]], [[concepts/variance-risk-premium]], [[concepts/implied-volatility]], [[concepts/realized-volatility]], [[concepts/volatility-skew]], [[concepts/term-structure]], [[concepts/outlier-strategy-process]]
- strategies: [[strategies/opening-range-breakout]], [[strategies/short-premium]], [[strategies/credit-spread]], [[strategies/short-straddle]], [[strategies/trend-following]]
- securities: [[securities/spx]]
- people: [[people/eric]]

## Regime / context
- Recent (2026) modern AI-in-trading theme: retail/prosumer traders using frontier LLM coding agents (Claude Code, ChatGPT/Codex) with ~1M-token context windows to build quant research infrastructure with no coding background.
- Timely detail: Claude 4.8 "just launched"; the project was built mostly on 4.7. The pace of model improvement is explicitly noted as a moving target ("this shit's moving fast"), so specific tool/version guidance may date quickly.
- This is a launch primer for a broader "Project No Code" release (a free ~17-20 page quick-start guide/playbook) plus paid Pro Plus Zoom build workshops; the trading substance (backtesting discipline, variance risk premium) is evergreen, but the AI-tooling specifics are regime-dependent on 2026 model capabilities and pricing.
