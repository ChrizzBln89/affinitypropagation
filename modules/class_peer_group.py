import pandas as pd
from modules.path import path_data


class Peer_Group:
    def __init__(self):
        # Connection to database
        self.info_data = pd.read_csv(path_data + "info_merged.csv")
        self.historical_data = pd.read_csv(path_data + "history_merged_reduced.csv")
        # Filtered data based on peer group selection
        self.peer_info_data = pd.DataFrame()
        self.peer_historical_data = pd.DataFrame()
        self.peer_companies = []
        # Attributes of peer group
        self.time_interval = 0
        self.fill_method = "ffill"
        self.index = "test_index"

    def add_company(self, ticker: str) -> list:
        """Adds companies to the peer group selection and is later used for data filtering form database."""
        self.peer_companies.append(ticker)
        return self.peer_companies

    def company_data(self) -> pd.DataFrame():
        """Downloads general peer group information from the database."""
        self.peer_info_data = self.info_data[
            self.info_data["symbol"].isin(self.peer_companies)
        ]
        return self.peer_info_data

    def stock_data(self) -> pd.DataFrame():
        """Downloads peer group stock data from the database for beta calculation."""
        self.peer_historical_data = self.historical_data[
            self.historical_data["symbol"].isin(self.peer_companies)
        ]
        return self.peer_historical_data

    def beta_calc(self) -> pd.DataFrame():
        pass
