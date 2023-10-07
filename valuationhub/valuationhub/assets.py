import pandas as pd
from google.oauth2 import service_account
from pandas_gbq import to_gbq
from dagster import asset


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
