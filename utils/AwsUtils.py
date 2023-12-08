from io import StringIO
import pandas as pd
from clients.AwsClient import AwsClient
import constants

class AwsUtils:

    @staticmethod
    def instance():
        return awsUtils

    def __init__(self, awsClient: AwsClient) -> None:
        self._awsClient = awsClient

    def getDynamoTable(self, table):
        try:
            dynamodb = self._awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
            items = []
            scan_complete = False
            while not scan_complete:
                response = dynamodb.scan(TableName = table)
                if 'Items' in response:
                    items.extend(self._itemsToJson(response['Items']))
                if 'LastEvaluatedKey' in response:
                    last_key = response['LastEvaluatedKey']
                    response = dynamodb.scan(TableName = table, ExclusiveStartKe = last_key)
                else:
                    scan_complete = True
            return items
        except Exception as e:
            return []

    def existInDynamo(self, table, key):
        dynamodb = self._awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        response = dynamodb.get_item(
            TableName = table,
            Key = self._toDynamoItem(key)
        )
        return 'Item' in response

    def addToDynamoDB(self, table, item):
        dynamodb = self._awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        dynamodb.put_item(
            TableName = table,
            Item = self._toDynamoItem(item)
        )

    def writeDataFrameToS3(self, path, df: pd.DataFrame):
        s3 = self._awsClient.get_client(constants.AwsConstants.S3.value)
        csvBuffer = StringIO()
        df.to_csv(csvBuffer)
        s3.put_object(Bucket = constants.AwsConstants.CANDLES_BUCKET.value, Key = path, Body = csvBuffer.getvalue())

    def getDataFrameFromS3(self, path) -> pd.DataFrame:
        s3 = self._awsClient.get_client(constants.AwsConstants.S3.value)
        s3Object = s3.get_object(Bucket = constants.AwsConstants.CANDLES_BUCKET.value, Key = path)
        return pd.read_csv(s3Object['Body'])

    def _itemsToJson(self, items):
        jsonItems = []
        for item in items:
            for key in item.keys():
                if isinstance(item[key], dict) and 'S' in item[key]:
                    item[key] = item[key]['S']
                elif isinstance(item[key], dict) and 'N' in item[key]:
                    item[key] = item[key]['N']
                elif isinstance(item[key], list):
                    item[key] = [self._itemsToJson(i) if isinstance(i, dict) else i for i in item[key]]
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

awsUtils = AwsUtils(AwsClient.instance())