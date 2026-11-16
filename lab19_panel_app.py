"""Streamlit app for the three-investor Legend Panel in Lab 19."""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path
import re

import pandas as pd
import streamlit as st

from lab18_edgar import (
    EdgarError,
    build_report,
    format_report,
    investor_memo,
    investor_verdict,
    unprinted_numbers,
)


TICKER_RE = re.compile(r"^[A-Z0-9.-]+$")
INVESTORS = ("Buffett", "Graham", "Burry")


st.set_page_config(page_title="Legend Panel", layout="wide")
st.title("Legend Panel — Buffett · Graham · Burry")
st.caption(
    "Same SEC EDGAR 10-K facts, three rule sets. Educational business-quality "
    "screens only; not investment advice."
)

with st.sidebar:
    st.header("Company")
    ticker_input = st.text_input("Ticker", value="COST").strip().upper()
    current_ratio_min = Decimal(
        str(
            st.number_input(
                "Graham current-ratio threshold",
                min_value=0.1,
                max_value=10.0,
                value=2.0,
                step=0.1,
            )
        )
    )
    analyze = st.button("Run panel", type="primary")

if "lab19_report" not in st.session_state:
    st.session_state.lab19_report = None
if "lab19_run_id" not in st.session_state:
    st.session_state.lab19_run_id = 0

if analyze:
    if not TICKER_RE.fullmatch(ticker_input):
        st.error("Enter a valid ticker using letters, numbers, periods, or hyphens.")
    else:
        try:
            with st.spinner(f"Downloading 10-K facts for {ticker_input} from SEC EDGAR..."):
                st.session_state.lab19_report = build_report(
                    ticker_input,
                    graham_current_ratio_min=current_ratio_min,
                )
                st.session_state.lab19_run_id += 1
        except EdgarError as exc:
            st.session_state.lab19_report = None
            st.error(str(exc))

report = st.session_state.lab19_report
if report is None:
    st.info("Enter a ticker, set Graham's threshold, and select **Run panel**.")
    st.stop()

st.subheader(f"{report['ticker']} — {report['company']}")
st.caption(f"CIK {report['cik']} · SEC facts downloaded {report['download_date']}")

verdicts = investor_verdict(report["checks"])
verdict_columns = st.columns(3)
for column, investor in zip(verdict_columns, INVESTORS):
    with column:
        st.metric(investor, verdicts[investor])

st.subheader("Investor × check")
check_rows = []
for investor, checks in (
    ("Buffett", list(report["checks"].items())[:3]),
    ("Graham", list(report["checks"].items())[3:6]),
    ("Burry", list(report["checks"].items())[6:]),
):
    check_rows.extend(
        {"Investor": investor, "Check": name, report["ticker"]: result}
        for name, result in checks
    )
st.dataframe(pd.DataFrame(check_rows), width="stretch", hide_index=True)

st.subheader("Five-year SEC facts")
st.caption(
    "Amounts in $ millions. Ratios use the reported facts shown below; missing "
    "facts and invalid denominators remain not known."
)
facts_table = pd.DataFrame(
    [
        {
            "Fiscal year end": row["fiscal_year_end"],
            "Revenue ($m)": (
                f"{row['revenue_m']:,.2f}" if row["revenue_m"] is not None else "not found"
            ),
            "Revenue tag": row["revenue_tag"],
            "Net income ($m)": (
                f"{row['net_income_m']:,.2f}"
                if row["net_income_m"] is not None
                else "not found"
            ),
            "Net income tag": row["net_income_tag"],
            "Operating cash flow ($m)": (
                f"{row['operating_cash_flow_m']:,.2f}"
                if row["operating_cash_flow_m"] is not None
                else "not found"
            ),
            "Operating cash flow tag": row["operating_cash_flow_tag"],
            "Capital spending ($m)": (
                f"{row['capital_spending_m']:,.2f}"
                if row["capital_spending_m"] is not None
                else "not found"
            ),
            "Capital spending tag": row["capital_spending_tag"],
            "Equity ($m)": (
                f"{row['equity_m']:,.2f}" if row["equity_m"] is not None else "not found"
            ),
            "Equity tag": row["equity_tag"],
            "Liabilities ($m)": (
                f"{row['liabilities_m']:,.2f}"
                if row["liabilities_m"] is not None
                else "not found"
            ),
            "Liabilities tag": row["liabilities_tag"],
            "Current assets ($m)": (
                f"{row['assets_current_m']:,.2f}"
                if row["assets_current_m"] is not None
                else "not found"
            ),
            "Current assets tag": row["assets_current_tag"],
            "Current liabilities ($m)": (
                f"{row['liabilities_current_m']:,.2f}"
                if row["liabilities_current_m"] is not None
                else "not found"
            ),
            "Current liabilities tag": row["liabilities_current_tag"],
            "ROE": (
                f"{row['roe_pct']:.1f}%" if row["roe_pct"] is not None else "not known"
            ),
            "Owner earnings ($m)": (
                f"{row['owner_earnings_m']:,.2f}"
                if row["owner_earnings_m"] is not None
                else "not found"
            ),
            "Current ratio": (
                f"{row['current_ratio']:.2f}"
                if row["current_ratio"] is not None
                else "not known"
            ),
            "Liabilities / equity": (
                f"{row['liabilities_to_equity']:.2f}"
                if row["liabilities_to_equity"] is not None
                else "not known"
            ),
        }
        for row in report["rows"]
    ]
)
st.dataframe(facts_table, width="stretch", hide_index=True)

st.subheader("Three memos")
report_output = format_report(report)
memo_columns = st.columns(3)
memos: dict[str, str] = {}
for column, investor in zip(memo_columns, INVESTORS):
    memo_path = Path(__file__).parent / f"{report['ticker']}_{investor.lower()}_memo.md"
    default_memo = investor_memo(report, investor)
    with column:
        st.markdown(f"#### {investor}")
        memos[investor] = st.text_area(
            f"{investor} memo",
            value=default_memo,
            height=330,
            key=(
                f"lab19_memo_{investor}_{report['ticker']}_"
                f"{st.session_state.lab19_run_id}"
            ),
            label_visibility="collapsed",
        )

if st.button("Save all three memos as Markdown"):
    for investor, memo in memos.items():
        memo_path = Path(__file__).parent / (
            f"{report['ticker']}_{investor.lower()}_memo.md"
        )
        memo_path.write_text(memo.rstrip() + "\n", encoding="utf-8")
    st.success("Saved all three investor memos.")

unprinted_by_investor = {
    investor: unprinted_numbers(memo, report_output)
    for investor, memo in memos.items()
}
unprinted_by_investor = {
    investor: numbers
    for investor, numbers in unprinted_by_investor.items()
    if numbers
}
if unprinted_by_investor:
    details = "; ".join(
        f"{investor}: {', '.join(numbers)}"
        for investor, numbers in unprinted_by_investor.items()
    )
    st.error(f"Unprinted numbers found across memos — {details}")
else:
    st.success("Number audit passed: every memo number appears in the printed report.")
