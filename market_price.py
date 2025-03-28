from api import client  # api.py dosyasından client'ı al
def get_price(symbol):
    price = client.get_symbol_ticker(symbol=symbol)
    return price['price']
    
symbol = 'BTCUSDT'  # BTC/USDT paritesi
print(get_price(symbol))