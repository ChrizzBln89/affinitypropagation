import pandas as pd
import requests
from bs4 import BeautifulSoup
import tqdm
import yfinance as yf
from modules.params import *
import yfinance as yf
import tqdm
import pandas as pd
import random
import requests

from bs4 import BeautifulSoup
from pathlib import Path
from google.oauth2 import service_account
from google.cloud import bigquery
from pandas_gbq import to_gbq
from dagster import (
    AssetCheckResult,
    RunRequest,
    asset,
    asset_check,
    define_asset_job,
    sensor,
)


def download_index_ticker():
    url = "https://de.finance.yahoo.com/world-indices/?guccounter=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")
    if tables:
        table = tables[0]
        df = pd.read_html(str(table))[0]

    df.columns = df.columns.str.lower()
    return df["symbol"].values


def upload_index_quotes():
    tickers = download_index_ticker()
    dfs = {}

    for symbol in tqdm.tqdm(
        tickers,
        ncols=100,
        desc="Progress merge: ",
        colour="#00d111",
    ):
        try:
            ticker = yf.Ticker(symbol)
            info_dict = ticker.history(period="max")
            df = pd.DataFrame.from_dict(info_dict, orient="columns")
            df["symbol"] = symbol
            dfs[ticker] = df
        except:
            continue

    dfs = dfs.values()
    df = pd.concat(dfs, axis=0).reset_index()
    df["timestamp"] = pd.Timestamp.now()
    df.columns = [x.replace(" ", "_").lower() for x in df.columns]
    df = df.infer_objects()
    df["date"] = df["date"].astype(str)

    project_id = "flash-realm-401106"
    dataset_id = "valuationhub"
    table_id = "h_index_quotes"
    credentials_file = "flash-realm-401106-a0bf29a37df7.json"
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=["https://www.googleapis.com/auth/bigquery"]
    )
    destination_table = f"{project_id}.{dataset_id}.{table_id}"
    to_gbq(
        df,
        destination_table,
        project_id=project_id,
        if_exists="append",
        credentials=credentials,
    )
    return df


upload_index_quotes()
