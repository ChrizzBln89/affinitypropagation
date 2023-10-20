import streamlit as st
from datetime import datetime
from modules.pages import peer_group_user


def beta_page(peer_group_user=peer_group_user) -> None:
    st.header("Peer Group Beta Overview", divider="blue")

    tabs_peer_group = st.tabs(peer_group_user.peer_companies)

    beta_dict = peer_group_user.beta_calc()

    for i, company in enumerate(peer_group_user.peer_companies):
        with tabs_peer_group[i]:
            st.subheader(f"{company} Beta")
            st.write(
                peer_group_user.peer_info_data[
                    peer_group_user.peer_info_data["symbol"] == company
                ]
            )
            st.line_chart(beta_dict[company]["beta"])
            st.table(beta_dict[company])
