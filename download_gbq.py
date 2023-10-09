from google.cloud import bigquery
import pandas as pd


def get_symbols():
    service_account_json = "flash-realm-401106-a0bf29a37df7.json"
    client = bigquery.Client.from_service_account_json(service_account_json)

    query = """
    SELECT DISTINCT(symbol)
    FROM flash-realm-401106.valuationhub.h_info
    """
    df = client.query(query).to_dataframe()
    return df["symbol"].values


if __name__ == "__main__":
    get_symbols()
