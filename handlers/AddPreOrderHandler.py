from models import AddPreOrderRequest
from utils import AwsUtils

class AddPreOrderHandler:

    @staticmethod
    def instance():
        return addPreOrderHandler

    def __init__(self):
        self._awsUtils = AwsUtils.instance()

    def handle(self, request: AddPreOrderRequest):
        self._awsUtils.addPreOrder(request.ip, request.email)

addPreOrderHandler = AddPreOrderHandler()