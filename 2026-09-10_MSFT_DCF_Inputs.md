# Microsoft FCFF DCF — Input Record

**Company:** Microsoft Corporation (`MSFT`)  
**Latest annual filing used:** Form 10-K for the fiscal year ended June 30, 2026, filed July 29, 2026. All filing amounts below are USD millions unless stated otherwise.

| Input | Value | Unit | As-of / period | Locator and treatment |
| --- | ---: | --- | --- | --- |
| Operating cash flow | 182,899 | USD millions | FY ended Jun. 30, 2026 | FY2026 10-K, Item 8, Consolidated Statements of Cash Flows, “Net cash from operations.” |
| Interest expense | 3,051 | USD millions | FY ended Jun. 30, 2026 | FY2026 10-K, Item 8, “Other income (expense), net” table, “Interest expense.” |
| Effective tax rate | 19.3970% | Percent | FY ended Jun. 30, 2026 | Calculated from 10-K Income Statements: provision for income taxes of 32,185 divided by income before income taxes of 165,934. |
| After-tax interest | 2,459.2199 | USD millions | FY ended Jun. 30, 2026 | Calculated: 3,051 × (1 − 19.3970%). |
| Capital expenditures | 115,950 | USD millions | FY ended Jun. 30, 2026 | FY2026 10-K, Item 8, Consolidated Statements of Cash Flows, “Additions to property and equipment.” This is the cash-flow-statement capex convention used in the model. |
| Starting FCFF | 69,408.2199 | USD millions | FY ended Jun. 30, 2026 | Calculated: 182,899 operating cash flow + 2,459.2199 after-tax interest − 115,950 capex. |
| FCFF growth, Year 1 | 15.0% | Percent | FY2027 forecast | Analyst forecast. It starts below FY2026’s 18% revenue growth and reflects the 10-K’s cloud-led growth and AI infrastructure spending discussion in Item 7, MD&A, pp. 37–44. |
| FCFF growth, Year 2 | 13.0% | Percent | FY2028 forecast | Analyst forecast; no company-supplied value is presented as fact. |
| FCFF growth, Year 3 | 11.0% | Percent | FY2029 forecast | Analyst forecast; no company-supplied value is presented as fact. |
| FCFF growth, Year 4 | 9.0% | Percent | FY2030 forecast | Analyst forecast; no company-supplied value is presented as fact. |
| FCFF growth, Year 5 | 7.0% | Percent | FY2031 forecast | Analyst forecast; the declining path explicitly models moderation rather than extrapolating FY2026 growth. |
| WACC | 10.0250% | Percent | Valuation assumption | Estimated once using the specified training inputs: cost of equity = 4.5% + 1.3 × 5.0% = 11.0%; after-tax cost of debt = 6.0% × (1 − 25.0%) = 4.5%; 85% equity / 15% debt weighting = 10.025%, rounded to 10.0% in `dcf.py`. These are assumptions, not filing facts. |
| Terminal growth | 3.0% | Percent | Perpetual period after FY2031 | Long-run economy assumption, not a Microsoft forecast. |
| Non-operating cash | 76,843 | USD millions | Jun. 30, 2026 | FY2026 10-K, Item 8, Balance Sheets: cash and cash equivalents of 20,935 plus short-term investments of 55,908. |
| Debt | 40,294 | USD millions | Jun. 30, 2026 | FY2026 10-K, Item 8, Balance Sheets / Note 10: current portion of long-term debt of 9,227 plus long-term debt of 31,067. |
| Diluted shares | 7,453 | Millions of shares | FY ended Jun. 30, 2026 | FY2026 10-K, Item 8, Note 2 — Earnings Per Share, weighted-average diluted shares. |
| MSFT target price | 491.65 | USD per share | Sep. 9, 2026, 4:00 PM EDT | Most recent regular-market close available on Sep. 10, 2026; use as the reverse-DCF target, not as a DCF input. [Price source](https://stockanalysis.com/stocks/msft/history/?page=2) |

## Source filing

[Microsoft FY2026 Form 10-K on SEC EDGAR](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm)

The FCFF calculation follows the requested convention: operating cash flow + after-tax interest − capex. The forecast rows and WACC are explicitly labelled assumptions; they should be replaced if you develop better supported estimates.
