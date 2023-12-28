from clients.AwsClient import AwsClient
import constants
import datetime
import pickle

class AwsUtils:

    @staticmethod
    def instance():
        return awsUtils

    def __init__(self) -> None:
        self._awsClient = AwsClient.instance()

    def getUserData(self, userId: str):
        dynamodb = self._awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        response = dynamodb.get_item(
            TableName = constants.AwsConstants.USERS_TABLE.value,
            Key = self._toDynamoItem({"userId": userId})
        )['Item']
        return {
            "userId": response["userId"]["S"],
            "apiKey": response["apiKey"]["S"]
        }

    def updateOrCreateDynamoItem(self, tableName, primaryKey, updateData):
        dynamodb = self._awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        update_expression = "SET "
        expression_attribute_values = {}
        for key, value in updateData.items():
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = self._getObjectWithType(value)
        update_expression = update_expression.rstrip(', ')
        response = dynamodb.update_item(
            TableName=tableName,
            Key={k: {'S': v} for k, v in primaryKey.items()},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response

    def addPreOrder(self, ip: str, email: str):
        dynamodb = self._awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        dynamodb.put_item(
            TableName = constants.AwsConstants.PRE_ORDERS_TABLE.value,
            Item = {"ip": {"S": ip}, "email": {"S": email}}
        )

    def getByBitCoinAsset(self, coin):
        dynamodb = self._awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        response = dynamodb.get_item(
            TableName=constants.AwsConstants.BYBIT_TABLE.value,
            Key={'coin': {'S': coin}}
        )
        return str(response['Item']['value']['S'])

    def updateByBitCoinAsset(self, coin, value):
        dynamodb = self._awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        dynamodb.delete_item(
            TableName=constants.AwsConstants.BYBIT_TABLE.value,
            Key={
                'coin': {'S': coin}
            }
        )
        dynamodb.put_item(
            TableName=constants.AwsConstants.BYBIT_TABLE.value,
            Item={
                'coin': {'S': coin},
                'value': {'S': value}
            }
        )

    def addIndicatorTest(self, indicatorTestData):
        dynamodb = self._awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        dynamodb.put_item(
            TableName = constants.AwsConstants.INDICATOR_TESTS_TABLE.value,
            Item = self._toDynamoItem(indicatorTestData)
        )

    def addIndicatorTestActions(self, userId, timestamp, symbol, actions):
        date = str(datetime.datetime.utcfromtimestamp(int(timestamp)).date())
        s3 = self._awsClient.get_client(constants.AwsConstants.S3.value)
        s3.put_object(
            Bucket=constants.AwsConstants.TESTS_RESULT_BUCKET.value,
            Key=f"{userId}/{symbol}/{date}/{timestamp}.json",
            Body=pickle.dumps(actions)
        )

    def _toDynamoItem(self, json_record):
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

    def _getObjectWithType(self, value):
        if isinstance(value, str):
            return {'S': value}
        elif isinstance(value, int):
            return {'N': str(value)}
        elif isinstance(value, float):
            return {'N': str(value)}
        elif isinstance(value, bool):
            return {'BOOL': value}
        else:
            return {'NULL': True}

awsUtils = AwsUtils()