from utils import AwsUtils

class GetUserHandler:

    @staticmethod
    def instance():
        return getUserHandler

    def __init__(self):
        self._awsUtils = AwsUtils.instance()

    def handle(self, userId):
        return self._awsUtils.getUserData(userId)

getUserHandler = GetUserHandler()