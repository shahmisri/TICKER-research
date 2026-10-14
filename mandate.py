
# Lab 13 — Meridian Foundation Mandate Checker

from collections import defaultdict

# EDITABLE INPUTS

reserve_size = 100.0
quarterly_distribution = 0.75
quarters_to_cover = 4
liquidity_window = 5
minimum_liquid_share = 90.0
issuer_limit = 8.0

holdings = {
    "Cash": {"issuer": "none", "days": 0, "reserve": True},
    "Treasury bills": {"issuer": "U.S. Treasury", "days": 1, "reserve": True},
    "Treasury 10-year note": {"issuer": "U.S. Treasury", "days": 1, "reserve": True},
    "Global equity index fund": {"issuer": "diversified fund", "days": 2, "reserve": False},
    "Investment-grade bond fund": {"issuer": "diversified fund", "days": 3, "reserve": False},
    "Private real estate fund": {"issuer": "diversified fund", "days": 90, "reserve": False},
    "Acme Corp bonds": {"issuer": "Acme Corp", "days": 4, "reserve": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "days": 1, "reserve": False}
}

candidates = {
    "A": [2, 2, 10, 60, 26, 0, 0, 0],
    "B": [1, 0, 0, 55, 20, 15, 5, 4],
    "C": [1, 1, 0, 70, 20, 0, 0, 8],
    "D": [100, 0, 0, 0, 0, 0, 0, 0]
}

# CALCULATIONS

reserve_minimum = (
    quarters_to_cover * quarterly_distribution
    / reserve_size * 100
)

exempt_issuers = {
    "none", "U.S. Treasury", "diversified fund"
}

def check_candidate(name, weights):
    if len(weights) != len(holdings):
        raise ValueError("Weight count must match holdings count.")

    portfolio = dict(zip(holdings, weights))

    total_weight = sum(portfolio.values())
    lowest_weight = min(portfolio.values())

    reserve_weight = sum(
        weight for holding, weight in portfolio.items()
        if holdings[holding]["reserve"]
    )

    liquid_weight = sum(
        weight for holding, weight in portfolio.items()
        if holdings[holding]["days"] <= liquidity_window
    )

    company_exposures = defaultdict(float)

    for holding, weight in portfolio.items():
        issuer = holdings[holding]["issuer"]
        if issuer not in exempt_issuers:
            company_exposures[issuer] += weight

    largest_company = max(
        company_exposures.values(), default=0.0
    )

    checks = [
        ("Weights sum to 100", total_weight,
         abs(total_weight - 100) < 1e-9),
        ("Long-only (lowest weight)", lowest_weight,
         lowest_weight >= 0),
        ("Reserve eligible weight", reserve_weight,
         reserve_weight + 1e-9 >= reserve_minimum),
        ("Redeemable within 5 days", liquid_weight,
         liquid_weight + 1e-9 >= minimum_liquid_share),
        ("Largest single company", largest_company,
         largest_company <= issuer_limit + 1e-9)
    ]

    failures = 0
    print(f"\nCandidate {name}")

    for label, value, passed in checks:
        result = "pass" if passed else "FAIL"
        print(f"{label}: {value:.1f} — {result}")
        if not passed:
            failures += 1

    print("Calendar-year loss: requires CIO clarification")

    if failures == 0:
        print("Verdict: passes every checkable rule")
    else:
        print(f"Verdict: fails {failures} rule(s)")


# RUN CHECKER

print(f"Reserve minimum: {reserve_minimum:.1f}%")

for name, weights in candidates.items():
    check_candidate(name, weights)
