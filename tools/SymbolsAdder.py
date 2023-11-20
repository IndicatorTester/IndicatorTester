import os
import sys

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)

import clients
import constants
import utils

awsClient = clients.AwsClient()
awsUtils = utils.AwsUtils()

class SymbolsAdder:
    @classmethod
    def add(cls):
        dynamodb = awsClient.get_client(constants.AwsConstants.DYNAMO_DB.value)
        newSymbols = cls._getNewSymbols()
        for symbolData in newSymbols:
            symbolKey = { 'symbol': symbolData['symbol'], 'exchange': symbolData['exchange'] }
            if awsUtils.existInDynamo(dynamodb, constants.AwsConstants.SYMBOLS_TABLE.value, symbolKey):
                continue
            awsUtils.addToDynamoDB(dynamodb, constants.AwsConstants.SYMBOLS_TABLE.value, symbolData)

    def _getNewSymbols():
        return [{
            'symbol': 'GOOGL',
            'name': 'Alphabet Inc.',
            'apiSymbol': 'GOOG',
            'exchange': 'NASDAQ'
        }]

if __name__ == "__main__":
    SymbolsAdder().add()