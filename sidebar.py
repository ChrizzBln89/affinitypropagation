import streamlit as st
import datetime
import pandas as pd
import datetime
import time

from modules.pages import peer_group_user
from valuationhub.valuationhub.assets import download_index_ticker, get_symbols


def sidebar(peer_group_user):
    with st.sidebar.status("Downloading data...", expanded=True) as status:
        st.write("Searching for data...")
        time.sleep(2)
        st.write("Query Database.")
        time.sleep(1)
        st.write("Downloading data...")
        time.sleep(1)
        status.update(label="Data is Loaded ✅", state="complete", expanded=False)

    st.sidebar.header("Peer Group Settings", divider="blue")

    today = datetime.date.today()
    five_years_ago = today - datetime.timedelta(days=365 * 5)

    observation_timeframe = st.sidebar.date_input(
        "Observation Timeframe",
        (
            five_years_ago,
            today,
        ),
        five_years_ago
        - datetime.timedelta(days=365 * 25),  # Set the default start date
        today,  # Set the default end date as today
        format="DD.MM.YYYY",
    )
    company_index_df = pd.DataFrame(
        {
            "Ticker": [
                "BMW.DE",
                "PAH3.DE",
                "RNO.PA",
                "F",
                "GM",
                "HMC",
                "TM",
            ],
            "Index": [
                "^STOXX50E",
                "^STOXX50E",
                "^STOXX50E",
                "^STOXX50E",
                "^STOXX50E",
                "^STOXX50E",
                "^STOXX50E",
            ],
        }
    )

    st.sidebar.header("Peer Group Selection", divider="blue")

    peer_index_selection_df = st.sidebar.data_editor(
        company_index_df,
        column_config={
            "Ticker": st.column_config.SelectboxColumn(
                "Company",
                help="Selected Companies for Peer Group.",
                width="medium",
                options=peer_group_user.info_data["Symbol"],
                required=True,
            ),
            "Index": st.column_config.SelectboxColumn(
                "Index",
                help="Selected Index for Peer Group.",
                width="medium",
                options=download_index_ticker(),
                required=True,
            ),
        },
        hide_index=True,
    )
