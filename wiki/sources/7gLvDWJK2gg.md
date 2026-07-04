---
type: source
title: "Rolling Options Explained & Why Most People Get It WRONG"
video_id: 7gLvDWJK2gg
url: https://www.youtube.com/watch?v=7gLvDWJK2gg
date: 2023-07-25
series: none
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [spx]
concepts: [rolling-options, loss-aversion, realized-vs-unrealized-pnl, net-liquidating-value, expiration-liquidity, delta, moneyness, days-to-expiration, mark-to-market]
strategies: [rolling-options]
saga: null
part: null
confidence: high
---

# Rolling Options Explained & Why Most People Get It WRONG

## Summary

Eric debunks widespread misinformation about rolling options, clarifying that a roll is simply closing one trade and opening a new one—not a mechanism to avoid losses. He walks through the mechanics of realized vs. unrealized P&L, explains why infinite rolling is impossible due to margin constraints, and demonstrates how loss aversion drives poor rolling decisions.

## Key takeaways

- **What a roll actually is** [04:00–04:41]: A roll is a closing trade (exit) mentally linked to an opening trade (entry). Your broker does not track rolls; it's a convenience-based accounting concept. You close trade one, open trade two—that's it.

- **Rolling does NOT avoid losses** [06:21–07:04]: When you buy back a short put at a loss, you realize that loss immediately. The subsequent roll (selling a new put for credit) creates unrealized gain potential, but the loss is already booked. Traders conflate realized and unrealized P&L.

- **Net liquidating value vs. cash and sweep** [10:18–12:15]: Net liquidating value reflects your account's true worth (including open position mark-to-market); cash and sweep is literal cash on hand. After rolling for a loss, your cash and sweep may increase (you collected credit), but your net liq decreases (you realized the loss). This asymmetry is why infinite rolling fails.

- **You cannot roll forever** [12:46–13:30]: Each roll for a loss trims your net liquidating value. Eventually, margin requirements force you to close the position at a loss. A large cash and sweep balance does not prevent insolvency if the open trade is deeply underwater.

- **Expiration liquidity constraint** [13:47–14:27]: As you roll further out in time, expiration cycles widen (45 → 60 → 70+ days). Rolling a deeply ITM short put far OTM requires rolling out 180+ days to capture credit, limiting flexibility.

- **You can always roll up or down** [14:44–15:06]: There are no directional rules. You can roll up, down, or sideways—but rolling for a debit locks in additional losses. The goal is to roll for a credit or break-even.

- **Loss aversion drives poor rolling habits** [02:58–03:23]: Traders avoid saying "loss" (using quotation marks instead) and rationalize infinite rolling as a way to eventually profit. This is psychological avoidance, not sound risk management.

## Notable quotes

> "A roll is just when we close the trade and we open up a new one very frequently."

> "Rolling does not avoid losses—it realizes the value of the trade."

> "Each time you roll for a loss, your net liquidating value is slowly getting trimmed down."

## Candidate wiki links

**concepts:** [[loss-aversion]], [[realized-vs-unrealized-pnl]], [[net-liquidating-value]], [[expiration-liquidity]], [[mark-to-market]], [[days-to-expiration]], [[moneyness]], [[delta]]

**strategies:** [[rolling-options]], [[short-put]]

**securities:** [[spx]]

**people:** [[eric]]

## Regime / context

Recorded July 2023. This is a foundational mechanics video addressing persistent retail trader misconceptions about rolling options. The examples use simple round numbers (1–3 dollar premiums) for pedagogical clarity; real-world rolls involve more complex Greeks and liquidity dynamics. The core principle—that rolling is a convenience-based accounting concept, not a loss-avoidance mechanism—is regime-independent.
