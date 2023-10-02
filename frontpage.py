import streamlit as st
from modules.class_peer_group import Peer_Group
from beta_page import beta_page
from peergroup_page import peergroup_page
from db import db

st.set_page_config(layout="wide")
peer_group_user = Peer_Group()

# Siderbar
add_selectbox = st.sidebar.selectbox(
    "Page Navigation", ("Peer Group Selection", "Beta Calculation", "Company Database")
)
st.sidebar.write("Selected Companies")
st.sidebar.write(peer_group_user.peer_companies)

if add_selectbox == "Peer Group Selection":
    peergroup_page(peer_group_user)

if add_selectbox == "Beta Calculation":
    beta_page()

if add_selectbox == "Company Database":
    db()
