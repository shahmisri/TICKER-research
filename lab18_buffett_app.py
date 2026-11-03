"""Streamlit app for the Legend Investor Lab 18."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from pathlib import Path
import re

import pandas as pd
import streamlit as st

from lab18_edgar import EdgarError, build_report, format_report


TICKER_RE = re.compile(r"^[A-Z0-9.-]+$")
NUMBER_RE = re.compile(
    r"(?<![\w.])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?!\w)(?!\.\d)"
)


def _number_key(token: str) -> tuple[Decimal, bool] | None:
    is_percent = token.endswith("%")
    cleaned = token[:-1] if is_percent else token
    try:
        return Decimal(cleaned.replace(",", "")).normalize(), is_percent
    except InvalidOperation:
        return None


def unprinted_numbers(memo: str, script_output: str) -> list[str]:
    """Return distinct memo numbers not present in the script's printed report."""
    printed = {
        key
        for token in NUMBER_RE.findall(script_output)
        if (key := _number_key(token)) is not None
    }
    unseen: list[str] = []
    for token in NUMBER_RE.findall(memo):
        key = _number_key(token)
        if key is not None and key not in printed and token not in unseen:
            unseen.append(token)
    return unseen


st.set_page_config(page_title="Legend Investor", layout="wide")
st.title("Legend Investor — Business Quality")
st.caption(
    "Data from SEC EDGAR; built with AI help, a learning demonstration, "
    "not investment advice."
)

with st.sidebar:
    st.header("Company")
    ticker_input = st.text_input("Ticker", value="COST").strip().upper()
    analyze = st.button("Analyze company", type="primary")

if "lab18_report" not in st.session_state:
    st.session_state.lab18_report = None
if "lab18_ticker" not in st.session_state:
    st.session_state.lab18_ticker = ""

if analyze:
    if not TICKER_RE.fullmatch(ticker_input):
        st.error("Enter a valid ticker using letters, numbers, periods, or hyphens.")
    else:
        try:
            with st.spinner(f"Downloading 10-K facts for {ticker_input} from SEC EDGAR..."):
                st.session_state.lab18_report = build_report(ticker_input)
                st.session_state.lab18_ticker = ticker_input
        except EdgarError as exc:
            st.session_state.lab18_report = None
            st.error(str(exc))

report = st.session_state.lab18_report
if report is None:
    st.info("Enter a ticker and select **Analyze company**.")
    st.stop()

st.subheader(f"{report['ticker']} — {report['company']}")
st.caption(f"CIK {report['cik']} · SEC facts downloaded {report['download_date']}")

rows = report["rows"]
chart = pd.DataFrame(
    {
        "Fiscal year end": [row["fiscal_year_end"] for row in rows],
        "Owner earnings ($m)": [
            float(row["owner_earnings_m"])
            if row["owner_earnings_m"] is not None
            else None
            for row in rows
        ],
        "Net income ($m)": [
            float(row["net_income_m"]) if row["net_income_m"] is not None else None
            for row in rows
        ],
    }
).set_index("Fiscal year end")
st.subheader("Owner earnings and net income")
st.line_chart(chart)

st.subheader("Five-year facts")
st.caption(
    "ROE = net income / equity when equity is positive; owner earnings = "
    "operating cash flow - capital spending. Source XBRL tags are shown beside "
    "the underlying reported facts."
)
table = pd.DataFrame(
    [
        {
            "Fiscal year end": row["fiscal_year_end"],
            "Revenue ($m)": row["revenue_m"],
            "Revenue tag": row["revenue_tag"],
            "Net income ($m)": row["net_income_m"],
            "Net income tag": row["net_income_tag"],
            "Operating cash flow ($m)": row["operating_cash_flow_m"],
            "Operating cash flow tag": row["operating_cash_flow_tag"],
            "Capital spending ($m)": row["capital_spending_m"],
            "Capital spending tag": row["capital_spending_tag"],
            "Equity ($m)": row["equity_m"],
            "Equity tag": row["equity_tag"],
            "ROE": (
                f"{row['roe_pct']:.1f}%"
                if row["roe_pct"] is not None
                else "not known"
            ),
            "Owner earnings ($m)": row["owner_earnings_m"],
        }
        for row in rows
    ]
)
st.dataframe(table, width="stretch", hide_index=True)

st.subheader("Buffett's checks")
for check, result in report["checks"].items():
    if result == "pass":
        st.success(f"{check}: pass")
    elif result == "fail":
        st.error(f"{check}: fail")
    else:
        st.warning(f"{check}: not known")

memo_path = Path(__file__).parent / f"{report['ticker']}_buffett_memo.md"
saved_memo = memo_path.read_text(encoding="utf-8") if memo_path.exists() else ""
memo = st.text_area(
    "Buffett-style business memo (editable)",
    value=saved_memo,
    height=260,
    key=f"memo_{report['ticker']}",
)
if st.button("Save memo as Markdown"):
    memo_path.write_text(memo.rstrip() + "\n", encoding="utf-8")
    st.success(f"Saved {memo_path.name}")

script_output = format_report(report)
unprinted = unprinted_numbers(memo, script_output)
if unprinted:
    st.error("Memo contains numbers not printed by the facts script: " + ", ".join(unprinted))
else:
    st.success("All numbers in the memo appear in the facts script output.")

st.markdown("#### Memo preview")
if memo.strip():
    st.markdown(memo)
else:
    st.info(f"No memo saved yet. Save a Buffett-style memo to {memo_path.name}.")
