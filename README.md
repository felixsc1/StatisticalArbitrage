# Statistical Arbitrage Bot

Using the bybit API (see [docs](https://bybit-exchange.github.io/docs/linear)) we try to find cointegrated coin pairs to do arbitrage. Register on testnet.bybit.com to get an API key and secret.

## ./Strategy

Run the individual steps in ./Strategy/main_strategy.py:

1. Get all tradeable pairs.
2. Get their price history
3. Find cointegrated pairs
4. Calculate and visualize spread/zscore

Outputs and statistics are stored as .csv files for further backtesting.


## ./Execution

