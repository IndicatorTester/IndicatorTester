import constants
from models import UpdateUserRequest
from utils import AwsUtils

class UpdateUserHandler:

    @staticmethod
    def instance():
        return updateUserHandler

    def __init__(self):
        self._awsUtils = AwsUtils.instance()

    def handle(self, request: UpdateUserRequest):
        self._awsUtils.updateOrCreateDynamoItem(
            constants.AwsConstants.USERS_TABLE.value,
            {"userId": request.userId},
            request.userData
        )

updateUserHandler = UpdateUserHandler()