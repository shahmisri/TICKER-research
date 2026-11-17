**AI-use disclosure:** AI assisted in organizing the project and drafting its code and documentation. No market data, holdings, validation evidence, prediction, or experiment results were invented. The changed-input prediction must be written by the student without AI.

**Education-only disclosure:** This application and its outputs are for educational purposes only and are not investment advice.

# FIN 43900 Project 2 — Meridian Foundation

A Streamlit decision-support app built in a separate project folder from the
existing Project 1 and Lab 13–19 materials. It uses the Lab 13 mandate, Lab 14
portfolio assumptions and baselines, Lab 15 monthly ETF prices, and Lab 17 DGS10
data card as references. It does not alter those source files.

## Run in the VS Code terminal (macOS)

From the current workspace root:

```bash
cd classrepo/TICKER-research/FIN43900_Project2
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints a local URL (normally `http://localhost:8501`) to open in your
browser. Stop it with **Control+C** in that terminal.

To run the focused tests in a second terminal:

```bash
cd classrepo/TICKER-research/FIN43900_Project2
source .venv/bin/activate
python -m unittest discover -s tests -v
```

## What's in the app

- Mandate and asset universe; 6.5% classroom return proxy shown separately from
  the actual CPI + 4% rolling-five-year, net-of-costs objective.
- Equal-weight baseline, 40% LQD / 60% VT benchmark, and a transparent 10% BIL /
  10% IEF / 20% LQD / 60% VT constrained candidate, with individual
  pass/fail/not-testable results.
- Lab 14 training-assumption return and volatility calculations, plus historical
  ETF window/risk summaries from the supplied Lab 15 prices.
- DGS10 sparse-vintage display with a 4:15 p.m. ET release-time control. DGS10 is
  quarantined and is not used to generate a portfolio signal.
- Stress controls for assumption changes, rolling windows, transaction costs,
  constraints, and stopping conditions.
- A one-run changed-input workflow gated by a locally saved prediction, a
  matching GitHub commit SHA and URL, and the student's own attestation.
- A committee view that does **not** authorize a pilot on the current evidence.

## Evidence limits and missing items

- The 6.5% Lab 14 number is a classroom proxy, not proof of the CPI + 4% objective.
- Lab 14 return and volatility assumptions are not independently substantiated
  ETF forecasts.
- The Lab 15 price file is copied unchanged; the accompanying card describes its
  provenance limitations.
- Only the DGS10 observations in the Lab 17 card are present. They are not a
  complete vintage history or a validated signal.
- Starting holdings, fund settlement/liquidity support, ETF issuer look-through,
  portfolio turnover, complete transaction costs, CPI data, out-of-sample
  validation, and the CIO's loss-limit procedure are not supplied.
- The AI-off prediction and the locked changed-input result do not exist until
  the student creates them. The app does not check GitHub remotely; the SHA/URL
  and checkbox are user attestations.

See [docs/decision-memo.md](docs/decision-memo.md),
[docs/validation-and-ai-use.md](docs/validation-and-ai-use.md),
[docs/video-script.md](docs/video-script.md), and
[submission-manifest.md](submission-manifest.md).
