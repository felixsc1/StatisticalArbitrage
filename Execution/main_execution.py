# Main file to run the statistical arbitrage bot.

from config_execution_api import signal_positive_ticker, signal_negative_ticker
from func_position_calls import open_position_confirmation, active_order_confirmation
from func_trade_management import manage_new_trades
from func_execution_calls import set_leverage
from func_close_positions import close_all_positions
import time
from func_save_status import save_status
from func_get_zscore import get_latest_zscore

""" RUN STATBOT """
if __name__ == "__main__":

    print("AutiBot initiated...")

    # initialize variables
    status_dict = {"message": "starting..."}
    order_long = {}
    order_short = {}
    signal_sign_positive = False
    signal_side = ""
    kill_switch = 0  # 0 = place trades, 1 = manage placed trades, 2 = close positions

    save_status(status_dict)

    # ensure that leverage is set to 1 for each trading pair
    set_leverage(signal_positive_ticker)
    set_leverage(signal_negative_ticker)

    # Commence bot
    print("Seeking trades...")
    while True:

        # pause to limit API calls
        time.sleep(3)

        # Check if any open trades already exist
        is_p_ticker_open = open_position_confirmation(signal_positive_ticker)
        is_n_ticker_open = open_position_confirmation(signal_negative_ticker)
        is_p_ticker_active = active_order_confirmation(signal_positive_ticker)
        is_n_ticker_active = active_order_confirmation(signal_negative_ticker)
        checks_all = [is_p_ticker_open, is_n_ticker_open,
                      is_p_ticker_active, is_n_ticker_active]
        # all of these have to be False in order to start new trades
        is_manage_new_trades = not any(checks_all)

        # Save status
        status_dict["message"] = "Initial checks made..."
        status_dict["checks"] = checks_all
        save_status(status_dict)

        # Check for signal and place new trades
        if is_manage_new_trades and kill_switch == 0:
            status_dict["message"] = "Managing new trades..."
            save_status(status_dict)
            kill_switch, signal_side = manage_new_trades(kill_switch)

        # Manage closing positions
        if kill_switch == 1:

            zscore, signal_sign_positive = get_latest_zscore()
            # If mean reversion happened -> close trades (kill_switch = 2)
            if signal_side == "positive" and zscore < 0:
                kill_switch = 2
            if signal_side == "negative" and zscore >= 0:
                kill_switch = 2

            # return kill_switch to zero once positions closed.
            # (is done anyways in the function close_all_positions())
            if is_manage_new_trades and kill_switch != 2:
                kill_switch = 0

        # Close all active orders and positions
        if kill_switch == 2:
            print("Closing all positions...")
            status_dict["message"] = "Closing existing trades..."
            save_status(status_dict)
            kill_switch = close_all_positions(kill_switch)
            time.sleep(5)  # before starting over
