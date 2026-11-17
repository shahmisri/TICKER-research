"""Transparent portfolio calculations for the Meridian Foundation course app."""
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import numpy as np
import pandas as pd


ASSETS = ("BIL", "IEF", "LQD", "VT")
TRAINING_RETURNS = np.array([0.035, 0.043, 0.050, 0.080], dtype=float)
TRAINING_VOLATILITIES = np.array([0.005, 0.070, 0.060, 0.160], dtype=float)
TRAINING_CORRELATIONS = np.array(
    [
        [1.00, 0.10, 0.05, 0.00],
        [0.10, 1.00, 0.80, -0.10],
        [0.05, 0.80, 1.00, 0.25],
        [0.00, -0.10, 0.25, 1.00],
    ],
    dtype=float,
)

RETURN_PROXY = 0.065
RESERVE_MINIMUM = 0.03
LIQUIDITY_MINIMUM = 0.90
ISSUER_LIMIT = 0.08
TURNOVER_LIMIT = 0.25
RELEASE_TIME = "16:15"

PORTFOLIOS: dict[str, tuple[float, ...]] = {
    "Equal weight": (0.25, 0.25, 0.25, 0.25),
    "Benchmark 40% LQD / 60% VT": (0.00, 0.00, 0.40, 0.60),
    "Constrained candidate": (0.10, 0.10, 0.20, 0.60),
}

_COMMIT_SHA = re.compile(r"^[0-9a-fA-F]{7,40}$")
_PREDICTION_INPUT = re.compile(
    r"^Changed input: VT expected return = (-?\d+(?:\.\d+)?)%$",
    flags=re.MULTILINE,
)


def _validated_weights(weights: Any) -> np.ndarray:
    result = np.asarray(weights, dtype=float)
    if result.shape != (len(ASSETS),) or not np.isfinite(result).all():
        raise ValueError(f"Weights must contain {len(ASSETS)} finite values.")
    if not np.isclose(result.sum(), 1.0, atol=1e-9):
        raise ValueError("Portfolio weights must sum to 100%.")
    return result


def _validated_inputs(
    returns: Any,
    volatilities: Any,
    correlations: Any,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    expected = np.asarray(returns, dtype=float)
    risk = np.asarray(volatilities, dtype=float)
    corr = np.asarray(correlations, dtype=float)
    size = len(ASSETS)
    if expected.shape != (size,) or risk.shape != (size,):
        raise ValueError("Return and volatility assumptions must match the ETF universe.")
    if corr.shape != (size, size):
        raise ValueError("Correlation matrix must be square and match the ETF universe.")
    if not np.isfinite(expected).all() or not np.isfinite(risk).all():
        raise ValueError("Return and volatility assumptions must be finite.")
    if (risk < 0).any():
        raise ValueError("Volatilities cannot be negative.")
    if not np.isfinite(corr).all() or (corr < -1).any() or (corr > 1).any():
        raise ValueError("Correlations must be finite and between -1 and 1.")
    if not np.allclose(corr, corr.T, atol=1e-10):
        raise ValueError("Correlation matrix must be symmetric.")
    if not np.allclose(np.diag(corr), 1.0, atol=1e-10):
        raise ValueError("Correlation matrix diagonal values must equal 1.")
    covariance = corr * np.outer(risk, risk)
    if np.linalg.eigvalsh(covariance).min() < -1e-10:
        raise ValueError("Inputs produce a non-positive-semidefinite covariance matrix.")
    return expected, risk, corr


def portfolio_metrics(
    weights: Any,
    returns: Any = TRAINING_RETURNS,
    volatilities: Any = TRAINING_VOLATILITIES,
    correlations: Any = TRAINING_CORRELATIONS,
) -> dict[str, float]:
    """Calculate model return, volatility, and reserve share from stated inputs."""
    w = _validated_weights(weights)
    expected, risk, corr = _validated_inputs(returns, volatilities, correlations)
    covariance = corr * np.outer(risk, risk)
    variance = float(w @ covariance @ w)
    if variance < -1e-10:
        raise ValueError("Portfolio variance is negative.")
    return {
        "expected_return": float(w @ expected),
        "volatility": float(np.sqrt(max(variance, 0.0))),
        "reserve_share": float(w[0] + w[1]),
    }


def mandate_checks(
    weights: Any,
    *,
    expected_return: float,
    redeemable_share: float | None = None,
    largest_company_share: float | None = None,
    annual_turnover: float | None = None,
) -> list[dict[str, str]]:
    """Return explicit checkable outcomes; missing mandate evidence stays unknown."""
    w = np.asarray(weights, dtype=float)
    if w.shape != (len(ASSETS),) or not np.isfinite(w).all():
        raise ValueError(f"Weights must contain {len(ASSETS)} finite values.")
    reserve_share = float(w[0] + w[1])
    checks = [
        {
            "Requirement": "Weights sum to 100%",
            "Result": "PASS" if np.isclose(w.sum(), 1.0, atol=1e-9) else "FAIL",
            "Basis": f"{w.sum():.1%}",
        },
        {
            "Requirement": "Long-only / no leverage in allocation",
            "Result": "PASS" if (w >= -1e-12).all() and w.sum() <= 1.0 + 1e-9 else "FAIL",
            "Basis": "Allocation weights; trading controls not modeled",
        },
        {
            "Requirement": "6.5% classroom return proxy",
            "Result": "PASS" if expected_return >= RETURN_PROXY - 1e-12 else "FAIL",
            "Basis": "Lab 14 assumptions only; not CPI + 4%",
        },
        {
            "Requirement": "Reserve-eligible assets >= 3%",
            "Result": "PASS" if reserve_share >= RESERVE_MINIMUM - 1e-12 else "FAIL",
            "Basis": f"{reserve_share:.1%}; BIL and IEF classified from Lab 13",
        },
        {
            "Requirement": "Redeemable within five business days >= 90%",
            "Result": (
                "NOT TESTABLE"
                if redeemable_share is None
                else "PASS" if redeemable_share >= LIQUIDITY_MINIMUM else "FAIL"
            ),
            "Basis": (
                "Fund-level settlement/liquidity evidence not supplied"
                if redeemable_share is None
                else f"{redeemable_share:.1%} entered for scenario only"
            ),
        },
        {
            "Requirement": "Single nonexempt company exposure <= 8%",
            "Result": (
                "NOT TESTABLE"
                if largest_company_share is None
                else "PASS" if largest_company_share <= ISSUER_LIMIT else "FAIL"
            ),
            "Basis": (
                "ETF look-through holdings not supplied"
                if largest_company_share is None
                else f"{largest_company_share:.1%} entered for scenario only"
            ),
        },
        {
            "Requirement": "Annual turnover <= 25% without approval",
            "Result": (
                "NOT TESTABLE"
                if annual_turnover is None
                else "PASS" if annual_turnover <= TURNOVER_LIMIT else "FAIL"
            ),
            "Basis": (
                "Prior holdings and turnover definition not supplied"
                if annual_turnover is None
                else f"{annual_turnover:.1%} scenario input; definition needs confirmation"
            ),
        },
        {
            "Requirement": "Actual CPI + 4% objective, net of costs",
            "Result": "NOT TESTABLE",
            "Basis": "CPI series, five-year forward estimates, and full cost data not supplied",
        },
        {
            "Requirement": "Calendar-year loss limit",
            "Result": "UNRESOLVED",
            "Basis": "Lab 13 says loss measure and breach procedure need CIO clarification",
        },
    ]
    return checks


def portfolio_verdict(checks: list[dict[str, str]]) -> str:
    outcomes = {check["Result"] for check in checks}
    if "FAIL" in outcomes:
        return "FAILS at least one checkable mandate rule"
    if outcomes.intersection({"NOT TESTABLE", "UNRESOLVED"}):
        return "NOT CLEARED — material mandate checks remain unverified"
    return "PASSES all supplied mandate checks"


def historical_metrics(prices: pd.DataFrame, window_months: int | None = None) -> dict[str, Any]:
    """Summarize supplied adjusted prices; these are historical, not forecasts."""
    missing = set(ASSETS).difference(prices.columns)
    if missing:
        raise ValueError(f"Price data is missing columns: {', '.join(sorted(missing))}")
    cleaned = prices.loc[:, ASSETS].apply(pd.to_numeric, errors="raise").dropna()
    if (cleaned <= 0).any().any():
        raise ValueError("Prices must be positive.")
    monthly_returns = cleaned.pct_change().dropna()
    if window_months is not None:
        if window_months <= 0:
            raise ValueError("Rolling window must be a positive number of months.")
        monthly_returns = monthly_returns.tail(window_months)
    if len(monthly_returns) < 2:
        raise ValueError("At least two monthly return observations are required.")

    annual_returns = monthly_returns.mean() * 12
    annual_volatility = monthly_returns.std(ddof=1) * np.sqrt(12)
    return {
        "observations": len(monthly_returns),
        "annual_returns": annual_returns,
        "annual_volatility": annual_volatility,
        "correlations": monthly_returns.corr(),
        "monthly_returns": monthly_returns,
    }


def max_drawdown(monthly_returns: pd.Series) -> float:
    """Calculate historical peak-to-trough drawdown from a return series."""
    if monthly_returns.empty or not np.isfinite(monthly_returns.to_numpy()).all():
        raise ValueError("A finite, non-empty return series is required.")
    wealth = (1.0 + monthly_returns).cumprod()
    drawdown = wealth / wealth.cummax() - 1.0
    return float(drawdown.min())


def historical_portfolio_metrics(
    weights: Any,
    history: dict[str, Any],
) -> dict[str, float]:
    w = _validated_weights(weights)
    returns = history["monthly_returns"].loc[:, ASSETS]
    portfolio_returns = returns @ w
    return {
        "annualized_arithmetic_return": float(portfolio_returns.mean() * 12),
        "annualized_volatility": float(portfolio_returns.std(ddof=1) * np.sqrt(12)),
        "max_drawdown": max_drawdown(portfolio_returns),
    }


def transaction_cost_drag(
    annual_turnover: float,
    cost_basis_points: float,
) -> float:
    if not 0 <= annual_turnover <= 1:
        raise ValueError("Annual turnover must be between 0% and 100%.")
    if cost_basis_points < 0 or not np.isfinite(cost_basis_points):
        raise ValueError("Transaction cost must be finite and non-negative.")
    return annual_turnover * cost_basis_points / 10_000


def observation_published_by(
    observation_date: str | pd.Timestamp,
    decision_date: str | pd.Timestamp,
    decision_time: str,
) -> bool:
    observed_day = pd.Timestamp(observation_date).date()
    decision_day = pd.Timestamp(decision_date).date()
    decision_clock = pd.Timestamp(f"2000-01-01 {decision_time}").time()
    release_clock = pd.Timestamp(f"2000-01-01 {RELEASE_TIME}").time()
    return observed_day < decision_day or (
        observed_day == decision_day and decision_clock >= release_clock
    )


def eligible_dgs10_observation(
    observations: pd.DataFrame,
    decision_date: str | pd.Timestamp,
    decision_time: str,
) -> pd.Series | None:
    """Select a checked vintage observation available by the stated decision time."""
    decision_day = pd.Timestamp(decision_date).date()
    if {"observation_date", "vintage_date", "value", "point_in_time_checked"} - set(
        observations.columns
    ):
        raise ValueError("DGS10 observation file is missing required columns.")
    data = observations.copy()
    data["observation_date"] = pd.to_datetime(data["observation_date"]).dt.date
    data["vintage_date"] = pd.to_datetime(data["vintage_date"]).dt.date
    data = data.loc[
        data["point_in_time_checked"].astype(str).str.lower().eq("true")
        & (data["vintage_date"] <= decision_day)
        & (data["observation_date"] <= decision_day)
    ]
    data = data.loc[
        data["observation_date"].map(
            lambda observed_day: observation_published_by(
                pd.Timestamp(observed_day),
                pd.Timestamp(decision_day),
                decision_time,
            )
        )
    ]
    if data.empty:
        return None
    return data.sort_values("observation_date").iloc[-1]


def prediction_input_from_document(document: str) -> float | None:
    match = _PREDICTION_INPUT.search(document)
    return float(match.group(1)) if match else None


def locked_experiment_ready(
    prediction_document: str,
    changed_vt_return: float,
    commit_sha: str,
    github_commit_url: str,
    personally_committed: bool,
) -> tuple[bool, str]:
    """Gate the changed-input run on a saved, matching, self-committed prediction."""
    if not prediction_document.strip():
        return False, "Write and save your own prediction before testing."
    saved_input = prediction_input_from_document(prediction_document)
    if saved_input is None:
        return False, "Saved prediction is missing its changed-input record."
    if not np.isclose(saved_input, changed_vt_return, atol=1e-9):
        return False, "The changed input differs from your saved prediction; rewrite and commit it."
    if not _COMMIT_SHA.fullmatch(commit_sha.strip()):
        return False, "Enter the GitHub commit SHA that contains this prediction."
    if not re.fullmatch(
        rf"https://github\.com/[^/\s]+/[^/\s]+/commit/{re.escape(commit_sha.strip())}",
        github_commit_url.strip(),
    ):
        return False, "Enter the matching GitHub commit URL for the prediction."
    if not personally_committed:
        return False, "Confirm that you personally wrote and committed the prediction."
    if not any(line.strip() for line in prediction_document.split("Prediction:")[-1].splitlines()):
        return False, "The prediction text cannot be blank."
    return True, "Prediction gate passed; the changed-input test can be run manually."


def run_changed_input_test(changed_vt_return: float) -> dict[str, dict[str, float]]:
    """Run the explicitly requested test after the app's prediction gate passes."""
    changed_returns = TRAINING_RETURNS.copy()
    changed_returns[3] = changed_vt_return / 100
    results: dict[str, dict[str, float]] = {}
    for name, weights in PORTFOLIOS.items():
        results[name] = portfolio_metrics(weights, returns=changed_returns)
    return results


def load_price_data(path: Path) -> pd.DataFrame:
    prices = pd.read_csv(path, parse_dates=["Date"]).set_index("Date").sort_index()
    if prices.index.has_duplicates:
        raise ValueError("Price data contains duplicate dates.")
    return prices
