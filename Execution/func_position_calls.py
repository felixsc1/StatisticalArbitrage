from config_execution_api import session_private


def open_position_confirmation(ticker):
    # Check for any open positions
    try:
        # https://bybit-exchange.github.io/docs/inverse/#t-position
        position = session_private.my_position(symbol=ticker)
        if position["ret_msg"] == "OK":
            for item in position["size"] > 0:
                return True  # for any position wheter buy or sell.
    except:
        # for safety, if there is any problem we assume that there is an open position.
        # since then the bot won't open a new one.
        return True
    return False


def active_order_confirmation(ticker):
    # Check for any active orders
    try:
        # https://bybit-exchange.github.io/docs/inverse/#t-getactive
        # https://bybit-exchange.github.io/docs/inverse/#order-status-order_status
        active_order = session_private.get_active_order(
            symbol=ticker,
            order_status="Created,New,PartiallyFilled,Active"
        )
        if active_order["ret_msg"] == "OK":
            print("data:", active_order["result"]["data"])
            if active_order["result"]["data"] != None:
                return True
    except:
        print("exception")
        return True
    return False
