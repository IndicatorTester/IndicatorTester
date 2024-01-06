from fastapi import HTTPException
from handlers.UpdateUserHandler import UpdateUserHandler
from models import UpdateUserRequest
import logging

class UpdateUserActivity:

    @staticmethod
    def instance():
        return updateUserActivity

    def __init__(self):
        self._handler = UpdateUserHandler.instance()

    def act(self, request: UpdateUserRequest):
        try:
            self._handler.handle(request)
        except Exception as e:
            logging.error(f"Exception while getting user data for user id: [{request.userId}]", e)
            raise HTTPException(status_code=500, detail=f"Exception while updating user: {request.userId}")

updateUserActivity = UpdateUserActivity()