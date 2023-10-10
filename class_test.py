import pandas as pd

from class_peer_group import Peer_Group


pg = Peer_Group()
pg.add_company("AAPL")
df = pg.stock_data().sort_values("date", ascending=False)[["symbol", "date", "open"]]
df["return"] = df["open"].pct_change()
df["beta"] = df["return"].rolling(window=2).corr(df["return"])
print(df)
