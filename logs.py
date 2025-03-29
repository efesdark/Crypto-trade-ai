# logs.py
import logging
#from binance.client import Client
#from dotenv import load_dotenv
#import os

#load_dotenv()
#API_KEY = os.getenv("BINANCE_API_KEY")
#API_SECRET = os.getenv("BINANCE_API_SECRET")
# Binance API key ve secret'ı .env dosyasından alıyoruz
from api import client 

logging.basicConfig(filename="trade_logs.txt", level=logging.INFO)
#client = Client(API_KEY, API_SECRET, testnet=True)

def log_balance():
    account = client.get_account()
    balances = account['balances']
    
    for balance in balances:
        asset = balance['asset']
        free = float(balance['free'])
        locked = float(balance['locked'])
        if asset in ['BTC', 'USDT']:
            logging.info(f"Asset: {asset}, Free: {free}, Locked: {locked}")

def log_trade(symbol, action, quantity, price, order_id):
    logging.info(f"{action.capitalize()} {quantity} {symbol} at {price} (Order ID: {order_id})")

def log_trade_history():
    # Bu fonksiyon burada basit bir tarihçe loglaması yapabilir, örneğin;
    orders = client.get_all_orders(symbol="BTCUSDT")
    for order in orders:
        logging.info(f"Order ID: {order['orderId']}, Status: {order['status']}, Price: {order['price']}")
