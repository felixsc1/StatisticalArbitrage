"""
API Documentation: https://bybit-exchange.github.io/docs/linear/#t-introduction
bybit module: https://github.com/bybit-exchange/pybit
"""

# API Imports
from pybit.usdt_perpetual import HTTP
from dotenv import load_dotenv
import os

load_dotenv()

# CONFIG VARIABLES
mode = "test"
# For development try "BTCUSDT" and "ETHUSDT" most transactions happening there
# --------------------
ticker_1 = "KDAUSDT"
ticker_2 = "GMTUSDT"


signal_positive_ticker = ticker_2
# -> when z-score is positive, go long on ticker_2 and vice versa.
signal_negative_ticker = ticker_1

# to find out rounding/decimals of each ticker, check the chart on testnet.bybit.com
# e.g. MATICUSDT has 4 decimals, STXUSDT has 3,  quantity is an integer for matic, one decimal for stx.
# Todo: make bot figure these out automatically.
rounding_ticker_1 = 3
rounding_ticker_2 = 4
quantity_rounding_ticker_1 = 1
quantity_rounding_ticker_2 = 0
# --------------------

# ensure positions (except for close) are placed on limit basis
limit_order_basis = True

# tradeable capital split between two pairs, 2000 meaning 1000 for each pair.
tradeable_capital_usdt = 1000
# fail safe in case of drastic events.
stop_loss_fail_safe = 0.15
# z-score threshold (must be above zero)
signal_trigger_threshold = 1.1

# make sure the following settings match those under strategy!
timeframe = 30  # minutes
kline_limit = 200
z_score_window = 21


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
ws_public_url = "wss://stream-testnet.bybit.com/realtime_public" if mode == "test" else "wss://stream.bybit.com/realtime_public"

# SESSION Activation
session_public = HTTP(api_url)  # market data
session_private = HTTP(api_url, api_key=api_key,
                       api_secret=api_secret)  # my account data
