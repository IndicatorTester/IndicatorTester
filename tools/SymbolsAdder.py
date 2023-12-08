import os
import sys
import json

current_script_path = os.path.abspath(__file__)
project_directory = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_directory)

import constants
import utils

awsUtils = utils.AwsUtils.instance()

class SymbolsAdder:
    @classmethod
    def add(cls):
        newSymbols = cls._getNewSymbols()
        for symbolData in newSymbols:
            symbolKey = { 'symbol': symbolData['symbol'], 'exchange': symbolData['exchange'] }
            if awsUtils.existInDynamo(constants.AwsConstants.SYMBOLS_TABLE.value, symbolKey):
                continue
            awsUtils.addToDynamoDB(constants.AwsConstants.SYMBOLS_TABLE.value, symbolData)

    def _getNewSymbols():
        with open('./play/output.json') as f:
            data = json.load(f)
        return data

if __name__ == "__main__":
    SymbolsAdder().add()