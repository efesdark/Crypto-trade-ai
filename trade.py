# trade_testnet.py
def place_order(symbol, quantity, buy=True):
    side = 'BUY' if buy else 'SELL'
    order = client.create_order(
        symbol=symbol,
        side=side,
        type='MARKET',
        quantity=quantity
    )
    return order

# Örnek alım (BUY)
symbol = 'BTCUSDT'
quantity = 0.001  # Alınacak BTC miktarı
print(place_order(symbol, quantity, buy=True))

# Örnek satış (SELL)
print(place_order(symbol, quantity, buy=False))
