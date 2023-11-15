import pandas as pd

# Bollinger Bands upper band
def bolu(prices):
    WINDOW = 20
    SMA = pd.Series(prices).rolling(window = WINDOW).mean()
    SD = pd.Series(prices).rolling(window = WINDOW).std()
    return SMA + 2 * SD