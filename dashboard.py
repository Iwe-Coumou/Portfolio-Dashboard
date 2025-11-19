import streamlit as st
import pandas as pd
import numpy as np


main_page = st.Page("main.py", title="Main Page")
factor_page = st.Page("factor_page.py", title="Factor Analysis")
risk_profit_page = st.Page("risk_profit.py", title="Risk & Profit")

st.set_page_config(initial_sidebar_state="expanded", layout="wide")
pg = st.navigation(
    [main_page, factor_page, risk_profit_page],
    position="top",
    expanded=True,
)

# Run the selected page
pg.run()