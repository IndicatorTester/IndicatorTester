import pandas as pd

# Volume Weighted Average Price
def vwap(data: pd.DataFrame, period = 20):
    volume = data['Volume']
    price = data['Close']
    vwap = (volume * price).rolling(period).sum() / volume.rolling(period).sum()
    return vwap