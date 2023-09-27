import pandas as pd


class peer_group:
    def __init__(self):
        self.data = pd.read_csv("Data/info_merged.csv", header=0, index_col=0)
        self.peer_group = []

    def add_company(self, ticker):
        # Grab Company from Database
        self.peer_group = self.peer_group.append(ticker)
        return self.peer_group
