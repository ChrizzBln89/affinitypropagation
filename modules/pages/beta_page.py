import pandas as pd
import streamlit as st
from class_peer_group import Peer_Group
import plotly.express as px
from datetime import datetime
from modules.pages.peer_group_user import peer_group_user


def beta_page():
    df = peer_group_user.beta_calc()

    st.title("Streamlit Scatterplot Example")
    scatterplot = px.scatter(df["NEDSE.AS"], x="return_stock", y="return_index")
    st.plotly_chart(scatterplot)
    st.write(df)
    start_time = st.slider(
        "When do you start?",
        value=datetime(2020, 1, 1, 9, 30),
        format="MM/DD/YY - hh:mm",
    )
    st.write("Start time:", start_time)
