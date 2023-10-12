import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import RobustScaler
from modules.pages.peer_group_user import peer_group_user
from modules.graph import create_3d_scatterplot


def peergroup_page():
    # Load Data
    df = peer_group_user.info_data
    df = df[df["currency"].isin(["EUR"])]
    sector_selection = list(df["sector"].unique())
    industry_selection = list(df["industry"].unique())

    # Marketcap Bins
    num = 10
    labels = np.linspace(start=1, stop=num, num=num)
    df["marketCap_bins"] = pd.qcut(df["marketcap"], q=num, labels=labels)

    feature_select = st.multiselect(
        "Features", df.columns, ["revenuegrowth", "profitmargins", "returnonequity"]
    )
    # sector_select = st.multiselect("Sector", sector_selection, ["Technology"])
    industry_select = st.multiselect(
        "industry", industry_selection, ["Software—Application"]
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

    df = st.data_editor(
        df,
        column_config={
            "Peer Group": st.column_config.CheckboxColumn(
                "Include in Peer Group?",
                default=False,
            )
        },
        disabled=["widgets"],
        hide_index=True,
    )

    for company in list(df.loc[df["Peer Group"] == True, "Symbol"]):
        peer_group_user.add_company(company)


if __name__ == "__main__":
    peergroup_page()
