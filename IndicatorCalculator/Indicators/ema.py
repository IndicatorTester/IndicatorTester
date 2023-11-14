import pandas as pd

def ema(prices, span):
    return pd.Series(prices).ewm(span = span, adjust = False).mean()