from utils import AwsUtils

class GetTestArchiveHandler:

    @staticmethod
    def instance():
        return getTestArchiveHandler

    def __init__(self) -> None:
        self._awsUtils = AwsUtils.instance()

    def handle(self, userId, timestamp, pageNumber):
        return self._awsUtils.getIndicatorTests(userId, timestamp, pageNumber)

getTestArchiveHandler = GetTestArchiveHandler()