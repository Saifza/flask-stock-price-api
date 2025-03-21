import yfinance as yf
import pandas as pd
import os
from fredapi import Fred

# Replace this with your actual FRED API Key
FRED_API_KEY = "ec5bbcdd3f0283d322dfd41371e05e95"
fred = Fred(api_key=FRED_API_KEY)

# Function to fetch stock data
def fetch_stock_data(ticker, start_date="2020-01-01", end_date="2025-01-01"):
    """
    Fetch historical stock data from Yahoo Finance.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL" for Apple).
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        pd.DataFrame: DataFrame containing stock data.
    """
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)

    if df.empty:
        print(f"Error: No data found for {ticker}. Check the ticker symbol.")
        return None

    df.index = df.index.tz_localize(None)  # 🛠 FIX: Remove timezone info
    return df

# Function to fetch economic indicators
def fetch_economic_data(start_date="2020-01-01", end_date="2025-01-01"):
    """
    Fetch economic indicators from FRED.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        pd.DataFrame: DataFrame containing economic indicators.
    """
    indicators = {
        "Interest Rate": "FEDFUNDS",
        "Inflation Rate": "CPIAUCSL",
        "GDP Growth": "GDPC1",
        "Unemployment Rate": "UNRATE"
    }

    econ_data = {}

    for name, fred_id in indicators.items():
        data = fred.get_series(fred_id, start_date, end_date)
        econ_data[name] = data

    df_econ = pd.DataFrame(econ_data)
    df_econ.index = pd.to_datetime(df_econ.index)
    df_econ = df_econ.resample("ME").mean()  

    return df_econ

# Function to merge stock and economic data
def merge_stock_economic_data(ticker):
    """
    Merge stock data with economic indicators.

    Args:
        ticker (str): Stock ticker symbol.

    Returns:
        pd.DataFrame: Merged DataFrame.
    """
    stock_df = fetch_stock_data(ticker)
    econ_df = fetch_economic_data()

    if stock_df is None or econ_df is None:
        print("Error: Data could not be fetched.")
        return None

    # Merge data on Date
    stock_df.index = pd.to_datetime(stock_df.index)
    merged_df = stock_df.merge(econ_df, left_index=True, right_index=True, how="left")

    # Save the merged dataset
   # output_path = os.path.join("..", "data", "processed", f"{ticker}_merged.csv")
    output_dir = "../stock_prediction_project/data/processed"
    output_path = os.path.abspath(os.path.join(output_dir, "merged_data.csv"))

    os.makedirs(output_dir, exist_ok=True)

    merged_df.to_csv(output_path)
    print(f"Merged data saved to {output_path}")

    return merged_df

# Example usage
if __name__ == "__main__":
    ticker = "AAPL"
    merged_data = merge_stock_economic_data(ticker)
    print(merged_data.head())  # Print first few rows
