from enum import Enum

class AwsConstants(Enum):
    DYNAMO_DB = 'dynamodb'
    USERS_TABLE = 'Users'
    PRE_ORDERS_TABLE = 'PreOrders'
    BYBIT_TABLE = 'ByBitAssets'

    S3 = 's3'