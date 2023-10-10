import pandas as pd
from modules.path import path_data
from class_gbq import info_data, historical_data


class Peer_Group:
    def __init__(self):
        # Connection to database
        self.info_data = info_data()
        # Filtered data based on peer group selection
        self.peer_info_data = pd.DataFrame()
        self.peer_historical_data = pd.DataFrame()
        self.peer_companies = []
        # Attributes of peer group
        self.time_interval = 0
        self.fill_method = "ffill"
        self.index = "test_index"
        self.peer_start_date = None
        self.peer_end_date = None

    def add_company(self, ticker: str) -> list:
        """Adds companies to the peer group selection and is later used for data filtering form database."""
        self.peer_companies.append(ticker)
        self.peer_companies = list(set(self.peer_companies))
        return self.peer_companies

    def company_data(self) -> pd.DataFrame():
        """Downloads general peer group information from the database."""
        self.peer_info_data = self.info_data[
            self.info_data["symbol"].isin(self.peer_companies)
        ]
        return self.peer_info_data

    def stock_data(self) -> pd.DataFrame():
        """Downloads peer group stock data from the database for beta calculation."""
        self.peer_historical_data = historical_data(self.peer_companies).infer_objects()
        return self.peer_historical_data

    def beta_calc(self) -> pd.DataFrame():
        df = self.peer_historical_data.pct_change()
        list_results = []
        for col in df.columns:
            list_results.append(df[col].rolling().corr(df[col]))
        return print(self.peer_historical_data)


if __name__ == "__main__":
    pg = Peer_Group()
    pg.add_company("AAPL")
    pg.stock_data()
    pg.beta_calc()
