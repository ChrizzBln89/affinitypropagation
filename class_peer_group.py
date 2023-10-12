import datetime
from click import DateTime
import pandas as pd
from modules.path import path_data
from class_gbq import historical_index_quotes, historical_peer_quotes, info_data


class Peer_Group:
    def __init__(self):
        # Data objects for calculations
        self.info_data = info_data()
        self.peer_companies = []
        self.peer_info_data = pd.DataFrame()
        self.peer_historical_data = pd.DataFrame()
        self.index_historical_data = {}
        self.index = {}

        # parameter beta calc
        self.time_interval = 0
        self.fill_method = "ffill"
        self.peer_start_date = None
        self.peer_end_date = None

    def add_company(self, ticker: str) -> list:
        """Adds companies to the peer group selection and is later used for data filtering form database."""
        self.peer_companies.append(ticker)
        self.peer_companies = list(set(self.peer_companies))
        return self.peer_companies

    def add_index(self, company: str, index: str) -> dict:
        self.index[company] = index
        return self.index

    def company_data(self) -> pd.DataFrame:
        """Downloads general peer group information from the database."""
        self.peer_info_data = self.info_data[
            self.info_data["symbol"].isin(self.peer_companies)
        ]
        return self.peer_info_data

    def stock_data(self) -> pd.DataFrame:
        """Downloads peer group stock data from the database for beta calculation."""
        self.peer_historical_data = historical_peer_quotes(
            self.peer_companies
        ).infer_objects()
        return self.peer_historical_data

    def index_data(self) -> pd.DataFrame:
        for key in self.index.keys():
            self.index_historical_data[key] = historical_index_quotes(self.index[key])
        return self.index_historical_data

    def beta_calc(self) -> pd.DataFrame:
        pass
