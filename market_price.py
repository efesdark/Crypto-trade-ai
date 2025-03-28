# Import necessary libraries
from binance.client import Client
import pandas as pd

# Function to fetch historical price data
def get_historical_prices(symbol, interval, start_time, end_time):
    """
    Fetch historical price data from Binance.
    
    Parameters:
    symbol (str): The symbol for the trading pair, e.g., 'BTCUSDT'.
    interval (str): The time interval between data points, e.g., '1h', '1d'.
    start_time (str): The start time for the data in timestamp format or ISO format.
    end_time (str): The end time for the data in timestamp format or ISO format.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the historical price data.
    """
    client = Client(api_key="your_api_key", api_secret="your_api_secret")
    klines = client.get_historical_klines(symbol, interval, start_time, end_time)

    # Convert the response into a pandas DataFrame
    data = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
    
    # Convert the timestamp column to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    
    return data

# Example usage
# Fetch historical data for the past 30 days
symbol = "BTCUSDT"
interval = "1d"  # daily interval
start_time = "30 days ago UTC"  # start 30 days ago
end_time = "now"  # until now

historical_data = get_historical_prices(symbol, interval, start_time, end_time)
print(historical_data)

# market_price.py

# Moving Average Calculation
def moving_average(df, period):
    return df['close'].astype(float).rolling(window=period).mean()

# RSI Calculation
def rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# MACD Calculation
def macd(df, fast_period=12, slow_period=26, signal_period=9):
    df['ema_fast'] = df['close'].astype(float).ewm(span=fast_period, adjust=False).mean()
    df['ema_slow'] = df['close'].astype(float).ewm(span=slow_period, adjust=False).mean()
    
    df['macd'] = df['ema_fast'] - df['ema_slow']
    df['macd_signal'] = df['macd'].astype(float).ewm(span=signal_period, adjust=False).mean()
    
    return df
