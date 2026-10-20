# Microsoft (MSFT) — Equity Research and Valuation

**Course:** FIN 43900 — Equity Research, Fall 2026  
**Company:** Microsoft Corporation (NASDAQ: MSFT)  
**Valuation Date:** September 1, 2026  
**Recommendation:** WATCH / DEFER

## Project Overview

This repository contains my Microsoft equity research project, including financial analysis, valuation models, sensitivity testing, validation documentation, and an interactive Streamlit valuation workbench.

The analysis uses Microsoft's FY2026 financial statements and evaluates the company through discounted cash flow, pro-forma forecasting, and comparable-company valuation.

## Valuation Models

- **FCFF DCF:** Approximately $197.71 per share
- **FCFE Pro-Forma:** Approximately $116.94 per share
- **Comparable Companies:** Approximately $371.30 per share

These approaches use different methodologies and assumptions. The differences are discussed in the research and valuation reconciliation documentation.

## Running the Models

Install the required Python packages in your Python environment:

```bash
pip install streamlit pandas numpy
```

Run the available analysis scripts from the repository's main directory:

```bash
python dcf.py
python msft_proforma.py
python comps.py
python project1_reconciliation.py
```

Launch the interactive valuation workbench:

```bash
python -m streamlit run app.py
```

## Submission Documents

The `docs/` folder contains:

- `Research-Evolution.pdf`
- `Decision-Memo.pdf`
- `Validation-and-AI-Use.pdf`

## Investment Recommendation

The recommendation is **WATCH / DEFER**. The estimated values from the modeled valuation approaches are below the September 1, 2026 reference market price of $501.02.

Key considerations include valuation sensitivity, capital expenditures, cloud and AI investment, and the dependence of the DCF on terminal value.

## Sources

Primary financial information is based on Microsoft's FY2026 Form 10-K. Additional market and peer valuation inputs are documented in the repository.
