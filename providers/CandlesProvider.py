import pandas as pd
import clients
import constants
import utils

awsClient = clients.AwsClient()
aswUtils = utils.AwsUtils()

class CandlesProvider:

    cache = {}

    @classmethod
    def getCandles(cls, exchange, interval, symbol) -> pd.DataFrame:
        path = f"{exchange}/{interval}/{symbol}.csv"
        if path in cls.cache:
            return cls.cache[path]

        s3 = awsClient.get_client(constants.AwsConstants.S3.value)
        candles = aswUtils.getDataFrameFromS3(s3, path)
        cls.cache[path] = candles
        return candles