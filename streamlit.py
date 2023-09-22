import pandas as pd
import numpy as np
import numpy as np
import plotly.express as px
from sklearn.preprocessing import RobustScaler
from sklearn.manifold import TSNE
import streamlit as st

df = pd.read_csv("Data/info_merged.csv", header=0, index_col=0)
df.reset_index(inplace=True)
df = df[df["currency"].isin(["EUR"])]
df = df[df["sector"] == "Technology"]


num = 10
labels = np.linspace(start=1, stop=num, num=num)
df["marketCap_bins"] = pd.qcut(df["marketCap"], q=num, labels=labels)

X = df[["marketCap", "revenueGrowth", "operatingMargins"]]
X = RobustScaler().fit_transform(X)

X_embedded_3d = TSNE(
    n_components=3, learning_rate="auto", init="random", perplexity=3
).fit_transform(X)
X_embedded_3d = pd.DataFrame(X_embedded_3d)
df.reset_index(drop=True, inplace=True)
embedding_3d = pd.concat([df, X_embedded_3d], axis=1)
embedding_3d.marketCap_bins = embedding_3d.marketCap_bins.astype(float)


def create_3d_scatterplot(embedding):
    fig = px.scatter_3d(
        embedding,
        x=0,
        y=1,
        z=2,
        size=embedding.marketCap_bins,
        hover_name=embedding.shortName,
        color=embedding.marketCap_bins,
        opacity=0.6,
        hover_data=embedding[
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

    fig.show()


# Assuming you have the 'embedding' data as a 3D array or list of lists
fig = create_3d_scatterplot(embedding_3d)

option = st.selectbox("Industry", ("Email", "Home phone", "Mobile phone"))

st.write("You selected:", option)
