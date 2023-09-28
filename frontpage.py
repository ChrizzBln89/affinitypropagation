import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import RobustScaler
from class_peer_group import peer_group
from graph import create_3d_scatterplot

add_selectbox = st.sidebar.selectbox(
    "Page Navigation",
    ("Peer Group", "Beta Calculation"),
)

# Load Data
df = pd.read_csv("Data/info_merged.csv", header=0, index_col=0)
df.reset_index(inplace=True)
df = df[df["currency"].isin(["EUR"])]
sector_selection = list(df["sector"].unique())
industry_selection = list(df["industry"].unique())

# Marketcap Bins
num = 10
labels = np.linspace(start=1, stop=num, num=num)
df["marketCap_bins"] = pd.qcut(df["marketCap"], q=num, labels=labels)

feature_select = st.multiselect(
    "Features", df.columns, ["revenueGrowth", "profitMargins", "returnOnEquity"]
)
# sector_select = st.multiselect("Sector", sector_selection, ["Technology"])
industry_select = st.multiselect(
    "Industry", industry_selection, ["Software—Application"]
)
st.multiselect("Algorithm", ["1", "2", "3"])

# peer_group_user.add_company()

# Filter Data for TSNE
X = df[feature_select].dropna(axis=1)
X = RobustScaler().fit_transform(X)
fig = create_3d_scatterplot(df=df, X=X)

# df = df[(df["sector"].isin(sector_select)) | (df["industry"].isin(industry_select))]
df = df[df["industry"].isin(industry_select)]

st.plotly_chart(fig, use_container_width=True)

df["Peer Group"] = False

df = st.data_editor(
    df,
    column_config={
        "Peer Group": st.column_config.CheckboxColumn(
            "Your favorite?",
            help="Select your **favorite** widgets",
            default=False,
        )
    },
    disabled=["widgets"],
    hide_index=True,
)

peer_group_user = peer_group()
peer_group_user.add_company(list(df.loc[df["Peer Group"] == True, "symbol"]))

st.sidebar.write("Selected Companies")
st.sidebar.write(peer_group_user.peer_companies)


st.sidebar.dataframe(
    df.loc[df["Peer Group"] == True, "shortName"],
    hide_index=True,
    use_container_width=True,
)
