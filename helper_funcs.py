import streamlit as st
import yfinance as yf

@st.cache_data(show_spinner=False, ttl="6h")
def load_data(tickers, period):
    tickers_obj = yf.Tickers(" ".join(tickers))
    data = tickers_obj.history(period=period)

    if data is None or data.empty:
        raise RuntimeError("YFinance returned no data.")

    return data