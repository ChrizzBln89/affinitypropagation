import streamlit as st
from modules.pages.peer_group_user import peer_group_user
from modules.pages.beta_page import beta_page
from modules.pages.peergroup_page import peergroup_page
from modules.pages.db import db

st.set_page_config(layout="wide")

# Siderbar
add_selectbox = st.sidebar.selectbox(
    "Page Navigation", ("Peer Group Selection", "Beta Calculation", "Company Database")
)
st.sidebar.write("Selected Companies")
st.sidebar.data_editor(peer_group_user.peer_companies)

if add_selectbox == "Peer Group Selection":
    peergroup_page()

if add_selectbox == "Beta Calculation":
    beta_page()

if add_selectbox == "Company Database":
    db()
