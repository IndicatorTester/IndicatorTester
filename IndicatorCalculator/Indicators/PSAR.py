import pandas as pd

# Parabolic SAR
def psar(data: pd.DataFrame, af_start = 0.02, af_increment = 0.02, af_max = 0.2):
    high = data['High']
    low = data['Low']

    sar = pd.Series(index=data.index)
    trend = pd.Series(0, index=data.index)
    acceleration = af_start
    extreme = high[0]
    sar[0] = low[0]

    for i in range(1, len(data)):
        if trend[i-1] > 0:  # Current trend is up
            sar[i] = sar[i-1] + acceleration * (extreme - sar[i-1])
            if sar[i] > low[i-1]:  # Switch to downtrend
                trend[i] = -1
                sar[i] = extreme
                extreme = low[i]
                acceleration = af_start
            else:
                trend[i] = 1
                acceleration = min(acceleration + af_increment, af_max)
                if high[i] > extreme:
                    extreme = high[i]
        else:  # Current trend is down
            sar[i] = sar[i-1] - acceleration * (sar[i-1] - extreme)
            if sar[i] < high[i-1]:  # Switch to uptrend
                trend[i] = 1
                sar[i] = extreme
                extreme = high[i]
                acceleration = af_start
            else:
                trend[i] = -1
                acceleration = min(acceleration + af_increment, af_max)
                if low[i] < extreme:
                    extreme = low[i]

    return sar