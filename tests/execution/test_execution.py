from Execution.func_price_calls import get_price_klines
from Execution.func_price_calls import get_ticker_trade_liquidity
from Execution.func_get_zscore import get_latest_zscore
from Execution.func_execution_calls import initialize_order_execution
from Execution.func_position_calls import active_order_confirmation, get_active_order
from Execution.func_close_positions import close_all_positions
import time


def test_price_calls():
    # See if API call returns something
    prices = get_price_klines("MATICUSDT")
    print(prices[0])
    assert prices[0]["symbol"] == "MATICUSDT"


def test_get_latest_klines():
    # test if we get two series of price candle data
    s_1, s_2 = get_latest_klines()
    print(s_1)
    print(s_2)
    assert len(s_1) > 0 and len(s_2) > 0


def test_get_ticker_trade_liquidity():
    # ideally run test with -s flag, and compare if print matches values on bybit website
    avg_liquidity, market_price = get_ticker_trade_liquidity("MATICUSDT")
    print(avg_liquidity, market_price)
    assert avg_liquidity > 0 and market_price > 0


def test_get_latest_zscore():
    zscore, signal_sign_positive = get_latest_zscore()
    print(zscore, signal_sign_positive)
    assert isinstance(zscore, float)
    assert isinstance(signal_sign_positive, bool)


def test_placing_checking_cancelling_orders():
    """
    This will test multiple execution functions.
    WARNING: this test will cancel all positions in the testnet account.
    """
    # 1. place a limit order
    order_id = initialize_order_execution("MATICUSDT", "Long", 10)
    print("order_id:", order_id)
    assert isinstance(order_id, str)
    # sometimes test still fails, because of delays apparently... increase sleep time then.
    time.sleep(15)

    # 2a. Check that order is active
    # test may fail if order gets filled immediately, i.e. is no longer active
    is_active = active_order_confirmation("MATICUSDT")
    assert is_active == True

    # 2b. Get order details
    order_price, order_quantity = get_active_order("MATICUSDT")
    assert order_price > 0
    assert order_quantity == 10

    # 3. Close active orders
    result = close_all_positions(1)
    assert result == 0
    time.sleep(15)

    # 4. Check again that there are no active orders
    is_active = active_order_confirmation("MATICUSDT")
    assert is_active == False
