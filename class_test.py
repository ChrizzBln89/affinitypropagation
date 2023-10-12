from numpy import inner
from class_peer_group import Peer_Group
import pandas as pd


def beta_calc() -> pd.DataFrame:
    pg = Peer_Group()

    pg.add_company("AAPL")
    pg.add_index("^GDAXI")

    stock = pg.stock_data()
    index = pg.index_data()

    stock = stock[["symbol", "date", "close"]]
    index = index[["symbol", "date", "close"]]

    stock["date"] = stock["date"].astype(str)
    index["date"] = index["date"].astype(str)

    stock["date"] = stock["date"].apply(lambda x: str(x)[0:10])
    index["date"] = index["date"].apply(lambda x: str(x)[0:10])

    beta_calc = stock.merge(
        index, on="date", how="inner", suffixes=["_stock", "_index"]
    )
    beta_calc["date"] = pd.to_datetime(beta_calc["date"])
    beta_calc["weekday"] = beta_calc["date"].dt.day_name()
    beta_calc = beta_calc.sort_values(by="date")

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

    beta_calc["return_stock"] = beta_calc["close_stock"].pct_change()
    beta_calc["return_index"] = beta_calc["close_index"].pct_change()

    beta_calc["beta"] = (
        beta_calc["return_stock"].rolling(window=5).corr(beta_calc["return_index"])
    )

    beta_calc = beta_calc.sort_values(by="date", ascending=False)

    return beta_calc


print(beta_calc())
