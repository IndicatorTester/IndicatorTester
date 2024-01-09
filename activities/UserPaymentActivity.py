from fastapi import HTTPException
from handlers.UserPaymentHandler import UserPaymentHandler
import logging

class UserPaymentActivity:

    @staticmethod
    def instance():
        return userPaymentActivity

    def __init__(self) -> None:
        self._handler = UserPaymentHandler.instance()

    def act(self, userId, priceId):
        try:
            logging.info(f"Successful payment from user: [{userId}], for price: [{priceId}]")
            return self._handler.handle(userId, priceId)
        except Exception as e:
            logging.error(f"Exception while handling payment for user id: [{userId}]", e)
            raise HTTPException(status_code = 500, detail = "Something went wrong")

userPaymentActivity = UserPaymentActivity()