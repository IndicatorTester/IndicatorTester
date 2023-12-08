import constants
from utils import AwsUtils
from itertools import groupby

class GetSymbolsHandler:

    @staticmethod
    def instance():
        return getSymbolsHandler

    def __init__(self, awsUtils: AwsUtils) -> None:
        self._awsUtils = awsUtils

    def handle(self):
        symbols = self._awsUtils.getDynamoTable(constants.AwsConstants.SYMBOLS_TABLE.value)
        symbols.sort(key=lambda x: x[constants.AwsConstants.SYMBOLS_TABLE_EXCHANGE_FIELD.value])
        return {key: list(group) for key, group in groupby(
            symbols, key=lambda x: x[constants.AwsConstants.SYMBOLS_TABLE_EXCHANGE_FIELD.value]
        )}

getSymbolsHandler = GetSymbolsHandler(AwsUtils.instance())