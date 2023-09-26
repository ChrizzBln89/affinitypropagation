import pandas as pd
import plotly.express as px


def create_3d_scatterplot(df: pd.DataFrame(), X: pd.DataFrame()):
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
        hover_data=embedding_3d[["marketCap", "revenueGrowth", "operatingMargins"]],
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
