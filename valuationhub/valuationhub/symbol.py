import pandas as pd


def get_symbols():
    data = pd.read_csv(
        "/home/chris/code/affinitypropagation/data/Yahoo Ticker Symbols - September 2017.csv"
    )
    tickers = list(data["Yahoo Stock Tickers"].dropna().iloc[2:].values)[0:10]
    return tickers
