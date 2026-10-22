
import pandas as pd
import numpy as np

from portfolio import optimize_portfolio

# Load monthly adjusted closing prices
prices = pd.read_csv(
    "prices.csv",
    index_col="Date",
    parse_dates=True,
)

tickers = ["BIL", "IEF", "LQD", "VT"]
prices = prices[tickers].sort_index()

# Calculate monthly percentage returns
monthly_returns = prices.pct_change().dropna()


def analyze_period(name, returns):
    annual_returns = returns.mean() * 12
    annual_volatilities = returns.std() * np.sqrt(12)
    correlations = returns.corr()

    result = optimize_portfolio(
        returns=annual_returns.to_numpy(),
        volatilities=annual_volatilities.to_numpy(),
        correlations=correlations.to_numpy(),
        target_return=0.065,
        reserve_minimum=0.03,
    )

    print(f"\n{name}")
    print("-" * 45)
    print("Monthly return observations:", len(returns))

    print("\nAnnualized expected returns:")
    for ticker, value in annual_returns.items():
        print(f"{ticker}: {value * 100:.2f}%")

    print("\nAnnualized volatility:")
    for ticker, value in annual_volatilities.items():
        print(f"{ticker}: {value * 100:.2f}%")

    if result is None:
        print("\nNo feasible portfolio meets the 6.5% target.")
    else:
        print("\nMinimum-risk portfolio:")
        for ticker, weight in zip(tickers, result["weights"]):
            print(f"{ticker}: {weight * 100:.1f}%")

        print(f"Expected return: {result['return'] * 100:.2f}%")
        print(f"Volatility: {result['volatility'] * 100:.2f}%")
        print(f"Reserve eligible: {result['reserve'] * 100:.1f}%")


analyze_period("FIVE-YEAR HISTORICAL ESTIMATES", monthly_returns)

analyze_period(
    "MOST RECENT 36 MONTHS",
    monthly_returns.tail(36),
)
