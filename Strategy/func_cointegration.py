# !!!!!!
# Make sure before execution, all changes here are also made in ./Execution/func_stats.py

from config_strategy_api import z_score_window
import math
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import pandas as pd
import numpy as np


def calculate_zscore(spread):
    df = pd.DataFrame(spread)
    # take mean/std within each rolling window
    mean = df.rolling(center=False, window=z_score_window).mean()
    std = df.rolling(center=False, window=z_score_window).std()
    x = df.rolling(center=False, window=1).mean()  # latest value
    df["ZSCORE"] = (x - mean) / std
    # put it into a list: [1.1, -1.5, 1.4]
    return df["ZSCORE"].astype(float).values


def calculate_spread(series_1, series_2, hedge_ratio):
    spread = pd.Series(series_1) - (pd.Series(series_2) * hedge_ratio)
    return spread


def calculate_cointegration(series_1, series_2):
    coint_flag = 0
    # See docs: https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.coint.html
    coint_res = coint(series_1, series_2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]  # i.e. the 5% level
    model = sm.OLS(series_1, series_2).fit()  # to calculate hedge ratio
    hedge_ratio = model.params[0]
    spread = calculate_spread(series_1, series_2, hedge_ratio)
    # zero_crossings = len(np.where(np.diff(np.sign(spread)))[0])
    zero_crossings = (np.diff(np.sign(spread)) != 0).sum()  # alternative
    # clever way to see where the sign (np.sign) from point n to n+1 changes direction (np.diff)
    # todo: plot those fits above

    if p_value < 0.05 and coint_t < critical_value:
        coint_flag = 1
    return (coint_flag, round(p_value, 2), round(coint_t, 2), round(critical_value, 2), round(hedge_ratio, 2), zero_crossings)


def extract_close_prices(prices):
    # Put close prices into a list
    close_prices = []
    for price_values in prices:
        if math.isnan(price_values["close"]):
            return []
        close_prices.append(price_values["close"])
    return close_prices


def get_cointegrated_pairs(prices):
    # Calculate cointegrated pairs

    # Loop through coins and check for cointegration
    coint_pair_list = []
    included_list = []  # to prevent duplicates
    for sym_1 in prices.keys():
        # e.g. "BTCUSD"
        # Check sym_1 against all other coins
        for sym_2 in prices.keys():
            if sym_2 != sym_1:

                # get unique combination id and ensure no duplicates
                # otherwise we would get everything twice.
                sorted_characters = sorted(sym_1 + sym_2)
                unique = "".join(sorted_characters)
                if unique in included_list:
                    continue  # jump to next item in for loop.
                    # or use break here to just abort and get a shorter list.

                # We only need the close prices
                series_1 = extract_close_prices(prices[sym_1])
                series_2 = extract_close_prices(prices[sym_2])

                # Check for cointegration and add cointegrated pair
                coint_flag, p_value, t_value, c_value, hedge_ratio, zero_crossings = calculate_cointegration(
                    series_1, series_2)
                # print(p_value, hedge_ratio, zero_crossings)
                if coint_flag == 1:
                    included_list.append(unique)
                    coint_pair_list.append({
                        "sym_1": sym_1,
                        "sym_2": sym_2,
                        "p_value": p_value,
                        "t_value": t_value,
                        "c_value": c_value,
                        "hedge_ratio": hedge_ratio,
                        "zero_crossings": zero_crossings
                    })

    # Output Results
    df_coint = pd.DataFrame(coint_pair_list)
    try:
        df_coint = df_coint.sort_values("zero_crossings", ascending=False)
    except KeyError:
        # then there won't be anything in coint_pair_list
        print("No cointegrated pairs found!")

    df_coint.to_csv("2_cointegrated_pairs.csv")
    return df_coint
