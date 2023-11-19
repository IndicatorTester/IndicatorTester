import os
import boto3
import time
import yfinance as yf
import pandas as pd

class CandlesFetcher:
    @classmethod
    def fetch(cls):
        symbols = cls._getSupportedSymbols()
        for symbol in symbols:
            time.sleep(30)
            data = yf.download(symbol['exchangeSymbol']['S'], start="2000-01-01", end="2025-01-01")
            home = os.path.expanduser("~")
            path = os.path.join(home, 'IndicatorTester/candles')
            if not os.path.exists(path):
                os.makedirs(path)
            with open(f"{path}/{symbol['symbol']['S']}.csv", 'w') as file:
                file.write(pd.DataFrame(data).to_csv())

    def _getSupportedSymbols():
        dynamodb = boto3.client('dynamodb', region_name='eu-west-1')
        tableName = 'CryptoSymbols'
        try:
            items = []
            scan_complete = False
            while not scan_complete:
                response = dynamodb.scan(TableName=tableName)
                if 'Items' in response:
                    items.extend(response['Items'])
                if 'LastEvaluatedKey' in response:
                    last_key = response['LastEvaluatedKey']
                    response = dynamodb.scan(TableName=tableName, ExclusiveStartKey=last_key)
                else:
                    scan_complete = True
            return items
        except Exception as e:
            return []

if __name__ == "__main__":
    CandlesFetcher().fetch()