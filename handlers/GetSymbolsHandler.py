from clients import AwsClient
import constants
from utils import AwsUtils
from itertools import groupby

class GetSymbolsHandler:

    @staticmethod
    def instance():
        return getSymbolsHandler

    def __init__(self, awsClient: AwsClient, awsUtils: AwsUtils) -> None:
        self._awsClient = awsClient
        self._awsUtils = awsUtils

    def handle(self):
        dynamodb = self._awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        symbols = self._awsUtils.getDynamoTable(dynamodb, constants.AwsConstants.SYMBOLS_TABLE.value)
        symbols.sort(key=lambda x: x[constants.AwsConstants.SYMBOLS_TABLE_EXCHANGE_FIELD.value])
        return {key: list(group) for key, group in groupby(
            symbols, key=lambda x: x[constants.AwsConstants.SYMBOLS_TABLE_EXCHANGE_FIELD.value]
        )}

getSymbolsHandler = GetSymbolsHandler(AwsClient.instance(), AwsUtils.instance())