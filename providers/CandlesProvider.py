import pandas as pd
import utils

class CandlesProvider:

    @staticmethod
    def instance():
        return candlesProvider

    def __init__(self, awsUtils: utils.AwsUtils) -> None:
        self._awsUtils = awsUtils
        self._cache = {}

    def getCandles(self, exchange, interval, symbol) -> pd.DataFrame:
        path = f"{exchange}/{interval}/{symbol}.csv"
        if path in self._cache:
            return self._cache[path]

        candles = self._awsUtils.getDataFrameFromS3(path)
        self._cache[path] = candles
        return candles

candlesProvider = CandlesProvider(utils.AwsUtils.instance())