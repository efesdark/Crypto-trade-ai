# trade_testnet.py
from api import client  # api.py dosyasından client'ı al
def place_order(symbol, quantity, buy=True):
    side = 'BUY' if buy else 'SELL'
    order = client.create_order(
        symbol=symbol,
        side=side,
        type='MARKET',
        quantity=quantity
    )
    return order

# Örnek alım (BUY) işlemi
symbol = 'BTCUSDT'
quantity = 0.001  # 0.001 BTC al
print(place_order(symbol, quantity, buy=True))

# Örnek satış (SELL) işlemi
print(place_order(symbol, quantity, buy=False))

