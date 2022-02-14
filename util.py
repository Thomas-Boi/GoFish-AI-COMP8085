from typing import Dict


def create_empty_cards_dict(amount=0) -> Dict[str]:
    """
    Create an empty dictionary containing the values (2, 3, J, Q, etc.)
    of a card as keys and the amount of it as values.
    :param amount, the default amount of each cards.
    """
    cards = {}
    # num values
    for i in range(2, 11):
        cards[i] = amount

    # face cards
    for i in ["J", "Q", "K", "A"]:
        cards[i] = amount

    return cards
