import boto3
import finnhub
import time
import json
import os
import calendar
from datetime import datetime, timedelta, timezone

def getSupportedSymbols():
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

def getYesterdayEpoch():
    current_time_utc = datetime.utcnow()
    yesterday_utc = current_time_utc - timedelta(days=1)
    yesterday_start_of_day_utc = yesterday_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(yesterday_start_of_day_utc.replace(tzinfo=timezone.utc).timestamp())

def generate_monthly_date_pairs(start_date, end_date):
    date_pairs = []
    current_date = start_date
    while current_date <= end_date:
        last_day_of_month = calendar.monthrange(current_date.year, current_date.month)[1]
        end_of_month = current_date.replace(day=last_day_of_month, hour=23, minute=59, second=59, tzinfo=timezone.utc)
        date_pairs.append((int(current_date.timestamp()), int(end_of_month.timestamp())))
        current_date = end_of_month + timedelta(seconds=1)
    return date_pairs

def fetchCandlesData(symbols):
    pairs = [(1262304000, 1735689600)]
    data = {}
    for symbol in symbols:
        data[symbol['symbol']['S']] = {}
        data[symbol['symbol']['S']]['t'] = []
        data[symbol['symbol']['S']]['o'] = []
        data[symbol['symbol']['S']]['h'] = []
        data[symbol['symbol']['S']]['l'] = []
        data[symbol['symbol']['S']]['c'] = []
        data[symbol['symbol']['S']]['v'] = []
        for s, e in pairs:
            time.sleep(10)
            print(f"Fetching data for symbol {symbol['symbol']['S']} from {s} to {e}")
            finnhub_client = finnhub.Client(api_key="cl2a54hr01qinfqol99gcl2a54hr01qinfqol9a0")
            gotData = False
            retries = 3
            while gotData == False and retries != 0:
                response = finnhub_client.crypto_candles(symbol['exchangeSymbol']['S'], 'D', s, e)
                if 't' in response and len(response['t']) != 0:
                    break
                retries = retries - 1
                time.sleep(10)
            if response['s'] == 'no_data':
                continue
            data[symbol['symbol']['S']]['t'].extend(response['t'])
            data[symbol['symbol']['S']]['o'].extend(response['o'])
            data[symbol['symbol']['S']]['h'].extend(response['h'])
            data[symbol['symbol']['S']]['l'].extend(response['l'])
            data[symbol['symbol']['S']]['c'].extend(response['c'])
            data[symbol['symbol']['S']]['v'].extend(response['v'])
            print(f"The number of candles -> {len(data[symbol['symbol']['S']]['t'])}")
    return data

def writeData(data):
    formattedData = {}
    for key, value in data.items():
        home = os.path.expanduser("~")
        path = os.path.join(home, 'IndicatorTester/candles')
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}/{key}.json", 'w') as json_file:
            json.dump(value, json_file)

def main():
    symbols = getSupportedSymbols()
    symbolsData = fetchCandlesData(symbols)
    writeData(symbolsData)

if __name__ == "__main__":
    main()