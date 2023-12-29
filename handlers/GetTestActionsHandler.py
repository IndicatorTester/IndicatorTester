from utils import AwsUtils

class GetTestActionsHandler:

    @staticmethod
    def instance():
        return getTestActionsHandler

    def __init__(self) -> None:
        self._awsUtils = AwsUtils.instance()

    def handle(self, userId, timestamp):
        testData = self._awsUtils.getIndicatorTest(userId, timestamp)
        return self._awsUtils.getIndicatorTestActions(userId, timestamp, testData['symbol'])

getTestActionsHandler = GetTestActionsHandler()