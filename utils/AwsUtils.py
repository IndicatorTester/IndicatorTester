from clients.AwsClient import AwsClient
import constants

class AwsUtils:

    @staticmethod
    def instance():
        return awsUtils

    def __init__(self, awsClient: AwsClient) -> None:
        self._awsClient = awsClient

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

awsUtils = AwsUtils(AwsClient.instance())