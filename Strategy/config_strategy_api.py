"""
API Documentation: https://bybit-exchange.github.io/docs/linear/#t-introduction
bybit module: https://github.com/bybit-exchange/pybit
"""

# API Imports
from pybit.usdt_perpetual import HTTP
import websocket

# CONFIG
mode = "test"
timeframe = 60  # interval in minutes
kline_limit = 200  # number of historical time points (200 is max size)
z_score_window = 21  # window for moving average

# LIVE API
api_key_mainnet = ""
api_secret_mainnet = ""

# TEST API
api_key_testnet = "O4sXpOwYcs10DqsD3x"
api_secret_testnet = "eg46qxjm4zjIe70cPoQDoXqs91VdQAhMluFX"

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
