from fastapi import HTTPException
from handlers.GetTestArchiveHandler import GetTestArchiveHandler
import logging

class GetTestArchiveActivity:

    @staticmethod
    def instance():
        return getTestArchiveActivity

    def __init__(self):
        self._handler = GetTestArchiveHandler.instance()

    def act(self, userId, timestamp, pageNumber):
        if not timestamp.isdigit():
            raise HTTPException(status_code = 403, detail = 'Invalid timestamp value')
        if userId is None:
            raise HTTPException(status_code = 403, detail = 'User Id can\'t be null')
        if pageNumber is None:
            raise HTTPException(status_code = 403, detail = 'Page number can\'t be null')
        if pageNumber < 1:
            raise HTTPException(status_code = 403, detail = 'Page number must be positive number')

        try:
            return self._handler.handle(userId, timestamp, pageNumber)
        except Exception as e:
            logging.error(f"Exception while processing /testArchive", e)
            raise HTTPException(status_code = 500, detail = 'Something went wrong')

getTestArchiveActivity = GetTestArchiveActivity()