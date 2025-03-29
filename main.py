# main.py
from binance.client import Client
from logs import log_balance, log_trade, log_trade_history


from market_price import fetch_data_from_binance
from market_price import moving_average, rsi, macd
from trade import generate_trade_signal, execute_trade
import pandas as pd


from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
# Binance API key ve secret'ı .env dosyasından alıyoruz


client = Client(API_KEY, API_SECRET, testnet=True)


# Example: Fetch market data (Assuming you have already fetched data as df)
# df = fetch_data_from_binance()
# Örnek: BTCUSDT için veri çekme
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1HOUR  # 1 saatlik veriler
lookback = 5  # Son 5 günün verisini al

# Binance'ten veri çekme
df = fetch_data_from_binance(symbol, interval, lookback)

# Hesap bakiyesini logla
log_balance()  # Bakiyenizi logluyoruz

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
    order = execute_trade(symbol, "buy", 0.01)  # Ticaret yapıldığında
    if order:  # Eğer işlem başarılıysa
        log_trade(symbol, "buy", 0.01, order['fills'][0]['price'], order['orderId'])  # Alım işlemi kaydedilir
        log_balance()  # Alım sonrası bakiyeyi logla

elif df['sell_signal'].iloc[-1]:
    print("Selling!")
    order = execute_trade(symbol, "sell", 0.01)  # Ticaret yapıldığında
    if order:  # Eğer işlem başarılıysa
        log_trade(symbol, "sell", 0.01, order['fills'][0]['price'], order['orderId'])  # Satış işlemi kaydedilir
        log_balance()  # Satış sonrası bakiyeyi logla

# Sonuçları kontrol et
print(df[['timestamp', 'rsi', 'buy_signal', 'sell_signal']].tail())  # Son 5 satırdaki veriyi yazdır