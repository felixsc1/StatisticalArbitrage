from config_execution_api import signal_positive_ticker
from config_execution_api import signal_negative_ticker
from config_execution_api import session_private


def get_position_info(ticker):
    # Get position information (see https://bybit-exchange.github.io/docs/linear/#t-myposition)
    # ticker argument is e.g. "MATICUSDT"

    # Declare output variables
    side = ""
    size = 0

    position = session_private.my_position(symbol=ticker)
    if "ret_msg" in position.keys():
        if position["ret_msg"] == "OK":
            # expect two elements, Buy and Sell:
            if len(position["result"]) == 2:
                if position["result"][0]["size"] > 0:
                    size = position["result"][0]["size"]
                    side = "Buy"
                else:
                    size = position["result"][1]["size"]
                    side = "Sell"

    # Return output
    return side, size


# to test: buy some asset on the website with my account.
# side, size = get_position_info("MATICUSDT")
# print(side, size)


def place_market_close_order(ticker, side, size):
    """
    Closing positions
    For simplicity here we close them as market orders (not limit order) that get filled immediately.

    For explanation of arguments see:
    https://bybit-exchange.github.io/docs/linear/#t-placeactive

    The way it works is by placing an order on the opposite side.
    e.g. placing a buy order cancels out an open buy order. No need to provide order ID then.
    reduce_only=True ensures that the current position can only decrease, it cant add a new order.
    """

    session_private.place_active_order(
        symbol=ticker,
        side=side,
        order_type="Market",
        qty=size,
        time_in_force="GoodTillCancel",
        reduce_only=True,
        close_on_trigger=False
    )

    return


def close_all_positions(kill_switch):
    """
    Here we want to close both the unfilled limit orders and our filled positions.
    active orders can be cancelled with built-in pybit session.cancel_all_active_orders()
    to close our positions we have our custom function above.
    """
    # Close all positions for both tickers
    session_private.cancel_all_active_orders(symbol=signal_positive_ticker)
    session_private.cancel_all_active_orders(symbol=signal_negative_ticker)

    # Get position information
    side_1, size_1 = get_position_info(signal_positive_ticker)
    side_2, size_2 = get_position_info(signal_negative_ticker)

    if size_1 > 0:
        # note: side_1 and side_2 are always opposites
        # so if side_1 was Buy, we want to Sell here, i.e. use side_2 as input
        place_market_close_order(signal_positive_ticker, side_2, size_1)

    if size_2 > 0:
        place_market_close_order(signal_negative_ticker, side_1, size_2)

    # Output results:
    kill_switch = 0
    return kill_switch


ks = close_all_positions(1)
print(ks)
