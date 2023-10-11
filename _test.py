import numpy as np
import pytest
from class_gbq import historical_data
from class_peer_group import Peer_Group
import pandas as pd
from valuationhub.valuationhub.assets import *


# Define custom markers directly using the @pytest.mark decorator
@pytest.mark.peer_group
def test_peer_group_init():
    pg = Peer_Group()
    assert pg.fill_method == "ffill"
    assert pg.index == "test_index"
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
def test_beta_calc():
    pg = Peer_Group()
    pg.add_company("AAPL")
    pg.stock_data()
    df = pg.beta_calc()
    assert type(df) == pd.DataFrame
    assert "beta" in df.columns
    assert "AAPL" in df["symbol"].values


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
def info_data():
    info = info_data()
    assert isinstance(info, pd.DataFrame)
