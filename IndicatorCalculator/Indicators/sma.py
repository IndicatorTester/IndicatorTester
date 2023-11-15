import pandas as pd

# Simple Moving Average
def sma(prices, window):
    return pd.Series(prices).rolling(window = window).mean()