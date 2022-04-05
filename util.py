from colorama import Fore
from typing import Dict
from collections import namedtuple
import torch
from collections import OrderedDict

card_values = [str(card) for card in range(2, 11)]
"""
Values of cards in a standard deck of cards.
"""
card_values.extend(["J", "Q", "K", "A"])

# for pytorch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def color_text(data, color) -> str:
    """
    Color the text based on the passed in color.
    :param data the data.
    :param color, a colorama.Fore enum
    """
    return f"{color}{data}{Fore.WHITE}"


def create_cards_dict(amount=0) -> OrderedDict:
    """
    Create an empty dictionary containing the values (2, 3, J, Q, etc.)
    of a card as keys and the amount of it as values.
    :param amount, the default amount of each cards.
    """
    # this ensures looping through the values will be consistent
    # like 2, 3, 4, 5, 6...J, Q, K, A
    cards = OrderedDict()
    for i in card_values:
        cards[i] = amount

    return cards


OppStat = namedtuple("OppStat", ['name', 'hand_size', 'fours'])
"""
Stores the stat that a Player can see from their opponents.
Contain a "name", a "hand_size", and the "fours" they have collected.
"""