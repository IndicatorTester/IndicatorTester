import pandas as pd

# Money Flow Index
def mfi(data: pd.DataFrame, period = 14):
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    raw_money_flow = typical_price * data['Volume']
    positive_money_flow = raw_money_flow * (typical_price > typical_price.shift(1))
    negative_money_flow = raw_money_flow * (typical_price < typical_price.shift(1))

    positive_money_flow_sum = positive_money_flow.rolling(period).sum()
    negative_money_flow_sum = negative_money_flow.rolling(period).sum()

    money_ratio = positive_money_flow_sum / negative_money_flow_sum
    mfi = 100 - (100 / (1 + money_ratio))

    return mfi