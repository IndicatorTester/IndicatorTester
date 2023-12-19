import os
from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0
from dotenv import load_dotenv
import logging

class AuthUtils:

    @staticmethod
    def instance():
        return authUtils

    def __init__(self):
        self._authenticate()

    async def isUserLoggedIn(self, userId: str, tries: int = 0) -> bool:
        try:
            logging.info(f"Check user login for id: [{userId}]")
            if userId == None:
                return False
            user_info = self._auth0.users.get(userId)
            return user_info != None
        except Auth0Error as e:
            if e.status_code == 401:
                self._authenticate()
                if tries == 0:
                    self._isUserLoggedIn(userId, 1)
                else:
                    return False
            else:
                logging.error(f"Auth Error while checking user login for id: [{userId}]", e)
                return False
        except Exception as e:
            logging.error(f"Error while checking user login for id: [{userId}]", e)
            return False

    def _authenticate(self):
        load_dotenv()
        auth0_domain = os.getenv("AUTH0_DOMAIN")
        client_id = os.getenv("AUTH0_CLIENT_ID")
        client_secret = os.getenv("AUTH0_CLIENT_SECRET")

        get_token = GetToken(auth0_domain)
        token = get_token.client_credentials(client_id, client_secret, f'https://{auth0_domain}/api/v2/')

        self._auth0 = Auth0(auth0_domain, token['access_token'])

        logging.info("Authenticate with new token")

authUtils = AuthUtils()