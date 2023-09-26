import pandas as pd
import numpy as np
import numpy as np
import plotly.express as px
from sklearn.preprocessing import RobustScaler
from sklearn.manifold import TSNE
import streamlit as st


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

# Filter Data for TSNE
X = df[["marketCap_bins", "revenueGrowth", "operatingMargins"]]
X = RobustScaler().fit_transform(X)


def create_3d_scatterplot(X: pd.DataFrame()) -> pd.DataFrame:
    X_embedded_3d = TSNE(
        n_components=3, learning_rate="auto", init="random", perplexity=3
    ).fit_transform(X)
    X_embedded_3d = pd.DataFrame(X_embedded_3d)
    df.reset_index(drop=True, inplace=True)
    embedding_3d = pd.concat([df, X_embedded_3d], axis=1)
    embedding_3d.marketCap_bins = embedding_3d.marketCap_bins.astype(float)

    fig = px.scatter_3d(
        embedding_3d,
        x=0,
        y=1,
        z=2,
        size=embedding_3d.marketCap_bins,
        hover_name=embedding_3d.shortName,
        color=embedding_3d.marketCap_bins,
        opacity=0.6,
        hover_data=embedding_3d[
            ["currency", "marketCap", "revenueGrowth", "operatingMargins"]
        ],
    )
    fig.update_traces(marker_size=8)

    # Remove x, y, and z labels and ticks
    fig.update_layout(
        scene=dict(
            xaxis_title=None,
            yaxis_title=None,
            zaxis_title=None,
            xaxis=dict(showticklabels=False),
            yaxis=dict(showticklabels=False),
            zaxis=dict(showticklabels=False),
        )
    )
    return fig


add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?", ("Email", "Home phone", "Mobile phone")
)

fig = create_3d_scatterplot(X)

feature_select = st.multiselect("Features", df.columns)
sector_select = st.multiselect("Sector", sector_selection, ["Technology"])
industry_select = st.multiselect("Industry", industry_selection)

df = df[(df["sector"].isin(sector_select)) | (df["industry"].isin(industry_select))]
st.plotly_chart(fig, use_container_width=True)
st.dataframe(df, hide_index=True)
