import streamlit as st


st.title("Stock Data Preview")


# Make sure data exists
if "data" in st.session_state:
    data = st.session_state.data

    # Show the full DataFrame
    st.subheader("Full DataFrame")
    st.dataframe(data)

    # Optionally, show just the Close prices
    if "Close" in data.columns.get_level_values(0):
        st.subheader("Close Prices Only")
        st.dataframe(data["Close"])
else:
    st.warning("No data loaded yet. Check your load_data function.")

if "tickers_info" in st.session_state:
    tickers_info = st.session_state.tickers_info
    portfolio_tickers = st.session_state.portfolio.keys()

    st.subheader("Tickers Information")
    for ticker in portfolio_tickers:
        if ticker in tickers_info:
            st.markdown(f"### {ticker}")
            st.json(tickers_info[ticker])