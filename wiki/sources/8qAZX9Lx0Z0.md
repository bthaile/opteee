---
type: source
title: "Ratio Call Diagonal (LEAPS) Option Strategy"
video_id: 8qAZX9Lx0Z0
url: https://www.youtube.com/watch?v=8qAZX9Lx0Z0
date: 2022-05-17
series: options-trench
format: [education, strategy-breakdown]
experts: [eric]
mentions: []
securities: [vlo]
concepts: [delta, delta-hedging, delta-neutral, days-to-expiration, deep-itm-calls, extrinsic-value, greeks, implied-volatility, intrinsic-value, leverage, liquidity-cycle, moneyness, position-sizing, risk-management, theta, theta-decay, vega, volatility-term-structure]
strategies: [ratio-call-diagonal, covered-call, leaps, long-call]
saga: null
part: null
confidence: high
---

# Ratio Call Diagonal (LEAPS) Option Strategy

## Summary

The ratio call diagonal is a multi-leg options strategy combining long calls (typically far out-of-the-money in time, deep in-the-money in strike) with short calls at a ratio less than 1:1, creating unlimited upside exposure while capping downside risk to the initial debit. By selling fewer short calls than long calls, the trader eliminates the upside risk inherent in traditional diagonals and covered calls, while benefiting from theta decay and potential implied volatility expansion.

## Key takeaways

- **Strategy structure** [00:46–01:38]: A diagonal uses long calls instead of long stock (like a covered call), with different expirations and strikes. The ratio diagonal sells short calls at a ratio *less than* 1:1 to the long calls, eliminating upside risk and creating unlimited profit potential.

- **Why deep in-the-money long calls** [07:12–08:35]: Trading 80+ delta long calls far out in time (90–257 days) minimizes theta decay (less than a penny per day), reduces vega sensitivity, and captures more of the underlying's move per dollar of premium paid.

- **Liquidity is critical** [13:56–15:05]: Check bid–ask spreads and open interest on long calls, especially for far-dated expirations. Shallow liquidity can trap you in a profitable position you cannot exit; prefer index ETFs, sector ETFs, and S&P 500 stocks.

- **Portfolio allocation and initial outlay** [15:45–17:10]: Set aside a fixed allocation (e.g., $25,000) before entering the trade to avoid emotional bias. Use only 50–80% of that allocation for the initial outlay, reserving capital to scale in on ~5% moves in your favor or against you.

- **Long-side setup** [18:15–19:15]: Choose a base expiration (typically 6 months to 1 year+), use 80+ delta, and size based on your allocation. Short calls should be 20–40 days to expiration to maximize theta decay harvesting and allow rolling.

- **Delta ratio formula** [20:20–21:07]: Maintain `(# long calls × long delta) / (2.1 × # short call deltas) ≥ 1` to ensure no upside risk and uncapped upside. In the example, 6 long calls (100 delta each = 600 total) vs. 3 short calls (100 delta each = 300 total) yields 300 excess deltas.

- **Exit when short calls are out-of-the-money** [22:15–22:35]: Close the entire trade at ~70% max profit. If short calls fall in-the-money, close the whole position for a profit rather than risk naked short calls.

- **Exit when short calls are in-the-money (advanced)** [22:35–24:27]: Sell one long call to gauge liquidity, then close all short calls at once, then close remaining longs. Alternatively, use long calls to cover the debit cost of closing short calls at a loss, realizing net profit from the long appreciation.

- **Critical strike calculation** [24:49–27:50]: The critical strike tells you the maximum short-call strike where you won't lock in a loss. Formula: `(adjusted long basis − current long price) / (current long delta) + stock price`. Use this to manage rolling short calls and maintain profitability.

- **Ratio trade-off** [12:19–13:32]: Selling more short calls collects more premium upfront but surrenders upside potential; selling fewer short calls collects less premium but preserves more upside. Adjust the ratio based on your risk tolerance and market outlook.

## Notable quotes

> "The main reason why I like to trade it at a ratio is it has a very different and in my opinion more advantageous risk–reward profile." [01:58]

> "Theta decay is the highest for at-the-money options and it obviously accelerates as we get closer to expiration, so we're doing two things to decrease the theta decay: we're going far out in time and then we are also going deep in the money." [07:54]

> "Liquidity can absolutely become an issue. Trading liquid underlyings is super important for this strategy because otherwise you might be able to worm your way into the strategy but you can get stuck pretty bad if you can't exit the trade for a profit." [14:44]

## Candidate wiki links

**Concepts:**
[[delta]], [[delta-hedging]], [[days-to-expiration]], [[deep-itm-calls]], [[greeks]], [[implied-volatility]], [[leverage]], [[liquidity-cycle]], [[position-sizing]], [[risk-management]], [[theta]], [[theta-decay]], [[vega]]

**Strategies:**
[[covered-call]], [[leaps]], [[long-call]], [[ratio-call-diagonal]]

**Securities:**
[[vlo]]

**People:**
[[eric]]

## Regime / context

Recorded May 17, 2022. The strategy is evergreen and applicable across market regimes, though the video emphasizes bullish setups and benefits from implied volatility expansion. The VLO example reflects mid-2022 energy sector conditions. This is a foundational education video on a core strategy in Eric's options-trading curriculum; no saga affiliation.
