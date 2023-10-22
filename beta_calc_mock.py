import random
from modules.pages.class_peer_group import Peer_Group
import pandas as pd
from valuationhub.valuationhub.assets import get_symbols

pg = Peer_Group()
symbols = get_symbols()


def random_beta_calc(pg, symbols):
    random_tickers = random.sample(symbols, k=10)

    for ticker in random_tickers:
        pg.add_company(ticker)
        pg.add_index(ticker, "^GDAXI")

    result_dict = pg.beta_calc()
    return print(result_dict)


random_beta_calc(pg, symbols)
