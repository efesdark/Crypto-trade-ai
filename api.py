# api.py
from binance.client import Client
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# Testnet API URL'si
testnet_url = os.getenv("BINANCE_TESTNET_URL")

# API anahtarlarını .env dosyasından al
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Binance Testnet client'ını başlat
client = Client(api_key, api_secret, testnet=testnet_url)

# Testnet'teki hesap bakiyesini al
balance = client.get_account()
print(balance)

