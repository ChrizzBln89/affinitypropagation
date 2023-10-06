import pandas as pd
from google.oauth2 import service_account
from pandas_gbq import to_gbq

project_id = "flash-realm-401106"
dataset_id = "valuationhub"
table_id = "history"
credentials_file = "flash-realm-401106-a0bf29a37df7.json"

df = pd.read_csv("data/info_merged_reduced.csv")

# Define the BigQuery schema based on the provided information
schema = [
    {"name": "Peer_Group", "type": "STRING"},
    {"name": "Long_Name", "type": "STRING"},
    {"name": "Exchange", "type": "STRING"},
    {"name": "Quote_Type", "type": "STRING"},
    {"name": "Symbol", "type": "STRING"},
    {"name": "Industry", "type": "STRING"},
    {"name": "Sector", "type": "STRING"},
    {"name": "Currency", "type": "STRING"},
    {"name": "Country", "type": "STRING"},
    {"name": "Website", "type": "STRING"},
    {"name": "Long_Business_Summary", "type": "STRING"},
    {"name": "Full_Time_Employees", "type": "INT64"},
    {"name": "Previous_Close", "type": "FLOAT64"},
    {"name": "Open", "type": "FLOAT64"},
    {"name": "Day_Low", "type": "FLOAT64"},
    {"name": "Day_High", "type": "FLOAT64"},
    {"name": "Regular_Market_Previous_Close", "type": "FLOAT64"},
    {"name": "Regular_Market_Open", "type": "FLOAT64"},
    {"name": "Regular_Market_Day_Low", "type": "FLOAT64"},
    {"name": "Regular_Market_Day_High", "type": "FLOAT64"},
    {"name": "Volume", "type": "INT64"},
    {"name": "Regular_Market_Volume", "type": "INT64"},
    {"name": "Average_Volume", "type": "INT64"},
    {"name": "Average_Volume_10_Days", "type": "INT64"},
    {"name": "Average_Daily_Volume_10_Day", "type": "INT64"},
    {"name": "52_Week_Low", "type": "FLOAT64"},
    {"name": "52_Week_High", "type": "FLOAT64"},
    {"name": "Fifty_Day_Average", "type": "FLOAT64"},
    {"name": "Two_Hundred_Day_Average", "type": "FLOAT64"},
    {"name": "Trailing_Annual_Dividend_Rate", "type": "FLOAT64"},
    {"name": "Trailing_Annual_Dividend_Yield", "type": "FLOAT64"},
    {"name": "Enterprise_Value", "type": "FLOAT64"},
    {"name": "Profit_Margins", "type": "FLOAT64"},
    {"name": "Float_Shares", "type": "INT64"},
    {"name": "Held_Percent_Insiders", "type": "FLOAT64"},
    {"name": "Held_Percent_Institutions", "type": "FLOAT64"},
    {"name": "Book_Value", "type": "FLOAT64"},
    {"name": "Price_To_Book", "type": "FLOAT64"},
    {"name": "Last_Fiscal_Year_End", "type": "INT64"},
    {"name": "Next_Fiscal_Year_End", "type": "INT64"},
    {"name": "Most_Recent_Quarter", "type": "INT64"},
    {"name": "Earnings_Quarterly_Growth", "type": "FLOAT64"},
    {"name": "Net_Income_To_Common", "type": "FLOAT64"},
    {"name": "Enterprise_To_Revenue", "type": "FLOAT64"},
    {"name": "Enterprise_To_Ebitda", "type": "FLOAT64"},
    {"name": "Total_Cash", "type": "FLOAT64"},
    {"name": "Total_Cash_PerShare", "type": "FLOAT64"},
    {"name": "Ebitda", "type": "FLOAT64"},
    {"name": "Total_Debt", "type": "FLOAT64"},
    {"name": "Quick_Ratio", "type": "FLOAT64"},
    {"name": "Current_Ratio", "type": "FLOAT64"},
    {"name": "Total_Revenue", "type": "FLOAT64"},
    {"name": "Debt_To_Equity", "type": "FLOAT64"},
    {"name": "Revenue_Per_Share", "type": "FLOAT64"},
    {"name": "Return_On_Assets", "type": "FLOAT64"},
    {"name": "Return_On_Equity", "type": "FLOAT64"},
    {"name": "Gross_Profits", "type": "FLOAT64"},
    {"name": "Free_Cashflow", "type": "FLOAT64"},
    {"name": "Operating_Cashflow", "type": "FLOAT64"},
    {"name": "Earnings_Growth", "type": "FLOAT64"},
    {"name": "Revenue_Growth", "type": "FLOAT64"},
    {"name": "Gross_Margins", "type": "FLOAT64"},
    {"name": "Ebitda_Margins", "type": "FLOAT64"},
    {"name": "Operating_Margins", "type": "FLOAT64"},
    {"name": "Trailing_Peg_Ratio", "type": "FLOAT64"},
    {"name": "Trailing_PE", "type": "FLOAT64"},
    {"name": "Bid", "type": "FLOAT64"},
    {"name": "Ask", "type": "FLOAT64"},
    {"name": "Bid_Size", "type": "INT64"},
    {"name": "Ask_Size", "type": "INT64"},
    {"name": "Market_Cap", "type": "FLOAT64"},
    {"name": "Price_To_Sales_Trailing_12_Months", "type": "FLOAT64"},
    {"name": "Shares_Outstanding", "type": "FLOAT64"},
    {"name": "Trailing_Eps", "type": "FLOAT64"},
    {"name": "Dividend_Rate", "type": "FLOAT64"},
    {"name": "Dividend_Yield", "type": "FLOAT64"},
    {"name": "Ex_Dividend_Date", "type": "STRING"},
    {"name": "Payout_Ratio", "type": "FLOAT64"},
    {"name": "Five_Year_Avg_Dividend_Yield", "type": "FLOAT64"},
    {"name": "Last_Split_Factor", "type": "STRING"},
    {"name": "Last_Split_Date", "type": "STRING"},
    {"name": "Forward_PE", "type": "FLOAT64"},
    {"name": "Forward_Eps", "type": "FLOAT64"},
    {"name": "Peg_Ratio", "type": "FLOAT64"},
    {"name": "Target_High_Price", "type": "FLOAT64"},
    {"name": "Target_Low_Price", "type": "FLOAT64"},
    {"name": "Target_Mean_Price", "type": "FLOAT64"},
    {"name": "Target_Median_Price", "type": "FLOAT64"},
    {"name": "Recommendation_Mean", "type": "FLOAT64"},
    {"name": "Number_Of_Analyst_Opinions", "type": "INT64"},
    {"name": "Open_Interest", "type": "INT64"},
    {"name": "Industry_Disp", "type": "STRING"},
    {"name": "Sector_Disp", "type": "STRING"},
    {"name": "Implied_Shares_Outstanding", "type": "FLOAT64"},
    {"name": "Fifty_Two_Week_Change", "type": "FLOAT64"},
    {"name": "SandP_52_Week_Change", "type": "FLOAT64"},
    {"name": "Last_Dividend_Value", "type": "FLOAT64"},
    {"name": "Last_Dividend_Date", "type": "STRING"},
    {"name": "Uuid", "type": "STRING"},
    {"name": "Message_Board_Id", "type": "STRING"},
    {"name": "Shares_Short", "type": "INT64"},
    {"name": "Shares_Short_Prior_Month", "type": "INT64"},
    {"name": "Shares_Short_Previous_Month_Date", "type": "STRING"},
    {"name": "Date_Short_Interest", "type": "STRING"},
    {"name": "Shares_Percent_Shares_Out", "type": "FLOAT64"},
]


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
    table_schema=schema,  # Specify the schema for the table
)

print(f"DataFrame uploaded to {destination_table} in BigQuery.")
