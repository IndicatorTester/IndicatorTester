import pandas as pd

# Standard Deviation
def sd(data: pd.DataFrame, period = 5):
    std_dev = data.rolling(window=period).std(ddof=0)
    return std_dev