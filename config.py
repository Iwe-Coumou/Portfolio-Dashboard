import pandas as pd

tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "MA",
    "PG", "KO", "PEP", "DIS", "NFLX", "INTC", "CSCO", "ADBE", "CRM", "ORCL",
    "IBM", "ACN", "TXN", "AVGO", "QCOM", "AMD", "SPGI", "AXP", "C", "WFC",
    "BAC", "T", "VZ", "UPS", "UNP", "MMM", "HON", "GE", "CAT", "DE",
    "LMT", "BA", "LOW", "HD", "NKE", "SBUX", "MDLZ", "MCD", "PFE", "MRK",
    "ABBV", "BMY", "GILD", "AMGN", "MO", "PM", "COST", "CVX", "XOM", "COP",
    "EOG", "SLB", "SCHW", "SPG", "PLD", "REGN", "NOW", "LIN", "TMO", "ISRG",
    "HUM", "UNH", "JNJ", "BKNG", "BK", "WMT", "WM", "FDX", "CSX", "ADI", "ZTS",
    "FIS", "FISV", "ADP", "ELV", "ICE", "CL", "CI", "DUK", "SO", "VLO", "PSA", "KO"
]

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