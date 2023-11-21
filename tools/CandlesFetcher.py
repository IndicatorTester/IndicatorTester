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
        dynamodb = awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        symbols = awsUtils.getDynamoTable(dynamodb, constants.AwsConstants.SYMBOLS_TABLE.value)
        for symbol in symbols:
            time.sleep(30)
            data = yf.download(symbol['apiSymbol'], start="2000-01-01", end="2025-01-01")
            home = os.path.expanduser("~")
            path = os.path.join(home, 'IndicatorTester/candles')
            if not os.path.exists(path):
                os.makedirs(path)
            with open(f"{path}/{symbol['symbol']}.csv", 'w') as file:
                file.write(pd.DataFrame(data).to_csv())

if __name__ == "__main__":
    CandlesFetcher().fetch()