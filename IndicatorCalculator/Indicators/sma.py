import pandas as pd

# Simple Moving Average
def sma(data: pd.DataFrame, window):
    return data.rolling(window = window).mean()