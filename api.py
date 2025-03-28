# api.py
from binance.client import Client
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

# API anahtarlarını .env dosyasından al
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Binance client'ını başlat
client = Client(api_key, api_secret)

# Örnek: Hesap bakiyelerini al
balance = client.get_account()
print(balance)
