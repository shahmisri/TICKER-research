
import os
import tempfile
import pandas as pd
import yfinance as yf

# Use a separate cache to avoid database locking
cache_dir = os.path.join(
    tempfile.gettempdir(), "fin43900_yfinance_cache"
)
os.makedirs(cache_dir, exist_ok=True)
yf.set_tz_cache_location(cache_dir)

tickers = ["BIL", "IEF", "LQD", "VT"]

data = yf.download(
    tickers,
    start="2021-09-01",
    end="2026-10-01",
    auto_adjust=True,
    progress=False,
    threads=False,
)

prices = data["Close"]

prices.index = pd.to_datetime(prices.index)

monthly = prices.resample("ME").last()

# Keep October 2021 through September 2026
monthly = monthly.loc["2021-10":"2026-09"]
monthly = monthly[tickers].dropna()

# Do not save an empty or incomplete CSV
if len(monthly) != 60:
    raise ValueError(
        f"Expected 60 monthly observations, got {len(monthly)}. "
        "Check for failed downloads or missing prices."
    )

monthly.index.name = "Date"
monthly.to_csv("prices.csv")

print("SUCCESS: prices.csv created!")
print("Rows:", len(monthly))
print("Tickers:", list(monthly.columns))
print("\nFirst 5 rows:")
print(monthly.head())
print("\nLast 5 rows:")
print(monthly.tail())
