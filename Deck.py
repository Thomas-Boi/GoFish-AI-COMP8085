from typing import List
import random

import util


class Deck:
    def __init__(self):	
        """
        A standard 52-cards deck of cards. There are no suits
        since it doesn't matter for Go Fish.
        """
        self.cards = []
        """
        Cards in the deck.
        """
        for card in util.card_values:
            for time in range(4):
                self.cards.append(card)
    

    def draw(self, amount: int) -> List[str]:
        """
        Draw amount of cards from the deck.
        :return a list of the cards drawn from the deck.
        """
        return random.choices(self.cards, k=amount)
            
    def go_fish(self) -> List[str]:
        """
        Draw a random card from the deck.
        """
        return self.draw(1)