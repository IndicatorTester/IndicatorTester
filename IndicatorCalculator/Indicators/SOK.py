import pandas as pd

# Stochastic Oscillator slow K
def sok(data: pd.DataFrame, period = 14):
    # Calculate %K
    lowest_low = data['Low'].rolling(window=period).min()
    highest_high = data['High'].rolling(window=period).max()
    return (data['Close'] - lowest_low) / (highest_high - lowest_low) * 100