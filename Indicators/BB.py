import pandas as pd

# Bollinger Bands lower band
def boll(data: pd.DataFrame):
    WINDOW = 20
    SMA = data.rolling(window = WINDOW).mean()
    SD = data.rolling(window = WINDOW).std()
    return SMA - 2 * SD

# Bollinger Bands upper band
def bolu(data: pd.DataFrame):
    WINDOW = 20
    SMA = data.rolling(window = WINDOW).mean()
    SD = data.rolling(window = WINDOW).std()
    return SMA + 2 * SD