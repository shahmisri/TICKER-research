# Project 1 — Edition B: Microsoft Equity Research

**Company:** Microsoft Corporation (NASDAQ: MSFT)  
**Valuation date:** September 1, 2026  
**Analyst role:** Buy-side equity research analyst  
**Investment committee position:** No existing Microsoft position  
**Recommendation:** **WATCH / DEFER**  
**Primary financial source:** Microsoft FY2026 Form 10-K, fiscal year ended June 30, 2026  
**Valuation currency:** USD; financial statement amounts in millions unless otherwise indicated

---

## 1. Executive Summary and Investment Recommendation

I recommend **watch/defer** rather than initiating a position in Microsoft Corporation at the September 1, 2026 reference share price of $501.02.

Microsoft is a high-quality technology company with strong positions in enterprise software, cloud infrastructure, productivity applications, and artificial intelligence. Its recurring revenue streams, enterprise customer relationships, and expanding cloud business provide meaningful long-term growth opportunities.

However, business quality does not automatically establish investment attractiveness at a particular market price.

My updated valuation analysis produces three reference estimates:

| Valuation methodology | Estimated value per share |
|---|---:|
| FCFE pro-forma valuation | $116.94 |
| FCFF discounted cash flow valuation | $197.71 |
| Comparable-company median P/E valuation | $371.30 |
| Reference market price | $501.02 |

All three model estimates fall below the reference share price.

The intrinsic valuation models are particularly sensitive to Microsoft's future free-cash-flow generation, AI infrastructure investment, and long-term growth assumptions. The comparable-company valuation produces a higher estimate but remains below the reference price and is sensitive to peer selection.

My recommendation is therefore to continue monitoring Microsoft rather than initiate a position without a stronger margin of safety.

**Model status:** The FCFF DCF, FCFE pro-forma, and comparable-company calculations are reproducible using the Python scripts in the project repository. Microsoft's FY2026 operating cash flow, capital expenditures, and September 1, 2026 reference closing price have been checked against their respective sources. The comparable-company price and EPS conventions require further verification, and the FCFF and FCFE models remain methodologically distinct rather than fully reconciled.

## 2. Evolution of the Investment Thesis From Edition A

Edition A established an initial **watch/defer** recommendation.

At that stage, I identified Microsoft as a financially strong business with compelling cloud growth but concluded that additional valuation work was necessary before recommending an investment.

The initial research emphasized:

- Strong Azure and Microsoft Cloud growth.
- Microsoft's established enterprise software ecosystem.
- Significant spending on AI infrastructure.
- Uncertainty about future margins and free-cash-flow conversion.
- The need to distinguish business quality from valuation attractiveness.

Edition B incorporates quantitative analysis completed during the course.

### Research Progression

| Area | Edition A | Edition B |
|---|---|---|
| Investment thesis | Initial watch/defer | Watch/defer supported by valuation analysis |
| Financial research | FY2026 10-K review | Historical input verification and forecasting |
| FCFF DCF | Planned | Completed; $197.71/share |
| Three-statement model | Planned | Simplified FY2027–2031 pro-forma completed |
| FCFE valuation | Not available | $116.94/share |
| Comparable-company analysis | Planned | Oracle and Adobe P/E comparison |
| Sensitivity analysis | Planned | Discount-rate, terminal-growth, revenue-growth, and margin scenarios |
| Model validation | Planned | Accounting and scenario checks |
| Interactive model | Not available | Streamlit valuation workbench |

The original recommendation has not changed, but the supporting evidence has become more quantitative and testable.

## 3. Company Overview and Business Fundamentals

Microsoft operates a diversified technology business with activities in productivity software, enterprise cloud infrastructure, business applications, personal computing, gaming, and digital advertising.

The company benefits from established enterprise relationships, subscription-based revenue, and a broad portfolio of products and services.

Its major growth opportunities include Azure cloud infrastructure, Microsoft 365, Dynamics, security products, and AI-enabled software and services.

### FY2026 Operating Evidence

According to Microsoft's FY2026 Form 10-K:

- Microsoft Cloud revenue increased 27% to approximately $214.4 billion.
- Azure and other cloud services revenue increased 41%.
- Consolidated revenue increased approximately 18%.
- Microsoft Cloud gross margin declined to approximately 66%.

These figures illustrate strong demand for Microsoft's cloud services alongside meaningful infrastructure-related cost pressure.

The central question is whether cloud and AI revenue growth will ultimately translate into sufficient incremental free cash flow to justify the capital invested.

### Financial Strength

The FY2026 balance sheet figures used in the analysis include:

| Financial item | Amount ($m) |
|---|---:|
| Revenue | 331,839 |
| Total assets | 758,376 |
| Total liabilities | 315,989 |
| Stockholders' equity | 442,387 |
| Cash and cash equivalents | 20,935 |
| Short-term investments | 55,908 |
| Current and long-term debt | 40,294 |

Cash and short-term investments total $76,843 million, compared with $40,294 million of current and long-term debt.

This provides Microsoft with financial flexibility, although liquidity does not eliminate the risks associated with large infrastructure investments.

## 4. Industry Position and Competitive Risks

Microsoft benefits from strong competitive positions in enterprise software and cloud computing.

Its integrated product ecosystem creates opportunities to distribute AI capabilities through existing customer relationships and software subscriptions.

However, several risks remain relevant.

**Cloud competition:** Microsoft competes with other major cloud infrastructure and software providers. Competition may influence pricing, customer acquisition, and infrastructure economics.

**AI capital intensity:** AI services require substantial investment in data centers, computing infrastructure, and related assets.

**Margin pressure:** Higher depreciation, infrastructure operating costs, and changing product mix could reduce margins.

**Cybersecurity and regulatory exposure:** Security incidents, privacy issues, and regulatory restrictions could affect Microsoft's costs, operations, or customer relationships.

**Forecast uncertainty:** Rapid technological change makes it difficult to predict sustainable long-term growth and returns on invested capital.

These risks are incorporated into the valuation analysis through forecast assumptions, sensitivity tests, and a cautious investment recommendation.

## 5. FCFF Discounted Cash Flow Valuation

The FCFF model estimates Microsoft's operating enterprise value by forecasting free cash flow to the firm and discounting those cash flows using the weighted average cost of capital.

A terminal value captures cash flows beyond the explicit five-year forecast period.

### 5.1 Model Assumptions

| Assumption | Base-case input |
|---|---:|
| Starting FY2026 FCFF | $69,446.2199 million |
| FY2027 FCFF growth | 15% |
| FY2028 FCFF growth | 13% |
| FY2029 FCFF growth | 11% |
| FY2030 FCFF growth | 9% |
| FY2031 FCFF growth | 7% |
| WACC | 10% |
| Terminal growth rate | 3% |
| Cash and short-term investments adjustment | $76,843 million |
| Debt adjustment | $40,294 million |
| Diluted share denominator | 7,453 million |

The declining growth path reflects an assumption that Microsoft's free-cash-flow growth moderates over time.

The 10% WACC and 3% terminal growth rate are analyst assumptions, not directly reported financial statement figures. Their reasonableness must be evaluated through sensitivity analysis.

The model uses FY2026 diluted weighted-average shares as its working denominator. This differs from actual shares outstanding at the valuation date and represents a simplifying convention.

### 5.2 Starting Free Cash Flow

The provisional starting FCFF is calculated as:

FCFF = Operating cash flow + After-tax interest adjustment − Capital expenditures

Using the working inputs:

FCFF = 182,935 + 2,459.2199 − 115,948

**Starting FCFF = $69,446.2199 million**

The FY2026 operating cash flow of $182,935 million and capital expenditures of $115,948 million were checked against Microsoft's FY2026 Form 10-K. The after-tax interest adjustment of $2,459.2199 million was calculated using interest expense of $3,051 million and an effective tax rate derived from reported income before taxes and income tax expense. These inputs support the revised starting FCFF of $69,446.2199 million.

### 5.3 Five-Year FCFF Forecast

| Fiscal year | Forecast FCFF ($m) |
|---|---:|
| FY2027 | 79,863.2 |
| FY2028 | 90,245.4 |
| FY2029 | 100,172.4 |
| FY2030 | 109,187.9 |
| FY2031 | 116,831.0 |

### 5.4 Enterprise-to-Equity Valuation Bridge

| Valuation component | Amount ($m) |
|---|---:|
| Present value of explicit FCFF | 369,566.4 |
| Present value of terminal value | 1,067,416.5 |
| Enterprise value | 1,436,982.9 |
| Add: cash and short-term investments | 76,843.0 |
| Less: debt | (40,294.0) |
| Equity value | 1,473,531.9 |
| Diluted shares (millions) | 7,453 |
| **Value per diluted share** | **$197.71** |

The terminal value represents approximately 74% of enterprise value.

This creates substantial sensitivity to long-term assumptions, particularly WACC and terminal growth.

The bridge is simplified and does not separately adjust for every possible nonoperating asset or non-common claim. The classification of cash, leases, pensions, and other liabilities requires consistent treatment before the model is considered fully reconciled.

## 6. FCFE Pro-Forma Financial Model

A separate financial model was developed to forecast Microsoft's financial statements and estimate free cash flow to equity.

The model projects FY2027 through FY2031 and incorporates revenue growth, profitability, depreciation, capital expenditures, and selected balance-sheet assumptions.

### 6.1 Key Operating Assumptions

| Assumption | Base case |
|---|---:|
| FY2027–FY2031 revenue growth | 12%, 11%, 10%, 9%, 8% |
| Gross margin | 68% |
| Operating expenses / revenue | 21.2% |
| Depreciation / opening PP&E | 12.3% |
| Tax rate | 19.4% |
| Inventory days | 5 |
| Cost of equity | 10% |
| Terminal growth | 3% |

### 6.2 Capital Expenditure Forecast

Microsoft's cloud and AI infrastructure investments are central to the financial forecast.

| Fiscal year | Forecast capital expenditures ($m) |
|---|---:|
| FY2027 | 120,000 |
| FY2028 | 125,000 |
| FY2029 | 130,000 |
| FY2030 | 135,000 |
| FY2031 | 140,000 |

These amounts are analyst forecast assumptions rather than management guidance.

The elevated investment path reflects the possibility that Microsoft's AI and cloud expansion requires sustained infrastructure spending.

### 6.3 Revenue and FCFE Forecast

| Fiscal year | Revenue ($m) | FCFE ($m) |
|---|---:|---:|
| FY2027 | 371,659.7 | 26,635.0 |
| FY2028 | 412,542.2 | 39,032.5 |
| FY2029 | 453,796.5 | 51,409.6 |
| FY2030 | 494,638.2 | 63,545.0 |
| FY2031 | 534,209.2 | 75,129.9 |

Revenue and FCFE increase across the projection period, but the model assumes substantial ongoing capital investment.

### 6.4 FCFE Valuation Results

| Valuation component | Amount ($m) |
|---|---:|
| Present value of explicit FCFE | 185,148.6 |
| Present value of terminal value | 686,417.7 |
| Equity value | 871,566.2 |
| **Value per diluted share** | **$116.94** |

The FCFE valuation is lower than the FCFF valuation.

The difference should not be interpreted as an error in arithmetic. The models use different cash-flow definitions and assumptions and have not been fully reconciled economically.

## 7. Comparable-Company Valuation

To complement the intrinsic valuation models, I conducted a relative valuation analysis using Oracle Corporation and Adobe Inc.

Oracle was selected because of its enterprise software and cloud infrastructure exposure.

Adobe was selected because of its subscription-based software model and recurring revenue characteristics.

Neither company is a perfect comparable for Microsoft. Microsoft differs in business diversification, cloud scale, profitability, growth opportunities, and capital intensity.

### 7.1 P/E Multiple Comparison

| Company | Reference price | EPS | P/E |
|---|---:|---:|---:|
| Microsoft (MSFT) | $501.02 | $17.95 | 27.91x |
| Oracle (ORCL) | $141.32 | $5.83 | 24.24x |
| Adobe (ADBE) | $286.08 | $16.70 | 17.13x |

The peer median P/E multiple is approximately **20.69x**.

Applying this multiple to Microsoft's reference EPS of $17.95 produces a median-implied valuation of **$371.30 per share**.

The peer-implied valuation range is **$307.49–$435.11 per share**.

These calculations reproduce the results from `comps.py`. The historical price inputs and EPS definitions still require independent verification to establish consistent valuation-date conventions.

### 7.2 Leave-One-Out Sensitivity

| Excluded company | Remaining implied MSFT price | Change from median |
|---|---:|---:|
| Oracle | $307.49 | −$63.81 |
| Adobe | $435.11 | +$63.81 |

The substantial changes demonstrate that the estimate is sensitive to peer selection.

Because the analysis includes only two peers, the median multiple should be treated as a cross-check rather than a precise measure of fair value.

### 7.3 Interpretation

The peer median-implied value of $371.30 is higher than both intrinsic valuation estimates.

This may reflect differences in forecast assumptions, cash-flow conversion, growth expectations, and the limitations of applying simplified valuation methods to Microsoft's business.

However, the peer-implied valuation remains below the reference share price of $501.02.

The comparable-company analysis therefore provides additional support for maintaining a cautious investment recommendation.

## 8. Sensitivity Analysis and Downside Testing

Sensitivity analysis was conducted to determine how changes in operating and valuation assumptions affect estimated intrinsic value.

### 8.1 FCFF Discount Rate and Terminal Growth Sensitivity

The FCFF discounted cash flow model evaluates how changes in the weighted average cost of capital (WACC) and perpetual terminal growth rate affect Microsoft's estimated intrinsic value.

The analysis uses the revised FY2026 starting FCFF of $69,446.2199 million.

**Sensitivity Grid — Estimated Value per Diluted Share**

| WACC | Terminal Growth 2% | Terminal Growth 3% | Terminal Growth 4% |
|---|---:|---:|---:|
| 9% | $204.33 | $230.77 | $267.78 |
| **10% (Base)** | $178.59 | **$197.71** | $223.20 |
| 11% | $158.60 | $172.94 | $191.38 |

**Key Findings**

The base-case valuation is $197.71 per diluted share, using a 10% WACC and 3% terminal growth rate.

The lowest valuation in the tested sensitivity grid is $158.60 per share, assuming an 11% WACC and 2% terminal growth rate.

The highest valuation is $267.78 per share, assuming a 9% WACC and 4% terminal growth rate.

The valuation range demonstrates that Microsoft's estimated intrinsic value is highly sensitive to discount-rate and terminal-growth assumptions.

Even the highest valuation in this grid remains below the September 1, 2026 reference price of $501.02 used in the model.

**Investment Interpretation**

The sensitivity analysis reinforces the watch/defer recommendation. Under all nine tested combinations of WACC and terminal growth, the estimated intrinsic value remains below the reference market price.

However, the results depend on the model's underlying FCFF forecast, financing assumptions, and terminal-value methodology. They should not be interpreted as a complete range of all possible outcomes.

### 8.2 Revenue Growth Sensitivity

The pro-forma model tests changes to the FY2027–FY2031 revenue growth path.

The base-case growth assumptions are 12%, 11%, 10%, 9%, and 8%.

A higher-growth scenario adds two percentage points to each forecast year.

Under the previously tested higher-growth scenario, estimated FCFE value increased from $116.94 to approximately **$144.44 per share**.

This demonstrates the importance of sustained revenue expansion.

### 8.3 Gross Margin Sensitivity

The base gross-margin assumption is 68%.

Under a tested 70% gross-margin scenario, the model produced an estimated value of approximately **$131.18 per share**.

This shows that improvements in operating profitability can increase estimated equity value.

### 8.4 Capital Expenditure Sensitivity

The interactive workbench also allows changes to the capital spending forecast.

Higher capital expenditures generally reduce cash available to equity investors unless the additional investment produces offsetting future operating benefits.

This is a particularly important risk for Microsoft because of the scale of AI infrastructure investment.

### 8.5 Sensitivity Conclusion

The tested scenarios demonstrate that Microsoft's valuation is sensitive to revenue growth, operating profitability, capital spending, and discounting assumptions.

The results reinforce the need for a margin of safety rather than relying on a single point estimate.

## 9. FCFF and FCFE Valuation Reconciliation

The FCFF and FCFE models produce materially different equity values.

### 9.1 Annual Cash Flow Comparison

| Fiscal year | FCFF ($m) | FCFE ($m) | Difference ($m) |
|---|---:|---:|---:|
| FY2027 | 79,863.2 | 26,635.0 | 53,228.1 |
| FY2028 | 90,245.4 | 39,032.5 | 51,212.8 |
| FY2029 | 100,172.4 | 51,409.6 | 48,762.8 |
| FY2030 | 109,187.9 | 63,545.0 | 45,642.8 |
| FY2031 | 116,831.0 | 75,129.9 | 41,701.1 |

These figures compare two distinct cash-flow measures, not economically interchangeable quantities.

### 9.2 Valuation Component Comparison

| Component | FCFF DCF ($m) | FCFE pro-forma ($m) |
|---|---:|---:|
| PV of explicit cash flows | 369,566.4 | 185,148.6 |
| PV of terminal value | 1,067,416.5 | 686,417.7 |
| Equity value | 1,473,531.9 | 871,566.2 |
| Value per diluted share | $197.71 | $116.94 |

The valuation difference is approximately **$80.77 per share**.

### 9.3 Reasons for the Difference

The two models differ in several ways.

**Cash-flow definition:** FCFF measures cash flow available to providers of debt and equity capital, while FCFE measures cash flow available to equity holders.

**Forecast construction:** The FCFF model applies growth assumptions to starting FCFF. The FCFE model derives cash flow from a more detailed operating and balance-sheet forecast.

**Capital expenditures:** The FCFE model explicitly forecasts substantial capital spending throughout FY2027–FY2031.

**Terminal value:** The models use different final-year cash-flow levels, producing materially different terminal values.

**Enterprise-to-equity bridge:** The FCFF model separately adjusts enterprise value for cash and debt. The FCFE model values equity directly.

A complete economic reconciliation would require aligning operating forecasts, financing flows, discount rates, and nonoperating adjustments.

The current comparison is therefore descriptive rather than a proof that both models are internally equivalent.

**Supporting file:** `project1_valuation_reconciliation.md`.

## 10. Interactive Valuation Workbench

I developed a Streamlit application to allow users to explore Microsoft's valuation assumptions interactively.

The application provides controls for:

- Revenue growth adjustments.
- Gross-margin assumptions.
- Capital expenditure multipliers.
- Cost of equity.
- FCFE terminal growth.
- WACC.
- FCFF terminal growth.
- Minimum cash requirements.

The workbench displays the FCFE and FCFF valuation estimates, projected financial statements, and validation warnings.

### Base-Case Dashboard Outputs

| Metric | Result |
|---|---:|
| FCFE pro-forma / share | $116.94 |
| FCFF DCF / share | $197.71 |
| FY2031 revenue | $534,209 million |
| FY2031 FCFE | $75,130 million |

The application was restarted after the FCFF model update, and the revised FCFF result was confirmed in the dashboard.

The two valuation models remain separate. Revenue, margin, and capital expenditure controls primarily affect the FCFE model, while WACC and FCFF terminal growth affect the independent FCFF DCF.

The dashboard does not represent a fully reconciled single valuation model.

**Supporting file:** `app.py`.

## 11. Model Validation and Quality Control

The financial modeling process included numerical, accounting, and scenario checks.

### 11.1 Reproducibility

The FCFF model was executed using `dcf.py`.

The FCFE pro-forma was executed using `msft_proforma.py`.

The comparable-company analysis was executed using `comps.py`.

The reconciliation results were reproduced using `project1_reconciliation.py`.

### 11.2 Accounting Validation

The pro-forma model includes checks for balance-sheet consistency and other financial constraints.

The base-case model passed its reported balance-sheet checks.

### 11.3 Failure and Recovery Test

The Streamlit workbench was tested using an elevated minimum cash requirement.

When the minimum cash requirement was increased to $100,000 million, the application displayed a validation warning.

Restoring the minimum cash requirement to zero returned the model to its base-case configuration.

This demonstrates that the application can identify and communicate at least one invalid or constrained scenario.

### 11.4 Historical Input Review

The original DCF used a starting FCFF of $69,408.2199 million.

The original DCF used a starting FCFF of $69,408.2199 million. After reviewing Microsoft's FY2026 Form 10-K, the operating cash flow and capital expenditure inputs were corrected, increasing starting FCFF to $69,446.2199 million.

This correction increased the estimated FCFF valuation from approximately $197.60 to $197.71 per diluted share. The revised historical inputs and after-tax interest calculation are documented in `2026-09-10_MSFT_DCF_Inputs.md`.

**Supporting files:** `project1_validation.md` and `project1_source_verification.md`.

## 12. Investment Decision and Margin of Safety

The September 1, 2026 reference share price used in the models is $501.02.

### Valuation Comparison

| Method | Estimated value | Difference from reference price |
|---|---:|---:|
| FCFE pro-forma | $116.94 | −$384.08 |
| FCFF DCF | $197.71 | −$303.31 |
| Peer median P/E | $371.30 | −$129.72 |
| Reference share price | $501.02 | — |

The estimates do not establish a margin of safety at the reference price.

The comparable-company analysis produces the highest estimated value, but even its upper peer-implied estimate of $435.11 is below the reference price.

The intrinsic models are also subject to meaningful forecast and methodology uncertainty.

Given these findings, I would not recommend initiating a Microsoft position based solely on the current evidence.

### Conditions That Could Change the Recommendation

I would reconsider the recommendation if:

1. Microsoft demonstrated sustained improvement in free-cash-flow conversion from AI and cloud investments.
2. Revenue growth and operating margins exceeded conservative expectations without requiring proportionately higher capital expenditures.
3. A revised and validated intrinsic valuation indicated a sufficient margin of safety relative to the market price.
4. Additional evidence supported higher sustainable returns on infrastructure investment.

The thesis would weaken further if cloud growth slowed materially, capital expenditures remained elevated without sufficient cash-flow improvement, or operating margins deteriorated.

## 13. Falsification and Investment Risks

A central falsification question is:

**What evidence would demonstrate that Microsoft's AI infrastructure investments are generating sufficient incremental free cash flow to justify a higher intrinsic valuation and change the watch/defer recommendation?**

This question connects the investment thesis to measurable financial outcomes rather than relying only on a favorable narrative.

Relevant indicators include Azure revenue growth, cloud gross margins, capital expenditures, depreciation, free-cash-flow conversion, and returns on invested capital.

This is an analyst-formulated question unless separately confirmed as the actual wording of a partner's question.

## 14. AI Use and Analyst Responsibility

AI assistance was used to support research organization, Python troubleshooting, model documentation, draft writing, and the preparation of financial analysis materials.

The analyst remains responsible for verifying primary-source financial information, selecting and defending model assumptions, interpreting results, and making the investment recommendation.

AI-generated explanations and calculations were checked against model outputs where possible.

Remaining unverified assumptions and methodological limitations are disclosed rather than presented as established facts.

## 15. Final Investment Conclusion

Microsoft has substantial competitive strengths and meaningful opportunities in cloud computing, enterprise software, and artificial intelligence.

However, my investment decision must consider valuation, capital intensity, forecast uncertainty, and downside risk.

The FCFF DCF estimates approximately $197.71 per share, the FCFE pro-forma estimates approximately $116.94 per share, and the comparable-company median P/E analysis implies approximately $371.30 per share.

All three estimates are below the $501.02 reference market price used in the analysis.

The results support maintaining a **WATCH / DEFER** recommendation rather than initiating a position.

The historical FY2026 cash-flow inputs and September 1, 2026 Microsoft reference price have been checked against their respective sources. However, the comparable-company price and EPS conventions require additional verification, and the differences between the FCFF and FCFE models remain an important methodological limitation. The valuation estimates should therefore be interpreted as scenario-based conclusions rather than precise predictions of future share prices.

## 16. Supporting Files and Reproducibility

The following files support this research:

| File | Purpose |
|---|---|
| `Project_1_Edition_A_MSFT.md` | Original investment thesis |
| `Project_1_Edition_B_MSFT.md` | Updated research and investment analysis |
| `dcf.py` | FCFF DCF valuation |
| `msft_proforma.py` | Financial forecast and FCFE valuation |
| `comps.py` | Comparable-company valuation |
| `project1_reconciliation.py` | FCFF versus FCFE comparison |
| `project1_valuation_reconciliation.md` | Reconciliation documentation |
| `project1_source_verification.md` | Historical input review |
| `project1_validation.md` | Model validation and AI-use documentation |
| `app.py` | Interactive Streamlit valuation workbench |

### Reproduction Commands

From the `TICKER-research` directory, with the Python environment activated:

```bash
python dcf.py
python msft_proforma.py
python comps.py
python project1_reconciliation.py
python -m streamlit run app.py
```

The Streamlit application runs locally at `http://localhost:8501`.

## 17. Sources

**Primary source**

Microsoft Corporation. *FY2026 Form 10-K*, fiscal year ended June 30, 2026.

https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm

**Additional research and model records**

- `MSFT-research/2026-09-10_Microsoft_Company_Research_Report.md`
- `2026-09-10_MSFT_DCF_Inputs.md`
- `sources.md`
- `dcf.py`
- `msft_proforma.py`
- `comps.py`

The Microsoft reference closing price of $501.02 on September 1, 2026, has been checked against Yahoo Finance historical data. The comparable-company share prices and EPS inputs still require independent source and date verification. Analyst forecast assumptions remain subject to sensitivity analysis and investment judgment.
---

**Edition B decision: WATCH / DEFER**

**Research status:** Working draft; subject to final financial input verification, valuation consistency review, and submission formatting.