import pandas as pd
import numpy as np
import talib
from binance.client import Client
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# .env dosyasını yükle
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Binance Client'ı başlat
client = Client(api_key, api_secret, testnet=True)

# Geçmiş verileri al (Son 500 mum verisi)
def get_historical_data(symbol="BTCUSDT", interval="1h", limit=500):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                       'close_time', 'quote_asset_volume', 'num_trades', 
                                       'taker_buy_base', 'taker_buy_quote', 'ignore'])
    df['close'] = df['close'].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df[['timestamp', 'close']]

# RSI & SMA ile sinyaller üret
def generate_signals(df):
    df['RSI'] = talib.RSI(df['close'], timeperiod=14)
    df['SMA'] = talib.SMA(df['close'], timeperiod=50)

    df['Buy'] = (df['RSI'] < 30) & (df['close'] > df['SMA'])  # RSI düşük ve fiyat SMA'dan yukarı çıkınca al
    df['Sell'] = (df['RSI'] > 70) & (df['close'] < df['SMA']) # RSI yüksek ve fiyat SMA'nın altına düşerse sat

    return df

# Backtest (Al-Sat işlemleri)
def backtest(df, initial_balance=10000):
    balance = initial_balance
    btc = 0
    last_buy_price = 0

    for index, row in df.iterrows():
        if row['Buy']:
            if balance > 0:
                btc = balance / row['close']
                last_buy_price = row['close']
                balance = 0
                print(f"BUY at {row['close']} on {row['timestamp']}")
        
        elif row['Sell']:
            if btc > 0:
                balance = btc * row['close']
                btc = 0
                print(f"SELL at {row['close']} on {row['timestamp']} - Profit: {row['close'] - last_buy_price}")

    final_balance = balance + (btc * df.iloc[-1]['close'])
    print(f"\nFinal Balance: ${final_balance:.2f}")
    return final_balance

# Grafikleri çizdir
def plot_signals(df):
    plt.figure(figsize=(12,6))
    plt.plot(df['timestamp'], df['close'], label="Close Price", color='blue', alpha=0.6)
    plt.scatter(df[df['Buy']]['timestamp'], df[df['Buy']]['close'], marker="^", color='green', label="Buy Signal", alpha=1)
    plt.scatter(df[df['Sell']]['timestamp'], df[df['Sell']]['close'], marker="v", color='red', label="Sell Signal", alpha=1)
    plt.legend()
    plt.title("BTCUSDT Trading Signals")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid()
    plt.show()

# Ana çalışma fonksiyonu
if __name__ == "__main__":
    df = get_historical_data()
    df = generate_signals(df)
    final_balance = backtest(df)
    plot_signals(df)
