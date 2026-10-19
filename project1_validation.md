# Project 1 — Microsoft Valuation Model Validation

## 1. Model Overview

The Microsoft valuation workbench uses an integrated five-year pro-forma model covering FY2027–FY2031 and a separate FCFF discounted cash flow model.

The dashboard allows users to modify revenue growth, gross margin, capital spending, discount rates, and terminal growth assumptions.

## 2. Base-Case Reconciliation

| Metric | Python Model | Streamlit Dashboard | Result |
|---|---:|---:|---|
| FCFE value per share | $116.94 | $116.94 | PASS |
| FCFF value per share | $197.60 | $197.60 | PASS |
| FY2031 revenue ($m) | 534,209 | 534,209 | PASS |
| FY2031 FCFE ($m) | 75,130 | 75,130 | PASS |

## 3. Revenue Growth Sensitivity

**Input change:** Revenue growth shift increased from 0 to +2 percentage points.

**Expected outcome:** Higher revenue growth increases operating income, free cash flow to equity, and estimated equity value.

| Metric | Base Case | Higher Growth |
|---|---:|---:|
| FCFE value per share | $116.94 | $144.44 |
| FY2031 FCFE ($m) | 75,130 | 93,799 |
| FY2031 operating income ($m) | 174,820 | 198,394 |

**Result:** PASS — The interactive model responds in the expected direction.

## 4. Gross Margin Sensitivity

**Input change:** Gross margin increased from 68% to 70%, with revenue growth assumptions restored to base.

**Expected outcome:** Higher gross margin increases operating profit, free cash flow, and estimated equity value.

**Result:** PASS — FCFE valuation increased from $116.94 to $131.18 per share.

## 5. Base-Case Restoration

Revenue growth shift was restored to zero and gross margin was restored to 68%.

**Result:** PASS — Base-case valuation returned to $116.94 per share (FCFE) and $197.60 per share (FCFF).

## 6. Accounting Checks

The five-year pro-forma model checks whether:

- Total assets equal total liabilities plus equity.
- Ending cash remains above the modeled minimum.
- Forecast outputs remain valid across tested scenarios.

**Result:** PASS — All five forecast years passed the dashboard's accounting and minimum-cash checks in the tested scenarios.

## 7. Outstanding Validation Work

The FCFE and FCFF models currently produce different equity valuations. Their assumptions, cash flow definitions, and discount rates must be reconciled or explicitly explained before the final investment recommendation.

Additional required work includes a deliberately failed check with recovery, an independently verified source input, and a documented changed-input prediction recorded before running the test.

## 8. AI Assistance

AI assistance was used to help structure the Streamlit interface. The underlying Microsoft pro-forma and DCF models were developed during earlier coursework.

Model outputs were checked against the existing Python scripts. Further independent source verification and model review are required before final submission.
## 9. Failure and Recovery Test

### Test Objective
Verify that the Microsoft valuation workbench detects
financial scenarios that violate the minimum cash requirement.

### Test Inputs
- Base minimum cash requirement: $0 million
- Modified minimum cash requirement: $100,000 million
- FY2027 projected ending cash: $47,570 million

### Expected Result
The model should flag FY2027 as invalid because its
ending cash is below the required minimum.

### Observed Result
PASS — The dashboard displayed a red validation warning
when the minimum cash requirement increased to
$100,000 million.

### Recovery
The minimum cash requirement was restored to $0 million.

### Recovery Result
The dashboard returned to its original valid state.

### Conclusion
The workbench successfully identified an invalid
cash constraint and demonstrated failure detection.
## Updated Valuation and Workbench Validation

### Revised FCFF DCF

The FY2026 starting FCFF was provisionally revised from $69,408.2199 million to $69,446.2199 million following a review of historical cash-flow inputs.

The revised reconciliation script produced:

- FCFF DCF valuation: $197.71 per diluted share
- FCFE pro-forma valuation: $116.94 per diluted share
- FCFF equity value: $1,473,531.9 million
- FCFE equity value: $871,566.2 million

The FCFF DCF increased by approximately $0.11 per share. The FCFE model remained unchanged.

### Streamlit Workbench Consistency Check

The Streamlit application was restarted after the Python model update.

Expected base-case dashboard results:

| Metric | Expected result |
|---|---:|
| FCFF DCF per share | $197.71 |
| FCFE pro-forma per share | $116.94 |
| FY2031 revenue | $534,209 million |
| FY2031 FCFE | $75,130 million |

**Validation status:** Pending confirmation that the dashboard displays the revised FCFF result.

### Remaining Verification

The historical operating cash flow, capital expenditure inputs, and after-tax interest adjustment require final source verification before the valuation is treated as final.