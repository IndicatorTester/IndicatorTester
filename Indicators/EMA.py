import pandas as pd

# Exponential Moving Average
def ema(data: pd.DataFrame, span = 14):
    return data.ewm(span = span, adjust = False).mean()