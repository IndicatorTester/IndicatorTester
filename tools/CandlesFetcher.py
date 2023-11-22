import os
import sys
import time
import yfinance as yf
import pandas as pd

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)

import clients
import constants
import utils

awsClient = clients.AwsClient()
awsUtils = utils.AwsUtils()

class CandlesFetcher:
    @classmethod
    def fetch(cls):
        s3 = awsClient.get_client(constants.AwsConstants.S3.value)
        dynamodb = awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        symbols = awsUtils.getDynamoTable(dynamodb, constants.AwsConstants.SYMBOLS_TABLE.value)
        for symbol in symbols:
            data = yf.download(
                symbol['apiSymbol'],
                start = constants.CandlesConstants.CANDLES_ABS_START_DATE.value,
                end = constants.CandlesConstants.CANDLES_ABS_END_DATE.value
            )
            path = f"{symbol['exchange']}/{constants.CandlesConstants.ONE_DAY_INTERVAL.value}/{symbol['symbol']}.csv"
            awsUtils.writeDataFrameToS3(s3, path, pd.DataFrame(data))
            time.sleep(30)

if __name__ == "__main__":
    CandlesFetcher().fetch()