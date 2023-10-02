import pandas as pd
import streamlit as st
from modules.class_peer_group import peer_group
import plotly.express as px
from datetime import datetime


def beta_page():
    peer_test = peer_group()
    peer_test.add_company("AAPL")
    st.write(peer_test.peer_companies)

    # Sample data for the scatterplot
    data = {"X": [1, 2, 3, 4, 5], "Y": [10, 11, 12, 13, 14]}
    st.title("Streamlit Scatterplot Example")
    scatterplot = px.scatter(data, x="X", y="Y", title="Scatterplot")
    st.plotly_chart(scatterplot)
    start_time = st.slider(
        "When do you start?",
        value=datetime(2020, 1, 1, 9, 30),
        format="MM/DD/YY - hh:mm",
    )
    st.write("Start time:", start_time)
