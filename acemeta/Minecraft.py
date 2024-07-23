import requests as WEB

class Player():
    """
    Contains information about a Minecraft player

    #### Arguments:
        name (str): The players Minecraft name

    #### Raises:
        ValueError: If no user with the given name exists
    """
    def __init__(self, name: str):
        self.name = name
        self._url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
        
        response = WEB.get(self._url)

        if response.status_code == 200:
            data = response.json()
            self.uuid = data['id']
        elif response.status_code == 404:
            raise ValueError(f"User with name '{name}' does not exist")       