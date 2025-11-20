import streamlit as st
from config import horizon_map, default_period

st.set_page_config(
    page_title="Hello",
)

"""
# :material/query_stats: Portfolio Dashboard

Easily analyze and visualize your stock portfolio's performance over different time horizons.
"""

cols = st.columns([1,2])
top_left_cell = cols[0].container(border=True, height="stretch", vertical_alignment="center")

with top_left_cell:
     tickers = st.multiselect(
        "Stock tickers",
        options=sorted(set(st.session_state.tickers) | set(st.session_state.portfolio_tickers)),
        default=st.session_state.portfolio_tickers,
        placeholder="Choose stocks to compare. Example: NVDA",
        accept_new_options=True,
    )
     
with top_left_cell:
    # Buttons for picking time horizon
    horizon = st.pills(
        "Time horizon",
        options=list(horizon_map.keys()),
        default=default_period,
    )

if not tickers:
    top_left_cell.info("Pick some stocks to compare", icon=":material/info:")
    st.stop()

right_cell = cols[1].container(
    border=True, height="stretch", vertical_alignment="center"
)

with right_cell:
    #create altair chart?
    pass