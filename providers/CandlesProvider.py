import pandas as pd
from os.path import expanduser

class CandlesProvider:
    @classmethod
    def getCandles(cls, symbol, startDate, endDate) -> pd.DataFrame:
        dataFilePath =  expanduser(f"~/IndicatorTester/candles/{symbol}.csv")
        with open(dataFilePath, 'r') as file:
            data = pd.read_csv(file)
        data['Date'] = pd.to_datetime(data['Date'])
        selectedData = data.set_index('Date').loc[startDate:endDate].reset_index()
        return selectedData