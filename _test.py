import numpy as np
import pytest
from class_gbq import historical_peer_quotes, historical_index_quotes, info_data
from class_peer_group import Peer_Group
import pandas as pd
from valuationhub.valuationhub.assets import *


# Define custom markers directly using the @pytest.mark decorator
@pytest.mark.peer_group
def test_peer_group_init():
    pg = Peer_Group()
    assert pg.fill_method == "ffill"
    assert pg.index == {}
    assert isinstance(pg.peer_companies, list)
    assert isinstance(pg.peer_historical_data, pd.DataFrame)
    assert isinstance(pg.info_data, pd.DataFrame)
    assert isinstance(pg.peer_info_data, pd.DataFrame)
    assert pg.time_interval == 0


@pytest.mark.peer_group
def test_peer_group_add_company():
    pg = Peer_Group()
    pg.add_company("AAPL")
    assert "AAPL" in pg.peer_companies
    assert isinstance(pg.add_company("AAPL"), list)


@pytest.mark.peer_group
def test_peer_group_stock_data():
    pg = Peer_Group()
    pg.add_company("AAPL")
    df = pg.stock_data()
    assert "AAPL" in list(df["symbol"])
    assert "volume" in pg.peer_historical_data.columns
    assert isinstance(pg.peer_historical_data, pd.DataFrame)


@pytest.mark.peer_group
def test_add_index():
    pg = Peer_Group()
    pg.add_company("AAPL")
    pg.add_index(index="^GDAXI", company="AAPL")
    assert "^GDAXI" in pg.index.values()
    assert "AAPL" in pg.index.keys()
    assert isinstance(pg.index, dict)


@pytest.mark.peer_group
def test_index_data():
    pg = Peer_Group()
    pg.add_company("AAPL")
    pg.add_index(index="^GDAXI", company="AAPL")
    index_dict = pg.index_data()
    assert isinstance(index_dict, dict)
    assert isinstance(index_dict["AAPL"], pd.DataFrame)


@pytest.mark.peer_group
def test_beta_calc():
    pass


@pytest.mark.gbq
def test_download_gbq():
    symbols = get_symbols()
    assert type(symbols) == np.ndarray
    assert "AAPL" in list(symbols)
    assert len(list(symbols)) > 10000


@pytest.mark.gbq
def test_upload_quotes():
    quotes = upload_quotes(get_symbols())
    assert isinstance(quotes, pd.DataFrame)


@pytest.mark.gbq
def test_upload_info():
    info = upload_info()
    assert isinstance(info, pd.DataFrame)


@pytest.mark.gbq
def test_upload_income_stmt():
    income_stmt = upload_income_stmt(get_symbols())
    assert isinstance(income_stmt, pd.DataFrame)


@pytest.mark.gbq
def test_info_data():
    info = info_data()
    assert isinstance(info, pd.DataFrame)


@pytest.mark.gbq
def test_download_index_ticker():
    ticker = download_index_ticker()
    assert isinstance(ticker, list)
    assert "^GDAXI" in ticker


@pytest.mark.gbq
def test_upload_index_quotes():
    ticker = download_index_ticker()
    df = upload_index_quotes(ticker)
    assert isinstance(df, pd.DataFrame)
    assert "^GDAXI" in df["symbol"].values
    assert "timestamp" in df.columns
    assert "open" in df.columns


@pytest.mark.gbq
def test_download_ticker_quotes():
    ticker_quotes = historical_index_quotes("^GDAXI")
    assert isinstance(ticker_quotes, pd.DataFrame)
    assert "open" in ticker_quotes.columns
    assert "symbol" in ticker_quotes.columns
    assert "^GDAXI" in list(ticker_quotes["symbol"].values)
