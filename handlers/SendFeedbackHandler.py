from accessors import TelegramAccessor
from models import SendFeedbackRequest
import constants

class SendFeedbackHandler:

    @staticmethod
    def instance():
        return sendFeedbackHandler

    def __init__(self) -> None:
        self._telegramAccessor = TelegramAccessor.instance(
            constants.TelegramConstants.FEEDBACK_BOT_TOKEN.value,
            constants.TelegramConstants.FEEDBACK_BOT_CHAT_ID.value
        )

    def handle(self, request: SendFeedbackRequest):
        telegramMessage = f"""
            Name: {request.firstName} {request.lastName}

            Email: {request.email}

            Message: {request.message}
        """
        self._telegramAccessor.sendMessage(telegramMessage)

sendFeedbackHandler = SendFeedbackHandler()