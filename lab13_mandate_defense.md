
## Part 1: Statement Classification

| Statement | Classification | Reason |
|---|---|---|
| S1 | Hard constraint | The seven-year investment horizon and annual rebalancing schedule establish the time frame and operating rules for the portfolio. |
| S2 | Objective | The foundation aims to earn CPI + 4% annually, net of costs, over rolling five-year periods. |
| S3 | Hard constraint | The foundation must maintain enough cash or daily-liquid government securities to cover four quarterly distributions, equal to 3% of the reserve. |
| S4 | Preference | The 60% global equity and 40% U.S. investment-grade bond benchmark provides a reference for performance evaluation rather than a required allocation. |
| S5 | Hard constraint | The portfolio must be long-only, with no borrowing, short selling, or derivatives. |
| S6 | Hard constraint | No single nonexempt company can represent more than 8% of the portfolio, including its combined securities. |
| S7 | Hard constraint | Annual turnover cannot exceed 25% without committee approval. |
| S8 | Hard constraint | At least 90% of the portfolio must be redeemable within five business days. |
| S9 | Unverifiable promise | A calendar-year loss limit of 10% cannot be guaranteed, and the CIO has not specified how losses or breaches would be measured and handled. |
| S10 | Missing | The CIO has not identified the pilot's optimization objective, leaving a critical portfolio-design decision unresolved. |

## Part 2: Investment Policy Statement (IPS)

### What is an Investment Policy Statement?

An Investment Policy Statement (IPS) is a document that outlines an investor's financial goals, risk tolerance, investment restrictions, and portfolio management guidelines. It helps investment managers make decisions that align with the client's needs.

### How Do Objectives and Constraints Work?

Objectives describe what the investor wants to achieve, such as a target return or acceptable level of risk. Constraints establish boundaries for portfolio construction, including liquidity requirements, investment horizons, concentration limits, and trading restrictions.

A portfolio should satisfy its mandatory constraints while pursuing the client's investment objectives. However, meeting every measurable constraint does not necessarily mean the portfolio is suitable for the client.

### Mapping S1–S10 to the IPS

- **S1 — Investment Horizon:** Establishes a seven-year investment horizon and annual rebalancing schedule.
- **S2 — Return Objective:** Targets CPI + 4% annually, net of costs, over rolling five-year periods.
- **S3 — Liquidity Constraint:** Requires at least $3 million, or 3% of the portfolio, in reserve-eligible assets.
- **S4 — Benchmark:** Uses a 60% global equity and 40% U.S. investment-grade bond portfolio as the performance benchmark.
- **S5 — Investment Restrictions:** Prohibits borrowing, short selling, and derivatives.
- **S6 — Diversification Constraint:** Limits exposure to any single nonexempt company to 8%.
- **S7 — Turnover Constraint:** Limits annual turnover to 25% unless the committee approves otherwise.
- **S8 — Liquidity Requirement:** Requires at least 90% of the portfolio to be redeemable within five business days.
- **S9 — Unresolved Risk Requirement:** The calendar-year loss statement cannot be enforced as written because the measurement method and breach procedure are undefined.
- **S10 — Missing Optimization Objective:** The CIO has not specified what the pilot portfolio should optimize. No sector, ESG, tax, or home-bias preferences have been expressed.

## Part 3: Checker Verification

### Original Portfolio Results

The Python checker evaluated candidates A, B, and C against five measurable investment constraints.

| Rule | Candidate A | Candidate B | Candidate C |
|---|---|---|---|
| Weights sum to 100% | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only (lowest weight) | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve-eligible weight >= 3% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable within 5 days >= 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest company exposure <= 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |

### Final Verdicts

- Candidate A passes every checkable rule.
- Candidate B fails three rules: reserve minimum, liquidity requirement, and issuer concentration.
- Candidate C fails one rule: reserve minimum.

The required reserve is calculated as:

(4 × $0.75 million / $100 million) × 100 = 3.0%

Candidate B's Acme Corp bonds (5%) and stock (4%) are combined because they belong to the same issuer, resulting in a 9% exposure.

### Negative-Weight Probe

To verify that the checker detects violations, I temporarily changed Candidate A's cash allocation from 2% to -2% and its global equity allocation from 60% to 64%.

The modified portfolio produced:

- Total weight: 100.0 — pass
- Lowest weight: -2.0 — FAIL
- Reserve-eligible weight: 10.0 — pass
- Five-day liquidity: 100.0 — pass
- Largest company exposure: 0.0 — pass

Verdict: fails 1 rule(s).

This confirms that the checker identifies a violation of the long-only requirement. After the test, I restored Candidate A to its original weights.

## Part 4: Candidate D — Adversarial Test

### Candidate D Allocation

I constructed Candidate D using a 100% cash allocation.

| Holding | Weight |
|---|---:|
| Cash | 100% |
| Treasury bills | 0% |
| Treasury 10-year note | 0% |
| Global equity index fund | 0% |
| Investment-grade bond fund | 0% |
| Private real estate fund | 0% |
| Acme Corp bonds | 0% |
| Acme Corp stock | 0% |
| Total | 100% |

### Checker Results

| Rule | Result |
|---|---|
| Weights sum to 100% | 100.0 pass |
| Long-only | 0.0 pass |
| Reserve-eligible weight | 100.0 pass |
| Redeemable within five days | 100.0 pass |
| Largest company exposure | 0.0 pass |
| Calendar-year loss | Requires CIO clarification |

Verdict: passes every checkable rule.

### My Independent Judgment

Yes, the CIO could reasonably reject Candidate D even though it passes every checkable rule. A portfolio invested entirely in cash is unlikely to achieve the foundation's CPI + 4% annual return objective over rolling five-year periods, which is established in S2.

### Skeptical Colleague Review

As a skeptical colleague, I would challenge Candidate D using S2 because meeting liquidity, concentration, and long-only requirements does not guarantee that the portfolio will achieve its investment objectives. Although Candidate D passes the Python checker, it may not be suitable for the foundation's long-term return goals.

## Part 5: One Question for the CIO

### My Question

Should the portfolio prioritize maximizing expected returns while meeting the foundation's constraints, or minimizing investment risk while targeting CPI + 4% annually?

### How the Answer Changes the Portfolio

If the CIO prioritizes maximizing expected returns, I would consider a larger allocation to global equities while maintaining the required liquidity reserve and other investment constraints.

If the CIO prioritizes minimizing risk, I would consider a larger allocation to Treasury securities and investment-grade bonds, with a smaller equity allocation.

This decision is necessary before optimization because the portfolio's objective function determines which allocation is considered optimal. S10 identifies this missing instruction.

## Part 6: Reflection

### Why Passing Every Check Is Not Enough

A portfolio can pass every measurable investment constraint and still be unsuitable for the client because the checker only evaluates specific numerical requirements. For example, Candidate D passes every programmed rule but may not achieve the foundation's CPI + 4% return objective. This demonstrates that compliance with portfolio restrictions does not automatically guarantee that the portfolio meets the client's financial goals.

### Most Difficult Statement to Classify

The most difficult statement to classify was S9 because it initially appears to be a hard risk constraint. However, the CIO's statement that the reserve cannot lose more than 10% in a calendar year is not a guarantee that can be reliably enforced. Without a defined loss measure and breach procedure, it remains an unverifiable promise requiring clarification.

## Part 7: Project 2 — Initial Client Mandate

### Client: University Scholarship Endowment

The client is a fictional university scholarship endowment managing a $50 million investment portfolio. The endowment provides annual scholarships to students while seeking long-term capital appreciation.

### Investment Objective

The primary objective is to achieve an annualized return of CPI + 3%, net of investment costs, over rolling five-year periods. The endowment also seeks to preserve sufficient liquidity to fund annual scholarship distributions.

### Hard Constraints

1. Investment Horizon: The endowment has a long-term investment horizon of at least 10 years.

2. Liquidity Requirement: At least 5% of the portfolio must be held in cash or U.S. Treasury bills to support scholarship distributions.

3. Diversification: No single nonexempt company may represent more than 10% of the portfolio.

4. Investment Restrictions: The portfolio must be long-only, with no borrowing, short selling, or derivatives.

5. Liquidity Window: At least 90% of the portfolio must be redeemable within five business days.

6. Rebalancing: The portfolio will be reviewed and rebalanced annually.

### One Unresolved Client Question

Should the endowment prioritize maximizing long-term expected returns or minimizing portfolio volatility while pursuing its CPI + 3% return objective?

The answer would influence the allocation between global equities and fixed-income securities. A return-focused approach would likely favor more equities, while a risk-minimizing approach would generally favor a larger allocation to bonds and Treasury securities.
