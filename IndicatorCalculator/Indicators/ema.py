import pandas as pd

# Exponential Moving Average
def ema(prices, span):
    return pd.Series(prices).ewm(span = span, adjust = False).mean()