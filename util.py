from colorama import Fore
from typing import Dict
from collections import namedtuple

card_values = [str(card) for card in range(2, 11)]
"""
Values of cards in a standard deck of cards.
"""
card_values.extend(["J", "Q", "K", "A"])

def color_text(data, color) -> str:
    """
    Color the text based on the passed in color.
    :param data the data.
    :param color, a colorama.Fore enum
    """
    return f"{color}{data}{Fore.WHITE}"


def create_cards_dict(amount=0) -> Dict[str, int]:
    """
    Create an empty dictionary containing the values (2, 3, J, Q, etc.)
    of a card as keys and the amount of it as values.
    :param amount, the default amount of each cards.
    """
    cards = {}
    for i in card_values:
        cards[i] = amount

    return cards


OppStat = namedtuple("OppStat", ['name', 'hand_size', 'fours'])
"""
Stores the stat that a Player can see from their opponents.
"""