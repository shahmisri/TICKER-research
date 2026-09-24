# Lab 09 — Pro-Forma Build: ABG Known Answer
# USD millions except per-share amounts

YEARS = [2026, 2027, 2028, 2029, 2030]

# Assumptions
REVENUE_GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_RATIOS = [0.665, 0.655, 0.645, 0.645, 0.645]

DEPRECIATION_RATIO = 82.4 / 3070.4
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255

INVENTORY_DAYS = 2135.8 / (17999.0 - 3071.7) * 365
FLOOR_PLAN_RATIO = 2027.0 / 2135.8
OTHER_WC_RATE = 0.008

MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06

DEBT_REPAYMENT = 150.0
SHARE_BUYBACK = 150.0

FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544

COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349


# FY2025 opening balance sheet
state = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}

results = []


def assert_balanced(year, gap, cash):
    if abs(gap) > 0.1:
        raise ValueError(
            f"{year} balance sheet does not balance. Gap = {gap:.1f}"
        )

    if cash < MINIMUM_CASH - 0.1:
        raise ValueError(
            f"{year} cash is below minimum. Cash = {cash:.1f}"
        )


for i, year in enumerate(YEARS):

    opening = state.copy()

    # -------------------------
    # Income statement
    # -------------------------

    revenue = opening["revenue"] * (1 + REVENUE_GROWTH)

    gross_profit = revenue * GROSS_MARGIN

    sga = gross_profit * SGA_RATIOS[i]

    depreciation = opening["ppe"] * DEPRECIATION_RATIO

    operating_income = (
        gross_profit
        - sga
        - depreciation
        - IMPAIRMENT
    )

    interest = (
        opening["floor_plan"] * FLOOR_PLAN_RATE
        + opening["term_debt"] * TERM_DEBT_RATE
        + opening["revolver"] * REVOLVER_RATE
    )

    pretax_income = operating_income - interest

    taxes = max(0, pretax_income) * TAX_RATE

    net_income = pretax_income - taxes

    # -------------------------
    # Balance sheet except cash
    # -------------------------

    cost_of_sales = revenue - gross_profit

    inventory = cost_of_sales * INVENTORY_DAYS / 365

    floor_plan = inventory * FLOOR_PLAN_RATIO

    ppe = opening["ppe"] + CAPEX - depreciation

    change_revenue = revenue - opening["revenue"]

    other_working_capital = OTHER_WC_RATE * change_revenue

    other_assets = (
        opening["other_assets"]
        + other_working_capital
        - IMPAIRMENT
    )

    term_debt = opening["term_debt"] - DEBT_REPAYMENT

    other_liabilities = opening["other_liabilities"]

    equity = (
        opening["equity"]
        + net_income
        - SHARE_BUYBACK
    )

    # -------------------------
    # Free cash flow to equity
    # -------------------------

    change_inventory = inventory - opening["inventory"]

    change_floor_plan = floor_plan - opening["floor_plan"]

    fcfe = (
        net_income
        + depreciation
        + IMPAIRMENT
        - CAPEX
        - change_inventory
        - other_working_capital
        + change_floor_plan
        - DEBT_REPAYMENT
    )

    # -------------------------
    # Cash and revolver
    # -------------------------

    cash_before_revolver = (
        opening["cash"]
        + fcfe
        - SHARE_BUYBACK
    )

    revolver = opening["revolver"]

    if cash_before_revolver < MINIMUM_CASH:

        required_draw = MINIMUM_CASH - cash_before_revolver

        available_revolver = REVOLVER_LIMIT - revolver

        draw = min(required_draw, available_revolver)

        revolver += draw
        cash = cash_before_revolver + draw

    else:

        revolver_repayment = min(
            revolver,
            cash_before_revolver - MINIMUM_CASH
        )

        revolver -= revolver_repayment
        cash = cash_before_revolver - revolver_repayment

    # -------------------------
    # Balance sheet check
    # -------------------------

    total_assets = (
        cash
        + inventory
        + ppe
        + other_assets
    )

    total_liabilities_and_equity = (
        floor_plan
        + term_debt
        + revolver
        + other_liabilities
        + equity
    )

    balance_gap = (
        total_assets
        - total_liabilities_and_equity
    )

    results.append({
        "year": year,
        "revenue": revenue,
        "gross_profit": gross_profit,
        "sga": sga,
        "depreciation": depreciation,
        "impairment": IMPAIRMENT,
        "operating_income": operating_income,
        "interest": interest,
        "pretax_income": pretax_income,
        "taxes": taxes,
        "net_income": net_income,
        "inventory": inventory,
        "floor_plan": floor_plan,
        "ppe": ppe,
        "other_assets": other_assets,
        "term_debt": term_debt,
        "revolver": revolver,
        "other_liabilities": other_liabilities,
        "equity": equity,
        "fcfe": fcfe,
        "cash": cash,
        "balance_gap": balance_gap,
    })

    state = {
        "revenue": revenue,
        "inventory": inventory,
        "ppe": ppe,
        "other_assets": other_assets,
        "cash": cash,
        "floor_plan": floor_plan,
        "term_debt": term_debt,
        "revolver": revolver,
        "other_liabilities": other_liabilities,
        "equity": equity,
    }


# -------------------------
# Print statements
# -------------------------

def print_table(title, rows):
    print("\n" + title)

    print(
        f"{'Line':<28}"
        + "".join(f"{year:>12}" for year in YEARS)
    )

    for label, key in rows:
        print(
            f"{label:<28}"
            + "".join(
                f"{result[key]:>12.1f}"
                for result in results
            )
        )


print_table(
    "INCOME STATEMENT",
    [
        ("Revenue", "revenue"),
        ("Gross profit", "gross_profit"),
        ("SG&A", "sga"),
        ("Depreciation", "depreciation"),
        ("Impairment", "impairment"),
        ("Operating income", "operating_income"),
        ("Interest", "interest"),
        ("Pretax income", "pretax_income"),
        ("Taxes", "taxes"),
        ("Net income", "net_income"),
    ],
)


print_table(
    "BALANCE SHEET",
    [
        ("Cash", "cash"),
        ("Inventory", "inventory"),
        ("PP&E", "ppe"),
        ("Other assets", "other_assets"),
        ("Floor plan", "floor_plan"),
        ("Term debt", "term_debt"),
        ("Revolver", "revolver"),
        ("Other liabilities", "other_liabilities"),
        ("Equity", "equity"),
    ],
)


print_table(
    "CASH FLOW",
    [
        ("Net income", "net_income"),
        ("Depreciation", "depreciation"),
        ("Impairment", "impairment"),
        ("FCFE", "fcfe"),
    ],
)


# -------------------------
# Checks
# -------------------------

print("\nCHECKS")

for result in results:

    print(
        f"FY{result['year']}E: "
        f"Assets - liabilities - equity = "
        f"{result['balance_gap']:.1f}; "
        f"Cash = {result['cash']:.1f}"
    )

    assert_balanced(
        f"FY{result['year']}E",
        result["balance_gap"],
        result["cash"],
    )


# -------------------------
# Equity valuation
# -------------------------

pv_fcfe = 0.0

for i, result in enumerate(results, start=1):
    pv_fcfe += (
        result["fcfe"]
        / ((1 + COST_OF_EQUITY) ** i)
    )


terminal_fcfe = (
    results[-1]["fcfe"]
    + DEBT_REPAYMENT
)

terminal_value = (
    terminal_fcfe
    * (1 + TERMINAL_GROWTH)
    / (COST_OF_EQUITY - TERMINAL_GROWTH)
)

pv_terminal_value = (
    terminal_value
    / ((1 + COST_OF_EQUITY) ** 5)
)

equity_value = pv_fcfe + pv_terminal_value

value_per_share = (
    equity_value
    / SHARES_OUTSTANDING
)

share_after_2030 = (
    pv_terminal_value
    / equity_value
)


print("\nVALUATION")

print(
    f"Equity value: ${equity_value:,.2f} million"
)

print(
    f"Share of value after 2030: "
    f"{share_after_2030:.1%}"
)

print(
    f"Value per share: ${value_per_share:.2f}"
)