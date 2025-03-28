# trade_testnet.py
from api import client  # api.py dosyasından client'ı al



# Function to generate buy/sell signals based on strategy
def generate_trade_signal(df):
    # Buy Signal: Short MA crosses above Long MA, RSI exits oversold zone, MACD crosses above signal line
    df['buy_signal'] = (df['short_ma'] > df['long_ma']) & (df['rsi'] < 30) & (df['macd'] > df['macd_signal'])
    
    # Sell Signal: Short MA crosses below Long MA, RSI exits overbought zone, MACD crosses below signal line
    df['sell_signal'] = (df['short_ma'] < df['long_ma']) & (df['rsi'] > 70) & (df['macd'] < df['macd_signal'])

    return df

# Function to execute the trade (buy or sell)
def execute_trade(symbol, action, quantity):
    if action == "buy":
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
    elif action == "sell":
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
    
    print(f"Executed {action} order: {order}")

