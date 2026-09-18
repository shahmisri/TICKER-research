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

- Market capitalization and implied valuation multiples on September 1, 2026; the September 1 closing share price used in the valuation comparison is $501.02.
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
## Lab 08 — Peer Policy and Selection

### Peer policy

Target: Microsoft Corporation (MSFT)  
Comparison date: September 1, 2026.

I will consider listed operating technology companies whose business economics materially overlap with Microsoft's core operations, particularly enterprise software, cloud computing, and recurring subscription-based services. A candidate must have positive annual reported diluted EPS that was publicly available by September 1, 2026 and a stock price available on the comparison date.

I will exclude a candidate if its primary business economics are not sufficiently comparable with Microsoft, if annual diluted EPS is zero or negative, or if the required earnings information was not public by the valuation date. Differences in business mix, scale, growth, and profitability will be documented rather than ignored.

### Candidate investigation and decisions

| Candidate | Business-model evidence | Annual reported diluted EPS | Important difference from Microsoft | Decision |
| --- | --- | ---: | --- | --- |
| Oracle (ORCL) | Oracle provides enterprise applications and infrastructure through cloud, on-premise, and hybrid deployment models. Its cloud offerings include Oracle Cloud Applications and Oracle Cloud Infrastructure. | FY2026 diluted EPS: $5.83 | Oracle is more concentrated in enterprise applications, databases, and cloud infrastructure, while Microsoft has a broader mix including productivity software, Windows, gaming, advertising, devices, and cloud. | USE |
| Adobe (ADBE) | Adobe generates substantial subscription revenue through Digital Media and Digital Experience products, including Creative Cloud, Acrobat, and enterprise digital-experience solutions. | FY2025 diluted EPS: $16.70 | Adobe is more concentrated in creative software, document productivity, and digital-experience products and does not have Microsoft's broad cloud-infrastructure and operating-system exposure. | QUALIFY |

### Decision rationale

I use Oracle because its enterprise software and cloud infrastructure operations provide meaningful economic overlap with Microsoft's enterprise software and Azure businesses. Oracle's FY2026 Form 10-K reports diluted EPS of $5.83.

I qualify Adobe rather than treating it as a perfect comparable. Its subscription software model and enterprise/customer productivity products overlap with parts of Microsoft's economics, but Adobe has a narrower business mix. Adobe's FY2025 Form 10-K reports diluted EPS of $16.70.

Both candidates have positive annual reported diluted earnings available before my September 1, 2026 valuation date. I retain their differences as limitations rather than selecting peers based on which produces a preferred valuation result.

### Sources

Oracle Corporation, FY2026 Form 10-K, Item 1 Business and consolidated financial statements:
https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm

Adobe Inc., FY2025 Form 10-K, business discussion and earnings-per-share note:
https://www.sec.gov/Archives/edgar/data/796343/000079634326000003/adbe-20251128.htm

## Lab 08 — Comparable-company validation

**Validation:** Oracle's P/E is $141.32 ÷ $5.83 = 24.2401×, which matches the calculator. Before removing Oracle, I expected the implied Microsoft value to decrease because Oracle has the higher P/E multiple. The leave-one-out test confirms this: removing Oracle reduces the implied price from $371.30 to $307.49, a decrease of $63.81. Removing Adobe instead increases the implied price to $435.11. This shows that the valuation is sensitive to peer selection and that removing either company significantly reduces the information in an already small two-peer set.
## Lab 08 — DCF and Peer Comparison
| Method | Result | Main support | Main limitation |
| --- | ---: | --- | --- |
| DCF | Base case: $197.60/share; sensitivity range: $158.51–$267.64 | Values Microsoft from forecast FCFF using explicit operating assumptions, WACC, and terminal growth | Sensitive to WACC, terminal growth, and forecast assumptions; 74.28% of enterprise value comes from terminal value |
| Peer P/E | Median-implied: $371.30/share; peer-implied range: $307.49–$435.11 | Applies the observed P/E multiples of Oracle and Adobe to Microsoft's annual diluted EPS | Sensitive to peer selection and differences in business mix, growth, scale, and profitability |
| Market price | $501.02/share on September 1, 2026 | Same-date market-price reference | Market price reflects expectations not necessarily captured by either valuation method |

The two valuation methods produce substantially different results. My DCF base case is $197.60 per share, with a sensitivity range of $158.51–$267.64. The peer P/E method gives a median-implied value of $371.30 and a peer-implied range of $307.49–$435.11. I do not mechanically average the methods because they rely on different assumptions and evidence.

The DCF is particularly sensitive to long-run assumptions because 74.28% of enterprise value comes from terminal value. The peer valuation is also sensitive to peer selection. Removing Oracle lowers the implied value to $307.49, while removing Adobe raises it to $435.11.

The September 1, 2026 market price of $501.02 is above both the DCF sensitivity range and the peer-implied range. The reverse DCF finds no solution within the tested uniform explicit-growth shift bracket of -5% to +10%, holding starting FCFF, WACC, terminal growth, cash, debt, diluted shares, and the relative differences among the five growth rates fixed.

## Provisional Call

My provisional decision remains **watch / defer**. The DCF and peer methods disagree substantially, and both remain below the September 1 market price. Rather than averaging the methods, I would investigate whether the difference reflects conservative DCF assumptions, limitations in the peer set, or market expectations that are not captured by my current model.

## What Could Change My Decision

I could change my decision if additional evidence supports materially different long-term cloud growth, margins, reinvestment, WACC, or terminal-growth assumptions while remaining consistent with Microsoft's operating evidence. A better-supported peer set that materially changes the comparable valuation could also affect my conclusion.
## Lab 08 — Skeptical-Colleague Review

The skeptical review identified peer comparability as the weakest-supported assumption because Oracle and Adobe overlap with only portions of Microsoft's broader business mix. It also identified the need to ensure that the target and peer prices, valuation date, valuation object, and earnings definitions are consistent.

**Disposition: ACCEPT.** The criticism is supported by my validation. The leave-one-out test shows that peer selection materially affects the P/E result: removing Oracle produces $307.49 per share, while removing Adobe produces $435.11 per share. I therefore retain peer selection as an important limitation rather than treating the $371.30 median-implied value as a precise estimate.

I also checked the date consistency. My comparison date is September 1, 2026, and the market-price input used in the revised analysis is $501.02. The DCF and P/E outputs are both ultimately expressed as value per share, although the DCF reaches equity value through an FCFF enterprise-value bridge while P/E directly applies an equity multiple to diluted EPS.

**Question that could change my decision:** If I use operating evidence to reassess the assumptions driving the gap between my DCF and peer valuation, can a defensible DCF case move materially toward the peer-implied range without requiring assumptions unsupported by Microsoft's filings?

