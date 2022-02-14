from typing import Dict, Set


class Player:
    def __init__(self) -> None:
        """
        An abstract player class that represents human or computer players.
        """
        
        self.hands: Dict[str] = {}
        """
        The cards in the player's hands.
        """

        self.fourOfAKinds: Set[str] = set()
        """
        The four of a kinds the player has collected.
        This only stores the value of the four-of-a-kinds.
        Ex: four 2s are stored as one 2 value in the set.
        """

    def ask_for_card(self) -> str:
        """
        Ask a player for a card.
        """
        raise NotImplementedError()

    def check_for_card(self, card) -> bool:
        """
        Check whether the player has the asked card.
        """
        return card in self.hands


    def get_card(self, card) -> bool:
        """
        Get the card from the player's hand.
        """
        pass

    def give_card(self, card):
        """
        Give a card to the player.
        """
        raise NotImplementedError()

