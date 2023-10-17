import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import RobustScaler
from modules.pages.peer_group_user import peer_group_user
from modules.graph import create_3d_scatterplot


def peergroup_page():
    st.header("Peer Group Filter", divider="blue")

    # Load Data
    df = peer_group_user.info_data
    industry_selection = list(df["industry"].unique())

    # Marketcap Bins
    num = 10
    labels = np.linspace(start=1, stop=num, num=num)
    df["marketCap_bins"] = pd.qcut(df["marketcap"], q=num, labels=labels)

    industry_select = st.multiselect(
        "Industry Selection - Multiple Industries can be Selected:",
        industry_selection,
        ["Auto Manufacturers", "Auto Parts"],
    )

    feature_select = st.multiselect(
        "Features (Benchmark) Selection:",
        df.columns,
        ["revenuegrowth", "profitmargins", "returnonequity"],
    )

    with st.expander("Ranges for selected Features:"):
        for feature in feature_select:
            values = st.slider(
                f"Select a range of values for {feature}", 0.0, 100.0, (25.0, 75.0)
            )
            st.write("Values:", values)

    # ... (existing code)

    filtered_df = df.copy()
    for feature in feature_select:
        values = st.session_state.get(feature + "_values", (0.0, 100.0))
        filtered_df = filtered_df[
            (filtered_df[feature] >= values[0]) & (filtered_df[feature] <= values[1])
        ]

    col_list = [
        "symbol",
        "website",
        "industry",
        "long_business_summary",
    ] + feature_select

    df = st.data_editor(
        filtered_df[col_list],
        disabled=["widgets"],
        hide_index=True,
    )


if __name__ == "__main__":
    peergroup_page()
