# Investment Committee Memorandum

**Company:** Microsoft Corporation (NASDAQ: MSFT)  
**Valuation Date:** September 1, 2026  
**Prepared for:** Investment Committee  
**Analyst:** Misri Shah  
**Recommendation:** WATCH / DEFER

---

## 1. Executive Investment Recommendation

I recommend that the investment committee **defer initiating a new position in Microsoft Corporation** at the September 1, 2026 reference closing price of $501.02.

Microsoft has a strong competitive position in enterprise software, cloud computing, and artificial intelligence. However, my valuation models do not support the current reference price under the assumptions tested.

The FCFF discounted cash flow model estimates intrinsic value at $197.71 per diluted share, while the FCFE pro-forma model produces $116.94 per share. A two-company P/E comparison using Oracle and Adobe produces a median-implied valuation of $371.30 per share.

These approaches differ significantly in methodology and assumptions, so their results should not be averaged into a single price target. Nevertheless, all three estimates fall below the reference market price.

**Investment decision:** Maintain Microsoft on the watchlist, monitor fundamental performance and valuation, and reconsider an investment when the risk-adjusted return becomes more attractive or when new evidence justifies revising the assumptions.

## 2. Business and Competitive Position

Microsoft operates across three principal segments: Productivity and Business Processes, Intelligent Cloud, and More Personal Computing.

The company's competitive advantages include its enterprise customer relationships, Microsoft 365 ecosystem, Azure cloud infrastructure, software distribution capabilities, and integration of AI technologies across products and services.

Microsoft's business benefits from recurring subscriptions, customer switching costs, enterprise integration, and the scale of its cloud infrastructure.

At the same time, Microsoft's AI strategy requires substantial investment in data centers, computing infrastructure, and other capital-intensive resources. The timing and magnitude of returns on these investments remain uncertain.

## 3. Valuation Summary

| Valuation Method | Estimated Value per Share |
|---|---:|
| FCFF DCF | $197.71 |
| FCFE Pro-Forma | $116.94 |
| Comparable-Company P/E | $371.30 |
| Reference Market Price | $501.02 |

### FCFF DCF

The FCFF model uses FY2026 starting free cash flow to the firm of $69,446.2199 million, projected annual FCFF growth of 15%, 13%, 11%, 9%, and 7%, a 10% WACC, and 3% perpetual terminal growth.

The model produces an enterprise value of approximately $1,436,982.92 million and an equity value of approximately $1,473,531.92 million.

Dividing by 7,453 million diluted shares results in an estimated intrinsic value of **$197.71 per share**.

Approximately 74.28% of enterprise value comes from the present value of the terminal value, indicating substantial dependence on long-run assumptions.

### FCFE Pro-Forma

The FCFE pro-forma model uses projected revenue growth, gross margins, operating expenses, depreciation, capital expenditures, and taxes to estimate future equity cash flows.

Its base-case equity valuation is **$116.94 per share**.

This result is a separate equity cash-flow scenario and should not be treated as directly interchangeable with the FCFF model without reconciling differences in cash-flow definitions, financing assumptions, and reinvestment.

### Comparable-Company Analysis

The comparable-company model uses Oracle and Adobe as reference peers.

| Company | P/E Multiple |
|---|---:|
| Oracle | 24.24x |
| Adobe | 17.13x |
| Peer Median | 20.69x |

Applying the median multiple to Microsoft's modeled EPS of $17.95 gives an implied valuation of **$371.30 per share**.

The peer-implied range is $307.49 to $435.11 per share. Because only two peers are used, the result is particularly sensitive to peer selection. Differences in growth, profitability, business mix, and EPS measurement also limit comparability.

## 4. Sensitivity Analysis

The FCFF valuation changes substantially with the WACC and terminal growth assumptions.

| WACC | Terminal Growth 2% | Terminal Growth 3% | Terminal Growth 4% |
|---|---:|---:|---:|
| 9% | $204.33 | $230.77 | $267.78 |
| **10%** | $178.59 | **$197.71** | $223.20 |
| 11% | $158.60 | $172.94 | $191.38 |

Across all nine tested scenarios, estimated intrinsic value remains below the $501.02 reference price.

The model's reverse-DCF calculation also found no solution within its configured uniform explicit-growth shift range of −5 to +10 percentage points. This does not prove that the market price cannot be justified; it means that the tested range was insufficient under the model's other fixed assumptions.

## 5. Key Investment Risks

**AI infrastructure spending:** Significant capital expenditures may reduce near-term free cash flow and generate returns later than expected.

**Cloud competition:** Competition from other hyperscale cloud providers and AI platforms may constrain growth or profitability.

**Valuation risk:** A strong underlying business may still be an unattractive investment when its market price assumes higher future cash flows than the analyst's forecast supports.

**Model risk:** The DCF valuation depends heavily on terminal value, discount rates, forecast cash flows, and treatment of cash and debt.

**Peer selection risk:** Oracle and Adobe do not perfectly represent Microsoft's diversified business mix, and the two-peer sample provides limited valuation evidence.

## 6. Conditions That Could Change the Recommendation

I would reconsider the watch/defer recommendation if one or more of the following developments occurred:

1. Microsoft's market price declined sufficiently to create an attractive margin of safety relative to a revised, supportable valuation.
2. Azure, Microsoft 365, and AI monetization generated sustained cash-flow growth above the current model assumptions.
3. Capital expenditure intensity declined without materially weakening Microsoft's competitive position.
4. A revised forecast supported materially higher intrinsic value based on documented operating improvements rather than unsupported terminal-growth assumptions.
5. Additional peer and valuation evidence supported a higher valuation after accounting for business-model differences.

## 7. Validation and Limitations

The historical FY2026 operating cash flow, capital expenditures, interest expense, and tax inputs were checked against Microsoft's FY2026 Form 10-K.

The September 1, 2026 reference closing price of $501.02 was checked against Yahoo Finance historical prices.

The valuation outputs were reproduced using Python scripts in the project repository.

The analysis remains subject to important limitations, including the simplified FCFF forecast, the differences between FCFF and FCFE methodologies, the limited comparable-company set, and uncertainty surrounding long-term AI infrastructure returns.

The valuation figures are scenario estimates rather than guarantees of future market prices.

## 8. Final Committee Decision

**Recommendation: WATCH / DEFER**

Microsoft remains a compelling business to monitor, but the evidence in the current valuation framework does not support initiating a new position at $501.02 per share.

The committee should revisit the investment as new earnings, capital expenditure, cloud growth, and free-cash-flow information becomes available.

---

## Sources and Reproducibility

**Primary source:** [Microsoft FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm)

**Historical market price:** [Yahoo Finance — MSFT Historical Data](https://finance.yahoo.com/quote/MSFT/history/)

**Reproducible analysis files:**
- `dcf.py`
- `msft_proforma.py`
- `comps.py`
- `project1_reconciliation.py`
- `app.py`

**Supporting documents:**
- `Project_1_Edition_A_MSFT.md`
- `Project_1_Edition_B_MSFT.md`
- `project1_source_verification.md`
- `project1_valuation_reconciliation.md`
- `project1_validation.md`

**AI-use disclosure:** AI assistance was used to support organization, and code review. I am  responsible for verifying the financial inputs, interpreting the valuation results, and making the final investment recommendation.