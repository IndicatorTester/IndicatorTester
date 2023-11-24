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

awsClient = clients.AwsClient.instance()
awsUtils = utils.AwsUtils.instance()
mailingUtils = utils.MailingUtils.instance()

class CandlesFetcher:
    @classmethod
    def fetch(cls):
        report = ''
        s3 = awsClient.get_client(constants.AwsConstants.S3.value)
        dynamodb = awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        symbols = awsUtils.getDynamoTable(dynamodb, constants.AwsConstants.SYMBOLS_TABLE.value)
        for symbol in symbols:
            time.sleep(30)
            data = yf.download(
                symbol['apiSymbol'],
                start = constants.CandlesConstants.CANDLES_ABS_START_DATE.value,
                end = constants.CandlesConstants.CANDLES_ABS_END_DATE.value
            )
            path = f"{symbol['exchange']}/{constants.CandlesConstants.ONE_DAY_INTERVAL.value}/{symbol['symbol']}.csv"
            existingData = awsUtils.getDataFrameFromS3(s3, path)

            symbolReport = cls._getSymbolReport(symbol['symbol'], existingData, pd.DataFrame(data).reset_index())
            report += symbolReport[1]
            if symbolReport[0] == False:
                continue

            awsUtils.writeDataFrameToS3(s3, path, pd.DataFrame(data).reset_index())
        mailingUtils.sendCandlesFetcherReport(report)

    def _getSymbolReport(symbol, existingData, newData):
        if len(existingData['Close']) >= len(newData['Close']):
            return (False, 
                f"<br><p><b>[WARNING] Current data size is larger than or equal to new data size for symbol: {symbol}</b></p><br>"
            )
        return (True,
            f"<br><p>[INFO] New data size is larger than the current data size for symbol: {symbol}</p><br>"
        )

if __name__ == "__main__":
    CandlesFetcher().fetch()