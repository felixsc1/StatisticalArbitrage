from func_cointegration import extract_close_prices
from func_cointegration import calculate_cointegration
from func_cointegration import calculate_spread
from func_cointegration import calculate_zscore
import matplotlib.pyplot as plt
import pandas as pd


def plot_trends(sym_1, sym_2, price_data):
    # Plot prices and trends

    # Extract prices
    prices_1 = extract_close_prices(price_data[sym_1])
    prices_2 = extract_close_prices(price_data[sym_2])

    # Get spread and zscore
    coint_flag, p_value, t_value, c_value, hedge_ratio, zero_crossings = calculate_cointegration(
        prices_1, prices_2)
    spread = calculate_spread(prices_1, prices_2, hedge_ratio)
    zscore = calculate_zscore(spread)
    # print(zscore)

    # Calculate percentage changes (relative to first data point)
    # so that both prices fit on same chart
    df = pd.DataFrame(columns=[sym_1, sym_2])
    df[sym_1] = prices_1
    df[sym_2] = prices_2
    df[f"{sym_1}_pct"] = df[sym_1] / prices_1[0]
    df[f"{sym_2}_pct"] = df[sym_2] / prices_2[0]
    series_1 = df[f"{sym_1}_pct"].astype(float).values
    series_2 = df[f"{sym_2}_pct"].astype(float).values

    # Save results for backtesting
    df_2 = pd.DataFrame()
    df_2[sym_1] = prices_1
    df_2[sym_2] = prices_2
    df_2["Spread"] = spread
    df_2["Zscore"] = zscore
    df_2.to_csv("3_backtest_file.csv")
    print("File for backtesting saved.")

    # Plot charts
    fig, axs = plt.subplots(3, figsize=(12, 6))
    fig.suptitle(f"Price and Spread - {sym_1} vs {sym_2}")
    axs[0].plot(series_1)
    axs[0].plot(series_2)
    axs[0].set_ylabel("price [%]")
    axs[1].plot(spread)
    axs[1].set_ylabel("spread")
    axs[2].plot(zscore)
    axs[2].set_ylabel("z-score")
    plt.show()
