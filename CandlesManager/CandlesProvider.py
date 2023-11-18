import pandas as pd
from os.path import expanduser

class CandlesProvider:
    @classmethod
    def getCandles(cls, symbol, startDate = '2000-01-01', endDate = '2029-12-31') -> pd.DataFrame:
        dataFilePath =  expanduser(f"~/IndicatorTester/candles/{symbol}.csv")
        with open(dataFilePath, 'r') as file:
            data = pd.read_csv(file)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
        return data.loc[pd.to_datetime(startDate):pd.to_datetime(endDate)]