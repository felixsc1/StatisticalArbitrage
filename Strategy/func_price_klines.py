"""
reminder:
interval: 60, "D"
from: integer from timestamp in seconds
limit: max size of 200
"""

from config_strategy_api import session
from config_strategy_api import timeframe
from config_strategy_api import kline_limit
import datetime
import time

# Get start times
time_start_date = 0
if timeframe == 60:
    time_start_date = datetime.datetime.now() - datetime.timedelta(hours=kline_limit)
if timeframe == "D":
    time_start_date = datetime.datetime.now() - datetime.timedelta(days=kline_limit)
time_start_seconds = int(time_start_date.timestamp())
# print(time_start_seconds)


# Get historical prices (klines = candles)
def get_price_klines(symbol):
    # Get Prices
    # required arguments are explained here: https://bybit-exchange.github.io/docs/linear/#t-markpricekline
    # Idea: to circumvent 200 datapoint limit, make 2 calls with different from_time, then concatenate them.
    prices = session.query_mark_price_kline(
        symbol=symbol,
        interval=timeframe,
        limit=kline_limit,
        from_time=time_start_seconds
    )

    # Manage API call limit
    time.sleep(0.1)

    # if there is not 200 datapoints, exclude it (may throw off statistical calculations)
    if len(prices["result"]) != kline_limit:
        return []

    return prices["result"]
