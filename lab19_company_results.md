# Lab 19 — Project 2 company panel

## Status: completed using NVDA SEC EDGAR data

The course project identifies the Project 2 ETF allocation as:

| Fund ticker | Fund | Portfolio weight |
|---|---|---:|
| BIL | SPDR Bloomberg 1–3 Month T-Bill ETF | 0% |
| IEF | iShares 7–10 Year Treasury Bond ETF | 20% |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | 25% |
| VT | Vanguard Total World Stock ETF | 55% |

For this Lab 19 panel, I selected NVIDIA (NVDA) as the company for the SEC EDGAR screen. The data source is the official SEC companyfacts JSON for CIK 0001045810, requested with the required local User-Agent environment values and a valid certificate bundle.

## Source and verification

- Ticker: NVDA
- Company: NVIDIA CORP
- CIK: 0001045810
- SEC data source: `https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json`
- Download date: 2026-11-16
- Graham current-ratio threshold: 2.0

I kept the SEC User-Agent values in the local shell environment only and did not copy them into any source file or report.

## Panel results

| Investor | Checks | Verdict | Memo |
|---|---|---|---|
| Buffett | ROE >= 15% every year; owner earnings positive and growing | Passes screen | [NVDA_buffett_memo.md](./NVDA_buffett_memo.md) |
| Graham | Current ratio >= 2.0 latest year; net income positive and growing | Passes screen | [NVDA_graham_memo.md](./NVDA_graham_memo.md) |
| Burry | Operating cash flow at least net income every year; liabilities <= 2x equity latest year | Fails screen | [NVDA_burry_memo.md](./NVDA_burry_memo.md) |

## Verified SEC check outcomes

The collector printed the following check results for NVDA:

- ROE of 15% or more every year: pass
- Owner earnings positive every year: pass
- Owner earnings grew, first year to last: pass
- Current ratio of 2.0 or more, latest year: pass (3.91 latest year)
- Net income positive every year: pass
- Net income grew, first year to last: pass
- Operating cash flow at least net income every year: fail (2026 operating cash flow was 102,718 vs. net income 120,067)
- Liabilities no more than twice equity, latest year: pass (0.31 latest year)

No missing data points were filled in or estimated; missing data would remain `not known`, and no fabricated SEC facts were used.

## Bull case for NVDA

The bull case is strong on reported business quality. NVIDIA passes Buffett's three business checks and Graham's three screens. ROE is above 15% in every fiscal year, owner earnings are positive and rising, net income is positive and rising, and the latest current ratio is 3.91 above the Graham 2.0 threshold. The company also ends with liabilities/equity of 0.31, which is comfortably below the 2.0 leverage screen.

## Bear case for NVDA

The bear case is that Burry fails the cash-flow conversion screen. The 2026 operating cash flow is below net income, so the firm does not satisfy the requirement that operating cash flow at least equals net income in every year. That is a real cash-flow caution, even though the company still passes Buffett and Graham screens.

## My decision

I would treat the panel as a first-pass screen and not as a valuation verdict. For NVDA, the Buffett and Graham screens pass, but Burry fails on cash-flow conversion, so I would not rely on one investor's screen alone. I would combine the panel with the full 10-K review, valuation, and business-model analysis before making any actual investment decision.

## Files generated

- [NVDA_buffett_memo.md](./NVDA_buffett_memo.md)
- [NVDA_graham_memo.md](./NVDA_graham_memo.md)
- [NVDA_burry_memo.md](./NVDA_burry_memo.md)
