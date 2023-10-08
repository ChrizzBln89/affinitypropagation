from class_peer_group import Peer_Group
import pytest
import pandas as pd

from valuationhub.valuationhub.assets import get_symbols, upload_quotes

pg = Peer_Group()


def test_peer_group_init():
    assert pg.fill_method == "ffill"
    assert pg.index == "test_index"
    assert type(pg.peer_companies) == list
    assert type(pg.historical_data) == pd.DataFrame
    assert type(pg.peer_historical_data) == pd.DataFrame
    assert type(pg.info_data) == pd.DataFrame
    assert type(pg.peer_info_data) == pd.DataFrame
    assert pg.time_interval == 0


def test_peer_group_add_company():
    pg.add_company("AAPL")
    assert "AAPL" in pg.peer_companies
    assert type(pg.add_company("AAPL")) == list


def test_peer_group_company_data():
    assert type(pg.company_data()) == pd.DataFrame


def test_peer_group_stock_data():
    assert type(pg.stock_data()) == pd.DataFrame


def test_peer_group_stock_data():
    comp_list_symbol = list(set(pg.historical_data["symbol"]))
    assert "AAPL" in comp_list_symbol
    assert "Adj Close" in pg.historical_data.columns
    assert pg.peer_companies == comp_list_symbol
    assert type(pg.historical_data) == pd.DataFrame


def test_get_symbols():
    symbols = get_symbols()
    assert type(symbols) == list
    assert "AAPL" in symbols
    assert type(symbols[0]) == str


def test_upload_quotes():
    assert type(upload_quotes()) == pd.DataFrame
