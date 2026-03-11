import os
import time
import MetaTrader5 as mt5
import pandas as pd
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
LOGIN = int(os.getenv("MT5_LOGIN"))
PASSWORD = os.getenv("MT5_PASSWORD")
SERVER = os.getenv("MT5_SERVER")

def initialize_mt5():
    if not mt5.initialize(login=LOGIN, password=PASSWORD, server=SERVER):
        print(f"Failed to connect to FXPesa: {mt5.last_error()}")
        return False
    print("Connected to FXPesa MT5")
    return True

def get_data(symbol, n_bars=100):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, n_bars)
    return pd.DataFrame(rates)

def simple_ml_logic(df):
    """
    REPLACE THIS: Insert your trained model.predict() here.
    Current: Simple RSI-style logic placeholder.
    """
    last_close = df['close'].iloc[-1]
    prev_close = df['close'].iloc[-2]
    return "BUY" if last_close > prev_close else "SELL"

def execute_trade(symbol, side):
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask if side == "BUY" else mt5.symbol_info_tick(symbol).bid
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.1,
        "type": mt5.ORDER_TYPE_BUY if side == "BUY" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "magic": 999111,
        "comment": "ML Bot Python",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    print(f"Trade {side} result: {result.comment}")

if __name__ == "__main__":
    if initialize_mt5():
        symbol = "EURUSD"
        while True:
            data = get_data(symbol)
            signal = simple_ml_logic(data)
            execute_trade(symbol, signal)
            time.sleep(900) # Wait 15 mins
