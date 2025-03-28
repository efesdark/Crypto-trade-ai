# api.py dosyasındaki test
from binance.client import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
testnet_url = os.getenv("BINANCE_TESTNET_URL")

# Testnet client'ını başlat
client = Client(api_key, api_secret, testnet=testnet_url)

# Hesap bilgilerini al
balance = client.get_account()
print(balance)
