import pandas as pd
import streamlit as st
from modules.pages.peer_group_user import peer_group_user


def db():
    st.dataframe(
        peer_group_user.info_data,
        use_container_width=True,
        hide_index=True,
        height=800,
    )
