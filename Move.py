from typing import Union
from colorama import Fore
from util import color_text

class Move:
    def __init__(self, asker: str, target: str, card: str):
        """
        Record a Move that was made. This is just a data container, no functionality.
        :param asker, name of the player that asked for the card.
        :param target, name of the target player that was asked for the card.
        :param card, card value.
        """
        self.asker = asker
        """
        Name of the player that asked for the card.
        """

        self.target = target
        """
        Name of the target player that was asked for the card.
        """

        self.card = card
        """
        Card value.
        """

        self.succeed: Union[bool, None] = None
        """
        Whether the player succeeded.
        """

        self.amount = 0
        """
        The amount of cards the asker gotten from the target.
        """

        self.found_fours: Union[str, None] = None
        """
        Whether the asker found a four-of-a-kind as a result of the move.
        """

    def __str__(self) -> str:
        txt = f"{color_text(self.asker, Fore.CYAN)} asked {color_text(self.target, Fore.CYAN)} for {color_text(self.card, Fore.YELLOW)}."
        if self.succeed is not None and self.amount is not None:
            succeed = 'successful' if self.succeed else 'not successful'
            txt += f"\nThe move was {color_text(succeed, Fore.YELLOW)} and {color_text(self.asker, Fore.CYAN)} got {color_text(self.amount, Fore.CYAN)} cards of value '{color_text(self.card, Fore.YELLOW)}'."

        if self.found_fours:
            txt += f"\n{color_text(self.asker, Fore.CYAN)} collected FOUR OF A KIND for {color_text(self.found_fours, Fore.GREEN)}"
        return txt