import datetime
from click import DateTime
import pandas as pd
from class_gbq import historical_index_quotes, historical_peer_quotes, info_data
from valuationhub.valuationhub.assets import download_index_ticker


class Peer_Group:
    def __init__(self):
        # Data objects for calculations
        self.info_data: pd.DataFrame = info_data()
        self.peer_companies: list = []
        self.peer_info_data: pd.DataFrame = pd.DataFrame()
        self.peer_historical_data: pd.DataFrame = pd.DataFrame()
        self.index_historical_data: dict = {}
        self.beta_calc_dict: dict = {}
        self.available_indices = download_index_ticker()
        self.index: dict = {}

        # parameter beta calc
        self.time_interval = 0
        self.fill_method: str = "ffill"
        self.peer_start_date = "2010-09-01"
        self.peer_end_date = "2023-10-01"

    def add_company(self, ticker: str) -> list:
        """Adds companies to the peer group selection and is later used for data filtering form database."""
        self.peer_companies.append(ticker)
        self.peer_companies = list(set(self.peer_companies))

        for company in self.peer_companies:
            self.index[company] = "^GDAXI"

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
        self.peer_historical_data = self.stock_data()
        self.index_historical_data = self.index_data()

        beta_calc_dict = {}

        for peer in self.peer_companies:
            stock = self.peer_historical_data.loc[
                self.peer_historical_data["symbol"] == peer, :
            ]
            stock = stock[["symbol", "date", "close"]]
            index = self.index_historical_data[peer][["symbol", "date", "close"]]

            stock["date"] = pd.to_datetime(stock["date"])
            index["date"] = pd.to_datetime(index["date"])

            stock["date"] = stock["date"].apply(lambda x: str(x)[0:10])
            index["date"] = index["date"].apply(lambda x: str(x)[0:10])

            date_range = pd.date_range(
                start=self.peer_start_date, end=self.peer_end_date
            )
            date_df = pd.DataFrame({"date": date_range})
            date_df["date"] = date_df["date"].apply(lambda x: str(x)[0:10])

            beta_calc = date_df.merge(index, on="date", how="left")
            beta_calc = beta_calc.merge(
                stock, on="date", how="left", suffixes=["_index", "_stock"]
            )

            beta_calc["date"] = pd.to_datetime(beta_calc["date"])
            beta_calc["weekday"] = beta_calc["date"].dt.day_name()
            beta_calc = beta_calc.sort_values(by="date")
            beta_calc = beta_calc.ffill()

            beta_calc = beta_calc[
                [
                    "date",
                    "weekday",
                    "symbol_stock",
                    "close_stock",
                    "symbol_index",
                    "close_index",
                ]
            ]

            beta_calc = beta_calc.loc[
                (beta_calc["weekday"] != "Saturday")
                & (beta_calc["weekday"] != "Sunday"),
                :,
            ]

            first_day = beta_calc["weekday"][0]
            beta_calc = beta_calc.loc[beta_calc["weekday"] == first_day, :]

            beta_calc["return_stock"] = beta_calc["close_stock"].pct_change()
            beta_calc["return_index"] = beta_calc["close_index"].pct_change()

            beta_calc["beta"] = (
                beta_calc["return_stock"]
                .rolling(window=52)
                .corr(beta_calc["return_index"])
            )

            beta_calc = beta_calc.sort_values(by="date", ascending=False)
            beta_calc_dict[peer] = beta_calc

        self.beta_calc_dict = beta_calc_dict

        return beta_calc_dict
