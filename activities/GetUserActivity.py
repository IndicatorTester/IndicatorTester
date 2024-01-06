from fastapi import HTTPException
from handlers.GetUserHandler import GetUserHandler
import logging

class GetUserActivity:

    @staticmethod
    def instance():
        return getUserActivity

    def __init__(self) -> None:
        self._handler = GetUserHandler.instance()

    def act(self, userId):
        try:
            return self._handler.handle(userId)
        except Exception as e:
            logging.error(f"Exception while getting user data for user id: [{userId}]", e)
            raise HTTPException(status_code = 500, detail = "Something went wrong")

getUserActivity = GetUserActivity()