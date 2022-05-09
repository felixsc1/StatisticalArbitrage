# Functions to check for any open orders and positions, retrieve details about them.

from requests import session
from config_execution_api import session_private


def open_position_confirmation(ticker):
    # Check for any open positions
    try:
        # https://bybit-exchange.github.io/docs/inverse/#t-position
        position = session_private.my_position(symbol=ticker)
        # print(position)
        if position["ret_msg"] == "OK":
            for item in position["result"]:
                if item["size"] > 0:
                    return True  # for any position whether buy or sell.
    except:
        print("exception when checking open position")
        # for safety, if there is any problem we assume that there is an open position.
        # since then the bot won't open a new one.
        return True
    return False


def active_order_confirmation(ticker):
    # Check for any active orders, just a binary result.
    try:
        # https://bybit-exchange.github.io/docs/inverse/#t-getactive
        # https://bybit-exchange.github.io/docs/inverse/#order-status-order_status
        active_order = session_private.get_active_order(
            symbol=ticker,
            order_status="Created,New,PartiallyFilled,Active"
        )
        if active_order["ret_msg"] == "OK":
            # print("data:", active_order["result"]["data"])
            if active_order["result"]["data"] != None:
                return True
    except:
        print("exception when checking active order")
        return True
    return False


def get_open_position(ticker, direction="Long"):
    # To get more detailed infos, amount and price

    position = session_private.my_position(symbol=ticker)
    # As shown in the docs https://bybit-exchange.github.io/docs/linear/#t-myposition
    # index 0 of result array is "Buy", index 1 is "Sell"
    index = 0 if direction == "Long" else 1

    if "ret_msg" in position.keys():
        if position["ret_msg"] == "OK":
            if "symbol" in position["result"][index].keys():
                order_price = position["result"][index]["entry_price"]
                order_quantity = position["result"][index]["size"]
                return order_price, order_quantity
            return (0, 0)
    return(0, 0)


def get_active_order(ticker):
    # same as above but for active orders
    # https://bybit-exchange.github.io/docs/linear/#t-getactive
    active_order = session_private.get_active_order(
        symbol=ticker,
        order_status="Created,New,PartiallyFilled,Active"
    )
    if "ret_msg" in active_order.keys():
        if active_order["ret_msg"] == "OK":
            if active_order["result"]["data"] != None:
                order_price = active_order["result"]["data"][0]["price"]
                order_quantity = active_order["result"]["data"][0]["qty"]
                return order_price, order_quantity
            return (0, 0)
    return(0, 0)


def query_existing_order(ticker, order_id):

    # https://bybit-exchange.github.io/docs/linear/#t-queryactive
    order = session_private.query_active_order(
        symbol=ticker, order_id=order_id)

    # Construct response
    if "ret_msg" in order.keys():
        if order["ret_msg"] == "OK":
            order_price = order["result"]["price"]
            order_quantity = order["result"]["qty"]
            order_status = order["result"]["order_status"]
            return order_price, order_quantity, order_status
    return (0, 0, 0)
