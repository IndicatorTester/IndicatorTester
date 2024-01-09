import constants
from utils import AwsUtils

class UserPaymentHandler:

    @staticmethod
    def instance():
        return userPaymentHandler

    def __init__(self):
        self._awsUtils = AwsUtils.instance()

    def handle(self, userId, priceId):
        userData = self._awsUtils.getUserData(userId)
        priceData = self._awsUtils.getPriceData(priceId)
        testType = priceData['testType']

        self._awsUtils.updateOrCreateDynamoItem(
            tableName=constants.AwsConstants.USERS_TABLE.value,
            primaryKey={"userId": userId},
            updateData={
               testType: str(int(userData.get(testType, "0")) + int(priceData['amount']))
            }
        )

        return {
            "success": True
        }

userPaymentHandler = UserPaymentHandler()