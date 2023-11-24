import pandas as pd
import clients
import constants
import utils

class CandlesProvider:

    @staticmethod
    def instance():
        return candlesProvider

    def __init__(self, awsClient: clients.AwsClient, awsUtils: utils.AwsUtils) -> None:
        self._awsClient = awsClient
        self._awsUtils = awsUtils
        self._cache = {}

    def getCandles(self, exchange, interval, symbol) -> pd.DataFrame:
        path = f"{exchange}/{interval}/{symbol}.csv"
        if path in self._cache:
            return self._cache[path]

        s3 = self._awsClient.get_client(constants.AwsConstants.S3.value)
        candles = self._awsUtils.getDataFrameFromS3(s3, path)
        self._cache[path] = candles
        return candles

candlesProvider = CandlesProvider(clients.AwsClient.instance(), utils.AwsUtils.instance())