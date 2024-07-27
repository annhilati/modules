"""
## Library for typical workflows
Made by Annhilati
"""

from .stochastics import binomialDF
from .numbers import isPrime, factorial
from .console import FancyConsole, Color, Time, log
from .files import fileToStr

FC = FancyConsole
C = Color
T = Time

__all__ = ["binomialDF", "isPrime", "factorial",
           "GitHub", "Webhook",
           "FancyConsole", "FC", "Color", "C", "Time", "T", "log",
           "fileToStr"]



class GitHub():
    "Utility class for interactions with GitHub"
    from .GitHub import Repository
    Repository = Repository

class Discord():
    "Utility class for interactions with Discord"
    from .Discord import Webhook
    Webhook = Webhook

class Minecraft():
    "Utility class for interactions with the Mojang-API"
    from .Minecraft import Player
    Player = Player