import hashlib
import os
from dotenv import load_dotenv
import logging

class AuthUtils:

    @staticmethod
    def instance():
        return authUtils

    def __init__(self) -> None:
        load_dotenv()
        self._X_INDICATOR_API_KEY = os.getenv("X_INDICATOR_API_KEY");

    def hasAccess(self, headers: {}) -> bool:
        try:
            value = headers["x_timestamp"] + self._X_INDICATOR_API_KEY + headers["x_timestamp"]
            hash = hashlib.sha512(value.encode('utf-8')).hexdigest()
            return hash == headers["x_auth"]
        except Exception as e:
            logging.error("Error while checking access", e)
            return False

authUtils = AuthUtils()