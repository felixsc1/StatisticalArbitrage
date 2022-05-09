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

Within an infinite loop:
- Monitor z-score signal
- Place long and short orders if z-score threshold is reached.
  - Order size is calculated depending on the liquidity of the assets. 
  - Once an order is filled, new order gets placed until capital limit is reached or signal disappeared.
- Wait for mean reversion (z-score reaching 0) and close all positions.