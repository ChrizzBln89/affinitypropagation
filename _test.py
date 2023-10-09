import numpy as np
import pytest
from class_peer_group import Peer_Group
import pandas as pd
from valuationhub.valuationhub.assets import (
    get_symbols,
    upload_income_stmt,
    upload_info,
    upload_quotes,
)


# Define custom markers directly using the @pytest.mark decorator
@pytest.mark.peer_group
def test_peer_group_init():
    pg = Peer_Group()
    assert pg.fill_method == "ffill"
    assert pg.index == "test_index"
    assert isinstance(pg.peer_companies, list)
    assert isinstance(pg.historical_data, pd.DataFrame)
    assert isinstance(pg.peer_historical_data, pd.DataFrame)
    assert isinstance(pg.info_data, pd.DataFrame)
    assert isinstance(pg.peer_info_data, pd.DataFrame)
    assert pg.time_interval == 0


pg = Peer_Group()
pg = pg.add_company("AAPL")


@pytest.mark.peer_group
def test_peer_group_add_company(pg):
    assert "AAPL" in pg.peer_companies
    assert isinstance(pg.add_company("AAPL"), list)


@pytest.mark.peer_group
def test_peer_group_company_data(pg):
    assert isinstance(pg.company_data(), pd.DataFrame)


@pytest.mark.peer_group
def test_peer_group_stock_data(pg):
    assert isinstance(pg.stock_data(), pd.DataFrame)


@pytest.mark.peer_group
def test_peer_group_stock_data():
    pg = Peer_Group()
    comp_list_symbol = list(set(pg.historical_data["symbol"]))
    assert "AAPL" in comp_list_symbol
    assert "Adj Close" in pg.historical_data.columns
    assert pg.peer_companies == comp_list_symbol
    assert isinstance(pg.historical_data, pd.DataFrame)


@pytest.mark.gbq
def test_download_gbq():
    symbols = get_symbols()
    assert type(symbols) == np.ndarray
    assert "AAPL" in list(symbols)
    assert len(list(symbols)) > 10000


@pytest.mark.gbq
def test_upload_quotes():
    quotes = upload_quotes(get_symbols()[0])
    assert isinstance(quotes, pd.DataFrame)


@pytest.mark.gbq
def test_upload_info():
    info = upload_info()
    assert isinstance(info, pd.DataFrame)


@pytest.mark.gbq
def test_upload_income_stmt():
    info = upload_income_stmt(get_symbols()[0])
    assert isinstance(info, pd.DataFrame)
