import pandas as pd

# Simple Moving Average
def sma(data: pd.DataFrame, window = 14):
    return data.rolling(window = window).mean()

# sma(close, 5) > sma(open, 5)