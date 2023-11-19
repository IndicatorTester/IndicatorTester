import pandas as pd

# Average Directional Index
def adx(data: pd.DataFrame, period = 14):
    high = data['High']
    low = data['Low']
    close = data['Close']

    tr = pd.DataFrame(index=data.index)
    tr['tr1'] = high - low  # True Range 1
    tr['tr2'] = abs(high - close.shift())  # True Range 2
    tr['tr3'] = abs(low - close.shift())  # True Range 3
    tr['true_range'] = tr.max(axis=1)  # True Range (largest of the three)

    tr['plus_dm'] = high - high.shift()
    tr['minus_dm'] = low.shift() - low
    tr['plus_dm'] = tr['plus_dm'].apply(lambda x: x if x > 0 else 0)  # Set negative values to 0
    tr['minus_dm'] = tr['minus_dm'].apply(lambda x: x if x > 0 else 0)  # Set negative values to 0

    tr['plus_di'] = 100 * (tr['plus_dm'].rolling(period).sum() / tr['true_range'].rolling(period).sum())
    tr['minus_di'] = 100 * (tr['minus_dm'].rolling(period).sum() / tr['true_range'].rolling(period).sum())

    tr['dx'] = 100 * (abs(tr['plus_di'] - tr['minus_di']) / abs(tr['plus_di'] + tr['minus_di']))

    adx = tr['dx'].rolling(period).mean()

    return adx