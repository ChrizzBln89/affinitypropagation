import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import RobustScaler
from modules.class_peer_group import peer_group
from beta_page import beta_page
from peergroup_page import peergroup_page
from db import db
from modules.graph import create_3d_scatterplot

st.set_page_config(layout="wide")

add_selectbox = st.sidebar.selectbox(
    "Page Navigation", ("Peer Group Selection", "Beta Calculation", "Company Database")
)

st.sidebar.write("Selected Companies")

if add_selectbox == "Peer Group":
    peergroup_page()


if add_selectbox == "Beta Calculation":
    beta_page()

if add_selectbox == "Company Database":
    db()
