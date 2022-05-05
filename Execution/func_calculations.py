from config_execution_api import stop_loss_fail_safe
from config_execution_api import ticker_1
from config_execution_api import rounding_ticker_1
from config_execution_api import rounding_ticker_2
from config_execution_api import quantity_rounding_ticker_1
from config_execution_api import quantity_rounding_ticker_2
import math


def extract_close_prices(prices):
    # Put all close prices in a list

    close_prices = []
    for price_values in prices:
        if math.isnan(price_values["close"]):
            return []
        close_prices.append(price_values["close"])
    return close_prices


def get_trade_details(orderbook, direction="Long", capital=0):
    """
    Get trade details and latest prices.
    Gets called from config_ws_connect.py
    See example output for how the orderbook is structured: https://bybit-exchange.github.io/docs/linear/#t-websocketorderbook25

    From that large orderbook dataset we calculate our order price, stop loss price and the quantity we want to order
    """

    # Set calculation output variables
    price_rounding = 20
    quantity_rounding = 20
    mid_price = 0
    quantity = 0
    stop_loss = 0
    bid_items_list = []
    ask_items_list = []

    # Get prices, stop loss and quantity
    if orderbook:
        price_rounding = rounding_ticker_1 if orderbook[0]["symbol"] == ticker_1 else rounding_ticker_2
        quantity_rounding = quantity_rounding_ticker_1 if orderbook[
            0]["symbol"] == ticker_1 else quantity_rounding_ticker_2

        # Organize prices
        for level in orderbook:
            if level["side"] == "Buy":
                bid_items_list.append(float(level["price"]))
            else:
                ask_items_list.append(float(level["price"]))

        # Calculate price, size, stop loss and average liquidity
        if len(ask_items_list) > 0 and len(bid_items_list) > 0:

            # Sort lists in ascending/descending order
            ask_items_list.sort()
            bid_items_list.sort()
            bid_items_list.reverse()  # i.e. get best price as first item

            # Get nearest ask, nearest bid
            nearest_ask = ask_items_list[0]
            nearest_bid = bid_items_list[0]

            # Calculate hard stop loss
            if direction == "Long":
                # mid_price = (nearest_bid + nearest_bid) / 2
                # actual mid price sometimes gets cancelled, so we just place it at bid price...
                mid_price = nearest_bid
                #  stop loss e.g. when it drops to 85%
                stop_loss = round(
                    mid_price * (1 - stop_loss_fail_safe), price_rounding)
            else:
                mid_price = nearest_ask
                stop_loss = round(
                    mid_price * (1 + stop_loss_fail_safe), price_rounding)

            # Calculate quantity
            quantity = round(capital / mid_price, quantity_rounding)

    # Output results
    print(mid_price, stop_loss, quantity)
    return (mid_price, stop_loss, quantity)
