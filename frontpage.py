import streamlit as st
import pandas as pd
from modules.pages.peer_group_user import peer_group_user
from modules.pages.beta_page import beta_page
from modules.pages.peergroup_page import peergroup_page
from modules.pages.db import db
from sidebar import sidebar


st.set_page_config(layout="wide")

st.sidebar.header("Page Navigation", divider="blue")


add_selectbox = st.sidebar.selectbox(
    "", ("Peer Group Selection", "Beta Calculation", "Company Database")
)

sidebar(peer_group_user=peer_group_user)

if add_selectbox == "Peer Group Selection":
    peergroup_page(peer_group_user=peer_group_user)

if add_selectbox == "Beta Calculation":
    beta_page(peer_group_user=peer_group_user)

if add_selectbox == "Company Database":
    db()
