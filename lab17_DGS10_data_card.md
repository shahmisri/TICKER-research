# Lab 17 Data Card — DGS10

**Downloaded:** November 3, 2026  
**Series:** DGS10 — Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis  
**Source:** Board of Governors of the Federal Reserve System, H.15 Selected Interest Rates, distributed by FRED  
**FRED page:** [DGS10](https://fred.stlouisfed.org/series/DGS10)

## What it measures

DGS10 is the daily 10-year constant-maturity Treasury yield, in percent and not
seasonally adjusted. A constant-maturity yield is interpolated from the Treasury
yield curve; it is not necessarily the yield on one particular Treasury security.

## Publication timing and revisions

FRED identifies the frequency as daily and the units as percent, not seasonally
adjusted. The Federal Reserve's H.15 release is posted Monday through Friday at
4:15 p.m. Eastern Time, except holidays and days the Board is closed. This is
after the regular U.S. equity-market close, so a same-day DGS10 observation is
not available for a decision made at that close.

The ALFRED vintage dated October 5, 2026 has October 2, 2026 as its latest DGS10
observation. This is the prior business day's observation (the intervening
October 3–4 dates were a weekend). For a daily backtest, use the ALFRED vintage
for the decision date and do not use the same-day observation before its
publication time.

Comparing the October 5, 2026 ALFRED vintage with the FRED download on November
3, 2026 showed **zero changed values among the overlapping observations** in
the app. The three observations below were unchanged. That comparison found no
revisions for this vintage window; it does not prove that the series can never
be revised.

## Three observation checks

The point-in-time column is from ALFRED with `vintage_date=2026-10-05`; the
current column is from FRED, downloaded November 3, 2026. Values are percentage
points.

| Observation date | As known October 5, 2026 | FRED on November 3, 2026 | Changed? |
|---|---:|---:|---|
| September 30, 2026 | 5.29 | 5.29 | No |
| October 1, 2026 | 5.24 | 5.24 | No |
| October 2, 2026 | 5.28 | 5.28 | No |

The latest observation in the November 3 FRED download was October 30, 2026:
**4.94 percent**.

## Project 2 call: Quarantine pending trading-time alignment

Do not use today's revised/latest FRED history as if it had been known at every
past decision. The app verifies the date-level ALFRED vintage for the dates
checked, but Project 2's exact decision and execution times still determine
whether a value was available in time. Keep DGS10 quarantined until the
backtest uses the vintage available on each decision date and excludes a
same-day observation when the decision occurs before the 4:15 p.m. H.15 release.
Then it is reasonable to admit DGS10 with that point-in-time rule; reject is not
warranted by these checks.

## Sources

- [FRED DGS10 series page and metadata](https://fred.stlouisfed.org/series/DGS10)
- [FRED current CSV download](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10)
- [ALFRED October 5, 2026 vintage CSV](https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-05)
- [Federal Reserve H.15 release schedule and notes](https://www.federalreserve.gov/releases/h15/)
