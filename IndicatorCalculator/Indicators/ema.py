import pandas as pd

# Exponential Moving Average
def ema(data: pd.DataFrame, span):
    return data.ewm(span = span, adjust = False).mean()

# ema(OPEN, 10) > ema(CLOSE, 50)