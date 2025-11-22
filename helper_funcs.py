import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import altair as alt

@st.cache_data(show_spinner=False, ttl="6h")
def load_data(tickers, period):
    tickers_obj = yf.Tickers(" ".join(tickers))
    data = tickers_obj.history(period=period)

    if data is None or data.empty:
        raise RuntimeError("YFinance returned no data.")

    return data


def returns(data, horizon='daily', log=False):
    """
    Compute returns for one or more stocks.
    
    Parameters
    ----------
    data : pd.DataFrame
        Stock price data, columns = tickers, index = datetime
    horizon : str
        Frequency of returns: 'daily', 'weekly', 'monthly', 'yearly'
    log : bool
        If True, compute log returns instead of simple returns
    
    Returns
    -------
    pd.DataFrame
        Returns for each stock
    """
    
    # Resample to desired horizon
    if horizon == 'daily':
        resampled = data
    elif horizon == 'weekly':
        resampled = data.resample('W').last()
    elif horizon == 'monthly':
        resampled = data.resample('ME').last()
    elif horizon == 'yearly':
        resampled = data.resample('YE').last()
    else:
        raise ValueError(f"Unsupported horizon: {horizon}. Use 'daily', 'weekly', 'monthly', or 'yearly'.")
    
    # Compute returns
    if log:
        ret = np.log(resampled / resampled.shift(1))
    else:
        ret = resampled.pct_change()
    
    return ret.dropna()

def get_return_horizons(loaded_range, returns_requirements):
    """
    Determine allowed return horizons based on loaded data range.
    
    Parameters
    ----------
    loaded_range : pd.Timedelta
        The time span of the loaded data
    returns_requirements : dict
        Mapping of return horizon names to required time deltas
    
    Returns
    -------
    list
        List of allowed return horizon names
    """
    allowed_return_horizons = [
        name for name, needed in returns_requirements.items()
        if loaded_range >= needed * 2  # Require at least 2 periods for a meaningful boxplot
    ]
    return allowed_return_horizons

def returns_boxplot(data, returns_horizon, x_label=True):
    return alt.Chart(
            data.reset_index().melt(
                id_vars=["Date"], var_name="Stock", value_name="Return"
            )
        ).mark_boxplot(color="white").encode(
            alt.X("Stock:N") if x_label else alt.X("Stock:N", axis=None),
            alt.Y(f"Return:Q", title=f"{returns_horizon} Return"),
            alt.Color("Stock:N"),
            
        ).properties(
            title="Return Distribution",
            height=400
        )

def price_chart(data):
    return alt.Chart(
            data.reset_index().melt(
                id_vars=["Date"], var_name="Stock", value_name="Normalized Price")
        ).mark_line().encode(
            alt.X("Date:T"),
            alt.Y("Normalized Price:Q").scale(zero=False),
            alt.Color(
                "Stock:N",
                legend=alt.Legend(
                    orient="top", 
                    title=None, 
                    direction="horizontal")),
        ).properties(
            title="Historical Stock Performance (normalized)",
            height=400)