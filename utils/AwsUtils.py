from io import StringIO
import pandas as pd
import constants

class AwsUtils:
    @classmethod
    def getDynamoTable(cls, dynamodb, table):
        try:
            items = []
            scan_complete = False
            while not scan_complete:
                response = dynamodb.scan(TableName = table)
                if 'Items' in response:
                    items.extend(cls._itemsToJson(cls, response['Items']))
                if 'LastEvaluatedKey' in response:
                    last_key = response['LastEvaluatedKey']
                    response = dynamodb.scan(TableName = table, ExclusiveStartKe = last_key)
                else:
                    scan_complete = True
            return items
        except Exception as e:
            return []

    @classmethod
    def existInDynamo(cls, dynamodb, table, key):
        response = dynamodb.get_item(
            TableName = table,
            Key = cls._toDynamoItem(key)
        )
        return 'Item' in response

    @classmethod
    def addToDynamoDB(cls, dynamodb, table, item):
        dynamodb.put_item(
            TableName = table,
            Item = cls._toDynamoItem(item)
        )

    @classmethod
    def writeDataFrameToS3(cls, s3, path, df: pd.DataFrame):
        csvBuffer = StringIO()
        df.to_csv(csvBuffer)
        s3.put_object(Bucket = constants.AwsConstants.CANDLES_BUCKET.value, Key = path, Body = csvBuffer.getvalue())

    @classmethod
    def getDataFrameFromS3(cls, s3, path) -> pd.DataFrame:
        s3Object = s3.get_object(Bucket = constants.AwsConstants.CANDLES_BUCKET.value, Key = path)
        return pd.read_csv(s3Object['Body'])

    def _itemsToJson(cls, items):
        jsonItems = []
        for item in items:
            for key in item.keys():
                if isinstance(item[key], dict) and 'S' in item[key]:
                    item[key] = item[key]['S']
                elif isinstance(item[key], dict) and 'N' in item[key]:
                    item[key] = item[key]['N']
                elif isinstance(item[key], list):
                    item[key] = [cls._itemsToJson(i) if isinstance(i, dict) else i for i in item[key]]
            jsonItems.append(item)
        return jsonItems

    def _toDynamoItem(json_record):
        item = {}

        for key, value in json_record.items():
            if isinstance(value, str):
                item[key] = {'S': value}
            elif isinstance(value, int):
                item[key] = {'N': str(value)}
            elif isinstance(value, float):
                item[key] = {'N': str(value)}
            elif isinstance(value, bool):
                item[key] = {'BOOL': value}
            else:
                item[key] = {'NULL': True}

        return item