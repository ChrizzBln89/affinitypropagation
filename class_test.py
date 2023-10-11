import pandas as pd

from class_peer_group import Peer_Group


pg = Peer_Group()
pg.add_company("AAPL")
pg.stock_data()
pg.beta_calc()
print(pg.beta_calc())
