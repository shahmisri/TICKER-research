# Lab 10 — Microsoft (MSFT) Pro-Forma
# Five-year personalized three-statement model
# USD millions except per-share amounts

YEARS = [2027, 2028, 2029, 2030, 2031]

# ============================================================
# FY2026 OPENING VALUES
# ============================================================

START_REVENUE = 331839.0

# FY2026 balance sheet
START_CASH = 20935.0
START_SHORT_TERM_INVESTMENTS = 55908.0
START_INVENTORY = 1397.0
START_PPE = 313076.0
START_TOTAL_ASSETS = 758376.0

START_DEBT = 40294.0
START_TOTAL_LIABILITIES = 315989.0
START_EQUITY = 442387.0

# Aggregate remaining assets and liabilities so the opening
# FY2026 balance sheet starts exactly balanced.

START_OTHER_ASSETS = (
    START_TOTAL_ASSETS
    - START_CASH
    - START_SHORT_TERM_INVESTMENTS
    - START_INVENTORY
    - START_PPE
)

START_OTHER_LIABILITIES = (
    START_TOTAL_LIABILITIES
    - START_DEBT
)

# ============================================================
# FORECAST ASSUMPTIONS
# ============================================================

# Revenue growth moderates over the forecast.
REVENUE_GROWTH = [
    0.12,
    0.11,
    0.10,
    0.09,
    0.08,
]

GROSS_MARGIN = 0.68

# Operating expenses as a percentage of revenue.
OPERATING_EXPENSE_RATIO = 0.212

# Depreciation as a percentage of opening PP&E.
DEPRECIATION_RATE = 0.123

TAX_RATE = 0.194

# Inventory remains small relative to Microsoft's cost of revenue.
INVENTORY_DAYS = 5.0

# Microsoft-specific assumption:
# elevated capital spending for cloud and AI infrastructure.
CAPEX = [
    120000.0,
    125000.0,
    130000.0,
    135000.0,
    140000.0,
]

# Aggregate other asset investment associated with revenue growth.
OTHER_ASSET_RATE = 0.02

# Microsoft has no ABG-style floor-plan financing.
FLOOR_PLAN = 0.0

# Hold debt and other liabilities constant in this simplified case.
DEBT = START_DEBT
OTHER_LIABILITIES = START_OTHER_LIABILITIES

# Short-term investments held constant.
SHORT_TERM_INVESTMENTS = START_SHORT_TERM_INVESTMENTS

# No modeled distributions in this simplified forecast.
DISTRIBUTIONS = 0.0

# Minimum cash check.
MINIMUM_CASH = 0.0

# Valuation assumptions.
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.03

# Diluted shares, millions.
SHARES = 7453.0


# ============================================================
# BALANCE CHECK
# ============================================================

def assert_balanced(year, gap, cash):
    if abs(gap) > 0.1:
        raise ValueError(
            f"{year} balance sheet does not balance. "
            f"Gap = {gap:.1f}"
        )

    if cash < MINIMUM_CASH - 0.1:
        raise ValueError(
            f"{year} cash is below the minimum. "
            f"Cash = {cash:.1f}"
        )


# ============================================================
# OPENING STATE
# ============================================================

state = {
    "revenue": START_REVENUE,
    "cash": START_CASH,
    "short_term_investments": START_SHORT_TERM_INVESTMENTS,
    "inventory": START_INVENTORY,
    "ppe": START_PPE,
    "other_assets": START_OTHER_ASSETS,
    "debt": START_DEBT,
    "other_liabilities": START_OTHER_LIABILITIES,
    "equity": START_EQUITY,
}

results = []


# ============================================================
# FIVE-YEAR FORECAST
# ============================================================

for i, year in enumerate(YEARS):

    opening = state.copy()

    # --------------------------------------------------------
    # INCOME STATEMENT
    # --------------------------------------------------------

    revenue = (
        opening["revenue"]
        * (1 + REVENUE_GROWTH[i])
    )

    gross_profit = revenue * GROSS_MARGIN

    operating_expenses = (
        revenue
        * OPERATING_EXPENSE_RATIO
    )

    depreciation = (
        opening["ppe"]
        * DEPRECIATION_RATE
    )

    operating_income = (
        gross_profit
        - operating_expenses
        - depreciation
    )

    pretax_income = operating_income

    taxes = (
        max(0, pretax_income)
        * TAX_RATE
    )

    net_income = (
        pretax_income
        - taxes
    )

    # --------------------------------------------------------
    # BALANCE SHEET EXCEPT CASH
    # --------------------------------------------------------

    cost_of_revenue = (
        revenue
        - gross_profit
    )

    inventory = (
        cost_of_revenue
        * INVENTORY_DAYS
        / 365
    )

    change_inventory = (
        inventory
        - opening["inventory"]
    )

    ppe = (
        opening["ppe"]
        + CAPEX[i]
        - depreciation
    )

    change_revenue = (
        revenue
        - opening["revenue"]
    )

    change_other_assets = (
        OTHER_ASSET_RATE
        * change_revenue
    )

    other_assets = (
        opening["other_assets"]
        + change_other_assets
    )

    short_term_investments = (
        opening["short_term_investments"]
    )

    debt = DEBT

    other_liabilities = OTHER_LIABILITIES

    # Equity roll-forward.
    equity = (
        opening["equity"]
        + net_income
        - DISTRIBUTIONS
    )

    # --------------------------------------------------------
    # FREE CASH FLOW TO EQUITY
    # --------------------------------------------------------

    fcfe = (
        net_income
        + depreciation
        - CAPEX[i]
        - change_inventory
        - change_other_assets
    )

    # --------------------------------------------------------
    # CASH — COMPUTED LAST
    # --------------------------------------------------------

    cash = (
        opening["cash"]
        + fcfe
        - DISTRIBUTIONS
    )

    # --------------------------------------------------------
    # BALANCE SHEET CHECK
    # --------------------------------------------------------

    total_assets = (
        cash
        + short_term_investments
        + inventory
        + ppe
        + other_assets
    )

    total_liabilities = (
        debt
        + other_liabilities
    )

    total_liabilities_and_equity = (
        total_liabilities
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
        "operating_expenses": operating_expenses,
        "depreciation": depreciation,
        "operating_income": operating_income,
        "pretax_income": pretax_income,
        "taxes": taxes,
        "net_income": net_income,
        "cash": cash,
        "short_term_investments": short_term_investments,
        "inventory": inventory,
        "ppe": ppe,
        "other_assets": other_assets,
        "total_assets": total_assets,
        "debt": debt,
        "other_liabilities": other_liabilities,
        "total_liabilities": total_liabilities,
        "equity": equity,
        "fcfe": fcfe,
        "capex": CAPEX[i],
        "balance_gap": balance_gap,
    })

    state = {
        "revenue": revenue,
        "cash": cash,
        "short_term_investments": short_term_investments,
        "inventory": inventory,
        "ppe": ppe,
        "other_assets": other_assets,
        "debt": debt,
        "other_liabilities": other_liabilities,
        "equity": equity,
    }


# ============================================================
# PRINT TABLES
# ============================================================

def print_table(title, rows):

    print("\n" + title)

    print(
        f"{'Line':<28}"
        + "".join(
            f"{year:>14}"
            for year in YEARS
        )
    )

    for label, key in rows:

        print(
            f"{label:<28}"
            + "".join(
                f"{result[key]:>14,.1f}"
                for result in results
            )
        )


print_table(
    "INCOME STATEMENT",
    [
        ("Revenue", "revenue"),
        ("Gross profit", "gross_profit"),
        ("Operating expenses", "operating_expenses"),
        ("Depreciation", "depreciation"),
        ("Operating income", "operating_income"),
        ("Pretax income", "pretax_income"),
        ("Taxes", "taxes"),
        ("Net income", "net_income"),
    ],
)


print_table(
    "BALANCE SHEET — ASSETS",
    [
        ("Cash", "cash"),
        ("Short-term investments", "short_term_investments"),
        ("Inventory", "inventory"),
        ("PP&E", "ppe"),
        ("Other assets", "other_assets"),
        ("Total assets", "total_assets"),
    ],
)


print_table(
    "BALANCE SHEET — L+E",
    [
        ("Debt", "debt"),
        ("Other liabilities", "other_liabilities"),
        ("Total liabilities", "total_liabilities"),
        ("Equity", "equity"),
    ],
)


print_table(
    "CASH FLOW",
    [
        ("Net income", "net_income"),
        ("Depreciation", "depreciation"),
        ("Capital spending", "capex"),
        ("FCFE", "fcfe"),
    ],
)


# ============================================================
# CHECK BLOCK
# ============================================================

print("\nCHECKS")

for result in results:

    print(
        f"FY{result['year']}E: "
        f"Assets - liabilities - equity = "
        f"{result['balance_gap']:.1f}; "
        f"Cash = {result['cash']:,.1f}"
    )

    assert_balanced(
        f"FY{result['year']}E",
        result["balance_gap"],
        result["cash"],
    )


# ============================================================
# EQUITY VALUATION
# ============================================================

pv_fcfe = 0.0

for i, result in enumerate(results, start=1):

    pv_fcfe += (
        result["fcfe"]
        / ((1 + COST_OF_EQUITY) ** i)
    )


terminal_fcfe = (
    results[-1]["fcfe"]
    * (1 + TERMINAL_GROWTH)
)

terminal_value = (
    terminal_fcfe
    / (COST_OF_EQUITY - TERMINAL_GROWTH)
)

pv_terminal = (
    terminal_value
    / ((1 + COST_OF_EQUITY) ** 5)
)

equity_value = (
    pv_fcfe
    + pv_terminal
)

value_per_share = (
    equity_value
    / SHARES
)

share_after_forecast = (
    pv_terminal
    / equity_value
)


print("\nVALUATION")

print(
    f"PV of explicit FCFE: "
    f"${pv_fcfe:,.1f} million"
)

print(
    f"PV of terminal value: "
    f"${pv_terminal:,.1f} million"
)

print(
    f"Equity value: "
    f"${equity_value:,.1f} million"
)

print(
    f"Share of value after 2031: "
    f"{share_after_forecast:.1%}"
)

print(
    f"Value per share: "
    f"${value_per_share:.2f}"
)