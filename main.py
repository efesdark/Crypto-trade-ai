# main.py
from binance.client import Client


from market_price import fetch_data_from_binance
from market_price import moving_average, rsi, macd
from trade import generate_trade_signal, execute_trade
import pandas as pd

# Binance API key ve secret'ı .env dosyasından alıyoruz
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

client = Client(API_KEY, API_SECRET)


# Example: Fetch market data (Assuming you have already fetched data as df)
# df = fetch_data_from_binance()
# Örnek: BTCUSDT için veri çekme
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1HOUR  # 1 saatlik veriler
lookback = 5  # Son 5 günün verisini al

# Binance'ten veri çekme
df = fetch_data_from_binance(symbol, interval, lookback)

# Calculate moving averages, RSI, and MACD
df['short_ma'] = moving_average(df, 50)  # 50-period short MA
df['long_ma'] = moving_average(df, 200)  # 200-period long MA
df['rsi'] = rsi(df)  # 14-period RSI
df = macd(df)  # MACD calculation

# Generate buy/sell signals
df = generate_trade_signal(df)

# RSI ve ticaret sinyallerini ekleyelim
df['buy_signal'] = (df['rsi'] < 30)  # RSI 30'un altına düştüğünde alım sinyali
df['sell_signal'] = (df['rsi'] > 70)  # RSI 70'in üstüne çıktığında satış sinyali


# Example: Execute trade if there's a buy/sell signal
symbol = "BTCUSDT"  # Define your trading pair
if df['buy_signal'].iloc[-1]:
    print("Buying!")
    execute_trade(symbol, "buy", 0.01)  # Example: Buy 0.01 BTC
elif df['sell_signal'].iloc[-1]:
    print("Selling!")
    execute_trade(symbol, "sell", 0.01)  # Example: Sell 0.01 BTC

# Sonuçları kontrol et
print(df[['timestamp', 'rsi', 'buy_signal', 'sell_signal']].tail())  # Son 5 satırdaki veriyi yazdır