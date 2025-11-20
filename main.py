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
    options=sorted(set(st.session_state.portfolio_tickers)),
    default=st.session_state.portfolio_tickers,
    placeholder="Choose stocks to compare. Example: NVDA",
    accept_new_options=True)

# Buttons for picking time horizon
horizon = st.pills(
    "Time horizon",
    options=list(horizon_map.keys()),
    default=default_period,
)

if st.session_state.selected_horizon != horizon:
    st.session_state.selected_horizon = horizon

# Use the user-selected tickers for the chart
if tickers:
    end_date = st.session_state.data.index[-1]
    start_date = end_date - horizon_offsets[st.session_state.selected_horizon]
    close_data = st.session_state.data.loc[start_date:end_date]["Close"][tickers]
    subset_data = close_data.copy()

    for ticker in subset_data.columns:
        first_valid = subset_data[ticker].first_valid_index()
        subset_data.loc[:first_valid, ticker] = subset_data.loc[first_valid, ticker]

    # Now normalize safely
    normalized_data = subset_data.div(subset_data.iloc[0])
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
            title="Normalized Stock Prices",
            height=400),
    )

if tickers:
    # normalized_data: original DataFrame with multiple tickers
    combined_line = normalized_data.mean(axis=1)  # average across tickers

    # Make a single-column DataFrame
    combined_df = combined_line.to_frame(name="Combined Stocks")



right_chart = cols[1].container(border=True, height="stretch", vertical_alignment="center")

with right_chart:
    st.altair_chart(
        alt.Chart(
            combined_df.reset_index().melt(
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
            title="Combined Portfolio Chart",
            height=400),
    )   

