import pandas as pd

# Moving Average Convergence Divergence - signal line
def macds(data: pd.DataFrame, short_period=12, long_period=26, signal_period=9):
    # Calculate the short-term exponential moving average (EMA)
    ema_short = data.ewm(span=short_period, adjust=False).mean()

    # Calculate the long-term exponential moving average (EMA)
    ema_long = data.ewm(span=long_period, adjust=False).mean()

    # Calculate the MACD line
    macd_line = ema_short - ema_long

    # Calculate the signal line
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    return signal_line