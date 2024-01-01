import pandas as pd
from errors.DataProviderError import DataProviderError
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

    def getCandles(self, request: CalculateRequest) -> pd.DataFrame:
        response = requests.get("https://api.twelvedata.com/time_series?" \
            f"apikey={request.apiKey}" \
            f"&exchange={request.exchange}" \
            f"&interval={request.interval}" \
            f"&symbol={request.symbol}" \
            f"&start_date={request.startDate}" \
            f"&end_date={request.endDate}" \
            f"&format=JSON")
        data = json.loads(response.text)

        if data['status'] != 'ok':
            raise DataProviderError(f"Data provider error: {data['message']}")

        if data['values'] == None:
            raise DataProviderError(f"Historical data not found")

        df = pd.json_normalize(data['values'])
        df = df.rename(columns={'datetime': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'})
        columns_to_float = ['Open', 'High', 'Low', 'Close']
        df[columns_to_float] = df[columns_to_float].astype(float)
        result_df = df.iloc[::-1].reset_index(drop=True)[['Date'] + columns_to_float]
        return result_df

candlesProvider = CandlesProvider(utils.AwsUtils.instance())