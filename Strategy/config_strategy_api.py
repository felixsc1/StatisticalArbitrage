"""
API Documentation: https://bybit-exchange.github.io/docs/linear/#t-introduction
bybit module: https://github.com/bybit-exchange/pybit
"""

# API Imports
from pybit.usdt_perpetual import HTTP
import websocket
from dotenv import load_dotenv
import os

load_dotenv()

# CONFIG
mode = "test"
timeframe = 30  # interval in minutes
# for availabe intervals, see: https://bybit-exchange.github.io/docs/linear/?python--pybit#tp-sl-mode-tp_sl_mode
kline_limit = 200  # number of historical time points (200 is max size)
z_score_window = 21  # window for moving average

# LIVE API
api_key_mainnet = ""
api_secret_mainnet = ""

# TEST API
api_key_testnet = os.getenv("API_KEY_TESTNET")
api_secret_testnet = os.getenv("API_SECRET_TESTNET")

# SELECTED API
api_key = api_key_mainnet if mode == "production" else api_key_testnet
api_secret = api_secret_mainnet if mode == "production" else api_secret_testnet

# SELECTED URL
api_url = "https://api-testnet.bybit.com" if mode == "test" else "https://api.bybit.com"

# SESSION Activation
session = HTTP(api_url)

# Web Socket Connection
ws = websocket.WebSocketApp(
    url="wss://stream-testnet.bybit.com/realtime_public",
)
# ws.send('{"op":"subscribe","args":["candle.1.BTCUSDT"]}')
