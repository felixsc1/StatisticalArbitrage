import pandas as pd
from func_get_symbols import get_tradeable_symbols
from func_prices_json import store_price_history
from func_cointegration import get_cointegrated_pairs
from func_plot_trends import plot_trends
import json


"""STRATEGY CODE"""
if __name__ == "__main__":

    # # STEP 1 - Get list of symbols
    # sym_response = get_tradeable_symbols(rebate=True)

    # # STEP 2 - Construct and save price history
    # if len(sym_response) > 0:
    #     # print(len(sym_response))
    #     store_price_history(sym_response)

    # # STEP 3 - Find cointegrated pairs
    # # note: steps 1-2 don't need to be run every time.
    # print("Calculating cointegration...")
    # with open("1_price_list.json") as json_file:
    #     price_data = json.load(json_file)
    # if len(price_data) > 0:
    #     coint_pairs = get_cointegrated_pairs(price_data)
    # print("Calculation done.")

    # STEP 4 - Plot trends and save for backtesting
    # Inspect the the csv of step 3 and enter two pairs of interest:
    symbol_1 = "KDAUSDT"
    symbol_2 = "GMTUSDT"
    with open("1_price_list.json") as json_file:
        price_data = json.load(json_file)
        if len(price_data) > 0:
            plot_trends(symbol_1, symbol_2, price_data)
