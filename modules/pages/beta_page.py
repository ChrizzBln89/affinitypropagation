import streamlit as st
from datetime import datetime
from modules.pages import peer_group_user
import plotly.graph_objs as go


def beta_page(peer_group_user=peer_group_user) -> None:
    st.header("Peer Group Beta Overview", divider="blue")
    tabs_peer_group = st.tabs(
        ["Peer Group Finder", "Peer Group Overview", "Beta Calculation", "Multiples"]
    )
    tabs_peer_group = st.tabs(peer_group_user.peer_companies)

    beta_dict = peer_group_user.beta_calc()

    for i, company in enumerate(peer_group_user.peer_companies):
        with tabs_peer_group[i]:
            st.subheader(f"{company} Beta")
            st.line_chart(beta_dict[company]["beta"])
            # Create a scatter plot
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=beta_dict[company]["return_index"],
                    y=beta_dict[company]["return_stock"],
                    mode="markers",
                    name="Returns",
                )
            )
            fig.update_layout(
                title="Stock vs Index Returns",
                xaxis_title="Index Returns",
                yaxis_title="Stock Returns",
            )

            # Display the scatter plot in Streamlit
            st.plotly_chart(fig)

            st.table(beta_dict[company].reset_index(drop=True))
            # Create a scatter plot
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=beta_dict[company]["return_index"],
                    y=beta_dict[company]["return_stock"],
                    mode="markers",
                    marker=dict(
                        color=[
                            "blue" if r == "return_index" else "red"
                            for r in beta_dict[company].reset_index().columns
                        ],
                        size=10,
                        symbol=[
                            "circle" if r == "return_index" else "square"
                            for r in beta_dict[company].reset_index().columns
                        ],
                        line=dict(
                            color=[
                                "blue" if r == "return_index" else "red"
                                for r in beta_dict[company].reset_index().columns
                            ],
                            width=2,
                        ),
                    ),
                    name="Returns",
                )
            )
            fig.update_layout(
                title="Stock vs Index Returns",
                xaxis_title="Index Returns",
                yaxis_title="Stock Returns",
            )

            # Display the scatter plot in Streamlit
            st.plotly_chart(fig)
