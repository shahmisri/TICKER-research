# Lab 14 — Portfolio Baselines

**Course:** FIN 43900 — Equity Research  
**Topic:** Portfolio Risk and Mandate Compliance

## 1. Portfolio Baseline Results

I created `portfolio.py` to calculate expected portfolio returns, volatility, reserve-eligible weights, and whether each portfolio meets the foundation's 6.5% return objective.

| Portfolio | Expected Return | Volatility | Reserve Eligible | Meets Return Objective |
|---|---:|---:|---:|---|
| Benchmark | 6.80% | 10.46% | 0.0% | Yes |
| Equal Weight | 5.20% | 5.21% | 50.0% | No |
| Inverse Volatility | 3.77% | 1.05% | 90.3% | No |

## 2. Diversification and Correlation

Combining risky assets can reduce overall portfolio risk because the assets do not always move together. Portfolio volatility depends on each asset's individual risk, portfolio weights, and the correlations between assets.

The benchmark consists of 40% investment-grade bonds and 60% global equities. Its calculated volatility is 10.46%.

When I increased the correlation between investment-grade bonds and global equities from 0.25 to 0.50, benchmark volatility increased to 11.00%. This shows that higher positive correlation reduces diversification benefits.

I also tested an invalid correlation of 1.20. The program correctly rejected the input with a `ValueError`.

## 3. Mandate Compliance — Candidate E

I updated `mandate.py` to include Candidate E, consisting of:

- 40% investment-grade bond fund
- 60% global equity index fund

Candidate E meets the 6.5% expected return objective but fails the foundation's 3% reserve requirement.

The mandate checker produced the following results:

| Requirement | Result |
|---|---|
| Weights sum to 100% | Pass |
| Long-only | Pass |
| Reserve eligible weight | Fail — 0.0% |
| Redeemable within five days | Pass |
| Single-company exposure | Pass |
| Calendar-year loss | Requires CIO clarification |

**Conclusion:** Candidate E fails one checkable mandate rule. A portfolio can satisfy its return objective while still being unsuitable under the foundation's investment restrictions.

## 4. Initial Fund Universe for Project 2

The following funds are proposed for the next stage of portfolio analysis.

| Ticker | Fund Name | Portfolio Role |
|---|---|---|
| BIL | SPDR Bloomberg 1–3 Month T-Bill ETF | Treasury bill exposure |
| IEF | iShares 7–10 Year Treasury Bond ETF | Government bond exposure |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Investment-grade corporate bonds |
| VT | Vanguard Total World Stock ETF | Global equity exposure |

These four funds represent the asset classes used in the portfolio baseline exercise.

For the next stage, I will use five years of monthly adjusted closing prices, arranged chronologically, to evaluate historical portfolio behavior.

## 5. Conclusion

The benchmark is the only one of the three baseline portfolios that meets the expected return objective, but it does not meet the reserve requirement. The equal-weight and inverse-volatility portfolios provide more reserve-eligible exposure but have expected returns below the objective.

The analysis demonstrates why portfolio construction requires evaluating expected return, risk, diversification, and mandate compliance together.
