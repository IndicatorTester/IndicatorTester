import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from dotenv import load_dotenv

class AuthUtils:

    @staticmethod
    def instance():
        return authUtils

    def __init__(self):
        load_dotenv()
        auth0_domain = os.getenv("AUTH0_DOMAIN")
        client_id = os.getenv("AUTH0_CLIENT_ID")
        client_secret = os.getenv("AUTH0_CLIENT_SECRET")

        get_token = GetToken(auth0_domain)
        token = get_token.client_credentials(client_id, client_secret, f'https://{auth0_domain}/api/v2/')

        self._auth0 = Auth0(auth0_domain, token['access_token'])

    async def isUserLoggedIn(self, userId: str) -> bool:
        try:
            user_info = self._auth0.users.get(userId)
            return user_info != None
        except Exception as e:
            return False

authUtils = AuthUtils()