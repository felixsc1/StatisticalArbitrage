from numpy import place
from config_execution_api import session_private
from config_execution_api import session_public
from config_execution_api import limit_order_basis
from func_calculations import get_trade_details


def set_leverage(ticker):
    # Set leverage to 1
    # see https://bybit-exchange.github.io/docs/linear/#t-marginswitch
    # bad practice to use try except here...
    try:
        leverage_set = session_private.cross_isolated_margin_switch(
            symbol=ticker,
            is_isolated=True,
            buy_leverage=1,
            sell_leverage=1
        )
    except Exception as e:
        pass
    return


def place_order(ticker, price, quantity, direction, stop_loss):

    # Set variables
    if direction == "Long":
        side = "Buy"
    elif direction == "Short":
        side = "Sell"

    # Place limit order
    if limit_order_basis:
        order = session_private.place_active_order(
            symbol=ticker,
            side=side,
            order_type="Limit",
            qty=quantity,
            price=price,
            time_in_force="PostOnly",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss=stop_loss
        )
    else:
        order = session_private.place_active_order(
            symbol=ticker,
            side=side,
            order_type="Market",
            qty=quantity,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False,
            stop_loss=stop_loss
        )

    return order


def initialize_order_execution(ticker, direction, capital):
    orderbook = session_public.orderbook(symbol=ticker)
    mid_price, stop_loss, quantity = get_trade_details(
        orderbook["result"], direction, capital)
    order = place_order(ticker, mid_price, quantity, direction, stop_loss)
    # for an example order response: https://bybit-exchange.github.io/docs/inverse/#t-placeactive
    # print(order)
    if "result" in order.keys():
        if "order_id" in order["result"]:
            return order["result"]["order_id"]
    return 0


# test:
# initialize_order_execution("MATICUSDT", "Short", 500)
