import requests
import logging

class TelegramAccessor:

    @staticmethod
    def instance(botToken, chatId):
        return TelegramAccessor(botToken, chatId)

    def __init__(self, botToken, chatId) -> None:
        self._botToken = botToken
        self._chatId = chatId

    def sendMessage(self, message):
        try:
            url = f"https://api.telegram.org/bot{self._botToken}/sendMessage"
            params = {
                "chat_id": self._chatId,
                "text": str(message)
            }
            response = requests.post(url, params=params)
            if response.status_code == 200:
                logging.info("Message sent successfully with Telegram")
            else:
                logging.warn(f"Failed to send message with Telegram. Error: {response.text}")
        except Exception as e:
            logging.error(f"An error occurred while sending message with Telegram: {str(e)}")