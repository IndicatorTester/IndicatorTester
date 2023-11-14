from pathlib import Path
from os.path import expanduser
import json

class CandlesProvider:
    @classmethod
    def getCandles(cls, symbol):
        dataFilePath =  expanduser(f"~/IndicatorTester/candles/{symbol}.json")
        with open(dataFilePath, 'r') as file:
            data = json.load(file)
        return data