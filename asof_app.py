"""Explore FRED interest-rate series using current and point-in-time data.

Run from this directory with:
    python -m streamlit run asof_app.py
"""
from datetime import date
from io import BytesIO
import re
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen

import pandas as pd
import streamlit as st


SERIES_NAMES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
SERIES_ID_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")
START_DATE = date(2020, 1, 1)


def _read_series_csv(content: bytes, series_id: str) -> pd.DataFrame:
    try:
        raw = pd.read_csv(BytesIO(content), na_values=["."])
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
        raise ValueError("FRED returned an unreadable CSV.") from exc

    date_column = next(
        (column for column in raw.columns if str(column).lower() == "observation_date"),
        None,
    )
    value_column = next(
        (
            column
            for column in raw.columns
            if str(column).upper() == series_id.upper()
            or str(column).upper().startswith(f"{series_id.upper()}_")
        ),
        None,
    )
    if date_column is None or value_column is None:
        raise ValueError(
            f"FRED's response did not contain the expected {series_id} series data."
        )

    observations = pd.DataFrame(
        {
            "date": pd.to_datetime(raw[date_column], errors="coerce"),
            "value": pd.to_numeric(raw[value_column], errors="coerce"),
        }
    )
    invalid_dates = raw[date_column].notna() & observations["date"].isna()
    invalid_values = raw[value_column].notna() & observations["value"].isna()
    if invalid_dates.any() or invalid_values.any():
        raise ValueError(f"FRED returned invalid dates or values for {series_id}.")

    return observations.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)


def _download_csv(url: str, series_id: str) -> pd.DataFrame:
    with urlopen(url, timeout=30) as response:
        return _read_series_csv(response.read(), series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_fred(series_id: str) -> pd.DataFrame:
    """Download the latest available observations for one FRED series."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={quote(series_id, safe='')}"
    return _download_csv(url, series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_alfred(series_id: str, vintage_date: date) -> pd.DataFrame:
    """Download observations as they were known on a specific date."""
    url = (
        "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
        f"?id={quote(series_id, safe='')}&vintage_date={vintage_date.isoformat()}"
    )
    return _download_csv(url, series_id)


def _format_date(value: pd.Timestamp) -> str:
    if value.day == 1:
        return value.strftime("%B %Y")
    return f"{value.strftime('%B')} {value.day}, {value.year}"


def _format_value(value: float) -> str:
    return f"{value:,.3f}".rstrip("0").rstrip(".")


def _latest_observation(
    observations: pd.DataFrame,
) -> tuple[pd.Timestamp, float] | None:
    available = observations.dropna(subset=["value"])
    if available.empty:
        return None
    latest = available.iloc[-1]
    return latest["date"], float(latest["value"])


def _unavailable_row(series_id: str) -> dict[str, str | int]:
    return {
        "Series": f"https://fred.stlouisfed.org/series/{quote(series_id, safe='')}",
        "Last date known then": "Unavailable",
        "Value known then": "Unavailable",
        "Last date measured today": "Unavailable",
        "Value today": "Unavailable",
        "Today's values after last known date": "Unavailable",
        "Values revised since": "Unavailable",
    }


st.set_page_config(page_title="Point-in-Time Rates", layout="wide")
st.title("Point-in-Time Interest Rates")
st.caption(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; "
    "built with AI help, a learning demonstration, not investment advice."
)

today = date.today()
st.session_state.setdefault("custom_series_ids", [])
st.session_state.setdefault("selected_series", list(SERIES_NAMES))

with st.sidebar:
    st.header("Series and dates")
    with st.form("add_series_form"):
        custom_series_id = st.text_input("Add another FRED series ID")
        add_series = st.form_submit_button("Add series")

    if add_series:
        custom_series_id = custom_series_id.strip().upper()
        if not custom_series_id:
            st.error("Enter a FRED series ID.")
        elif not SERIES_ID_PATTERN.fullmatch(custom_series_id):
            st.error("Use only letters, numbers, and underscores in a series ID.")
        else:
            if custom_series_id not in st.session_state["custom_series_ids"]:
                st.session_state["custom_series_ids"].append(custom_series_id)
            if custom_series_id not in st.session_state["selected_series"]:
                st.session_state["selected_series"] = [
                    *st.session_state["selected_series"],
                    custom_series_id,
                ]

    available_series = list(SERIES_NAMES) + st.session_state["custom_series_ids"]
    selected_series = st.multiselect(
        "Series",
        options=available_series,
        key="selected_series",
        format_func=lambda series_id: (
            f"{series_id} — {SERIES_NAMES.get(series_id, 'Custom FRED series')}"
        ),
    )
    start_date = st.date_input(
        "Start date",
        value=START_DATE,
        max_value=today,
    )
    as_known_on = st.date_input(
        "As known on",
        value=today,
        max_value=today,
    )

st.subheader("Today's observations")
table_rows: list[dict[str, str | int]] = []

if not selected_series:
    st.info("Select at least one series to display its chart and point-in-time data.")

for series_id in selected_series:
    if not SERIES_ID_PATTERN.fullmatch(series_id):
        st.error(f"{series_id}: invalid FRED series ID.")
        table_rows.append(_unavailable_row(series_id))
        continue

    current: pd.DataFrame | None = None
    vintage: pd.DataFrame | None = None

    try:
        current = download_fred(series_id)
    except (URLError, TimeoutError, UnicodeDecodeError, ValueError) as exc:
        st.error(f"{series_id}: could not download today's FRED data: {exc}")

    try:
        vintage = download_alfred(series_id, as_known_on)
    except (URLError, TimeoutError, UnicodeDecodeError, ValueError) as exc:
        st.error(f"{series_id}: could not download ALFRED data: {exc}")

    if current is not None:
        chart_data = current.loc[
            current["date"] >= pd.Timestamp(start_date), ["date", "value"]
        ].dropna(subset=["value"])
        st.markdown(f"#### {series_id} — {SERIES_NAMES.get(series_id, 'Custom FRED series')}")
        if chart_data.empty:
            st.info(f"{series_id}: no observations on or after {start_date}.")
        else:
            st.line_chart(chart_data.set_index("date"), y="value")

    known_latest: tuple[pd.Timestamp, float] | None = None
    current_latest = _latest_observation(current) if current is not None else None
    known_values = pd.DataFrame(columns=["date", "value"])
    if vintage is not None:
        known_values = vintage.loc[
            vintage["date"] <= pd.Timestamp(as_known_on)
        ].dropna(subset=["value"])
        known_latest = _latest_observation(known_values)

    if known_latest is None:
        st.caption(f"Last observation known on {as_known_on}: unavailable.")
    else:
        known_date, known_value = known_latest
        st.caption(
            f"Last observation known on {as_known_on}: "
            f"{_format_date(known_date)} ({_format_value(known_value)})."
        )

    if current is None:
        table_rows.append(_unavailable_row(series_id))
        continue

    row = _unavailable_row(series_id)
    if current_latest is not None:
        current_date, current_value = current_latest
        row["Last date measured today"] = _format_date(current_date)
        row["Value today"] = _format_value(current_value)

    if known_latest is not None:
        known_date, known_value = known_latest
        row["Last date known then"] = _format_date(known_date)
        row["Value known then"] = _format_value(known_value)

        if vintage is not None:
            later_values = current.loc[
                (current["date"] > known_date) & current["value"].notna()
            ]
            row["Today's values after last known date"] = str(len(later_values))

            comparison = known_values.merge(
                current[["date", "value"]].dropna(subset=["value"]),
                on="date",
                how="inner",
                suffixes=("_known", "_today"),
            )
            revised_count = int(
                (comparison["value_known"] != comparison["value_today"]).sum()
            )
            row["Values revised since"] = str(revised_count)
    elif vintage is not None:
        row["Today's values after last known date"] = "Unavailable"
        row["Values revised since"] = "0"

    table_rows.append(row)

st.subheader("Point-in-time comparison")
if table_rows:
    comparison_table = pd.DataFrame(table_rows)
    st.dataframe(
        comparison_table,
        width="stretch",
        hide_index=True,
        column_config={
            "Series": st.column_config.LinkColumn(
                "Series",
                display_text=r"https://fred\.stlouisfed\.org/series/(.*)",
            )
        },
    )
