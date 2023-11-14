import pandas as pd

def sma(prices, window):
    return pd.Series(prices).rolling(window = window).mean()