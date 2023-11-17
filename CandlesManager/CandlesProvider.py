from pathlib import Path
from os.path import expanduser
import pandas as pd

class CandlesProvider:
    @classmethod
    def getCandles(cls, symbol) -> pd.DataFrame:
        dataFilePath =  expanduser(f"~/IndicatorTester/candles/{symbol}.csv")
        with open(dataFilePath, 'r') as file:
            data = pd.read_csv(file)
        return data