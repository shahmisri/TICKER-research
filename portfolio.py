
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
