import requests as WEB
from discord import User, Client, Intents
from requests import request, HTTPError

class Webhook():
    """
    Contains the information to access a Discord webhook

    #### Arguments:
        url (str): The webhook url to send messages through 

    #### Methods:
        send(): Sends a message through the webhook
    """
    def __init__(self, url: str):
        self._url = url

    def send(self, msg: str):
        """
        Sends a message through the webhook

        #### Arguments
            msg (str): 

        #### Raises:
            requests.exceptions.HTTPError: If the message couldn't be sent
        """
        payload = {"content": msg}
        response = WEB.post(self._url, json=payload)
        
        response.raise_for_status()

def fetch_user(id:int, token: str) -> User:
    """
    Fetches a Discord user by their ID using the provided bot token

    #### Returns
        - discord.User: The user object 
        - None: If the user is not found

    #### Raises
        - PermissionError: If the provided token is invalid or does not have the required permissions
        - HTTPError: If the request to the Discord API fails for any other reason
    """

    client = Client(intents=Intents.default())

    try:
        call = request("GET", f"https://discord.com/api/v10/users/{id}", headers={"Authorization":f"Bot {token}", "Content-Type":"application/json"})
        call.raise_for_status()
        data = call.json()
        user = User(state=client._connection, data=data)
        return user
    
    except HTTPError as e:
        if e.response.status_code == 401:
            raise PermissionError("Invalid Discord token")
        elif e.response.status_code == 404:
            return None
        else:
            raise e