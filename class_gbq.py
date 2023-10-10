from google.cloud import bigquery
import pandas as pd

project_id = "flash-realm-401106"
dataset_id = "valuationhub"


def info_data():
    service_account_json = "flash-realm-401106-a0bf29a37df7.json"
    client = bigquery.Client.from_service_account_json(service_account_json)

    query = """
    WITH ranked_data AS (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp DESC) AS row_num
        FROM flash-realm-401106.valuationhub.h_info
    )
    SELECT *
    FROM ranked_data
    WHERE row_num = 1
    """
    df = client.query(query).to_dataframe()
    return df


tickers = ["AAPL"]


def historical_data(tickers: list) -> pd.DataFrame:
    """Download historical data of selected peer group."""
    service_account_json = "flash-realm-401106-a0bf29a37df7.json"
    client = bigquery.Client.from_service_account_json(service_account_json)

    query = """
    WITH ranked_data AS (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY symbol, date ORDER BY timestamp DESC) AS row_num
        FROM flash-realm-401106.valuationhub.h_quotes
    )
    SELECT *
    FROM ranked_data
    WHERE row_num = 1 AND
    symbol in UNNEST(@tickers)
    """

    # Define query parameters
    query_params = [bigquery.ArrayQueryParameter("tickers", "STRING", tickers)]

    # Run the query with parameters
    job_config = bigquery.QueryJobConfig(query_parameters=query_params)
    query_job = client.query(query, job_config=job_config)
    df = query_job.to_dataframe()
    return df


if __name__ == "__main__":
    historical_data(tickers)
