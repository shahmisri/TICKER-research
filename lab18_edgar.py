"""Collect five years of annual company facts from SEC EDGAR."""
from __future__ import annotations

import argparse
from datetime import date
from decimal import Decimal
import gzip
import json
import os
import re
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
FLOW_TAGS = {
    "Revenue": (
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
    ),
    "Net income": ("NetIncomeLoss",),
    "Operating cash flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "Capital spending": (
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ),
}
EQUITY_TAG = "StockholdersEquity"
TICKER_RE = re.compile(r"^[A-Z0-9.-]+$")
FLOW_MIN_DAYS = 350
FLOW_MAX_DAYS = 380
MILLION = Decimal(1_000_000)


class EdgarError(RuntimeError):
    """Raised when EDGAR data cannot support a requested report."""


def _user_agent() -> str:
    name = os.environ.get("SEC_USER_AGENT_NAME", "").strip()
    email = os.environ.get("SEC_USER_AGENT_EMAIL", "").strip()
    if not name or not email or "@" not in email:
        raise EdgarError(
            "Set SEC_USER_AGENT_NAME and SEC_USER_AGENT_EMAIL in the environment "
            "before requesting SEC data."
        )
    return f"{name} {email}"


def _get_json(url: str) -> dict[str, Any]:
    request = Request(
        url,
        headers={
            "User-Agent": _user_agent(),
            "Accept": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            body = response.read()
            if response.headers.get("Content-Encoding", "").lower() == "gzip":
                body = gzip.decompress(body)
            return json.loads(body)
    except (
        HTTPError,
        URLError,
        TimeoutError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        OSError,
    ) as exc:
        raise EdgarError(f"SEC request failed for {url}: {exc}") from exc


def _find_cik(ticker: str) -> str:
    directory = _get_json(TICKERS_URL)
    for company in directory.values():
        if str(company.get("ticker", "")).upper() == ticker:
            return str(company["cik_str"]).zfill(10)
    raise EdgarError(f"Ticker {ticker} was not found in the SEC company ticker list.")


def _period_days(item: dict[str, Any]) -> int | None:
    if "start" not in item:
        return None
    try:
        return (
            date.fromisoformat(item["end"]) - date.fromisoformat(item["start"])
        ).days
    except (TypeError, ValueError):
        return None


def _latest_item(items: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not items:
        return None
    return max(
        items,
        key=lambda item: (
            item.get("filed", ""),
            item.get("accn", ""),
            item.get("start", ""),
        ),
    )


def _annual_flow(
    facts: dict[str, Any], tags: tuple[str, ...]
) -> dict[str, tuple[Decimal, str]]:
    """Return one-year 10-K flows keyed by fiscal-year-end date."""
    selected: dict[str, tuple[Decimal, str, str, str]] = {}
    for tag in tags:
        units = facts.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {})
        annual: dict[str, list[dict[str, Any]]] = {}
        for unit_rows in units.values():
            for item in unit_rows:
                days = _period_days(item)
                if (
                    item.get("form") == "10-K"
                    and days is not None
                    and FLOW_MIN_DAYS <= days <= FLOW_MAX_DAYS
                ):
                    annual.setdefault(item["end"], []).append(item)

        for end, candidates in annual.items():
            chosen = _latest_item(candidates)
            if chosen is not None:
                candidate = (
                    Decimal(str(chosen["val"])),
                    tag,
                    chosen.get("filed", ""),
                    chosen.get("accn", ""),
                )
                selected.setdefault(end, candidate)
    return {
        end: (value, tag)
        for end, (value, tag, _, _) in selected.items()
    }


def _annual_equity(facts: dict[str, Any]) -> dict[str, tuple[Decimal, str]]:
    units = (
        facts.get("facts", {})
        .get("us-gaap", {})
        .get(EQUITY_TAG, {})
        .get("units", {})
    )
    annual: dict[str, list[dict[str, Any]]] = {}
    for unit_rows in units.values():
        for item in unit_rows:
            if item.get("form") == "10-K" and "start" not in item:
                annual.setdefault(item["end"], []).append(item)

    selected: dict[str, tuple[Decimal, str]] = {}
    for end, candidates in annual.items():
        chosen = _latest_item(candidates)
        if chosen is not None:
            selected[end] = (Decimal(str(chosen["val"])), EQUITY_TAG)
    return selected


def _value(value: Decimal | None) -> str:
    if value is None:
        return "not found"
    return f"{value:,.0f}" if value == value.to_integral_value() else f"{value:,.2f}"


def _ratio(value: Decimal | None) -> str:
    return "not known" if value is None else f"{value:.1f}%"


def _check(values: list[Decimal | None], predicate: Any) -> str:
    if not values or any(value is None for value in values):
        return "not known"
    return "pass" if all(predicate(value) for value in values if value is not None) else "fail"


def build_report(ticker: str) -> dict[str, Any]:
    """Fetch EDGAR facts and calculate the annual values and three checks."""
    ticker = ticker.strip().upper()
    if not TICKER_RE.fullmatch(ticker):
        raise EdgarError("Enter a ticker using letters, numbers, periods, or hyphens.")

    cik = _find_cik(ticker)
    company_facts = _get_json(FACTS_URL.format(cik=cik))
    flows = {
        name: _annual_flow(company_facts, tags)
        for name, tags in FLOW_TAGS.items()
    }
    equity = _annual_equity(company_facts)
    fiscal_ends = sorted(
        set().union(*(set(values) for values in flows.values()), set(equity))
    )[-5:]
    if not fiscal_ends:
        raise EdgarError(f"No annual 10-K XBRL facts were found for {ticker}.")

    rows = []
    for end in fiscal_ends:
        cells = {
            name: flows[name].get(end, (None, tags[0]))
            for name, tags in FLOW_TAGS.items()
        }
        equity_value, equity_tag = equity.get(end, (None, EQUITY_TAG))
        revenue, revenue_tag = cells["Revenue"]
        net_income, net_income_tag = cells["Net income"]
        operating_cash_flow, cash_flow_tag = cells["Operating cash flow"]
        capital_spending, capital_spending_tag = cells["Capital spending"]
        owner_earnings = (
            operating_cash_flow - capital_spending
            if operating_cash_flow is not None and capital_spending is not None
            else None
        )
        roe = (
            net_income / equity_value * 100
            if net_income is not None and equity_value is not None and equity_value > 0
            else None
        )
        rows.append(
            {
                "fiscal_year_end": end,
                "revenue_m": revenue / MILLION if revenue is not None else None,
                "revenue_tag": revenue_tag,
                "net_income_m": net_income / MILLION if net_income is not None else None,
                "net_income_tag": net_income_tag,
                "operating_cash_flow_m": (
                    operating_cash_flow / MILLION
                    if operating_cash_flow is not None
                    else None
                ),
                "operating_cash_flow_tag": cash_flow_tag,
                "capital_spending_m": (
                    capital_spending / MILLION
                    if capital_spending is not None
                    else None
                ),
                "capital_spending_tag": capital_spending_tag,
                "equity_m": equity_value / MILLION if equity_value is not None else None,
                "equity_tag": equity_tag,
                "roe_pct": roe,
                "owner_earnings_m": (
                    owner_earnings / MILLION if owner_earnings is not None else None
                ),
            }
        )

    roe_values = [row["roe_pct"] for row in rows]
    owner_values = [row["owner_earnings_m"] for row in rows]
    roe_check = _check(roe_values, lambda value: value >= 15)
    positive_owner_check = _check(
        owner_values, lambda value: value > 0
    )
    growth_check = (
        "not known"
        if len(rows) < 2 or any(value is None for value in owner_values)
        else (
            "pass"
            if owner_values[-1] > owner_values[0]
            else "fail"
        )
    )

    return {
        "ticker": ticker,
        "company": company_facts.get("entityName", ticker),
        "cik": cik,
        "download_date": date.today().isoformat(),
        "rows": rows,
        "checks": {
            "ROE of 15% or more every year": roe_check,
            "Owner earnings positive every year": positive_owner_check,
            "Owner earnings grew, first year to last": growth_check,
        },
    }


def format_report(report: dict[str, Any]) -> str:
    """Format all calculated facts, source tags, and checks for CLI/memo use."""
    lines = [
        f"# {report['ticker']} — {report['company']}",
        f"CIK: {report['cik']} | Downloaded: {report['download_date']}",
        "Amounts in $ millions; fiscal years labelled by year-end date.",
        "ROE = NetIncomeLoss / StockholdersEquity when equity is positive; "
        "owner earnings = operating cash flow - capital spending. "
        "Tags for each source fact are shown in the table.",
        "",
        "| Fiscal year end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE | Owner earnings |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["rows"]:
        lines.append(
            "| {fiscal_year_end} | {revenue} `({revenue_tag})` | "
            "{net_income} `({net_income_tag})` | "
            "{operating_cash_flow} `({operating_cash_flow_tag})` | "
            "{capital_spending} `({capital_spending_tag})` | "
            "{equity} `({equity_tag})` | {roe} | {owner_earnings} |".format(
                fiscal_year_end=row["fiscal_year_end"],
                revenue=_value(row["revenue_m"]),
                revenue_tag=row["revenue_tag"],
                net_income=_value(row["net_income_m"]),
                net_income_tag=row["net_income_tag"],
                operating_cash_flow=_value(row["operating_cash_flow_m"]),
                operating_cash_flow_tag=row["operating_cash_flow_tag"],
                capital_spending=_value(row["capital_spending_m"]),
                capital_spending_tag=row["capital_spending_tag"],
                equity=_value(row["equity_m"]),
                equity_tag=row["equity_tag"],
                roe=_ratio(row["roe_pct"]),
                owner_earnings=_value(row["owner_earnings_m"]),
            )
        )
    lines.extend(["", "## Buffett's checks"])
    lines.extend(f"- {name}: **{result}**" for name, result in report["checks"].items())
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print five years of annual SEC EDGAR XBRL facts and Buffett checks."
    )
    parser.add_argument("ticker", help="Company ticker symbol, for example COST")
    args = parser.parse_args()
    try:
        print(format_report(build_report(args.ticker)))
    except EdgarError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
