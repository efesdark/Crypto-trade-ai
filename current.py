import time
import logging
from binance.client import Client
import numpy as np
import talib
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# API anahtarı ve gizli anahtarını .env'den al
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
testnet_url = os.getenv("BINANCE_TESTNET_URL")

# Binance client'ını başlat
client = Client(api_key, api_secret, testnet=True)

# Logger ayarları
logging.basicConfig(filename="trade_logs.txt", level=logging.INFO)

# Anlık fiyatları al
def get_latest_prices(symbol="BTCUSDT", interval="1m", limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    close_prices = [float(kline[4]) for kline in klines]  # 4. index kapanış fiyatıdır
    return close_prices

# RSI hesapla
def calculate_rsi(prices, period=14):
    return talib.RSI(np.array(prices), timeperiod=period)

# Moving Average hesapla
def calculate_moving_average(prices, period=14):
    return talib.SMA(np.array(prices), timeperiod=period)

# MACD hesapla
def calculate_macd(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    macd, macdsignal, macdhist = talib.MACD(np.array(prices), fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
    return macd, macdsignal, macdhist

# Alım/Satım sinyalleri üret
def generate_trade_signal(prices):
    rsi = calculate_rsi(prices)
    sma = calculate_moving_average(prices)
    macd, macdsignal, macdhist = calculate_macd(prices)

    last_rsi = rsi[-1]
    last_sma = sma[-1]
    last_macd = macd[-1]
    last_macdsignal = macdsignal[-1]

    # Ekrana yazdır
    print(f"RSI: {last_rsi:.2f}, SMA: {last_sma:.2f}, MACD: {last_macd:.2f}, Signal: {last_macdsignal:.2f}")
    
    # Sinyal belirleme
    buy_signal = (last_rsi < 30 and last_macd > last_macdsignal and prices[-1] > last_sma)
    sell_signal = (last_rsi > 70 and last_macd < last_macdsignal and prices[-1] < last_sma)

    if buy_signal:
        return "Buy"
    elif sell_signal:
        return "Sell"
    else:
        return "Hold"

# Hesap bakiyesini logla ve ekrana yazdır
def log_balance():
    account = client.get_account()
    balances = account['balances']
    
    for balance in balances:
        asset = balance['asset']
        free = float(balance['free'])
        locked = float(balance['locked'])
        if asset in ['BTC', 'USDT']:
            logging.info(f"Asset: {asset}, Free: {free}, Locked: {locked}")
            print(f"{asset}: Free: {free}, Locked: {locked}")

# Ticaret sinyallerini izleyen fonksiyon
def monitor_market():
    while True:
        print("\n--- Anlık Piyasa Verileri ---")
        prices = get_latest_prices(symbol="BTCUSDT", interval="1m", limit=100)
        signal = generate_trade_signal(prices)
        print(f"Trade Signal from current.py: {signal}")
        logging.info(f"Trade Signal from current.py: {signal}")
        log_balance()
        time.sleep(60)

# Ana fonksiyonu çalıştır
if __name__ == "__main__":
    monitor_market()
