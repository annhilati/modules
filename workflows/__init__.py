"""
## Library for typical workflows
Made by Annhilati
"""


__all__ = ["GitHub", "Discord"]



class GitHub():
    "Utility class for interactions with GitHub"
    from .GitHub import Repository
    Repository = Repository

class Discord():
    "Utility class for interactions with Discord"
    from .Discord import Webhook
    Webhook = Webhook