---
type: source
title: "Institutional Market Research for Retail Traders | Project No Code"
video_id: _R71zK5XEew
url: https://www.youtube.com/watch?v=_R71zK5XEew
date: 2026-05-31
series: project-no-code
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spy, spx]
concepts: [no-code-tools, backtesting, quantitative-research, edge, outlier-strategy-process, market-efficiency, support-and-resistance, fomc, market-regimes, price-action, context-window-management, large-language-model, prompt-engineering, ai-assisted-trading]
strategies: [breakout]
saga: null
part: null
confidence: high
---

# Institutional Market Research for Retail Traders | Project No Code

## Summary

Eric introduces Project No Code, a framework for retail traders to build institutional-grade research infrastructure using AI agents (Claude Code, ChatGPT, Codeex) without writing code themselves. The system democratizes access to backtesting, data ingestion, and hypothesis testing by automating database construction, API management, and research iteration through conversational AI prompts. Traders can now definitively test profit mechanisms—such as market proximity to all-time highs (SPY within 10% of ATH ~68% of the time)—without fumbling through years of manual iteration or expensive proprietary tools.

## Key takeaways

### Evergreen mechanics

- **The core problem solved** [00:31–02:23]: Retail traders historically lack time and capital to test ideas systematically. Project No Code eliminates API quota limits, coding barriers, and data costs by building a personal local database that can be queried infinitely after initial setup.

- **Three data stages** [17:27–18:12]: Maintain hygiene by separating raw (immutable source), clean (normalized tables), and derived (calculated/permuted) data. This allows full reconstruction if the database breaks.

- **AI agent workflow** [13:51–14:46]: Use Claude Code (or Codeex) as the workhorse for code generation and CLI interaction; use ChatGPT/Gemini for review and general reasoning. Free tier works but subscription recommended for reasonable iteration speed.

- **Context window management** [24:50–26:01]: As AI chats grow, context compacts imperfectly. Maintain three documents: SOP (single source of truth, ~4,000 lines), Roadmap (session-specific tasks and research goals), and Claude.md (auto-updated by AI at chat end). This prevents knowledge loss across sessions.

- **Infrastructure scaling** [18:33–19:15]: Start with a 4 TB external SSD for equities data; add RAM as needed for in-memory operations. Options data is exponentially heavier (SPX has ~2,000 expirations × ~200 strikes per expiration at each timestamp). Use RAID enclosures for redundancy: primary (Raid Alpha) + complete backup (Raid Bravo).

- **Cost model** [20:19–21:05]: API costs are front-loaded (1–2 months of historical data pulls, potentially $1,000+) but one-time. Once the database is built, cancel APIs and use free data (e.g., Schwab API) for incremental updates. Maintenance cost is the AI subscription only.

- **Incremental updates** [23:13–23:35]: Set up automated daily pulls to fetch only new data since the last run. Spot-check for corruption; fix with AI; done. Minimal ongoing human effort.

- **Research iteration** [23:35–24:01]: Think of ideas → discuss with Claude → generate study → iterate → document in trading plan. AI powers all execution; human provides direction.

- **Testable hypotheses** [10:34–10:58]: Examples include breakout mechanics (15-min vs 5-min candles, profit maximization), FOMC impact on volatility/price, presidential election cycles and their profit mechanisms.

### Dated market read (2026-05-31)

- **Market proximity to all-time highs** [01:28–01:58]: Over ~20 years of SPY data, the S&P 500 closed within 2% of rolling all-time highs on ~39% of days, within 5% on ~55%, and within 10% on ~68%. This refutes doomsayer narratives; crashes are rare and often telegraphed by signals.

## Notable quotes

> "This makes meaningful research accessible to literally everybody. This used to be gated by cost and it mostly was gated by knowhow."

> "I didn't write any of this. All I did was come into Claude Code and I told it this. This is what I want you to do."

> "You do not have enough time to fumble your way through the market reliably and actually hit the outcome that you want."

## Candidate wiki links

**concepts:** [[no-code-tools]], [[backtesting]], [[quantitative-research]], [[edge]], [[outlier-strategy-process]], [[market-efficiency]], [[support-and-resistance]], [[fomc]], [[market-regimes]], [[price-action]], [[context-window-management]], [[large-language-model]], [[prompt-engineering]], [[ai-assisted-trading]]

**strategies:** [[breakout]]

**securities:** [[spy]], [[spx]]

**people:** [[eric]]

## Regime / context

Recorded 2026-05-31. This is a foundational education video introducing Project No Code as a meta-framework for building research infrastructure. The market read (SPY proximity to ATH) is illustrative of the *type* of analysis the system enables, not a tactical market call. The project began 2026-05-18 and represents Eric's synthesis of six years of YouTube content on edge-building with recent advances in AI code generation (Claude Code, Codeex). Applicable to any market regime; the framework is regime-agnostic.
