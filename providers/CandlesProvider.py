import pandas as pd
import utils
import requests
import json
import constants

class CandlesProvider:

    @staticmethod
    def instance():
        return candlesProvider

    def __init__(self, awsUtils: utils.AwsUtils) -> None:
        self._awsUtils = awsUtils
        self._cache = {}

    def getCandles(self, exchange, interval, symbol) -> pd.DataFrame:
        response = requests.get(f"https://api.twelvedata.com/time_series?apikey=e21a1ce91bfc46d79fa61834cfcedff3&interval=1day&symbol={symbol}&start_date={constants.CandlesConstants.CANDLES_ABS_START_DATE.value}&end_date={constants.CandlesConstants.CANDLES_ABS_END_DATE.value}&format=JSON")
        df = pd.json_normalize(json.loads(response.text)['values'])
        df = df.rename(columns={'datetime': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'})
        columns_to_float = ['Open', 'High', 'Low', 'Close']
        df[columns_to_float] = df[columns_to_float].astype(float)
        result_df = df.iloc[::-1].reset_index(drop=True)[['Date'] + columns_to_float]
        return result_df

candlesProvider = CandlesProvider(utils.AwsUtils.instance())