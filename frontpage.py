import streamlit as st
import pandas as pd
import datetime

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

selection_dict = {"Stock": None, "Index": "^MDAXI"}

selection_dict["Stock"] = st.sidebar.multiselect(
    "Select Company", peer_group_user.info_data["symbol"]
)

for key in selection_dict.keys():
    selection_dict[key] = "^MDAXI"

selection_dict["Index"] = st.sidebar.multiselect(
    "Select Index", peer_group_user.available_indices
)

today = datetime.datetime.now()
current_year = today.year
jan_1 = datetime.date(current_year, 1, 1)
dec_31 = datetime.date(current_year, 12, 31)

d = st.sidebar.date_input(
    "Observation Timeframe",
    (jan_1, datetime.date(current_year, 1, 7)),
    jan_1,
    dec_31,
    format="MM.DD.YYYY",
)


st.sidebar.write(pd.DataFrame.from_dict(selection_dict))

if add_selectbox == "Peer Group Selection":
    peergroup_page()

if add_selectbox == "Beta Calculation":
    beta_page()

if add_selectbox == "Company Database":
    db()
