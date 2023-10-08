import pandas as pd
from google.oauth2 import service_account
from pandas_gbq import to_gbq
from dagster import asset
import yfinance as yf


@asset
def upload_info():
    project_id = "flash-realm-401106"
    dataset_id = "valuationhub"
    table_id = "info"
    credentials_file = (
        "/home/chris/code/affinitypropagation/flash-realm-401106-a0bf29a37df7.json"
    )

    df = pd.read_csv(
        "/home/chris/code/affinitypropagation/data/history_merged_reduced.csv"
    )

    df["timestamp"] = pd.Timestamp.now()

    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=["https://www.googleapis.com/auth/bigquery"]
    )

    destination_table = f"{project_id}.{dataset_id}.{table_id}"

    to_gbq(
        df,
        destination_table,
        project_id=project_id,
        if_exists="replace",  # Choose whether to replace or append to the table
        credentials=credentials,  # Specify the schema for the table
    )

    print(f"DataFrame uploaded to {destination_table} in BigQuery.")
    return df


@asset
def quotes_update():
    data = pd.read_csv(
        "/home/chris/code/affinitypropagation/data/Yahoo Ticker Symbols - September 2017.csv"
    )
    tickers = list(data["Yahoo Stock Tickers"].dropna().iloc[2:].values)[0:10]

    dfs = {}

    for symbol in tqdm.tqdm(
        tickers,
        ncols=100,
        desc="Progress merge: ",
        colour="#00d111",
    ):
        try:
            ticker = yf.Ticker(symbol)
            info_dict = ticker.history(period="1mo")
            df = pd.DataFrame.from_dict(info_dict, orient="columns")
            df["symbol"] = str(ticker).strip("yfinance.Ticker object <").strip(">")
            dfs[ticker] = df
        except:
            continue

    dfs = dfs.values()
    box_score_advanced_df = pd.concat(dfs, axis=0).reset_index()
    box_score_advanced_df["timestamp"] = pd.Timestamp.now()
    box_score_advanced_df.columns = [
        x.replace(" ", "_").lower() for x in box_score_advanced_df.columns
    ]

    project_id = "flash-realm-401106"
    dataset_id = "valuationhub"
    table_id = "test"
    credentials_file = "flash-realm-401106-a0bf29a37df7.json"

    df = box_score_advanced_df

    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=["https://www.googleapis.com/auth/bigquery"]
    )

    destination_table = f"{project_id}.{dataset_id}.{table_id}"

    to_gbq(
        df,
        destination_table,
        project_id=project_id,
        if_exists="replace",  # Choose whether to replace or append to the table
        credentials=credentials,
    )
    return box_score_advanced_df
