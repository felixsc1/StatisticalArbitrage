"""
API Documentation: https://bybit-exchange.github.io/docs/linear/#t-introduction
bybit module: https://github.com/bybit-exchange/pybit
"""

# API Imports
from pybit.usdt_perpetual import HTTP

# CONFIG VARIABLES
mode = "test"
ticker_1 = "MATICUSDT"
ticker_2 = "STXUSDT"
signal_positive_ticker = ticker_2
# -> when z-score is positive, go long on ticker_2 and vice versa.
signal_negative_ticker = ticker_1

# to find out rounding/decimals of each ticker, check the chart on testnet.bybit.com
# e.g. MATICUSDT has 4 decimals, STXUSDT has 3,  quantity is an integer for matic, one decimal for stx.
# Todo: make bot figure these out automatically.
rounding_ticker_1 = 4
rounding_ticker_2 = 3
quantity_rounding_ticker_1 = 0
quantity_rounding_ticker_2 = 1

# ensure positions (except for close) are placed on limit basis
limit_order_basis = True

# tradeable capital split between two pairs, 2000 meaning 1000 for each pair.
tradeable_capital_usdt = 2000
# fail safe in case of drastic events.
stop_loss_fail_safe = 0.15
# z-score threshold (must be above zero)
signal_trigger_threshold = 1.1

# make sure the following settings match the strategy!
timeframe = 60  # hourly
kline_limit = 200
z_score_window = 21


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
ws_public_url = "wss://stream-testnet.bybit.com/realtime_public" if mode == "test" else "wss://stream.bybit.com/realtime_public"

# SESSION Activation
session_public = HTTP(api_url)  # market data
session_private = HTTP(api_url, api_key=api_key,
                       api_secret=api_secret)  # my account data
