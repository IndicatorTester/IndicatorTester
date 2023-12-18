import pandas as pd
from models import CalculateRequest
import utils
import requests
import json

class CandlesProvider:

    @staticmethod
    def instance():
        return candlesProvider

    def __init__(self, awsUtils: utils.AwsUtils) -> None:
        self._awsUtils = awsUtils
        self._cache = {}

    def getCandles(self, request: CalculateRequest, apiKey: str) -> pd.DataFrame:
        response = requests.get("https://api.twelvedata.com/time_series?" \
            f"apikey={apiKey}" \
            f"&exchange={request.exchange}" \
            f"&interval={request.interval}" \
            f"&symbol={request.symbol}" \
            f"&start_date={request.startDate}" \
            f"&end_date={request.endDate}" \
            f"&format=JSON")
        df = pd.json_normalize(json.loads(response.text)['values'])
        df = df.rename(columns={'datetime': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'})
        columns_to_float = ['Open', 'High', 'Low', 'Close']
        df[columns_to_float] = df[columns_to_float].astype(float)
        result_df = df.iloc[::-1].reset_index(drop=True)[['Date'] + columns_to_float]
        return result_df

candlesProvider = CandlesProvider(utils.AwsUtils.instance())