"""FIN 43900 Project 1 — Microsoft interactive valuation workbench.
Run from the directory containing msft_proforma.py and dcf.py:
    python -m streamlit run app.py
"""
from copy import deepcopy

import pandas as pd
import streamlit as st

from msft_proforma import base_inputs, run_model
from dcf import value_per_share as fcff_value_per_share

st.set_page_config(page_title="MSFT Valuation Workbench", layout="wide")
st.title("Microsoft (MSFT) — Project 1 Valuation Workbench")
st.caption("FIN 43900 | Forecast FY2027–FY2031 | USD millions unless per-share")

base = base_inputs()
with st.sidebar:
    st.header("Scenario assumptions")
    growth_shift = st.slider("Revenue growth shift (percentage points)", -6.0, 6.0, 0.0, 0.5)
    gross_margin = st.slider("Gross margin (%)", 60.0, 75.0, base["gross_margin"] * 100, 0.5)
    capex_multiplier = st.slider("Capital spending multiplier", 0.70, 1.30, 1.0, 0.05)
    cost_of_equity = st.slider("Cost of equity (%)", 8.0, 15.0, base["cost_of_equity"] * 100, 0.5)
    terminal_growth = st.slider("FCFE terminal growth (%)", 1.0, 5.0, base["terminal_growth"] * 100, 0.5)
    minimum_cash = st.number_input(
        "Minimum cash requirement ($ millions)",
        min_value=0.0,
        max_value=300000.0,
        value=0.0,
        step=10000.0
    )

    st.divider()
    st.subheader("Separate FCFF DCF")
    wacc = st.slider("WACC (%)", 8.0, 14.0, 10.0, 0.5)
    fcff_terminal_growth = st.slider("FCFF terminal growth (%)", 1.0, 5.0, 3.0, 0.5)
    st.caption("To reset: choose 0 pp growth shift, 68% margin, 1.0× capex, 10% discount rates, and 3% terminal growth.")

inputs = deepcopy(base)
inputs["revenue_growth"] = [x + growth_shift / 100 for x in base["revenue_growth"]]
inputs["gross_margin"] = gross_margin / 100
inputs["capex"] = [x * capex_multiplier for x in base["capex"]]
inputs["cost_of_equity"] = cost_of_equity / 100
inputs["terminal_growth"] = terminal_growth / 100
inputs["minimum_cash"] = minimum_cash

if inputs["terminal_growth"] >= inputs["cost_of_equity"]:
    st.error("FCFE terminal growth must be below cost of equity.")
    st.stop()
if fcff_terminal_growth >= wacc:
    st.error("FCFF terminal growth must be below WACC.")
    st.stop()

model = run_model(inputs)
base_model = run_model(base)
fcff_price = fcff_value_per_share(wacc / 100, fcff_terminal_growth / 100)

st.subheader("Valuation summary")
a, b, c, d = st.columns(4)
a.metric("FCFE pro-forma / share", f"${model['value_per_share']:,.2f}", f"${model['value_per_share']-base_model['value_per_share']:+,.2f} vs base")
b.metric("FCFF DCF / share", f"${fcff_price:,.2f}")
c.metric("FY2031 revenue ($m)", f"{model['results'][-1]['revenue']:,.0f}")
d.metric("FY2031 FCFE ($m)", f"{model['results'][-1]['fcfe']:,.0f}")
st.info("FCFE and FCFF valuations are separate models. Revenue, margin and capex controls affect FCFE; WACC and FCFF terminal growth affect the independent FCFF DCF. Do not treat them as a reconciled valuation.")

st.subheader("Three-statement forecast")
rows = model["results"]
sections = {
    "Income statement": ["revenue", "gross_profit", "operating_expenses", "depreciation", "operating_income", "pretax_income", "taxes", "net_income"],
    "Balance sheet": ["cash", "short_term_investments", "inventory", "ppe", "other_assets", "total_assets", "debt", "other_liabilities", "total_liabilities", "equity"],
    "Cash flow (simplified)": ["net_income", "depreciation", "capex", "fcfe"],
}
for name, fields in sections.items():
    with st.expander(name, expanded=name == "Income statement"):
        df = pd.DataFrame({str(r["year"]): {k: r[k] for k in fields} for r in rows})
        st.dataframe(df.style.format("{:,.1f}"), use_container_width=True)

st.subheader("Validation checks")
check_df = pd.DataFrame([{
    "Year": r["year"],
    "Assets − liabilities − equity ($m)": r["balance_gap"],
    "Cash ($m)": r["cash"],
    "Status": "PASS" if not r["invalid_reasons"] else "FAIL: " + "; ".join(r["invalid_reasons"]),
} for r in rows])
st.dataframe(check_df, use_container_width=True, hide_index=True)
if model["invalid"]:
    st.error("Model check failed. Review the affected year(s); do not use this scenario for an investment decision.")
else:
    st.success("All five forecast years pass the model's balance and minimum-cash checks.")

st.subheader("Scenario comparison")
scenarios = []
for label, shift, margin in [("Lower", -2, 0.68), ("Base", 0, 0.68), ("Higher", 2, 0.68), ("Lower margin", 0, 0.66), ("Higher margin", 0, 0.70)]:
    case_inputs = deepcopy(base)
    case_inputs["revenue_growth"] = [g + shift / 100 for g in base["revenue_growth"]]
    case_inputs["gross_margin"] = margin
    result = run_model(case_inputs)
    scenarios.append({"Scenario": label, "FCFE value/share ($)": result["value_per_share"], "FY2031 operating income ($m)": result["results"][-1]["operating_income"], "Status": "FAIL" if result["invalid"] else "PASS"})
st.dataframe(pd.DataFrame(scenarios), use_container_width=True, hide_index=True)

st.caption("Analyst note: Balance-sheet balance alone does not validate the model's economic assumptions. Independently reconcile FCFE and FCFF inputs, opening balances, cash flows, and terminal value before final submission.")
