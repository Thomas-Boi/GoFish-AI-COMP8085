from colorama import Fore

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