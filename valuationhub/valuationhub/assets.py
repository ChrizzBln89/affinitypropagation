from tomlkit import table
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

PATH_MAIN_DIR = str(Path(__file__).parent.parent.parent)
PATH_DATA_DIR = str(PATH_MAIN_DIR + "/data")


def gbq_upload(data: pd.DataFrame, table_id: str):
    project_id = "flash-realm-401106"
    dataset_id = "valuationhub"
    table_id = table_id
    credentials_file = PATH_MAIN_DIR + "/flash-realm-401106-a0bf29a37df7.json"

    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=["https://www.googleapis.com/auth/bigquery"]
    )

    destination_table = f"{project_id}.{dataset_id}.{table_id}"

    to_gbq(
        data,
        destination_table,
        project_id=project_id,
        if_exists="append",  # Choose whether to replace or append to the table
        credentials=credentials,  # Specify the schema for the table
    )


@asset
def get_symbols():
    service_account_json = PATH_MAIN_DIR + "/flash-realm-401106-a0bf29a37df7.json"
    client = bigquery.Client.from_service_account_json(service_account_json)

    query = """
    SELECT DISTINCT(symbol)
    FROM flash-realm-401106.valuationhub.h_info
    """
    df = client.query(query).to_dataframe()
    tickers = df["symbol"].values
    return tickers


@asset()
def download_index_ticker():
    url = "https://de.finance.yahoo.com/world-indices/?guccounter=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")
    if tables:
        table = tables[0]
        df = pd.read_html(str(table))[0]

    df.columns = df.columns.str.lower()
    return list(df["symbol"].values)


@asset()
def upload_index_quotes(download_index_ticker):
    tickers = download_index_ticker
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

    gbq_upload(data=df, table_id="h_index_quotes")

    return df


@asset()
def upload_quotes(get_symbols):
    tickers = random.sample(list(get_symbols), 10)
    dfs = {}

    for symbol in tqdm.tqdm(
        tickers,
        ncols=100,
        desc="Progress merge: ",
        colour="#00d111",
    ):
        try:
            ticker = yf.Ticker(symbol)
            info_dict = ticker.history(period="1d")
            df = pd.DataFrame.from_dict(info_dict, orient="columns")
            df["symbol"] = str(ticker).strip("yfinance.Ticker object <").strip(">")
            dfs[ticker] = df
        except:
            continue

    dfs = dfs.values()
    df = pd.concat(dfs, axis=0).reset_index()
    df["timestamp"] = pd.Timestamp.now()
    df.columns = [x.replace(" ", "_").lower() for x in df.columns]
    df = df.infer_objects()
    df["date"] = df["date"].astype(str)
    gbq_upload(data=df, table_id="h_index_quotes")
    return df


@asset(deps=[get_symbols])
def upload_info():
    df = pd.read_csv(
        "/home/chris/code/affinitypropagation/data/info_merged_reduced.csv"
    )
    df["timestamp"] = pd.Timestamp.now()
    gbq_upload(data=df, table_id="h_info")
    return df


@asset()
def upload_income_stmt(get_symbols):
    tickers = random.sample(list(get_symbols), 10)

    dfs = {}

    for symbol in tqdm.tqdm(
        tickers,
        ncols=100,
        desc="Progress merge: ",
        colour="#00d111",
    ):
        try:
            ticker = yf.Ticker(symbol)
            info_dict = ticker.income_stmt
            df = pd.DataFrame.from_dict(info_dict, orient="columns")
            df["symbol"] = str(ticker)
            dfs[ticker] = df
        except:
            continue

    dfs = dfs.values()
    df = pd.concat(dfs, axis=0).reset_index()
    df["timestamp"] = pd.Timestamp.now()
    df = df.melt(
        id_vars=["index", "symbol", "timestamp"], var_name="date", value_name="amount"
    )
    df["symbol"] = (
        df["symbol"].str.replace("yfinance.Ticker object <", "").str.replace(">", "")
    )
    df.columns = [x.replace(" ", "_").lower() for x in df.columns]
    df = df.infer_objects()

    gbq_upload(data=df, table_id="h_income_stmt")

    return df
