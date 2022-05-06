# Mostly copy & pasted from ./Strategy/func_cointegration.py

from config_execution_api import z_score_window
import math
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
import pandas as pd


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


def calculate_metrics(series_1, series_2):
    coint_flag = 0
    # See docs: https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.coint.html
    coint_res = coint(series_1, series_2)
    coint_t = coint_res[0]
    p_value = coint_res[1]
    critical_value = coint_res[2][1]  # i.e. the 5% level
    model = sm.OLS(series_1, series_2).fit()  # to calculate hedge ratio
    hedge_ratio = model.params[0]
    spread = calculate_spread(series_1, series_2, hedge_ratio)
    zscore_list = calculate_zscore(spread)

    if p_value < 0.05 and coint_t < critical_value:
        coint_flag = 1
    return (coint_flag, zscore_list.tolist())
