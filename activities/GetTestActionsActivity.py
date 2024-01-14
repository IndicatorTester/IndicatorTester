from fastapi import HTTPException
from handlers.GetTestActionsHandler import GetTestActionsHandler
import logging

class GetTestActionsActivity:

    @staticmethod
    def instance():
        return getTestActionsActivity

    def __init__(self) -> None:
        self._handler = GetTestActionsHandler.instance()

    def act(self, userId, timestamp):
        if not timestamp.isdigit():
            raise HTTPException(status_code = 403, detail = 'Invalid timestamp value')
        if userId is None:
            raise HTTPException(status_code = 403, detail = 'User Id can\'t be null')

        try:
            return self._handler.handle(userId, timestamp)
        except Exception as e:
            logging.error(f"Exception while processing /testActions for user id: [{userId}]", e)
            raise HTTPException(status_code = 500, detail = 'Something went wrong')

getTestActionsActivity = GetTestActionsActivity()