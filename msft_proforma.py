# Lab 10 — Microsoft (MSFT) Pro-Forma
# Five-year personalized three-statement model
# USD millions except per-share amounts

from copy import deepcopy

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
# MODEL INPUTS AND RECALCULATION
# ============================================================

def base_inputs():
    return {
        "revenue_growth": deepcopy(REVENUE_GROWTH),
        "gross_margin": GROSS_MARGIN,
        "operating_expense_ratio": OPERATING_EXPENSE_RATIO,
        "depreciation_rate": DEPRECIATION_RATE,
        "tax_rate": TAX_RATE,
        "inventory_days": INVENTORY_DAYS,
        "capex": deepcopy(CAPEX),
        "other_asset_rate": OTHER_ASSET_RATE,
        "floor_plan": FLOOR_PLAN,
        "debt": DEBT,
        "other_liabilities": OTHER_LIABILITIES,
        "short_term_investments": SHORT_TERM_INVESTMENTS,
        "distributions": DISTRIBUTIONS,
        "minimum_cash": MINIMUM_CASH,
        "cost_of_equity": COST_OF_EQUITY,
        "terminal_growth": TERMINAL_GROWTH,
        "shares": SHARES,
    }


def opening_state():
    return {
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


def run_model(inputs):
    state = opening_state()
    results = []

    for i, year in enumerate(YEARS):
        opening = state.copy()
        revenue = opening["revenue"] * (1 + inputs["revenue_growth"][i])
        gross_profit = revenue * inputs["gross_margin"]
        operating_expenses = revenue * inputs["operating_expense_ratio"]
        depreciation = opening["ppe"] * inputs["depreciation_rate"]
        operating_income = gross_profit - operating_expenses - depreciation
        pretax_income = operating_income
        taxes = max(0, pretax_income) * inputs["tax_rate"]
        net_income = pretax_income - taxes

        cost_of_revenue = revenue - gross_profit
        inventory = cost_of_revenue * inputs["inventory_days"] / 365
        change_inventory = inventory - opening["inventory"]
        ppe = opening["ppe"] + inputs["capex"][i] - depreciation
        change_revenue = revenue - opening["revenue"]
        change_other_assets = inputs["other_asset_rate"] * change_revenue
        other_assets = opening["other_assets"] + change_other_assets
        short_term_investments = opening["short_term_investments"]
        debt = inputs["debt"]
        other_liabilities = inputs["other_liabilities"]
        equity = opening["equity"] + net_income - inputs["distributions"]

        fcfe = (
            net_income
            + depreciation
            - inputs["capex"][i]
            - change_inventory
            - change_other_assets
        )
        cash = opening["cash"] + fcfe - inputs["distributions"]
        total_assets = cash + short_term_investments + inventory + ppe + other_assets
        total_liabilities = debt + other_liabilities
        balance_gap = total_assets - (total_liabilities + equity)
        invalid_reasons = []
        if abs(balance_gap) > 0.1:
            invalid_reasons.append(f"balance gap {balance_gap:.1f}")
        if cash < inputs["minimum_cash"] - 0.1:
            invalid_reasons.append(f"cash {cash:.1f} below minimum")

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
            "capex": inputs["capex"][i],
            "balance_gap": balance_gap,
            "invalid_reasons": invalid_reasons,
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

    pv_fcfe = sum(
        result["fcfe"] / ((1 + inputs["cost_of_equity"]) ** i)
        for i, result in enumerate(results, start=1)
    )
    terminal_fcfe = results[-1]["fcfe"] * (1 + inputs["terminal_growth"])
    terminal_value = terminal_fcfe / (
        inputs["cost_of_equity"] - inputs["terminal_growth"]
    )
    pv_terminal = terminal_value / ((1 + inputs["cost_of_equity"]) ** 5)
    equity_value = pv_fcfe + pv_terminal

    return {
        "inputs": deepcopy(inputs),
        "results": results,
        "pv_fcfe": pv_fcfe,
        "pv_terminal": pv_terminal,
        "equity_value": equity_value,
        "value_per_share": equity_value / inputs["shares"],
        "share_after_forecast": pv_terminal / equity_value,
        "invalid": any(result["invalid_reasons"] for result in results),
    }


# ============================================================
# REPORTING AND ONE-AT-A-TIME SENSITIVITY
# ============================================================

def print_table(title, model, rows):
    print("\n" + title)
    print(
        f"{'Line':<28}"
        + "".join(f"{year:>14}" for year in YEARS)
    )
    for label, key in rows:
        print(
            f"{label:<28}"
            + "".join(
                f"{result[key]:>14,.1f}"
                for result in model["results"]
            )
        )


def print_statement_details(model):
    print_table(
        "INCOME STATEMENT — BASE CASE",
        model,
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
        "BALANCE SHEET — BASE CASE",
        model,
        [
            ("Cash", "cash"),
            ("Short-term investments", "short_term_investments"),
            ("Inventory", "inventory"),
            ("PP&E", "ppe"),
            ("Other assets", "other_assets"),
            ("Total assets", "total_assets"),
            ("Debt", "debt"),
            ("Other liabilities", "other_liabilities"),
            ("Total liabilities", "total_liabilities"),
            ("Equity", "equity"),
        ],
    )
    print_table(
        "CASH FLOW — BASE CASE",
        model,
        [
            ("Net income", "net_income"),
            ("Depreciation", "depreciation"),
            ("Capital spending", "capex"),
            ("FCFE", "fcfe"),
        ],
    )


def print_checks(label, model):
    print(f"\nCHECKS — {label}")
    for result in model["results"]:
        status = "INVALID: " + "; ".join(result["invalid_reasons"])
        if not result["invalid_reasons"]:
            status = "OK"
        print(
            f"FY{result['year']}E: "
            f"Assets - liabilities - equity = {result['balance_gap']:.1f}; "
            f"Cash = {result['cash']:,.1f}; {status}"
        )


def print_sensitivity_table(driver, scenarios, base_model):
    print(f"\nSENSITIVITY — {driver}")
    print("All values are actual inputs; revenue growth and gross margin are percentages.")
    print(
        f"{'Case':<9}{'Revenue growth FY27-FY31':<31}"
        f"{'Gross margin FY27-FY31':<27}"
        f"{'FY2031 operating profit ($m)':>30}"
        f"{'FY2031 FCFE ($m)':>20}"
        f"{'Value/share ($)':>18}"
        f"{'Status':>12}"
    )
    for label, model in scenarios.items():
        inputs = model["inputs"]
        growth = ", ".join(f"{value:.0%}" for value in inputs["revenue_growth"])
        margin = ", ".join(
            f"{inputs['gross_margin']:.0%}" for _ in YEARS
        )
        final_year = model["results"][-1]
        op_change = final_year["operating_income"] - base_model["results"][-1]["operating_income"]
        fcfe_change = final_year["fcfe"] - base_model["results"][-1]["fcfe"]
        value_change = model["value_per_share"] - base_model["value_per_share"]
        status = "INVALID" if model["invalid"] else "OK"
        print(
            f"{label:<9}{growth:<31}{margin:<27}"
            f"{final_year['operating_income']:>14,.1f} ({op_change:+,.1f})"
            f"{final_year['fcfe']:>10,.1f} ({fcfe_change:+,.1f})"
            f"{model['value_per_share']:>10,.2f} ({value_change:+,.2f})"
            f"{status:>12}"
        )

    valid_models = [model for model in scenarios.values() if not model["invalid"]]
    if valid_models:
        operating_values = [model["results"][-1]["operating_income"] for model in valid_models]
        fcfe_values = [model["results"][-1]["fcfe"] for model in valid_models]
        share_values = [model["value_per_share"] for model in valid_models]
        print(
            f"Spans across valid runs: operating profit ${max(operating_values) - min(operating_values):,.1f}m; "
            f"FCFE ${max(fcfe_values) - min(fcfe_values):,.1f}m; "
            f"value/share ${max(share_values) - min(share_values):,.2f}."
        )
    else:
        print("Spans not ranked because every run is invalid.")


def main():
    original_base_inputs = base_inputs()
    original_base_run = run_model(deepcopy(original_base_inputs))
    print_statement_details(original_base_run)
    print_checks("BASE CASE", original_base_run)

    sensitivity_sets = {
        "Revenue growth": {
            "Lower": [0.10, 0.09, 0.08, 0.07, 0.06],
            "Base": [0.12, 0.11, 0.10, 0.09, 0.08],
            "Higher": [0.14, 0.13, 0.12, 0.11, 0.10],
        },
        "Gross margin": {
            "Lower": 0.66,
            "Base": 0.68,
            "Higher": 0.70,
        },
    }

    for driver, values in sensitivity_sets.items():
        scenarios = {}
        for label, value in values.items():
            inputs = deepcopy(original_base_inputs)
            if driver == "Revenue growth":
                inputs["revenue_growth"] = deepcopy(value)
            else:
                inputs["gross_margin"] = value
            scenarios[label] = run_model(inputs)
            print_checks(f"{driver} — {label}", scenarios[label])
        print_sensitivity_table(driver, scenarios, original_base_run)

    restored_base_inputs = deepcopy(original_base_inputs)
    restored_base_run = run_model(restored_base_inputs)
    input_match = restored_base_inputs == original_base_inputs
    output_match = all(
        abs(restored_base_run[key] - original_base_run[key]) <= 0.01
        for key in ("pv_fcfe", "pv_terminal", "equity_value", "value_per_share")
    )
    print("\nRESTORED BASE CASE")
    print(f"Base inputs restored: {'YES' if input_match else 'NO'}")
    print(f"Base outputs match within rounding tolerance: {'YES' if output_match else 'NO'}")
    print(
        f"FY2031 operating profit: ${restored_base_run['results'][-1]['operating_income']:,.1f} million; "
        f"FY2031 FCFE: ${restored_base_run['results'][-1]['fcfe']:,.1f} million; "
        f"Value per share: ${restored_base_run['value_per_share']:.2f}"
    )


if __name__ == "__main__":
    main()