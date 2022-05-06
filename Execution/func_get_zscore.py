from func_calculations import get_trade_details
from func_price_calls import get_latest_klines
from func_stats import calculate_metrics
from config_execution_api import session_public, ticker_1, ticker_2


def get_latest_zscore():

    # get latest orderbook prices
    orderbook_1 = session_public.orderbook(symbol=ticker_1)
    orderbook_2 = session_public.orderbook(symbol=ticker_2)
    mid_price_1, _, _, = get_trade_details(orderbook_1["result"])
    mid_price_2, _, _, = get_trade_details(orderbook_2["result"])

    # get latest price history
    series_1, series_2 = get_latest_klines()

    # get z_score and confirm signal
    if len(series_1) > 0 and len(series_2) > 0:

        # Replace last kline price with latest orderbook mid price
        # I assume because this is more recent than the kline price (which is some average over older time periods)
        series_1 = series_1[:-1]
        series_2 = series_2[:-1]
        series_1.append(mid_price_1)
        series_2.append(mid_price_2)

        # Get latest zscore
        # optional: could also add coint_flag as requirement
        _, zscore_list = calculate_metrics(series_1, series_2)
        zscore = zscore_list[-1]
        if zscore > 0:
            signal_sign_positive = True
        else:
            signal_sign_positive = False

        # Return output
        return (zscore, signal_sign_positive)
    return
