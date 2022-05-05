from config_execution_api import ws_public_url
from config_execution_api import ticker_1
from config_execution_api import ticker_2
from func_calculations import get_trade_details

from pybit.usdt_perpetual import WebSocket
from time import sleep


# see the example here: https://github.com/bybit-exchange/pybit/blob/master/examples/websocket_example.py
ws_public = WebSocket(test=True, domain="bybit")


def handle_orderbook(message):
    # I will be called every time there is new orderbook data!
    # print(message)
    orderbook_data = message["data"]
    get_trade_details(orderbook_data, direction="Long", capital=1000)


def run_ws():

    ws_public.orderbook_25_stream(handle_orderbook, [ticker_1, ticker_2])

    while True:
        # This while loop is required for the program to run. You may execute
        # additional code for your trading logic here.
        sleep(1)


run_ws()
