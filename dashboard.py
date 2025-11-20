import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import json
from helper_funcs import load_data
from config import tickers, default_period as period, horizon_map


main_page = st.Page("main.py", title="Main Page")
factor_page = st.Page("factor_page.py", title="Factor Analysis")
risk_profit_page = st.Page("risk_profit.py", title="Risk & Profit")
data_page = st.Page("data_page.py", title="Data Preview",)

st.set_page_config(initial_sidebar_state="expanded", layout="wide")
pg = st.navigation(
    [main_page, factor_page, risk_profit_page, data_page],
    position="top",
    expanded=True,
)

PORTFOLIO_FILE = "portfolio.json"

# initialize session state

if "tickers" not in st.session_state:
    st.session_state.tickers = tickers

if "period" not in st.session_state:
    st.session_state.period = period

if "portfolio_tickers" not in st.session_state:
    try:
        with open(PORTFOLIO_FILE) as f:
            st.session_state.portfolio_tickers = json.load(f).get("portfolio_tickers", [])
    except FileNotFoundError:
        st.session_state.portfolio_tickers = []

# load data

try: 
    if "data" not in st.session_state:
        st.session_state.data = load_data(st.session_state.tickers, horizon_map[st.session_state.period])
    data = st.session_state.data
except yf.exceptions.YFRateLimitError as e:
    st.warning("YFinance is rate-limiting us :(\nTry again later.")
    load_data.clear()  # Remove the bad cache entry.
    st.session_state.pop("data", None)
    st.stop()

if "portfolio_data" not in st.session_state:
    st.session_state.portfolio_data = load_data(st.session_state.portfolio_tickers, horizon_map[st.session_state.period])

pg.run()