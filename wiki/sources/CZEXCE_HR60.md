---
type: source
title: "O/TOC Research Terminal Update & Open Q&A | Options Trading for Beginners"
video_id: CZEXCE_HR60
url: https://www.youtube.com/watch?v=CZEXCE_HR60
date: 2026-06-07
series: project-no-code
format: [education, live]
experts: [eric]
mentions: []
securities: []
concepts: [no-code-tools, context-window-management, ai-assisted-trading, market-breadth, standard-deviation-move, fat-tails, market-regimes, edge, seasonality]
strategies: [earnings-vol-play]
saga: null
part: null
confidence: medium
---

# O/TOC Research Terminal Update & Open Q&A | Options Trading for Beginners

## Summary

Eric walks through the finalized storage architecture for the O/TOC research terminal—a multi-drive NVMe setup with hot, warm, and cold backup tiers—and introduces two new tools: the Quick Reference Guide (QRG) for system monitoring and Huginn, an early-stage visual market-scanning dashboard. The session includes live troubleshooting of drive pooling and open Q&A on edge discovery, seasonality, and market regime analysis.

## Key takeaways

- **Storage architecture finalized** [08:04–13:57]: Three internal 8 TB NVMe drives pooled as primary data tier (E, F, N); external 4 TB NVMe drives (U, V, W) as secondary hot stage; H as warm backup; I as cold backup (disconnected between sessions). Total capacity designed for expansion into novel datasets (insider trading, peer research, FTD data).
- **Drive pooling and naming conventions** [10:02–12:43]: Thunderbolt-connected external NVMe performs as fast as internal; pooling strategy balances speed (NVMe for tabular data) vs. capacity; drive letter organization (E, F, H, I, J) maps to operational priority.
- **Quick Reference Guide (QRG) tool** [54:39–56:23]: Interactive menu for system status, pipeline monitoring, roadmap reconciliation, and live chat aggregation (C2 function). Circular navigation (stay in menu after selecting item) improves workflow efficiency.
- **Huginn scanning dashboard (early stage)** [56:51–01:00:32]: Visual market-monitoring tool aggregating multiple data sources; toggleable by index/sector; custom scanning for consolidation breakouts, volume patterns, and strategy-specific conditions unavailable in standard platforms like Barchart.
- **Edge and seasonality discussion** [42:31–48:24]: Edge is rarely steady; traders choose between tailored seasonal strategies (e.g., earnings tweaks by quarter) vs. simpler blunt-force approaches. Consistent edge requires decision-cycle alignment; performance reflects precision vs. simplicity trade-off.
- **Standard deviation and market distribution** [40:21–42:31]: Markets do not follow normal distribution; large moves (3+ SD) occur more frequently than theory predicts. Context matters: rolling window, skew, and system type determine actual probability; Friday's ~4 SD move illustrates tail-risk reality.
- **Pro Plus Zoom Workshop opening** [01:03:00–01:04:29]: First and third Monday of each month, 5 p.m. Pacific; open to Project No Code builders; pro members get two submissions, non-pro guaranteed at least one seat. Apply via eric@outliertrading.io.

## Notable quotes

"The entire purpose of what I'm doing here is to try and front run you all a little bit, meaning progress ahead of where you likely are current state so that ideally you can make design decisions with better information than I had." [06:21]

"These really small minor things that I stack over time that genuinely leads to like pretty marked increase efficiency." [56:23]

## Candidate wiki links

**concepts:** [[no-code-tools]], [[context-window-management]], [[ai-assisted-trading]], [[market-breadth]], [[standard-deviation-move]], [[fat-tails]], [[market-regimes]], [[edge]], [[seasonality]]

**strategies:** [[earnings-vol-play]]

**people:** [[eric]]

## Regime / context

Recorded 2026-06-07 as a live Saturday session. Storage architecture represents final steady-state configuration; no further hardware changes planned. Huginn tool is in early development and not yet production-ready. Friday's market move (referenced as ~4 SD) occurred 2026-06-06 and serves as a case study in tail-risk and non-normal distribution behavior. Project No Code and O/TOC are ongoing community initiatives with expanding access to research infrastructure.
