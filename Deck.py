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
    
        random.shuffle(self.cards)

    def draw(self, amount: int) -> List[str]:
        """
        Draw amount of cards from the deck.
        :return a list of the cards drawn from the deck.
        """
        cards = []
        for i in range(amount):
            # since deck is already shuffled, just draw from top.
            cards.append(self.cards.pop())
        return cards
            
    def go_fish(self) -> str:
        """
        Draw a random card from the deck.
        """
        return self.draw(1)[0]