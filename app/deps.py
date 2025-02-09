
import httpx
from fastapi import Depends
import os


PASSWORD = os.environ.get("LOGIN_PASSWORD")
EMAIL = os.environ.get("LOGIN_EMAIL")
# Authentication details
LOGIN_URL = "https://connect.soligent.net/sca/services/Account.Login.Service.ss"
CHECK_LOGIN_URL = "https://connect.soligent.net/store/services/ShoppingUserEnvironment.Service.ss"
QUERYSTRING = {"n": "2", "c": "3510556"}
LOGIN_PAYLOAD = {
    "email": EMAIL,
    "password": PASSWORD,
    "redirect": "true"
}
HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "content-type": "application/json; charset=UTF-8",
    "origin": "https://connect.soligent.net",
    "referer": "https://connect.soligent.net/sca/checkout.ssp?is=login",
    "x-requested-with": "XMLHttpRequest",
    "x-sc-touchpoint": "checkout"
}

class AuthenticatedClient:
    def __init__(self):
        """Initialize an HTTPX client and log in automatically."""
        self.client = httpx.AsyncClient(headers=HEADERS)
    
    async def check_login(self) -> bool:
        """Check if the session is still active."""
        querystring = {"lang": "en_US", "cur": "", "X-SC-Touchpoint": "shopping"}
        response = await self.client.get(CHECK_LOGIN_URL, params=querystring)
        
        try:
            response_data = response.json()
            status = response_data['ENVIRONMENT']['PROFILE']['isLoggedIn']
            return status == "T"
        except (KeyError, ValueError):
            return False

    async def login(self):
        """Logs in and stores session cookies if not already logged in."""
        if await self.check_login():
            print("Already logged in.")
            return
        
        response = await self.client.post(LOGIN_URL, json=LOGIN_PAYLOAD, params=QUERYSTRING)
        if response.status_code == 200:
            print("Login successful!")
        else:
            print("Login failed:", response.text)
            raise Exception("Failed to authenticate with Soligent")

    async def get_client(self) -> httpx.AsyncClient:
        """Ensure login is valid before returning the client."""
        await self.login()
        return self.client

# Dependency function
async def get_http_client() -> httpx.AsyncClient:
    return await client_manager.get_client()

# Create a single instance for reuse
client_manager = AuthenticatedClient()
