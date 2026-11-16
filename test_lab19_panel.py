"""Focused tests for the Lab 19 investor screens."""
from decimal import Decimal
from pathlib import Path
import unittest
from unittest.mock import patch

from lab18_edgar import (
    build_report,
    calculate_checks,
    format_report,
    investor_memo,
    investor_verdict,
    unprinted_numbers,
)


def cost_rows() -> list[dict[str, Decimal | None]]:
    current_ratios = ("1.02", "1.07", "0.97", "1.03", "1.06")
    liabilities_to_equity = ("2.11", "1.75", "1.96", "1.64", "1.49")
    rows = []
    for index, (current_ratio, leverage) in enumerate(
        zip(current_ratios, liabilities_to_equity)
    ):
        rows.append(
            {
                "roe_pct": Decimal("20"),
                "owner_earnings_m": Decimal(100 + index * 10),
                "net_income_m": Decimal(100 + index * 10),
                "operating_cash_flow_m": Decimal(120 + index * 10),
                "current_ratio": Decimal(current_ratio),
                "liabilities_to_equity": Decimal(leverage),
            }
        )
    return rows


def synthetic_company_facts() -> dict:
    """Non-SEC test data; these values are never presented as Costco results."""
    fiscal_ends = (
        "2022-08-28",
        "2023-09-03",
        "2024-09-01",
        "2025-08-31",
        "2026-08-30",
    )
    tags = (
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "NetIncomeLoss",
        "NetCashProvidedByUsedInOperatingActivities",
        "PaymentsToAcquirePropertyPlantAndEquipment",
    )
    income_values = {
        tags[0]: [500, 550, 600, 650, 700],
        tags[1]: [100, 110, 120, 130, 140],
        tags[2]: [120, 130, 140, 150, 160],
        tags[3]: [20, 20, 20, 20, 20],
    }
    us_gaap = {}
    for tag, values in income_values.items():
        us_gaap[tag] = {
            "units": {
                "USD": [
                    {
                        "start": f"{int(end[:4]) - 1}{end[4:]}",
                        "end": end,
                        "val": amount * 1_000_000,
                        "form": "10-K",
                        "filed": f"{int(end[:4]) + 1}-10-01",
                        "accn": str(index),
                    }
                    for index, (end, amount) in enumerate(zip(fiscal_ends, values))
                ]
            }
        }

    instant_values = {
        "StockholdersEquity": [100, 100, 100, 100, 100],
        "Liabilities": [211, 175, 196, 164, 149],
        "AssetsCurrent": [102, 107, 97, 103, 106],
        "LiabilitiesCurrent": [100, 100, 100, 100, 100],
    }
    for tag, values in instant_values.items():
        us_gaap[tag] = {
            "units": {
                "USD": [
                    {
                        "end": end,
                        "val": amount * 1_000_000,
                        "form": "10-K",
                        "filed": f"{int(end[:4]) + 1}-10-01",
                        "accn": str(index),
                    }
                    for index, (end, amount) in enumerate(zip(fiscal_ends, values))
                ]
            }
        }
    return {"entityName": "Costco Wholesale Corporation", "facts": {"us-gaap": us_gaap}}


class PanelChecksTests(unittest.TestCase):
    def test_cost_known_answer(self) -> None:
        checks = calculate_checks(cost_rows())
        self.assertEqual(list(checks.values()), [
            "pass",
            "pass",
            "pass",
            "fail",
            "pass",
            "pass",
            "pass",
            "pass",
        ])
        self.assertEqual(
            investor_verdict(checks),
            {
                "Buffett": "Passes screen",
                "Graham": "Fails screen",
                "Burry": "Passes screen",
            },
        )
        self.assertEqual(list(checks.values()).count("pass"), 7)
        self.assertEqual(list(checks.values()).count("fail"), 1)

    def test_threshold_probe_changes_graham_current_ratio_check(self) -> None:
        checks = calculate_checks(cost_rows(), Decimal("1.0"))
        self.assertEqual(
            checks["Current ratio of 1.0 or more, latest year"],
            "pass",
        )
        self.assertEqual(investor_verdict(checks)["Graham"], "Passes screen")

    def test_missing_values_remain_not_known(self) -> None:
        rows = cost_rows()
        rows[0]["operating_cash_flow_m"] = None
        rows[-1]["current_ratio"] = None
        rows[-1]["liabilities_to_equity"] = None
        checks = calculate_checks(rows)
        self.assertEqual(
            checks["Operating cash flow at least net income every year"],
            "not known",
        )
        self.assertEqual(
            checks["Current ratio of 2.0 or more, latest year"],
            "not known",
        )
        self.assertEqual(
            checks["Liabilities no more than twice equity, latest year"],
            "not known",
        )
        self.assertEqual(investor_verdict(checks)["Burry"], "Not known")

    def test_build_report_adds_balance_sheet_ratios_and_prints_them(self) -> None:
        with (
            patch("lab18_edgar._find_cik", return_value="0000000001"),
            patch("lab18_edgar._get_json", return_value=synthetic_company_facts()),
        ):
            report = build_report("COST")

        self.assertEqual(report["rows"][-1]["current_ratio"], Decimal("1.06"))
        self.assertEqual(
            report["rows"][-1]["liabilities_to_equity"],
            Decimal("1.49"),
        )
        self.assertEqual(report["graham_current_ratio_min"], Decimal("2.0"))
        self.assertEqual(
            report["checks"]["Current ratio of 2.0 or more, latest year"],
            "fail",
        )
        output = format_report(report)
        self.assertIn("Current ratio of 2.0 or more, latest year: **fail**", output)
        self.assertIn("Liabilities no more than twice equity, latest year: **pass**", output)
        self.assertIn("| 2026-08-30 |", output)

    def test_memos_match_each_threshold_and_pass_number_audit(self) -> None:
        for threshold, current_result, graham_verdict in (
            (Decimal("2.0"), "fail", "Fails screen"),
            (Decimal("1.0"), "pass", "Passes screen"),
        ):
            with (
                patch("lab18_edgar._find_cik", return_value="0000000001"),
                patch("lab18_edgar._get_json", return_value=synthetic_company_facts()),
            ):
                report = build_report("COST", threshold)

            checks = report["checks"]
            output = format_report(report)
            graham_memo = investor_memo(report, "Graham")
            check_name = f"Current ratio of {threshold:g} or more, latest year"
            self.assertEqual(checks[check_name], current_result)
            self.assertIn(f"Threshold kept: {threshold:g}", graham_memo)
            self.assertIn(f"- {check_name}: {current_result}", graham_memo)
            self.assertIn(f"**Verdict: {graham_verdict}.**", graham_memo)
            self.assertEqual(unprinted_numbers(graham_memo, output), [])

            for investor in ("Buffett", "Burry"):
                memo = investor_memo(report, investor)
                self.assertEqual(unprinted_numbers(memo, output), [])

    def test_saved_cost_memos_match_default_panel_and_audit(self) -> None:
        with (
            patch("lab18_edgar._find_cik", return_value="0000000001"),
            patch("lab18_edgar._get_json", return_value=synthetic_company_facts()),
        ):
            report = build_report("COST")
        output = format_report(report)
        project_dir = Path(__file__).parent
        expected_checks = {
            "Buffett": list(report["checks"].items())[:3],
            "Graham": list(report["checks"].items())[3:6],
            "Burry": list(report["checks"].items())[6:],
        }

        for investor, checks in expected_checks.items():
            memo_path = project_dir / f"COST_{investor.lower()}_memo.md"
            memo = memo_path.read_text(encoding="utf-8")
            for name, result in checks:
                self.assertIn(f"- {name}: {result}", memo)
            self.assertEqual(unprinted_numbers(memo, output), [])


if __name__ == "__main__":
    unittest.main()
