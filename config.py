import pandas as pd

tickers = ["AAPL", "MSFT", "GOOGL", "KO","TSLA"]
data_horizon = "20 Years"
default_period = "1 Year"
horizon_map = {
    "1 Months": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "5 Years": "5y",
    "10 Years": "10y",
    "20 Years": "20y",
}
horizon_offsets = {
    "1 Months": pd.DateOffset(months=1),
    "3 Months": pd.DateOffset(months=3),
    "6 Months": pd.DateOffset(months=6),
    "1 Year": pd.DateOffset(years=1),
    "5 Years": pd.DateOffset(years=5),
    "10 Years": pd.DateOffset(years=10),
    "20 Years": pd.DateOffset(years=20),
}