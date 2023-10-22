import streamlit as st
import pandas as pd
from modules.pages.peer_group_user import peer_group_user
from modules.pages.beta_page import beta_page


st.set_page_config(layout="wide")
beta_page(peer_group_user=peer_group_user)
