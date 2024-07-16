"""
Main module
"""

__all__ = ["stochastics"]


class stochastics:
    """
    Collection of tools for calculating probabilities
    """
    from .stochastics import binomialDF, chance

    binomialDF = binomialDF
    chance = chance