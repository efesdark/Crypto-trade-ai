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

def get_historical_data(symbol="BTCUSDT", interval="15m",limit=5000):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    print(f"Binance'ten çekilen mum sayısı: {len(klines)}")  # Debugging için eklenmiştir
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                       'close_time', 'quote_asset_volume', 'num_trades', 
                                       'taker_buy_base', 'taker_buy_quote', 'ignore'])
    df['close'] = df['close'].astype(float)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df[['timestamp', 'close']]

def generate_signals(df):
    # Göstergeleri hesapla
    df['RSI'] = talib.RSI(df['close'], timeperiod=14)
    
    df['SMA_50'] = talib.SMA(df['close'], timeperiod=50)
    df['SMA_20'] = talib.SMA(df['close'], timeperiod=20)  # Yeni eklenen SMA
    macd, macd_signal, macd_hist = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['MACD'] = macd
    df['MACD_signal'] = macd_signal
    df['MACD_hist'] = macd_hist

    # Sinyal koşullarını optimize et
   #df['Buy'] = (df['RSI'] < 35) & (df['close'] > df['SMA_20']) & (df['MACD_hist'] > 0)
   #df['Sell'] = (df['RSI'] > 65) & (df['close'] < df['SMA_20']) & (df['MACD_hist'] < 0)
      # Daha geniş RSI aralığı ve MACD geçişleri
    df['Buy'] = (df['RSI'] < 40) & (df['close'] > df['SMA_20']) & (df['MACD_hist'] > 0)
    df['Sell'] = (df['RSI'] > 60) & (df['close'] < df['SMA_20']) & (df['MACD_hist'] < 0)
    df.dropna(inplace=True)  # NaN değerleri sil
    return df

def backtest(df, initial_balance=10000):
    balance = initial_balance
    btc = 0
    last_buy_price = 0
    total_profit = 0
    total_trades = 0

    for index, row in df.iterrows():
        if row['Buy'] and balance > 0:
            btc = balance / row['close']
            last_buy_price = row['close']
            balance = 0
            total_trades += 1
            print(f"BUY at {row['close']} on {row['timestamp']}")
        
        elif row['Sell'] and btc > 0:
            balance = btc * row['close']
            profit = balance - (last_buy_price * btc)
            total_profit += profit
            btc = 0
            total_trades += 1
            print(f"SELL at {row['close']} on {row['timestamp']} - Profit: {profit:.2f}")

    final_balance = balance + (btc * df.iloc[-1]['close'])
    print(f"\nFinal Balance: ${final_balance:.2f}")
    print(f"Total Profit: ${total_profit:.2f}")
    print(f"Total Trades: {total_trades}")
    if total_trades > 0:
        print(f"Profit per Trade: ${total_profit / total_trades:.2f}")
    return final_balance

def plot_signals(df):
    plt.figure(figsize=(12,8))
    
    # Fiyat Grafiği
    plt.subplot(3,1,1)
    plt.plot(df['timestamp'], df['close'], label="Price", color='blue')
    plt.plot(df['timestamp'], df['SMA_20'], label="SMA 20", color='orange', alpha=0.7)
    plt.plot(df['timestamp'], df['SMA_50'], label="SMA 50", color='green', alpha=0.7)
    plt.scatter(df[df['Buy']]['timestamp'], df[df['Buy']]['close'], marker="^", color='green', label="Buy", s=100)
    plt.scatter(df[df['Sell']]['timestamp'], df[df['Sell']]['close'], marker="v", color='red', label="Sell", s=100)
    plt.legend()
    plt.title("Price and Signals")
    plt.grid()

    # RSI Grafiği
    plt.subplot(3,1,2)
    plt.plot(df['timestamp'], df['RSI'], label="RSI", color='purple')
    plt.axhline(35, linestyle='--', color='green', alpha=0.5)
    plt.axhline(65, linestyle='--', color='red', alpha=0.5)
    plt.ylim(0, 100)
    plt.legend()
    plt.title("RSI")
    plt.grid()

    # MACD Grafiği
    plt.subplot(3,1,3)
    plt.bar(df['timestamp'], df['MACD_hist'], label="MACD Hist", color=np.where(df['MACD_hist'] > 0, 'green', 'red'))
    plt.plot(df['timestamp'], df['MACD'], label="MACD", color='blue')
    plt.plot(df['timestamp'], df['MACD_signal'], label="Signal", color='orange')
    plt.legend()
    plt.title("MACD")
    plt.grid()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = get_historical_data()
    print(f"İşlenen veri boyutu (NaN'ler silindikten sonra): {len(df)}")
    
    df = generate_signals(df)
    
    # Sinyal sayılarını kontrol et
    print(f"Toplam Alım Sinyali: {df['Buy'].sum()}")
    print(f"Toplam Satım Sinyali: {df['Sell'].sum()}")
    
    final_balance = backtest(df)
    plot_signals(df)