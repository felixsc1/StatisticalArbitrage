from func_position_calls import query_existing_order, get_open_position, get_active_order
from func_calculations import get_trade_details
from config_execution_api import session_public


def check_order(ticker, order_id, remaining_capital, direction="Long"):
    """
    calls position query functions, and determines next action.
    Not all data obtained here is used in the example bot, could be included in later versions.
    """

    # Get latest price
    orderbook = session_public.orderbook(symbol=ticker)
    mid_price, _, _ = get_trade_details(orderbook["result"])

    # Get more details
    order_price, order_quantity, order_status = query_existing_order(
        ticker, order_id)

    # Get open position / active orders
    position_price, position_quantity = get_open_position(ticker, direction)
    active_order_price, active_order_quantity = get_active_order(ticker)

    # --- Determine action (note: order of these checks is important!) ---

    # - If trade is complete (capital used up) -> stop placing orders
    if position_quantity >= remaining_capital and position_quantity > 0:
        return "Trade Complete"

    # - If order is filled -> buy more
    if order_status == "Filled":
        return "Position Filled"

    # - If order is still active -> Do nothing
    # optional idea: could check how long it has been active, if too long, cancel and reorder at latest price.
    active_items = ["Created", "New"]
    # Created: order accepted but not yet put through matching engine
    # New: order placed successfully
    if order_status in active_items:
        return "Order Active"

    # - If order is partially filled -> Do nothing
    if order_status == "PartiallyFilled":
        return "Partial Fill"

    # - If order failed -> Try placing it again
    # todo idea: check reason for cancellation. Maybe insufficient funds?
    cancel_items = ["Cancelled", "Rejected", "PendingCancel"]
    if order_status in cancel_items:
        return "Try Again"
