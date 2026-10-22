
import math

# LAB 14 — PORTFOLIO BASELINES
# Course-provided training assumptions

ASSETS = [
    "Treasury bills",
    "Treasury 10-year note",
    "Investment-grade bond fund",
    "Global equity index fund",
]

RETURNS = [0.035, 0.043, 0.050, 0.080]
VOLATILITIES = [0.005, 0.070, 0.060, 0.160]

CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]

OBJECTIVE_RETURN = 0.065
RESERVE_INDICES = [0, 1]


def validate_correlations(correlations):
    n = len(VOLATILITIES)

    if len(correlations) != n:
        raise ValueError("Correlation matrix has wrong dimensions.")

    for i in range(n):
        if len(correlations[i]) != n:
            raise ValueError("Correlation matrix must be square.")

        for j in range(n):
            value = correlations[i][j]

            if not math.isfinite(value) or not -1 <= value <= 1:
                raise ValueError(
                    f"Invalid correlation at ({i}, {j}): {value}"
                )

            if not math.isclose(
                value, correlations[j][i], abs_tol=1e-10
            ):
                raise ValueError("Correlation matrix is not symmetric.")

        if not math.isclose(
            correlations[i][i], 1.0, abs_tol=1e-10
        ):
            raise ValueError("Diagonal correlations must equal 1.")


def build_covariance_matrix(volatilities, correlations):
    validate_correlations(correlations)
    n = len(volatilities)

    return [
        [
            correlations[i][j] * volatilities[i] * volatilities[j]
            for j in range(n)
        ]
        for i in range(n)
    ]


def expected_return(weights, returns):
    return sum(w * r for w, r in zip(weights, returns))


def portfolio_volatility(weights, covariance):
    variance = sum(
        weights[i] * weights[j] * covariance[i][j]
        for i in range(len(weights))
        for j in range(len(weights))
    )
    if variance < -1e-12:
        raise ValueError("Portfolio variance is negative.")
    return math.sqrt(max(variance, 0.0))


def reserve_weight(weights):
    return sum(weights[i] for i in RESERVE_INDICES)


def inverse_volatility_weights(volatilities):
    inverse = [1.0 / v for v in volatilities]
    total = sum(inverse)
    return [v / total for v in inverse]


def evaluate_portfolio(name, weights, covariance):
    if not math.isclose(sum(weights), 1.0, abs_tol=1e-9):
        raise ValueError("Portfolio weights must sum to 100%.")

    ret = expected_return(weights, RETURNS)
    vol = portfolio_volatility(weights, covariance)
    reserve = reserve_weight(weights)

    print(f"\n{name}")
    for asset, weight in zip(ASSETS, weights):
        print(f"  {asset}: {weight * 100:.1f}%")

    print(f"Expected return: {ret * 100:.2f}%")
    print(f"Volatility: {vol * 100:.2f}%")
    print(f"Reserve eligible: {reserve * 100:.1f}%")
    print(f"Meets 6.5% objective: {'Yes' if ret >= OBJECTIVE_RETURN else 'No'}")


def main():
    covariance = build_covariance_matrix(
        VOLATILITIES, CORRELATIONS
    )

    portfolios = {
        "Benchmark": [0.0, 0.0, 0.40, 0.60],
        "Equal weight": [0.25, 0.25, 0.25, 0.25],
        "Inverse volatility": inverse_volatility_weights(
            VOLATILITIES
        ),
    }

    print("LAB 14 — PORTFOLIO BASELINES")
    print(f"Objective return: {OBJECTIVE_RETURN * 100:.1f}%")

    for name, weights in portfolios.items():
        evaluate_portfolio(name, weights, covariance)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"ERROR: {error}")
        raise SystemExit(1)

# LAB 15 — PORTFOLIO OPTIMIZER

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def optimize_portfolio(
    returns=None,
    volatilities=None,
    correlations=None,
    target_return=0.065,
    reserve_minimum=0.03,
    step=0.05,
):
    if returns is None:
        returns = RETURNS
    if volatilities is None:
        volatilities = VOLATILITIES
    if correlations is None:
        correlations = CORRELATIONS

    covariance = np.array(correlations) * np.outer(
        volatilities, volatilities
    )

    best = None

    n_steps = round(1 / step)

    for a in range(n_steps + 1):
        for b in range(n_steps - a + 1):
            for c in range(n_steps - a - b + 1):
                d = n_steps - a - b - c

                weights = np.array([a, b, c, d]) * step

                portfolio_return = np.dot(weights, returns)

                reserve = weights[0] + weights[1]

                if portfolio_return < target_return - 1e-9:
                    continue

                if reserve < reserve_minimum - 1e-9:
                    continue

                variance = weights @ covariance @ weights
                volatility = np.sqrt(max(variance, 0))

                if best is None or volatility < best["volatility"]:
                    best = {
                        "weights": weights.tolist(),
                        "return": float(portfolio_return),
                        "volatility": float(volatility),
                        "reserve": float(reserve),
                    }

    return best


def estimate_from_prices(prices):
    monthly_returns = prices.pct_change().dropna()

    annual_returns = monthly_returns.mean() * 12
    annual_volatilities = monthly_returns.std() * np.sqrt(12)
    correlations = monthly_returns.corr()

    return (
        annual_returns,
        annual_volatilities,
        correlations,
    )


def run_optimizer_test():
    print("\nLAB 15 — MINIMUM RISK PORTFOLIO")

    result = optimize_portfolio()

    if result is None:
        print("No feasible portfolio found.")
        return

    for asset, weight in zip(ASSETS, result["weights"]):
        print(f"{asset}: {weight * 100:.1f}%")

    print(f"Expected return: {result['return'] * 100:.2f}%")
    print(f"Volatility: {result['volatility'] * 100:.2f}%")
    print(f"Reserve eligible: {result['reserve'] * 100:.1f}%")


run_optimizer_test()
