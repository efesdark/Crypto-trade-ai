# main.py

from market_price import moving_average, rsi, macd
from trade import generate_trade_signal, execute_trade
import pandas as pd

# Example: Fetch market data (Assuming you have already fetched data as df)
# df = fetch_data_from_binance()

# Calculate moving averages, RSI, and MACD
df['short_ma'] = moving_average(df, 50)  # 50-period short MA
df['long_ma'] = moving_average(df, 200)  # 200-period long MA
df['rsi'] = rsi(df)  # 14-period RSI
df = macd(df)  # MACD calculation

# Generate buy/sell signals
df = generate_trade_signal(df)

# Example: Execute trade if there's a buy/sell signal
symbol = "BTCUSDT"  # Define your trading pair
if df['buy_signal'].iloc[-1]:
    print("Buying!")
    execute_trade(symbol, "buy", 0.01)  # Example: Buy 0.01 BTC
elif df['sell_signal'].iloc[-1]:
    print("Selling!")
    execute_trade(symbol, "sell", 0.01)  # Example: Sell 0.01 BTC
