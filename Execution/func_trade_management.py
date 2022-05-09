# High level body of the bot.

from os import kill
from config_execution_api import (
    signal_positive_ticker, signal_negative_ticker, signal_trigger_threshold,
    tradeable_capital_usdt, limit_order_basis, session_private)
from func_price_calls import get_ticker_trade_liquidity
from func_get_zscore import get_latest_zscore
from func_execution_calls import initialize_order_execution
from func_order_review import check_order
import time


def manage_new_trades(kill_switch):

    # Set variables
    order_long_id = ""
    order_short_it = ""
    signal_side = ""
    hot = False

    # Get and save the latest z-score
    zscore, signal_sign_positive = get_latest_zscore()
    print("zscore:", zscore)

    # Switch to hot if signal threshold met
    # Optional: Add coint-flag check too for extra vigilance.
    if abs(zscore) >= signal_trigger_threshold:
        hot = True
        print("-- Trade Status HOT --")
        print("-- Placing and monitoring existing trades --")

    # Place and manage trades
    if hot and kill_switch == 0:

        # Get trades history to determine liquidity
        avg_liquidity_ticker_p, last_price_p = get_ticker_trade_liquidity(
            signal_positive_ticker)
        avg_liquidity_ticker_n, last_price_n = get_ticker_trade_liquidity(
            signal_negative_ticker)

        # Determine which ticker is long and short
        if signal_sign_positive:
            long_ticker = signal_positive_ticker
            short_ticker = signal_negative_ticker
            avg_liquidity_long = avg_liquidity_ticker_p
            avg_liquidity_short = avg_liquidity_ticker_n
            last_price_long = last_price_p
            last_price_short = last_price_n
        else:
            long_ticker = signal_negative_ticker
            short_ticker = signal_positive_ticker
            avg_liquidity_long = avg_liquidity_ticker_n
            avg_liquidity_short = avg_liquidity_ticker_p
            last_price_long = last_price_n
            last_price_short = last_price_p

        # Fill targets
        capital_long = tradeable_capital_usdt / 2
        capital_short = tradeable_capital_usdt - capital_long
        initial_fill_target_long_usdt = avg_liquidity_long * last_price_long
        initial_fill_target_short_usdt = avg_liquidity_short * last_price_short
        # we pick whichever asset has the smaller fill target and use this for both, so that we spend the same amount on long and short
        initial_capital_injection_usdt = min(
            initial_fill_target_long_usdt, initial_fill_target_short_usdt)

        # Ensure initial capital does not exceed limits set in config
        if limit_order_basis:
            if initial_capital_injection_usdt > capital_long:
                initial_capital_usdt = capital_long
            else:
                initial_capital_usdt = initial_capital_injection_usdt
        else:
            # for market orders we don't care about any of the above.
            initial_capital_usdt = capital_long

        # Set remaining capital
        remaining_capital_long = capital_long
        remaining_capital_short = capital_short

        # Trade until filled or signal is false
        order_status_long = ""
        order_status_short = ""
        counts_long = 0
        counts_short = 0
        while kill_switch == 0:

            # Place order - long
            if counts_long == 0:
                order_long_id = initialize_order_execution(
                    long_ticker, "Long", initial_capital_usdt)
                counts_long = 1 if order_long_id else 0
                remaining_capital_long = remaining_capital_long - initial_capital_usdt
                # print(order_long_id)

            # Place order - short
            if counts_short == 0:
                order_short_id = initialize_order_execution(
                    short_ticker, "Short", initial_capital_usdt)
                counts_short = 1 if order_short_id else 0
                remaining_capital_short = remaining_capital_short - initial_capital_usdt
                # print(order_short_id)

            # Update signal side
            if zscore > 0:
                signal_side = "positive"
            else:
                signal_side = "negative"

            # Handle kill switch
            if not limit_order_basis and counts_long and counts_short:
                kill_switch = 1  # will stop placing limit orders

            time.sleep(3)  # Allow time for exchange to register trades

            # Check limit orders and check if zscore still within range
            zscore_new, signal_sign_p_new = get_latest_zscore()
            if kill_switch == 0:
                # give it some room by allowing it to drop to 90% of threshold
                if abs(zscore_new) > signal_trigger_threshold * 0.9 and signal_sign_p_new == signal_sign_positive:

                    # Check long order status
                    if counts_long == 1:
                        order_status_long = check_order(
                            long_ticker, order_long_id, remaining_capital_long, "Long")

                    # Check short order status
                    if counts_short == 1:
                        order_status_short = check_order(
                            short_ticker, order_short_id, remaining_capital_short, "Short")

                    # If orders still active -> do nothing
                    if order_status_long == "Order Active" or order_status_short == "Order Active":
                        continue

                    # If orders partially filled -> do nothing
                    if order_status_long == "Partial Fill" or order_status_short == "Partial Fill":
                        continue

                    # If trade complete (capital used up) -> stop opening trades
                    if order_status_long == "Trade Complete" and order_status_short == "Trade Complete":
                        kill_switch = 1

                    # If positions are filled -> place another trade
                    if order_status_long == "Position Filled" and order_status_short == "Position Filled":
                        counts_long = 0
                        counts_short = 0

                    # If order cancelled for long -> try again
                    if order_status_long == "Try Again":
                        counts_long = 0

                    # If order cancelled for short -> try again
                    if order_status_short == "Try Again":
                        counts_short = 0

                # else if zscore is too low:
                else:
                    # Cancel all active orders
                    session_private.cancel_all_active_orders(
                        symbol=signal_positive_ticker)
                    session_private.cancel_all_active_orders(
                        symbol=signal_negative_ticker)
                    kill_switch = 1

    # Output status
    return kill_switch, signal_side
