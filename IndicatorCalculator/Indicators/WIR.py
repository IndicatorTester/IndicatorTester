import pandas as pd

# Williams %R
def wir(data: pd.DataFrame, period = 5):
    high = data['High']
    low = data['Low']
    close = data['Close']

    highest_high = high.rolling(window=period).max()
    lowest_low = low.rolling(window=period).min()

    williams_r = (highest_high - close) / (highest_high - lowest_low) * -100
    return williams_r