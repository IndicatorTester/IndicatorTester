from enum import Enum

class AwsConstants(Enum):
    DYNAMO_DB = 'dynamodb'
    USERS_TABLE = 'Users'
    PRICES_TABLE = 'Prices'
    BYBIT_TABLE = 'ByBitAssets'
    INDICATOR_TESTS_TABLE = 'IndicatorTests'

    S3 = 's3'
    TESTS_RESULT_BUCKET = 'xindicatortestsresult'