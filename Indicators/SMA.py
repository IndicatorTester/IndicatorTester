import pandas as pd

# Simple Moving Average
def sma(data: pd.DataFrame, window = 14):
    return data.rolling(window = window).mean()