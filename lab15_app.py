
import streamlit as st
import pandas as pd

from portfolio import (
    ASSETS,
    RETURNS,
    VOLATILITIES,
    CORRELATIONS,
    optimize_portfolio,
)

st.set_page_config(
    page_title="Portfolio Stability Lab",
    layout="wide",
)

st.title("Lab 15 — Portfolio Stability Decision")

st.write(
    "Explore how changes in expected returns and correlations "
    "affect the minimum-risk portfolio."
)

st.sidebar.header("Portfolio Assumptions")

equity_return = st.sidebar.slider(
    "Global equity expected return (%)",
    min_value=5.0,
    max_value=10.0,
    value=8.0,
    step=1.0,
)

ig_equity_corr = st.sidebar.slider(
    "IG bond–equity correlation",
    min_value=-0.50,
    max_value=0.90,
    value=0.25,
    step=0.05,
)

target_return = st.sidebar.number_input(
    "Target return (%)",
    min_value=0.0,
    max_value=20.0,
    value=6.5,
    step=0.1,
)

returns = RETURNS.copy()
returns[3] = equity_return / 100

correlations = [row.copy() for row in CORRELATIONS]
correlations[2][3] = ig_equity_corr
correlations[3][2] = ig_equity_corr

result = optimize_portfolio(
    returns=returns,
    volatilities=VOLATILITIES,
    correlations=correlations,
    target_return=target_return / 100,
)

if result is None:
    st.error("No feasible portfolio meets the selected constraints.")
else:
    st.subheader("Minimum-Risk Portfolio")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Expected Return",
        f"{result['return'] * 100:.2f}%",
    )

    col2.metric(
        "Volatility",
        f"{result['volatility'] * 100:.2f}%",
    )

    col3.metric(
        "Reserve Eligible",
        f"{result['reserve'] * 100:.1f}%",
    )

    weights_df = pd.DataFrame({
        "Asset": ASSETS,
        "Weight (%)": [
            round(w * 100, 1)
            for w in result["weights"]
        ],
    })

    st.dataframe(weights_df, hide_index=True)
    st.bar_chart(weights_df.set_index("Asset"))

    st.info(
        "Compare the original assumptions with changes in "
        "equity returns and bond–equity correlation."
    )
