import streamlit as st
import altair as alt
import pandas as pd
from config import horizon_map, default_period, horizon_offsets

st.set_page_config(
    page_title="Hello",
)

"""
# :material/query_stats: Portfolio Dashboard

Easily analyze and visualize your stock portfolio's performance over different time horizons.
"""

tickers = st.multiselect(
    "Stock tickers",
    options=sorted(set(st.session_state.tickers) | set(st.session_state.portfolio.keys())),
    default=st.session_state.portfolio.keys(),
    placeholder="Choose stocks to compare. Example: NVDA",
    accept_new_options=True)

# Buttons for picking time horizon
horizon = st.pills(
    "Time horizon",
    options=list(horizon_map.keys()),
    default=default_period,
)

if horizon is not None:
    st.session_state.selected_horizon = horizon


if tickers:
    end_date = st.session_state.data.index[-1]
    start_date = end_date - horizon_offsets[st.session_state.selected_horizon]
    close_data = st.session_state.data.loc[start_date:end_date]["Close"][tickers]

    for ticker in close_data.columns:
        first_valid = close_data[ticker].first_valid_index()
        close_data.loc[:first_valid, ticker] = close_data.loc[first_valid, ticker]

    # Now normalize safely
    normalized_data = close_data.div(close_data.iloc[0])
else:
    st.info("Pick some stocks to compare")
    st.stop()



cols = st.columns(2)
left_chart = cols[0].container(border=True, height="stretch", vertical_alignment="center")

with left_chart:
    st.altair_chart(
        alt.Chart(
            normalized_data.reset_index().melt(
                id_vars=["Date"], var_name="Stock", value_name="Normalized Price")
        )
        .mark_line()
        .encode(
            alt.X("Date:T"),
            alt.Y("Normalized Price:Q").scale(zero=False),
            alt.Color(
                "Stock:N",
                legend=alt.Legend(
                    orient="top", 
                    title=None, 
                    direction="horizontal")),
        )
        .properties(
            title="Historical Stock Performance (normalized)",
            height=400),
    )

if tickers:
    combined_portfolio = normalized_data.mean(axis=1)
    combined_portfolio /= combined_portfolio.iloc[0]
    combined_portfolio.name = "Combined stocks"

right_chart = cols[1].container(border=True, height="stretch", vertical_alignment="center")

with right_chart:
    st.altair_chart(
        alt.Chart(
            combined_portfolio.reset_index().melt(
                id_vars=["Date"], var_name="Stock", value_name="Normalized Price")
        )
        .mark_line()
        .encode(
            alt.X("Date:T"),
            alt.Y("Normalized Price:Q").scale(zero=False),
            alt.Color(
                "Stock:N",
                legend=alt.Legend(
                    orient="top", 
                    title=None, 
                    direction="horizontal")),
        )
        .properties(
            title="Historical Portfolio Performance (normalized)",
            height=400),
    )   
