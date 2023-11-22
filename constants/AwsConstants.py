from enum import Enum

class AwsConstants(Enum):
    DYNAMO_DB = 'dynamodb'
    SYMBOLS_TABLE = 'Symbols'

    S3 = 's3'
    CANDLES_BUCKET = 'indicatortestercandles'