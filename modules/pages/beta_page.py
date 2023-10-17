import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime


def beta_page():
    st.header("Peer Group Beta Overview", divider="blue")

    tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

    with tab1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

    # df = peer_group_user.beta_calc()

    st.title("Streamlit Scatterplot Example")
    # scatterplot = px.scatter(df["NEDSE.AS"], x="return_stock", y="return_index")
    # st.plotly_chart(scatterplot)
    # st.write(df)
    start_time = st.slider(
        "When do you start?",
        value=datetime(2020, 1, 1, 9, 30),
        format="MM/DD/YY - hh:mm",
    )
    st.write("Start time:", start_time)
