import time
import streamlit as st
from datetime import datetime

from tomlkit import date
from peer_group_user import peer_group_user
from peer_group_page import peergroup_page
import plotly.graph_objs as go
import pandas as pd


def beta_page(peer_group_user=peer_group_user) -> None:
    st.set_page_config(layout="wide")
    st.header("Peer Group Tool v0.01", divider="blue")
    tabs_peer_group = st.tabs(
        [
            "1. Peer Group Company Finder",
            "2. Peer Group Selection",
            "3. Beta Calculation",
            "4. Results Overview Beta/Multiples",
        ]
    )

    with tabs_peer_group[0]:
        peergroup_page(peer_group_user=peer_group_user)

    with tabs_peer_group[1]:
        with st.status("Downloading data...", expanded=True) as status:
            st.write("Searching for data...")
            time.sleep(2)
            st.write("Query Database.")
            time.sleep(1)
            st.write("Downloading data...")
            time.sleep(1)
            status.update(label="Data is Loaded ✅", state="complete", expanded=False)

        st.header("Peer Group Settings", divider="blue")

        todays_date = datetime.today().date()
        five_years_ago = todays_date - datetime.datetime.timedelta(days=365 * 5)

        observation_timeframe = st.date_input(
            "Observation Timeframe",
            (
                five_years_ago,
                todays_date,
            ),
            five_years_ago
            - datetime.timedelta(days=365 * 25),  # Set the default start date
            todays_date,  # Set the default end date as todays_date
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

        st.header("Peer Group Selection", divider="blue")

        peer_index_selection_df = st.data_editor(
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
                    options=["^STOXX50E", "^GDAXI", "^GSPC"],
                    required=True,
                ),
            },
            hide_index=True,
        )

    with tabs_peer_group[2]:
        tabs_peer_group = st.tabs(peer_group_user.peer_companies)
        beta_dict = peer_group_user.beta_calc()

        for i, company in enumerate(peer_group_user.peer_companies):
            with tabs_peer_group[i]:
                st.subheader(f"{company} Beta")
                st.line_chart(beta_dict[company]["beta"])
                # Create a scatter plot
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=beta_dict[company]["return_index"],
                        y=beta_dict[company]["return_stock"],
                        mode="markers",
                        name="Returns",
                    )
                )
                fig.update_layout(
                    title="Stock vs Index Returns",
                    xaxis_title="Index Returns",
                    yaxis_title="Stock Returns",
                )

                # Display the scatter plot in Streamlit
                st.plotly_chart(fig)

                st.table(beta_dict[company].reset_index(drop=True))


if __name__ == "__main__":
    beta_page()
