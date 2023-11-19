import pandas as pd

# On-Balance Volume
def obv(data: pd.DataFrame, period = 1):
    obv = pd.Series(index=data.index)  # Create an empty Series to store OBV values

    # Calculate the difference in closing prices
    price_diff = data['Close'].diff()
    
    # Assign volume values based on the price difference
    obv[0] = data['Volume'].iloc[0]
    obv[1:] = data['Volume'].iloc[1:].where(price_diff >= 0, -data['Volume'].iloc[1:])
    
    # Calculate the cumulative sum of volume based on the price difference within the specified period
    obv = obv.rolling(period).sum()

    return obv