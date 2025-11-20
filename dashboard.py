import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import json
from helper_funcs import load_data
from config import tickers, default_period, horizon_map, data_horizon


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
    st.session_state.period = data_horizon

if "selected_horizon" not in st.session_state:
    st.session_state.selected_horizon = default_period

if "portfolio" not in st.session_state:
    try:
        with open(PORTFOLIO_FILE) as f:
            portfolio_data = json.load(f).get("portfolio", [])
            # store as a dict: {ticker: quantity}
            st.session_state.portfolio = {item["ticker"]: item["quantity"] for item in portfolio_data}
    except FileNotFoundError:
        st.session_state.portfolio = {}

# load data

try: 
    if "data" not in st.session_state:
        st.session_state.data = load_data(list(st.session_state.tickers), horizon_map[st.session_state.period])
    data = st.session_state.data
except yf.exceptions.YFRateLimitError as e:
    st.warning("YFinance is rate-limiting us :(\nTry again later.")
    load_data.clear()  # Remove the bad cache entry.
    st.session_state.pop("data", None)
    st.stop()

if "portfolio_data" not in st.session_state:
    st.session_state.portfolio_data = load_data(list(st.session_state.portfolio.keys()), horizon_map[st.session_state.period])

pg.run()