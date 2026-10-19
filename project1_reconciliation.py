
"""Compare Microsoft FCFF and FCFE valuation model outputs."""

from msft_proforma import base_inputs, run_model
import dcf

# Run the existing pro-forma model.
inputs = base_inputs()
model = run_model(inputs)

# Reconstruct the FCFF forecast using the existing DCF assumptions.
fcff = dcf.STARTING_FCFF
fcff_forecast = []

for growth_rate in dcf.YEARLY_GROWTH_RATES:
    fcff *= 1 + growth_rate
    fcff_forecast.append(fcff)

print("\nMICROSOFT VALUATION RECONCILIATION")
print("-" * 80)
print(f"{'Year':<10}{'FCFF ($m)':>18}{'FCFE ($m)':>18}{'Difference ($m)':>20}")

for year, fcff_value, result in zip(
    range(2027, 2032), fcff_forecast, model["results"]
):
    fcfe_value = result["fcfe"]
    print(
        f"{year:<10}"
        f"{fcff_value:>18,.1f}"
        f"{fcfe_value:>18,.1f}"
        f"{fcff_value - fcfe_value:>20,.1f}"
    )

print("\nVALUATION COMPONENTS")
print("-" * 80)

fcff_pv = sum(
    cf / (1 + dcf.WACC) ** year
    for year, cf in enumerate(fcff_forecast, start=1)
)
fcff_terminal = (
    fcff_forecast[-1] * (1 + dcf.TERMINAL_GROWTH)
    / (dcf.WACC - dcf.TERMINAL_GROWTH)
)
fcff_pv_terminal = fcff_terminal / (1 + dcf.WACC) ** 5
fcff_equity = fcff_pv + fcff_pv_terminal + dcf.NON_OPERATING_CASH - dcf.DEBT

print(f"FCFF PV of explicit cash flows: ${fcff_pv:,.1f}m")
print(f"FCFF PV of terminal value:      ${fcff_pv_terminal:,.1f}m")
print(f"FCFF equity value:              ${fcff_equity:,.1f}m")
print(f"FCFF value/share:               ${fcff_equity / dcf.DILUTED_SHARES:,.2f}")

print()
print(f"FCFE PV of explicit cash flows: ${model['pv_fcfe']:,.1f}m")
print(f"FCFE PV of terminal value:      ${model['pv_terminal']:,.1f}m")
print(f"FCFE equity value:              ${model['equity_value']:,.1f}m")
print(f"FCFE value/share:               ${model['value_per_share']:,.2f}")

print("\nNOTE: FCFF and FCFE are different cash-flow definitions.")
print("The difference shown is descriptive, not a complete")
print("economic reconciliation of the two valuation methods.")
