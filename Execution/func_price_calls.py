# Much of the code here is duplicated from the Strategy section.
# Getting historical candle data and calculating z-scores etc. to initiate trades

from config_execution_api import ticker_1
from config_execution_api import ticker_2
from config_execution_api import session_public
from config_execution_api import timeframe
from config_execution_api import kline_limit
from func_calculations import extract_close_prices
import datetime
import time


def get_ticker_trade_liquidity(ticker):
    # To know the average trading size, which we use for placing our orders.
    # see https://bybit-exchange.github.io/docs/linear/#t-publictradingrecords
    # limit = 50 means, taking the last 50 historic trades.
    trades = session_public.public_trading_records(
        symbol=ticker,
        limit=50
    )

    # Calculate average liquidity
    quantity_list = []
    if "result" in trades.keys():
        for trade in trades["result"]:
            quantity_list.append(trade["qty"])

    # Return output
    if len(quantity_list) > 0:
        avg_liquidity = sum(quantity_list) / len(quantity_list)
        res_trades_price = float(
            trades["result"][0]["price"])  # latest trade price
        return (avg_liquidity, res_trades_price)
    return (0, 0)


def get_timestamps():
    """
    Several ways to run the bot. Either something like cronjob to run script e.g. once an hour.
    or run it constantly, buy position and time_start_date, 
    then wait until time_next_date to re-check prices and do something.
    time_next_date is not actually used in the example bot, but calculated here.
    """
    time_start_date = 0
    time_next_date = 0
    now = datetime.datetime.now()
    if timeframe == 60:
        time_start_date = now - datetime.timedelta(hours=kline_limit)
        time_next_date = now + datetime.timedelta(seconds=30)
    if timeframe == "D":
        time_start_date = now - datetime.timedelta(days=kline_limit)
        time_next_date = now + datetime.timedelta(minutes=1)

    else:
        # for arbitrary times in minutes
        time_start_date = now - \
            datetime.timedelta(minutes=(timeframe * kline_limit))
        time_next_date = now + datetime.timedelta(minutes=1)

    time_start_seconds = int(time_start_date.timestamp())
    time_next_seconds = int(time_next_date.timestamp())
    time_now_seconds = int(now.timestamp())
    # print(f"start timestamp: {time_start_seconds}, now:  {time_now_seconds}")
    return (time_start_seconds, time_now_seconds, time_next_seconds)


def get_price_klines(ticker):
    # Get the historical candle data from API
    time_start_seconds, _, _ = get_timestamps()
    # see: https://bybit-exchange.github.io/docs/linear/#t-markpricekline
    prices = session_public.query_mark_price_kline(
        symbol=ticker,
        interval=timeframe,
        limit=kline_limit,
        from_time=time_start_seconds
    )
    time.sleep(0.1)  # limit API calls

    # return price output
    if len(prices["result"]) != kline_limit:
        return[]
    return prices["result"]


def get_latest_klines():
    # Call the previous function and extract the close prices in a list.
    series_1 = []
    series_2 = []
    prices_1 = get_price_klines(ticker_1)
    prices_2 = get_price_klines(ticker_2)
    if len(prices_1) > 0:
        series_1 = extract_close_prices(prices_1)
    if len(prices_2) > 0:
        series_2 = extract_close_prices(prices_2)
    # print(series_1)
    return (series_1, series_2)
