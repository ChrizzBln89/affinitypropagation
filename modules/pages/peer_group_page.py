import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import RobustScaler
from peer_group_user import peer_group_user


def peergroup_page(peer_group_user=peer_group_user):
    st.header("1. Peer Group Company Finder", divider="blue")

    # Load Data
    df = peer_group_user.info_data
    industry_selection = list(df["Industry"].unique())

    # Marketcap Bins
    num = 10
    labels = np.linspace(start=1, stop=num, num=num)
    df["marketCap_bins"] = pd.qcut(df["Market Cap"], q=num, labels=labels)

    industry_select = st.multiselect(
        "Industry Selection - Multiple Industries can be Selected:",
        industry_selection,
        ["Auto Manufacturers", "Auto Parts"],
    )

    df = df.loc[df["Industry"].isin(industry_select), :]

    feature_select = st.multiselect(
        "Features (Benchmark) Selection:",
        df.columns,
        ["Revenue Growth %", "Profit Margins %", "Return On Equity %"],
    )

    filtered_df = df.copy()

    with st.expander("Ranges for selected Features:"):
        for feature in feature_select:
            values = st.slider(
                f"Select a range of values for {feature}",
                min(filtered_df[feature]),
                max(filtered_df[feature]),
                (min(filtered_df[feature]), max(filtered_df[feature])),
            )
            filtered_df = filtered_df[
                (filtered_df[feature] >= values[0])
                & (filtered_df[feature] <= values[1])
            ]

    col_list = [
        "Symbol",
        "Website",
        "Industry",
        "Long Business Summary",
    ] + feature_select

    df = st.dataframe(
        filtered_df[col_list].style.format(
            {"Revenue Growth %": "{:.2%}", "Profit Margins %": "{:.2%}"}
        ),
        column_config={
            "Website": st.column_config.LinkColumn(
                "Website (Use Doubleclick)",
                help="Website of the Company.",
                max_chars=100,
            )
        },
        hide_index=True,
    )


if __name__ == "__main__":
    peergroup_page()
