"""Collect five years of annual company facts from SEC EDGAR."""
from __future__ import annotations

import argparse
from datetime import date
from decimal import Decimal, InvalidOperation
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
BALANCE_TAGS = {
    "liabilities": "Liabilities",
    "assets_current": "AssetsCurrent",
    "liabilities_current": "LiabilitiesCurrent",
}
TICKER_RE = re.compile(r"^[A-Z0-9.-]+$")
FLOW_MIN_DAYS = 350
FLOW_MAX_DAYS = 380
MILLION = Decimal(1_000_000)
NUMBER_RE = re.compile(
    r"(?<![\w.])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?!\w)(?!\.\d)"
)


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


def _annual_instant(
    facts: dict[str, Any], tag: str
) -> dict[str, tuple[Decimal, str]]:
    units = (
        facts.get("facts", {})
        .get("us-gaap", {})
        .get(tag, {})
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
            selected[end] = (Decimal(str(chosen["val"])), tag)
    return selected


def _annual_equity(facts: dict[str, Any]) -> dict[str, tuple[Decimal, str]]:
    return _annual_instant(facts, EQUITY_TAG)


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


def _growth_check(values: list[Decimal | None]) -> str:
    if len(values) < 2 or values[0] is None or values[-1] is None:
        return "not known"
    return "pass" if values[-1] > values[0] else "fail"


def calculate_checks(
    rows: list[dict[str, Any]],
    graham_current_ratio_min: Decimal = Decimal("2.0"),
) -> dict[str, str]:
    """Apply all investor checks to the same annual rows."""
    checks = {
        "ROE of 15% or more every year": _check(
            [row["roe_pct"] for row in rows], lambda value: value >= 15
        ),
        "Owner earnings positive every year": _check(
            [row["owner_earnings_m"] for row in rows], lambda value: value > 0
        ),
        "Owner earnings grew, first year to last": _growth_check(
            [row["owner_earnings_m"] for row in rows]
        ),
        f"Current ratio of {graham_current_ratio_min:g} or more, latest year": (
            "not known"
        ),
        "Net income positive every year": _check(
            [row["net_income_m"] for row in rows], lambda value: value > 0
        ),
        "Net income grew, first year to last": _growth_check(
            [row["net_income_m"] for row in rows]
        ),
        "Operating cash flow at least net income every year": _check(
            [
                (
                    row["operating_cash_flow_m"] - row["net_income_m"]
                    if row["operating_cash_flow_m"] is not None
                    and row["net_income_m"] is not None
                    else None
                )
                for row in rows
            ],
            lambda value: value >= 0,
        ),
        "Liabilities no more than twice equity, latest year": "not known",
    }

    if rows:
        latest_current_ratio = rows[-1]["current_ratio"]
        if latest_current_ratio is not None:
            checks[
                f"Current ratio of {graham_current_ratio_min:g} or more, latest year"
            ] = (
                "pass"
                if latest_current_ratio >= graham_current_ratio_min
                else "fail"
            )
        latest_leverage = rows[-1]["liabilities_to_equity"]
        if latest_leverage is not None:
            checks["Liabilities no more than twice equity, latest year"] = (
                "pass" if latest_leverage <= 2 else "fail"
            )
    return checks


def investor_verdict(checks: dict[str, str]) -> dict[str, str]:
    """Summarize each investor's checks without treating missing data as a pass."""
    check_items = list(checks.items())
    groups = {
        "Buffett": check_items[:3],
        "Graham": check_items[3:6],
        "Burry": check_items[6:],
    }
    verdicts = {}
    for investor, investor_checks in groups.items():
        results = [result for _, result in investor_checks]
        if "fail" in results:
            verdicts[investor] = "Fails screen"
        elif results and all(result == "pass" for result in results):
            verdicts[investor] = "Passes screen"
        else:
            verdicts[investor] = "Not known"
    return verdicts


def investor_memo(report: dict[str, Any], investor: str) -> str:
    """Build one investor memo from the report's current threshold and checks."""
    checks = report["checks"]
    if investor == "Buffett":
        names = list(checks)[0:3]
        evidence = "\n".join(f"- {name}: {checks[name]}" for name in names)
        return (
            f"# Buffett-style business memo\n\n"
            f"**Verdict: {investor_verdict(checks)['Buffett']}.**\n\n"
            f"{evidence}\n\n"
            "I trust this as a limited business-quality screen, not as a valuation "
            "or investment recommendation."
        )
    if investor == "Graham":
        names = list(checks)[3:6]
        evidence = "\n".join(f"- {name}: {checks[name]}" for name in names)
        threshold = report["graham_current_ratio_min"]
        return (
            f"# Graham-style business memo\n\n"
            f"**Verdict: {investor_verdict(checks)['Graham']}.**\n\n"
            f"{evidence}\n\n"
            f"Threshold kept: {threshold:g} for the current ratio; it is a "
            "conservative screen, not a universal rule.\n\n"
            "I trust this only as a limited defensive screen; it does not assess "
            "valuation or the full business."
        )
    if investor == "Burry":
        names = list(checks)[6:]
        evidence = "\n".join(f"- {name}: {checks[name]}" for name in names)
        return (
            f"# Burry-style business memo\n\n"
            f"**Verdict: {investor_verdict(checks)['Burry']}.**\n\n"
            f"{evidence}\n\n"
            "I trust this only as a limited cash-flow and balance-sheet screen; it "
            "does not replace filing-footnote review."
        )
    raise ValueError(f"Unknown investor: {investor}")


def unprinted_numbers(memo: str, script_output: str) -> list[str]:
    """Return memo numbers not present in the formatted report."""
    def number_key(token: str) -> tuple[Decimal, bool] | None:
        is_percent = token.endswith("%")
        cleaned = token[:-1] if is_percent else token
        try:
            return Decimal(cleaned.replace(",", "")).normalize(), is_percent
        except InvalidOperation:
            return None

    printed = {
        key
        for token in NUMBER_RE.findall(script_output)
        if (key := number_key(token)) is not None
    }
    unseen: list[str] = []
    for token in NUMBER_RE.findall(memo):
        key = number_key(token)
        if key is not None and key not in printed and token not in unseen:
            unseen.append(token)
    return unseen


def build_report(
    ticker: str,
    graham_current_ratio_min: Decimal = Decimal("2.0"),
) -> dict[str, Any]:
    """Fetch EDGAR facts and calculate annual values and eight investor checks."""
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
    balance_facts = {
        key: _annual_instant(company_facts, tag)
        for key, tag in BALANCE_TAGS.items()
    }
    fiscal_ends = sorted(
        set().union(
            *(set(values) for values in flows.values()),
            set(equity),
            *(set(values) for values in balance_facts.values()),
        )
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
        balance_cells = {
            key: values.get(end, (None, BALANCE_TAGS[key]))
            for key, values in balance_facts.items()
        }
        liabilities, liabilities_tag = balance_cells["liabilities"]
        assets_current, assets_current_tag = balance_cells["assets_current"]
        liabilities_current, liabilities_current_tag = balance_cells[
            "liabilities_current"
        ]
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
        current_ratio = (
            assets_current / liabilities_current
            if assets_current is not None
            and liabilities_current is not None
            and liabilities_current > 0
            else None
        )
        liabilities_to_equity = (
            liabilities / equity_value
            if liabilities is not None and equity_value is not None and equity_value > 0
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
                "liabilities_m": (
                    liabilities / MILLION if liabilities is not None else None
                ),
                "liabilities_tag": liabilities_tag,
                "assets_current_m": (
                    assets_current / MILLION if assets_current is not None else None
                ),
                "assets_current_tag": assets_current_tag,
                "liabilities_current_m": (
                    liabilities_current / MILLION
                    if liabilities_current is not None
                    else None
                ),
                "liabilities_current_tag": liabilities_current_tag,
                "roe_pct": roe,
                "owner_earnings_m": (
                    owner_earnings / MILLION if owner_earnings is not None else None
                ),
                "current_ratio": current_ratio,
                "liabilities_to_equity": liabilities_to_equity,
            }
        )

    checks = calculate_checks(rows, graham_current_ratio_min)

    return {
        "ticker": ticker,
        "company": company_facts.get("entityName", ticker),
        "cik": cik,
        "download_date": date.today().isoformat(),
        "rows": rows,
        "graham_current_ratio_min": graham_current_ratio_min,
        "checks": checks,
    }


def format_report(report: dict[str, Any]) -> str:
    """Format all calculated facts, source tags, and checks for CLI/memo use."""
    lines = [
        f"# {report['ticker']} — {report['company']}",
        f"CIK: {report['cik']} | Downloaded: {report['download_date']}",
        "Amounts in $ millions; fiscal years labelled by year-end date.",
        "ROE = net income / equity when equity is positive; owner earnings = "
        "operating cash flow - capital spending; current ratio = current assets / "
        "current liabilities; liabilities/equity = total liabilities / equity. "
        "Tags for each source fact are shown in the table.",
        "",
        f"Graham current-ratio threshold: {report['graham_current_ratio_min']:g}",
        "",
        "| Fiscal year end | Revenue | Net income | Operating cash flow | Capital spending | Equity | Liabilities | Current assets | Current liabilities | ROE | Owner earnings | Current ratio | Liabilities/equity |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in report["rows"]:
        lines.append(
            "| {fiscal_year_end} | {revenue} `({revenue_tag})` | "
            "{net_income} `({net_income_tag})` | "
            "{operating_cash_flow} `({operating_cash_flow_tag})` | "
            "{capital_spending} `({capital_spending_tag})` | "
            "{equity} `({equity_tag})` | "
            "{liabilities} `({liabilities_tag})` | "
            "{assets_current} `({assets_current_tag})` | "
            "{liabilities_current} `({liabilities_current_tag})` | "
            "{roe} | {owner_earnings} | {current_ratio} | "
            "{liabilities_to_equity} |".format(
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
                liabilities=_value(row["liabilities_m"]),
                liabilities_tag=row["liabilities_tag"],
                assets_current=_value(row["assets_current_m"]),
                assets_current_tag=row["assets_current_tag"],
                liabilities_current=_value(row["liabilities_current_m"]),
                liabilities_current_tag=row["liabilities_current_tag"],
                roe=_ratio(row["roe_pct"]),
                owner_earnings=_value(row["owner_earnings_m"]),
                current_ratio=(
                    f"{row['current_ratio']:.2f}"
                    if row["current_ratio"] is not None
                    else "not known"
                ),
                liabilities_to_equity=(
                    f"{row['liabilities_to_equity']:.2f}"
                    if row["liabilities_to_equity"] is not None
                    else "not known"
                ),
            )
        )
    lines.extend(["", "## Panel checks"])
    lines.extend(f"- {name}: **{result}**" for name, result in report["checks"].items())
    lines.extend(["", "## Screen verdicts"])
    lines.extend(
        f"- {investor}: **{verdict}**"
        for investor, verdict in investor_verdict(report["checks"]).items()
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print five years of annual SEC EDGAR facts and investor checks."
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
