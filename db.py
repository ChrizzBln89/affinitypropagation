import pandas as pd
import streamlit as st


def db():
    st.dataframe(
        pd.read_csv("data/info_merged.csv"),
        use_container_width=True,
        hide_index=True,
        height=800,
    )
