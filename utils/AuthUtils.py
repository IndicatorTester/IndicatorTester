import hashlib
import os
from dotenv import load_dotenv

class AuthUtils:

    @staticmethod
    def instance():
        return authUtils

    def __init__(self) -> None:
        load_dotenv()
        self._X_INDICATOR_API_KEY = os.getenv("X_INDICATOR_API_KEY");

    def hasAccess(self, headers: {}) -> bool:
        value = headers["timestamp"] + self._X_INDICATOR_API_KEY + headers["timestamp"]
        hash = hashlib.sha512(value.encode('utf-8')).hexdigest()
        return hash == headers["auth"]

authUtils = AuthUtils()