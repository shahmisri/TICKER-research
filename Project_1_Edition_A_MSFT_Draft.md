# Project 1 — Edition A (draft)

**Prepared:** September 1, 2026  
**Company:** Microsoft Corporation (`MSFT`)  
**Valuation date:** September 1, 2026  
**Decision and user:** As an equity-research analyst, I am advising a buy-side investment committee that has no current position in Microsoft on whether to initiate research and, ultimately, whether to initiate a position.

## Initial thesis: watch / defer

My initial recommendation is **watch / defer**, not initiate. Microsoft has operating characteristics that justify deeper valuation work, especially rapid cloud growth and substantial liquidity. However, a decision to initiate requires an explicit intrinsic-value range and a comparison with the market price as of the valuation date. I do not yet have a defensible range, and I will not treat strong growth as proof that the shares are undervalued.

## Filing evidence already known

The primary source is Microsoft Corporation's Form 10-K for the fiscal year ended June 30, 2026, filed July 29, 2026.

| Field | Evidence from the 10-K |
| --- | --- |
| Entity | Microsoft Corporation; CIK 0000789019; common stock ticker `MSFT` |
| Filing / accession | Form 10-K; accession 0001193125-26-323660 |
| Reporting period / filing date | Fiscal year ended June 30, 2026 / filed July 29, 2026 |
| Currency and units | U.S. dollars; financial-statement tables cited here are in millions except per-share amounts |
| Diluted-share evidence | 7,453 million FY2026 diluted weighted-average shares. The filing reconciles 7,429 million basic weighted-average shares plus 24 million dilutive stock-based awards. This is the correct denominator concept for a per-share valuation bridge; it differs from the 7,425,545,491 shares outstanding reported on the cover as of July 23, 2026. |
| Cash | $20,935 million cash and cash equivalents plus $55,908 million short-term investments = $76,843 million total cash, cash equivalents, and short-term investments at June 30, 2026. |
| Debt | $9,227 million current portion of long-term debt plus $31,067 million long-term debt = $40,294 million carrying amount. |
| Operating-value driver | Microsoft Cloud revenue rose 27% to $214.4 billion. Azure and other cloud-services revenue grew 41%; this growth is material to the revenue, margin, capital-expenditure, and terminal-value assumptions in a future FCFF model. |

Source: [Microsoft Corporation, FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm); [SEC filing index and accession record](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/0001193125-26-323660-index.htm).

The Week 1 offline screening case also identified MSFT as an eligible operating-company candidate with a 14% annualized return, 24% annualized volatility, 54% positive-day share, no missing observations, and an available filing. Those values are labelled **synthetic training evidence, not market evidence**; they support the choice to investigate but do not support a valuation conclusion.

Source: [Week 1 offline screening case](https://raw.githubusercontent.com/CinderZhang/FIN43900-Fall2026/main/lessons/week-01/starter/offline-screening-case.csv).

## Synthetic enterprise-to-equity bridge check

All amounts are in USD millions except per-share values.

| Step | Calculation | Result |
| --- | --- | ---: |
| Enterprise value | Given | $1,000 |
| Add nonoperating cash | $1,000 + $100 | $1,100 |
| Less debt | $1,100 − $250 | $850 |
| Less noncontrolling interest | $850 − $20 | $830 |
| Less unfunded pension | $830 − $10 | $820 equity value |
| Divide by diluted shares | $820 / 100 million | **$8.20 per share** |

This confirms the mechanics: enterprise value is converted to common-equity value by adding nonoperating cash and subtracting debt and other senior/non-common claims before dividing by diluted shares. It is a synthetic classroom check, not a Microsoft valuation.

## Consequential assumptions

- An FCFF / enterprise-value approach is appropriate because Microsoft is an operating company rather than a bank, insurer, REIT, fund, or other excluded vehicle.
- Azure and other cloud-services growth can be modeled separately enough to inform consolidated revenue growth, but growth will slow from the latest reported rate over a finite forecast horizon.
- The AI infrastructure buildout can create near-term margin and capital-intensity pressure. Any assumption that growth converts fully into free cash flow must be tested rather than presumed.
- Cash, short-term investments, debt, noncontrolling interests, pensions, leases, and other nonoperating items must be classified consistently between enterprise and equity value. The classroom bridge is only a mechanics check, not the final classification policy.
- Diluted weighted-average shares are the working per-share denominator unless the final valuation date and model convention require a dated fully diluted share count.

## Unknowns and risks

- The current market price, market capitalization, and implied valuation multiples on September 1, 2026.
- The pace and durability of Azure growth, including demand, capacity availability, competition, and customer spending.
- The scale, timing, and useful life of AI-related capital expenditures and their effect on free cash flow.
- The appropriate revenue-growth path, operating-margin path, tax rate, reinvestment rate, WACC, and terminal growth rate.
- Whether investments, lease liabilities, other financing arrangements, and nonoperating assets need adjustments in the final enterprise-to-equity bridge.
- Material downside risks, including cloud competition, data-center execution, cybersecurity, regulation, and changes in the economics of AI products.

## Research plan

1. Build a three-statement historical dataset from Microsoft’s 10-Ks and 10-Qs; reconcile every load-bearing figure to the filing and preserve units, period, and source locator.
2. Separate the main operating drivers—Azure/cloud, Microsoft 365, LinkedIn, Dynamics, Windows/devices, gaming, and search—to develop a reasoned revenue forecast rather than extrapolating one consolidated growth rate.
3. Forecast EBIT, cash taxes, depreciation and amortization, capital expenditures, and operating working capital to calculate unlevered FCFF.
4. Estimate WACC using a documented beta, risk-free rate, equity-risk-premium assumption, debt cost, and market-value capital structure; test a reasonable range rather than relying on a single point estimate.
5. Value Microsoft using DCF sensitivity tables and comparable-company cross-checks. Convert EV to equity value with a dated, documented bridge and divide by the selected diluted-share convention.
6. Test the thesis against downside cases: lower cloud growth, weaker margins, higher AI infrastructure spending, and a higher discount rate. Initiation would require a margin of safety that survives a reasonable downside case.

## Partner-generated falsification question

**Required before submission:** Paste your partner's question here verbatim and name the partner. Do not use the suggested wording below as if it came from a partner.

> Partner name: Connor Guthrie  
> Question: to send to partner: “What single fact or valuation result would most strongly falsify my watch/defer thesis on Microsoft, and why?


