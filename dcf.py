"""Five-year FCFF DCF training model (USD millions, except per-share value)."""

# Inputs: edit these values by hand as needed.
# Source record: MSFT-research/2026-09-10_MSFT_DCF_Inputs.md
# Starting FCFF = 182,899 operating cash flow + 2,459.2199 after-tax interest
#                 - 115,950 capital expenditures (all USD millions).
STARTING_FCFF = 69_408.2199
# Analyst FCFF forecast; it fades from FY2026's 18% revenue growth.
YEARLY_GROWTH_RATES = [0.15, 0.13, 0.11, 0.09, 0.07]
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 76_843.0
DEBT = 40_294.0
DILUTED_SHARES = 7_453.0

# Sensitivity and reverse-DCF inputs.
SENSITIVITY_WACCS = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTHS = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 501.02
REVERSE_SHIFT_LOWER_BOUND = -0.05
REVERSE_SHIFT_UPPER_BOUND = 0.10


def value_per_share(wacc: float, terminal_growth: float, growth_shift: float = 0.0) -> float:
    """Return DCF value per diluted share for a uniform FCFF-growth shift."""
    if terminal_growth >= wacc:
        raise ValueError("terminal growth must be less than WACC")

    adjusted_growth_rates = [rate + growth_shift for rate in YEARLY_GROWTH_RATES]
    if any(rate <= -1.0 for rate in adjusted_growth_rates):
        raise ValueError("a growth rate is -100% or below")

    fcff = []
    current_fcff = STARTING_FCFF
    for growth_rate in adjusted_growth_rates:
        current_fcff *= 1.0 + growth_rate
        fcff.append(current_fcff)

    present_value_explicit_fcff = sum(
        cash_flow / (1.0 + wacc) ** year
        for year, cash_flow in enumerate(fcff, start=1)
    )
    terminal_value_year_5 = fcff[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    present_value_terminal_value = terminal_value_year_5 / (1.0 + wacc) ** 5
    enterprise_value = present_value_explicit_fcff + present_value_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    return equity_value / DILUTED_SHARES


def reverse_dcf_growth_shift() -> float | None:
    """Solve for the uniform explicit-growth shift by bisection, if bracketed."""
    lower = REVERSE_SHIFT_LOWER_BOUND
    upper = REVERSE_SHIFT_UPPER_BOUND

    try:
        lower_value = value_per_share(WACC, TERMINAL_GROWTH, lower)
        upper_value = value_per_share(WACC, TERMINAL_GROWTH, upper)
    except ValueError:
        return None

    if not min(lower_value, upper_value) <= TARGET_SHARE_PRICE <= max(lower_value, upper_value):
        return None

    for _ in range(100):
        midpoint = (lower + upper) / 2.0
        midpoint_value = value_per_share(WACC, TERMINAL_GROWTH, midpoint)
        if midpoint_value < TARGET_SHARE_PRICE:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2.0


def print_sensitivity_grid() -> None:
    print("\nSensitivity Grid — Value per Diluted Share")
    header = "WACC \\ Terminal Growth" + "".join(
        f" | {growth:.0%}" for growth in SENSITIVITY_TERMINAL_GROWTHS
    )
    print(header)
    print("---" + "|---" * len(SENSITIVITY_TERMINAL_GROWTHS))
    for wacc in SENSITIVITY_WACCS:
        cells = []
        for terminal_growth in SENSITIVITY_TERMINAL_GROWTHS:
            if terminal_growth >= wacc:
                cells.append("invalid")
            else:
                cells.append(f"${value_per_share(wacc, terminal_growth):.4f}")
        print(f"{wacc:.0%}" + "".join(f" | {cell}" for cell in cells))


def print_reverse_dcf() -> None:
    shift = reverse_dcf_growth_shift()
    print("\nReverse DCF — Uniform Explicit-Growth Shift")
    print(f"Target Share Price: ${TARGET_SHARE_PRICE:.4f}")
    print(
        "Inputs held fixed: starting FCFF, WACC, terminal growth, cash, debt, "
        "diluted shares, and the relative differences among the five growth rates."
    )
    if shift is None:
        print(
            "No solution in the configured shift bracket "
            f"[{REVERSE_SHIFT_LOWER_BOUND:.2%}, {REVERSE_SHIFT_UPPER_BOUND:.2%}]."
        )
    else:
        print(f"Solved Uniform Growth Shift: {shift:.4%}")


def main() -> None:
    if TERMINAL_GROWTH >= WACC:
        print("Error: terminal growth must be less than WACC.")
        return

    fcff = []
    current_fcff = STARTING_FCFF
    for growth_rate in YEARLY_GROWTH_RATES:
        current_fcff *= 1.0 + growth_rate
        fcff.append(current_fcff)

    present_value_explicit_fcff = sum(
        cash_flow / (1.0 + WACC) ** year
        for year, cash_flow in enumerate(fcff, start=1)
    )
    terminal_value_year_5 = fcff[-1] * (1.0 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    present_value_terminal_value = terminal_value_year_5 / (1.0 + WACC) ** 5
    enterprise_value = present_value_explicit_fcff + present_value_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_diluted_share = equity_value / DILUTED_SHARES
    terminal_value_share_of_enterprise_value = present_value_terminal_value / enterprise_value

    for year, cash_flow in enumerate(fcff, start=1):
        print(f"FCFF Year {year}: {cash_flow:.4f}")
    print(f"PV of Five Explicit FCFF: {present_value_explicit_fcff:.4f}")
    print(f"Terminal Value at Year 5: {terminal_value_year_5:.4f}")
    print(f"PV of Terminal Value: {present_value_terminal_value:.4f}")
    print(f"Enterprise Value: {enterprise_value:.4f}")
    print(f"Equity Value: {equity_value:.4f}")
    print(f"Value per Diluted Share: {value_per_diluted_share:.4f}")
    print(
        "PV of Terminal Value as Share of Enterprise Value: "
        f"{terminal_value_share_of_enterprise_value:.4f}"
    )
    print_sensitivity_grid()
    print_reverse_dcf()


if __name__ == "__main__":
    main()
