import requests
import logging

BOT_TOKEN = "6989207560:AAGe3KWZRhrhVhTlJ5H8zRDmQJtsi3Vb7cU"
BOT_NAME = "XIndicator_bot"

class TelegramUtils:

    @staticmethod
    def instance():
        return telegramUtils

    def __init__(self) -> None:
        pass

    def sendMessage(self, message):
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            params = {
                "chat_id": "6228767723",
                "text": str(message)
            }
            response = requests.post(url, params=params)
            if response.status_code == 200:
                logging.info("Message sent successfully with Telegram")
            else:
                logging.warn(f"Failed to send message with Telegram. Error: {response.text}")
        except Exception as e:
            logging.error(f"An error occurred while sending message with Telegram: {str(e)}")

telegramUtils = TelegramUtils()