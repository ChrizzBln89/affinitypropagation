from modules.pages.class_peer_group import Peer_Group
import pandas as pd


peer_group_user = Peer_Group()

column_mapping = {
    "country": "Country",
    "website": "Website",
    "longBusinessSummary": "Long Business Summary",
    "fullTimeEmployees": "Full Time Employees",
    "beta": "Beta",
    "volume": "Volume",
    "regularMarketVolume": "Regular Market Volume",
    "averageVolume": "Average Volume",
    "trailingAnnualDividendRate": "Trailing Annual Dividend Rate %",
    "trailingAnnualDividendYield": "Trailing Annual Dividend Yield %",
    "currency": "Currency",
    "enterpriseValue": "Enterprise Value",
    "profitMargins": "Profit Margins %",
    "floatShares": "Float Shares",
    "bookValue": "Book Value",
    "priceToBook": "Price To Book",
    "enterpriseToRevenue": "Enterprise To Revenue",
    "enterpriseToEbitda": "Enterprise To EBITDA",
    "exchange": "Exchange",
    "quoteType": "Quote Type",
    "symbol": "Symbol",
    "longName": "Long Name",
    "totalCash": "Total Cash",
    "totalCashPerShare": "Total Cash Per Share",
    "ebitda": "EBITDA",
    "totalDebt": "Total Debt",
    "quickRatio": "Quick Ratio %",
    "currentRatio": "Current Ratio %",
    "totalRevenue": "Total Revenue",
    "debtToEquity": "Debt to Equity",
    "revenuePerShare": "Revenue Per Share",
    "returnOnAssets": "Return On Assets %",
    "returnOnEquity": "Return On Equity %",
    "grossProfits": "Gross Profits",
    "freeCashflow": "Free Cash Flow",
    "operatingCashflow": "Operating Cashflow",
    "earningsGrowth": "Earnings Growth %",
    "revenueGrowth": "Revenue Growth %",
    "grossMargins": "Gross Margins %",
    "ebitdaMargins": "EBITDA Margins %",
    "operatingMargins": "Operating Margins %",
    "financialCurrency": "Financial Currency",
    "trailingPegRatio": "Trailing Peg Ratio %",
    "trailingPE": "Trailing PE",
    "marketCap": "Market Cap",
    "priceToSalesTrailing12Months": "Price To Sales Trailing 12 Months",
    "sharesOutstanding": "Shares Outstanding",
    "trailingEps": "Trailing Earnings Per Share",
    "industry": "Industry",
    "sector": "Sector",
    "dividendRate": "Dividend Rate %",
    "dividendYield": "Dividend Yield %",
    "payoutRatio": "Payout Ratio %",
    "fiveYearAvgDividendYield": "Five-Year Avg Dividend Yield",
    "forwardPE": "Forward PE",
    "forwardEps": "Forward Earnings Per Share",
    "pegRatio": "PEG Ratio",
    "targetHighPrice": "Target High Price",
    "targetLowPrice": "Target Low Price",
    "targetMeanPrice": "Target Mean Price",
    "targetMedianPrice": "Target Median Price",
}

company_index_df = pd.DataFrame(
    {
        "Ticker": [
            "BMW.DE",
            "PAH3.DE",
            "RNO.PA",
            "F",
            "GM",
            "HMC",
            "TM",
        ],
        "Index": [
            "^STOXX50E",
            "^STOXX50E",
            "^STOXX50E",
            "^STOXX50E",
            "^STOXX50E",
            "^STOXX50E",
            "^STOXX50E",
        ],
    }
)

peer_group_user.peer_companies = company_index_df["Ticker"].tolist()
peer_group_user.index = dict(zip(company_index_df["Ticker"], company_index_df["Index"]))
peer_group_user.info_data = peer_group_user.info_data[column_mapping.keys()]
peer_group_user.info_data.rename(columns=column_mapping, inplace=True)
