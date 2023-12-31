from fastapi import HTTPException
from handlers.SendFeedbackHandler import SendFeedbackHandler
from models import SendFeedbackRequest
import logging

class SendFeedbackActivity:

    @staticmethod
    def instance():
        return sendFeedbackActivity

    def __init__(self) -> None:
        self._handler = SendFeedbackHandler.instance()

    def act(self, request: SendFeedbackRequest):
        try:
            self._handler.handle(request)
        except Exception as e:
            logging.error(f"Exception while adding per order for email: [{request.email}], error: {e}")
            raise HTTPException(status_code = 500, detail = "Something went wrong")

sendFeedbackActivity = SendFeedbackActivity()