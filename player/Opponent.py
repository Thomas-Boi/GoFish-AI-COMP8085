from typing import Set

from util import *


class Opponent:
    """
    Represents an opponent from the player's POV.
    """

    def __init__(self, stats: OppStat) -> None:
        """
        Represents an opponent player from the view of a player.
        This means certain data are not visible to the player.
        :param stats the stats of an opponent as seen from the player's POV.
        """

        self.name = stats.name
        """
        Name of the player.
        """
        
        self.hand = create_cards_dict()
        """
        The cards in the player's hands.
        """

        self.hand_size = stats.hand_size
        """
        The amount of cards in the player's hand.
        """

        self.fours: Set[str] = stats.fours
        """
        The four of a kinds the player has collected.
        This only stores the value of the four-of-a-kinds.
        Ex: four 2s are stored as one 2 value in the set.
        """


    def update(self, stat: OppStat):
        """
        Update the opponent's stat.
        """
        for attr, value in stat._asdict().items():
            setattr(self, attr, value)

    def has_card(self, card) -> bool:
        """
        Check whether the player has the asked card.
        """
        try:
            return self.hand[card] > 0
        except KeyError:
            # invalid key => wrong card name
            return False

    def give_cards(self, card: str, amount: int=1):
        """
        Give the cards to the player based on the amount
        given. If the player got a four-of-a-kind, also update
        itself.
        NOTE: No error check here since we assume the deck is 
        fairly constructed aka no more than 4 cards per value.
        :param card
        :param amount, the amount we are giving to the player.
        """
        self.hand[card] += amount
        if self.hand[card] > 4:
            self.hand[card] = 4

    def remove_card(self, card: str):
        """
        Remove all cards with the same value from the player's hand.
        :param the card value we are getting from the players.
        """
        self.hand[card] = 0

    def __str__(self) -> str:
        txt = f"{color_text(self.name, Fore.CYAN)} has {color_text(self.hand_size, Fore.CYAN)} cards with at least: "
        cards = []
        for value, amount in self.hand.items():
            if amount == 0:
                continue
            cards.append(f"{color_text(amount, Fore.CYAN)} of {color_text(value, Fore.YELLOW)}s")

        # format it
        txt += ", ".join(cards) + "."
        return txt