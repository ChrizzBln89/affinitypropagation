import pandas as pd


class peer_group:
    def __init__(self):
        self.data = pd.read_csv("Data/info_merged.csv", header=0, index_col=0)
        self.peer_companies = []

    def add_company(self, ticker: str):
        # Grab Company from Database
        self.peer_companies.append(ticker)
        return self.peer_companies

    def company_data(self) -> pd.DataFrame():
        self.data = self.data[self.data["symbol"].isin(self.peer_companies)]
        return self.data
