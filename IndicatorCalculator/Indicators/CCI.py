import pandas as pd
import numpy as np

# Commodity Channel Index
def cci(data: pd.DataFrame, period = 20):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    mean_deviation = typical_price.rolling(period).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    cci = (typical_price - typical_price.rolling(period).mean()) / (0.015 * mean_deviation)
    return cci