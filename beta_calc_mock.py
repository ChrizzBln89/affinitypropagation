from class_peer_group import Peer_Group
import pandas as pd

pg = Peer_Group()

pg.add_company("AAPL")
pg.add_index("AAPL", "^GDAXI")
print(pg.beta_calc()["AAPL"].head())
